"""
File    : ollama_scene_lighting_node.py
Purpose : Ollama-powered Scene & Lighting node for the Refactored pipeline.
          Hits a local Ollama endpoint with a tight 1-sentence prompt to generate
          a cinematic scene + lighting description.
          Falls back gracefully to the static pool if Ollama is offline/timeout.
"""

import json
import random
import urllib.request
import urllib.error

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None


# ─────────────────────────── Static Fallback Pool ────────────────────────────
FALLBACK_SCENES = {
    "Rainy Parisian Street":        "rain-slicked cobblestones, warm amber streetlamp halos, mist drifting through the dark alley, cinematic shallow depth of field",
    "Dark Parisian Boudoir":        "candlelit ornate Haussmannian boudoir, deep shadow contrast, velvet drapes, intimate low-key chiaroscuro",
    "Parisian Neon Noir":           "volumetric blue hour dusk, vibrant neon reflections on wet pavement, cinematic chiaroscuro, urban nightscape",
    "Golden Terrace":               "golden hour Parisian rooftop terrace, warm diffused backlight, distant Eiffel Tower silhouette, cinematic bokeh",
    "Steamy Marble Bath":           "luxurious white marble bathroom, soft diffused mist, warm directional shafts of light, glistening specularity",
    "Minimalist Editorial Studio":  "high-contrast editorial studio, clean off-white solid backdrop, sharp crisp rim lighting, fashion magazine aesthetic",
    "Urban Office":                 "sleek modern Paris office at dusk, floor-to-ceiling windows, ambient city glow, soft directional desk lamp accent",
    "Neutral Daylight":             "neutral overcast outdoor daylight, soft even illumination, no harsh shadows, clean photographic base",
    "Underground Club":             "dimly lit subterranean Parisian club, pulsing red and violet spotlights, haze machine smoke, electrifying nightlife energy",
    "Rooftop Dawn":                 "pre-dawn Paris rooftop, pale rose and indigo gradient sky, cool morning mist, dramatic wide-angle cinematic framing",
}

SCENE_OPTIONS = ["🎲 Dynamic / Random Scene"] + list(FALLBACK_SCENES.keys())

# ─────────────────────────── Ollama Helper ───────────────────────────────────
OLLAMA_URL  = "http://127.0.0.1:11434/api/generate"
TIMEOUT_SEC = 20

SYSTEM_PROMPT = (
    "You are a cinematic photography prompt writer. "
    "Your ONLY job is to output a single comma-separated descriptive phrase "
    "(15-30 words) describing a scene environment and its lighting for a fashion/portrait photograph. "
    "Do NOT include any character description, clothing, or body parts. "
    "Do NOT use bullet points, numbering, or quotation marks. "
    "Output ONLY the raw phrase with no preamble."
)


def _call_ollama(model: str, user_prompt: str) -> str | None:
    payload = json.dumps({
        "model":  model,
        "prompt": user_prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {"temperature": 0.85, "num_predict": 80},
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    result = None
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            result = body.get("response", "").strip() or None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        result = None
    finally:
        # ── Immediately evict model from VRAM — do not hog GPU memory ──
        _purge_vram(model)
    return result


def _purge_vram(model: str) -> None:
    """Force Ollama to unload the model from VRAM by sending keep_alive=0."""
    try:
        purge_payload = json.dumps({
            "model":      model,
            "keep_alive": 0,
        }).encode("utf-8")
        purge_req = urllib.request.Request(
            OLLAMA_URL,
            data=purge_payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(purge_req, timeout=5)
    except Exception:
        pass  # Silent — purge failure is non-critical


# ─────────────────────────── Node Class ──────────────────────────────────────
class OllamaSceneLightingNode:
    """Ollama-powered Scene & Lighting generator.

    - Calls a local Ollama model with a tight system prompt.
    - Falls back to the static scene pool if Ollama is offline or times out.
    - ``scene_mode`` allows locking to a specific environment or using dynamic generation.
    - ``master_seed`` is used ONLY for static-fallback determinism (ignored when LLM is live).
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":  ("INT",    {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "ollama_model": ("STRING", {"default": "qwen2.5:7b-instruct"}),
                "scene_mode":   (SCENE_OPTIONS, {"default": "🎲 Dynamic / Random Scene"}),
            },
            "optional": {
                "scene_style_hint": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "forceInput": True,
                    "tooltip": "Optional keyword hint fed to the LLM (e.g. 'dark rainy', 'bright summer')",
                }),
            },
        }

    RETURN_TYPES  = ("STRING", "STRING")
    RETURN_NAMES  = ("scene_lighting_prompt", "source")
    FUNCTION      = "run"
    CATEGORY      = "ZIT/Dataset Workstation"

    def run(
        self,
        master_seed: int,
        ollama_model: str,
        scene_mode: str,
        scene_style_hint: str = "",
        **kwargs,
    ):
        # ── If a specific scene is locked, use the static definition directly ──
        if scene_mode != "🎲 Dynamic / Random Scene" and scene_mode in FALLBACK_SCENES:
            prompt = f"{scene_mode}, {FALLBACK_SCENES[scene_mode]}"
            return (prompt, "static-locked")

        # ── Build LLM user prompt ──
        hint_clause = f" The mood/style hint is: {scene_style_hint.strip()}." if scene_style_hint.strip() else ""
        user_msg = (
            f"Write a cinematic scene + lighting description for a high-fashion portrait photograph set in Paris or a dramatic interior.{hint_clause} "
            f"The scene must feel unique, atmospheric, and cinematic. Output only the raw phrase."
        )

        # ── Try Ollama ──
        result = _call_ollama(ollama_model, user_msg)
        if result:
            return (result, f"ollama:{ollama_model}")

        # ── Fallback: deterministic static selection ──
        keys  = list(FALLBACK_SCENES.keys())
        idx   = (master_seed // 5000) % len(keys)
        env   = keys[idx]
        lighting = FALLBACK_SCENES[env]
        fallback_prompt = f"{env}, {lighting}"
        return (fallback_prompt, "static-fallback")
