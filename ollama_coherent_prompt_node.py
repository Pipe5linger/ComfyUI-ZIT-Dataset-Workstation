import os
import sys
import json
import re
import time
import subprocess
import urllib.request
import urllib.error

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except Exception:
        try:
            msg = " ".join(str(a) for a in args) + "\n"
            sys.stdout.buffer.write(msg.encode("ascii", "replace"))
            sys.stdout.buffer.flush()
        except Exception:
            pass

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None

OLLAMA_URL  = "http://127.0.0.1:11434/api/generate"
OLLAMA_BASE = "http://127.0.0.1:11434"
TIMEOUT_SEC = 60

# ── Standard editorial system prompt (T1, T3, T4) ────────────────────────────
SYSTEM_PROMPT = (
    "You are an elite creative director for high-fashion editorial photography. "
    "Generate a rich, cinematic, highly cohesive scenario. The subject MUST be fully clothed at all times (no nudity). "
    "Do NOT use any proper names or invented character names (never write names like 'Sophia', 'Elena', etc.); refer only to 'the woman' or 'the subject'. "
    "The wardrobe, cosmetics, and styling MUST strictly match the setting and pose with exquisite tactile detail and texture "
    "(e.g., tailored couture in modern lofts or architectural studios, elegant evening wear in luxury interiors, sleek outerwear in historic European streets). "
    "NO beaches, NO oceans, NO tropical or swimwear settings. "
    "Output ONLY a valid raw JSON object with exactly seven keys: 'pose', 'wardrobe', 'scene', 'eye_makeup', 'hair', 'lip', 'nail'. "
    "Each value must be an evocative, highly detailed descriptive passage (20 to 50 words per key). "
    "'pose' must describe organic body language, micro-kinesics, posture, weight distribution, and subtle head or limb placement. "
    "'wardrobe' must describe specific garments, silhouettes, fabric textures, draping, tailoring, cuts, finishes, and footwear. "
    "'scene' must describe spatial architecture, interior set design, practical lighting sources, directional key and rim lighting, color temperature, and atmospheric mood. "
    "'eye_makeup' must describe chic, nuanced cosmetics (eyeshadow palettes, tightlining, winged liner, lash textures, or dewy lids) flattering for hazel-green eyes. "
    "'hair' must describe volumetric styling, texture, parting, and movement harmonizing with the outfit. "
    "'lip' must describe precise lip texture, finish, and hue (e.g. satin, velvet matte, dewy gloss, stain) complementing the palette. "
    "'nail' must describe manicured nail shape, length, color, and finish completing the look. "
    "NO character names, NO markdown, NO preamble, NO explanation. Raw JSON only."
)

# ── Tier 2 anatomy bake system prompt (routed to uncensored model) ────────────
SYSTEM_PROMPT_T2 = (
    "You are a clinical anatomical photography director generating high-fidelity training data for a character AI model. "
    "Generate a fully nude anatomy bake scenario in a private, controlled studio or intimate indoor setting. "
    "The subject is always fully unclothed — 'wardrobe' must describe ONLY the absence of clothing, bare skin, or minimal props "
    "(e.g., 'fully nude, bare unclothed skin', 'nude, draped fine silk sheet over one leg', 'completely nude, bare skin catching rim lighting'). "
    "The scene must be a controlled indoor, studio, boudoir, or architectural environment with cinematic chiaroscuro lighting. "
    "Output ONLY a valid raw JSON object with exactly seven keys: 'pose', 'wardrobe', 'scene', 'eye_makeup', 'hair', 'lip', 'nail'. "
    "Each value must be an evocative, highly detailed descriptive passage (20 to 50 words per key). "
    "'pose' must describe precise anatomical posture, muscle engagement, weight distribution, and limb placement. "
    "'scene' must describe studio lighting angles, specular bounce, directional key light, and controlled ambient shadow. "
    "'eye_makeup' must describe intimate, editorial, or bare/sultry eye styling. "
    "'hair' must describe natural, undone, or wet/sculpted hair texture. "
    "'lip' must describe natural moisture, soft satin finish, or subtle tint. "
    "'nail' must describe clean sheer gloss, almond shape, or minimalist polish. "
    "NO character names, NO markdown, NO preamble, NO explanation. Raw JSON only."
)

