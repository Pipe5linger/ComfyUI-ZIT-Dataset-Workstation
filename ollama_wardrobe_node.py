"""
File    : ollama_wardrobe_node.py
Purpose : Ollama-powered Dynamic Wardrobe node for the Refactored pipeline.
          Calls a local Ollama endpoint with a tight system prompt to generate
          a cohesive fashion wardrobe description (top + bottom + shoes + accessories).
          Auto-launches Ollama daemon if offline, enforces keep_alive=0, and sweeps VRAM.
          Falls back gracefully to the static wardrobe pool if Ollama is offline/timeout.
"""

import os
import json
import random
import time
import subprocess
import urllib.request
import urllib.error

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None


# ─────────────────────────── Static Fallback Pool ────────────────────────────
FALLBACK_WARDROBES = {
    "gothic": "fitted black leather corset, high-waisted black tulle skirt, platform stiletto boots, silver chain choker",
    "cyberpunk": "chrome metallic vest, holo iridescent cargo pants, high-tech combat boots, LED-accent wrist cuffs",
    "haute couture": "embroidered silk evening blouse, flowing satin palazzo trousers, pearl-strap stilettos, delicate drop earrings",
    "streetwear": "cropped graphic tee, relaxed high-waist denim jeans, chunky white sneakers, layered gold chains",
    "vintage": "high-collar tweed blazer, tailored high-waist pencil skirt, classic mary jane heels, pearl brooch",
    "bohemian": "sheer embroidered kimono over bandeau, wide-leg linen trousers, leather strappy sandals, stacked turquoise rings",
    "sporty": "fitted performance crop top, sleek compression leggings, high-top trainers, minimalist silver studs",
    "formal": "structured tailored blazer, slim cigarette trousers, patent leather pumps, slim leather belt",
    "ethereal": "iridescent chiffon haori over silk bralette, layered tulle culottes, transparent acrylic heels, delicate floral pins",
    "noir detective": "long belted trench coat over silk blouse, slim tailored trousers, pointed-toe ankle boots, sleek leather gloves",
}

STYLE_OPTIONS = ["🎲 Dynamic / Random Style"] + list(FALLBACK_WARDROBES.keys())

# ─────────────────────────── Ollama Config ───────────────────────────────────
OLLAMA_URL  = "http://127.0.0.1:11434/api/generate"
OLLAMA_BASE = "http://127.0.0.1:11434"
TIMEOUT_SEC = 20

SYSTEM_PROMPT = (
    "You are a high-fashion wardrobe stylist for editorial photography. "
    "Your ONLY job is to output a single comma-separated list describing: "
    "top garment, bottom garment, shoes, and one accessory — all cohesive and stylistically matched. "
    "Keep it concise: 15-25 words total. "
    "Do NOT include any character description, body parts, or colors of skin/hair. "
    "Do NOT use bullet points, numbering, or quotation marks. "
    "Output ONLY the raw comma-separated phrase with no preamble."
)


# ─────────────────────────── Ollama Helpers ──────────────────────────────────
def _ensure_ollama_online(timeout_sec=4.0) -> bool:
    """Checks if Ollama server is responsive. If offline, attempts to launch it."""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                return True
    except Exception:
        pass

    try:
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NO_WINDOW
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags
        )
        start_t = time.time()
        while time.time() - start_t < timeout_sec:
            time.sleep(0.5)
            try:
                req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    if resp.status == 200:
                        return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def _purge_vram(model: str) -> None:
    """Force Ollama to unload the model from VRAM immediately (keep_alive=0)."""
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
        urllib.request.urlopen(purge_req, timeout=3)
    except Exception:
        pass


def _call_ollama(model: str, user_prompt: str) -> str | None:
    if not _ensure_ollama_online(timeout_sec=3.0):
        return None

    payload = json.dumps({
        "model":      model,
        "prompt":     user_prompt,
        "system":     SYSTEM_PROMPT,
        "stream":     False,
        "keep_alive": 0,
        "options":    {"temperature": 0.9, "num_predict": 80},
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


# ─────────────────────────── Node Class ──────────────────────────────────────
class OllamaWardrobeNode:
    """Ollama-powered Dynamic Wardrobe generator.

    - Calls a local Ollama model with a tight fashion-stylist system prompt.
    - Immediately purges the model from VRAM after each generation (keep_alive=0).
    - Falls back to the static wardrobe pool if Ollama is offline or times out.
    - ``style_mode`` locks to a specific aesthetic or lets the LLM choose freely.
    - ``master_seed`` drives deterministic fallback selection only.
    """

    @classmethod
    def IS_CHANGED(s, **kwargs):
        # DEFECT 7 FIX: Ensure fresh generation across queue passes
        return time.time_ns()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":  ("INT",    {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "ollama_model": ("STRING", {"default": "qwen2.5:7b-instruct"}),
                "style_mode":   (STYLE_OPTIONS, {"default": "🎲 Dynamic / Random Style"}),
            },
            "optional": {
                "style_hint": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "forceInput": True,
                    "tooltip": "Optional keyword hint fed to the LLM (e.g. 'dark edgy', 'soft romantic')",
                }),
            },
        }

    RETURN_TYPES  = ("STRING", "STRING")
    RETURN_NAMES  = ("wardrobe_prompt", "source")
    FUNCTION      = "run"
    CATEGORY      = "ZIT/Dataset Workstation"

    def run(
        self,
        master_seed: int,
        ollama_model: str,
        style_mode: str,
        style_hint: str = "",
        **kwargs,
    ):
        # ── If a specific style is locked, use the static definition directly ──
        if style_mode != "🎲 Dynamic / Random Style" and style_mode in FALLBACK_WARDROBES:
            return (FALLBACK_WARDROBES[style_mode], "static-locked")

        # ── Build LLM user prompt ──
        hint_clause = f" Style direction: {style_hint.strip()}." if style_hint.strip() else ""
        user_msg = (
            f"Write a cohesive high-fashion wardrobe outfit for an editorial portrait photo.{hint_clause} "
            f"Include: top garment, bottom garment or full outfit, shoes, and one accessory. "
            f"Output only the raw comma-separated phrase."
        )

        # ── Try Ollama ──
        result = _call_ollama(ollama_model, user_msg)
        if result:
            return (result, f"ollama:{ollama_model}")

        # ── Fallback: deterministic static selection ──
        keys  = list(FALLBACK_WARDROBES.keys())
        idx   = master_seed % len(keys)
        style = keys[idx]
        return (FALLBACK_WARDROBES[style], "static-fallback")