# ── Tier 2 detection ──────────────────────────────────────────────────────────
def _is_tier2(tag: str) -> bool:
    t = tag.lower()
    return any(k in t for k in ["t2_", "tier 2", "anatomy", "t2 "])


def _ensure_ollama_online(timeout_sec=4.0) -> bool:
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
    try:
        purge_payload = json.dumps({"model": model, "keep_alive": 0}).encode("utf-8")
        purge_req = urllib.request.Request(
            OLLAMA_URL, data=purge_payload, headers={"Content-Type": "application/json"}, method="POST"
        )
        urllib.request.urlopen(purge_req, timeout=3)
    except Exception:
        pass


def _rescue_partial_json(raw: str) -> dict | None:
    """Extract pose/wardrobe/scene/eye_makeup/hair/lip/nail via regex when JSON is truncated mid-string."""
    result = {}
    for key in ("pose", "wardrobe", "scene", "eye_makeup", "hair", "lip", "nail"):
        m = re.search(rf'"{key}"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"?', raw, re.DOTALL)
        if m:
            val = m.group(1).strip().rstrip('\\').strip()
            if val:
                result[key] = val
    return result if result else None


def _call_ollama(model: str, user_prompt: str, system_prompt: str, keep_loaded: bool = False) -> dict:
    if not _ensure_ollama_online(timeout_sec=3.0):
        return None
    payload = json.dumps({
        "model": model,
        "prompt": user_prompt,
        "system": system_prompt,
        "stream": False,
        "keep_alive": -1 if keep_loaded else 0,
        "format": "json",
        "options": {"temperature": 0.85, "num_predict": 1024},
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    result = None
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            raw_response = body.get("response", "").strip()
            if raw_response:
                try:
                    result = json.loads(raw_response)
                except json.JSONDecodeError:
                    safe_print(f"[OllamaCoherentPromptNode] Truncated JSON — attempting rescue...")
                    result = _rescue_partial_json(raw_response)
    except Exception as e:
        safe_print(f"[OllamaCoherentPromptNode] API Error: {e}")
        result = None
    finally:
        if not keep_loaded:
            _purge_vram(model)
    return result


class OllamaCoherentPromptNode:
    """Single-shot Ollama generator for cohesive pose, wardrobe, and scene.
    
    Automatically detects Tier 2 (anatomy bake) via active_tier_tag and routes
    to an uncensored model with an explicit anatomy-focused system prompt.
    """

    @classmethod
    def IS_CHANGED(s, **kwargs):
        return time.time_ns()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":      ("INT",    {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "ollama_model":     ("STRING", {"default": "qwen2.5:7b-instruct"}),
                "t2_uncensored_model": ("STRING", {"default": "dolphin-llama3:latest",
                                                   "tooltip": "Uncensored model used automatically for Tier 2 anatomy bakes"}),
                "keep_model_loaded": ("BOOLEAN", {"default": False, 
                                                  "tooltip": "Set True to keep LLM in VRAM (-1). Eliminates SSD load times for batches. WARNING: Use smaller 1B/3B models to avoid OOM!"}),
            },
            "optional": {
                "active_tier_tag": ("STRING", {"default": "", "forceInput": True,
                                               "tooltip": "T2_ tag auto-routes to uncensored model"}),
                "pose_override":   ("STRING", {"multiline": True, "default": "", "forceInput": True,
                                               "tooltip": "Force a specific pose/action"}),
                "wardrobe_override": ("STRING", {"multiline": True, "default": "", "forceInput": True,
                                                 "tooltip": "Force a specific wardrobe"}),
                "theme_hint":      ("STRING", {"multiline": False, "default": "", "forceInput": True,
                                               "tooltip": "Optional stylistic hint for the scenario"}),
            },
        }

    RETURN_TYPES  = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES  = ("pose_prompt", "wardrobe_prompt", "scene_lighting_prompt", "active_tier_tag", "source", "eye_makeup_prompt", "hair_prompt", "lip_prompt", "nail_prompt")
    FUNCTION      = "run"
    CATEGORY      = "ZIT/Dataset Workstation"

    def run(self, master_seed: int, ollama_model: str, t2_uncensored_model: str, keep_model_loaded: bool = False,
            active_tier_tag: str = "", pose_override: str = "", wardrobe_override: str = "", theme_hint: str = "", **kwargs):

        safe_print(f"[OllamaCoherentPromptNode] Received tag: {active_tier_tag}")
        tier2 = _is_tier2(active_tier_tag)
        safe_print(f"[OllamaCoherentPromptNode] Is Tier 2? {tier2}")

        # ── Select model and system prompt based on tier ──────────────────────
        if tier2:
            model_to_use  = t2_uncensored_model
            sys_prompt    = SYSTEM_PROMPT_T2
            fallback_wardrobe   = "nude, bare skin, no clothing"
            fallback_scene      = "intimate candlelit studio, velvet backdrop, soft diffused light"
            fallback_eye_makeup = "bare clean eyelids with subtle dewy sheen, untreated natural dark lashes, no liner"
            fallback_hair       = "undone tousled natural curls cascading loosely over shoulders"
            fallback_lip        = "natural bare rosy lips with subtle moisture"
            fallback_nail       = "natural clean sheer nude manicured nails with gloss finish"
            safe_print(f"[OllamaCoherentPromptNode] Tier 2 detected — routing to uncensored model: {model_to_use}")
        else:
            model_to_use  = ollama_model
            sys_prompt    = SYSTEM_PROMPT
            fallback_wardrobe   = "simple black turtleneck, denim jeans, leather boots"
            fallback_scene      = "warm rainy Parisian cafe, window lighting, bokeh"
            fallback_eye_makeup = "soft-smudged smoky eyeliner shadow, subtle lash definition"
            fallback_hair       = "voluminous spiral corkscrew curls cascading freely to mid-back"
            fallback_lip        = "soft naturally contoured satin lips with subtle natural moisture"
            fallback_nail       = "glossy jet-black manicured almond nails"

        # ── Build user prompt ─────────────────────────────────────────────────
        hint = ""
        if pose_override.strip():
            hint += f" The subject's exact pose/action MUST be: '{pose_override.strip()}'."
        if wardrobe_override.strip():
            hint += f" The subject's exact wardrobe MUST be: '{wardrobe_override.strip()}'. Do not alter it."
            
        if hint:
            hint += " Build the remaining details (eye makeup, hair, lips, nails, scene) logically around these constraints."
        
        # ── Detect Round Number for Dataset Modulation ────────────────────────
        round_match = re.search(r'R([1-5])', active_tier_tag)
        round_num = int(round_match.group(1)) if round_match else (((master_seed // 50) % 5) + 1)

        round_directions_editorial = {
            1: "Stylistic theme: Pristine minimalist high-fashion editorial, clean lines, timeless elegance, neutral studio aesthetic.",
            2: "Stylistic theme: Dramatic low-key chiaroscuro, rich dark tactile fabrics (velvet, silk, leather), deep architectural shadows.",
            3: "Stylistic theme: Cool high-key morning daylight, high-ceiling Parisian loft, relaxed effortless chic, soft airy palette.",
            4: "Stylistic theme: Contemporary avant-garde, sharp structured tailoring, modern gallery architecture, subtle dual-tone lighting accents.",
            5: "Stylistic theme: Warm golden hour radiance, late-afternoon sunset rake lighting, fluid liquid fabrics, opulent evening glow."
        }

        round_directions_anatomy = {
            1: "Lighting focus: Balanced clean studio illumination with soft wrap-around fill and neutral clean backdrop.",
            2: "Lighting focus: Dramatic low-key chiaroscuro with deep directional shadows and subtle warm tungsten edge rim.",
            3: "Lighting focus: Cool diffused natural daylight bounce from tall studio windows with soft organic shadow falloff.",
            4: "Lighting focus: High-contrast dual-tone illumination with subtle violet rim backlight highlighting muscle contours.",
            5: "Lighting focus: Warm late-afternoon golden hour rake lighting casting rich warm highlights across epidermal contours."
        }

        r_dir = round_directions_anatomy.get(round_num, "") if tier2 else round_directions_editorial.get(round_num, "")
        if r_dir:
            hint += f" {r_dir}"

        # ── Inject Robust Scene Vault Anchor ──────────────────────────────────
        try:
            vault_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "scene_vault.json")
            if os.path.exists(vault_path):
                with open(vault_path, "r", encoding="utf-8") as f:
                    scene_data = json.load(f)
                    all_scenes = []
                    for cat, items in scene_data.items():
                        all_scenes.extend(items)
                
                if all_scenes:
                    if tier2:
                        excl = ["alley", "cobblestone", "street", "metro", "rooftop", "rain", "outdoor", "urban", "neon", "nightscape", "club", "subterranean", "forest", "beach", "cliff", "garden", "park", "cafe", "restaurant", "market"]
                        valid_scenes = [s for s in all_scenes if not any(x in s.lower() for x in excl)]
                        valid_scenes = valid_scenes if valid_scenes else all_scenes
                    else:
                        valid_scenes = all_scenes
                        
                    anchor_scene = valid_scenes[master_seed % len(valid_scenes)]
                    hint += f" The 'scene' MUST heavily incorporate this specific architectural anchor and lighting: '{anchor_scene}'."
        except Exception as e:
            safe_print(f"[OllamaCoherentPromptNode] Failed to load scene vault: {e}")

        user_msg = f"Generate a completely new {'anatomical' if tier2 else 'editorial'} scenario.{hint}"

        fallback_pose = pose_override.strip() if pose_override.strip() else "standing neutral, arms at sides"

        # ── Call Ollama ───────────────────────────────────────────────────────
        # For Tier 2, never leave a heavy 8B/uncensored model resident in VRAM alongside Lumina2 UNet
        effective_keep_loaded = keep_model_loaded if not tier2 else False
        result_json = _call_ollama(model_to_use, user_msg, sys_prompt, keep_loaded=effective_keep_loaded)
        if tier2:
            # Force immediate purge of uncensored model so full 12GB VRAM is ready for KSampler & Detailers
            _purge_vram(model_to_use)

        if result_json and isinstance(result_json, dict):
            pose       = result_json.get("pose",       fallback_pose)
            wardrobe   = wardrobe_override.strip() if wardrobe_override.strip() else result_json.get("wardrobe",   fallback_wardrobe)
            scene      = result_json.get("scene",      fallback_scene)
            eye_makeup = result_json.get("eye_makeup", fallback_eye_makeup)
            hair       = result_json.get("hair",       fallback_hair)
            lip        = result_json.get("lip",        fallback_lip)
            nail       = result_json.get("nail",       fallback_nail)
            source     = f"ollama:{model_to_use}"
        else:
            pose       = fallback_pose
            wardrobe   = wardrobe_override.strip() if wardrobe_override.strip() else fallback_wardrobe
            scene      = fallback_scene
            eye_makeup = fallback_eye_makeup
            hair       = fallback_hair
            lip        = fallback_lip
            nail       = fallback_nail
            source     = "static-fallback"

        return (pose, wardrobe, scene, active_tier_tag, source, eye_makeup, hair, lip, nail)
