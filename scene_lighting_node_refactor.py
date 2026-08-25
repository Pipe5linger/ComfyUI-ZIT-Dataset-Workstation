"""
File    : scene_lighting_node_refactor.py
Purpose : Standalone Refactored Scene & Lighting node — 130+ curated cinematic, Parisian,
          luxury interior, and studio environments with pure atmospheric and lighting physics.
          Zero character/human prompt bleed.
"""

import json
import os

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None

# Locate data vault
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_PATH = os.path.join(CURRENT_DIR, "data", "scene_vault.json")

def _load_vault():
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data and isinstance(data, dict):
                    # Flatten into name -> prompt map
                    result = {}
                    for cat, items in data.items():
                        for item in items:
                            # Use first 40 chars as title or full text
                            short_title = item.split(",")[0].strip()
                            result[short_title] = item
                    return result
        except Exception:
            pass
    return {
        "Rainy Parisian Cobblestone Alley": (
            "rain-slicked dark cobblestone Parisian alley at night, warm amber reflections from vintage streetlamps, "
            "subtle drifting atmospheric mist, wet specular pavement, cinematic shallow depth of field"
        ),
        "Golden Hour Rooftop Terrace": (
            "golden hour sunset on a private Parisian limestone rooftop terrace, warm diffused golden backlight, "
            "distant soft silhouette of Parisian zinc roofs and Eiffel Tower, cinematic lens flare and bokeh"
        ),
        "Dark Parisian Haussmannian Boudoir": (
            "candlelit ornate Haussmannian salon, deep shadow contrast, tall arched French windows with sheer dark drapes, "
            "intimate low-key chiaroscuro lighting, warm rim highlights"
        ),
        "Steamy White Marble Bath": (
            "luxurious high-ceiling white marble bathroom, soft rising diffused steam mist, "
            "warm directional sunlight shafts through frosted glass, glistening specularity on polished stone"
        ),
        "Parisian Neon Noir Metro Entrance": (
            "volumetric blue hour dusk, vibrant neon ruby and cyan light reflections on wet pavement, "
            "Art Nouveau metro archway backdrop, cinematic chiaroscuro, high-contrast atmospheric glow"
        ),
        "Minimalist Editorial Studio": (
            "high-contrast editorial studio photography, clean seamless solid grey cyclorama backdrop, "
            "sharp crisp dual rim strobes, pristine fill light, sharp micro-contrast, Vogue editorial lighting"
        ),
    }

SCENE_MAP = _load_vault()
ENV_OPTIONS = ["🎲 Dynamic / Random Scene Sweep"] + list(SCENE_MAP.keys())


class RefactoredSceneLightingNode:
    """Massive Scene & Lighting matrix generator with zero character bleed.

    - 130+ distinct atmospheric environments and cinematic lighting setups.
    - Emits ONLY environmental architecture, spatial depth, atmospheric weather, and lighting physics.
    - Zero human/subject tokens, eliminating any conflict with PuLID or subject identity.
    - Master seed drives deterministic modulo selection across all environments.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":     ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "environment_mode": (ENV_OPTIONS, {"default": "🎲 Dynamic / Random Scene Sweep"}),
            },
            "optional": {
                "custom_scene_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("scene_lighting_prompt",)
    FUNCTION     = "run"
    CATEGORY     = "ZIT/Dataset Workstation"

    def run(self, master_seed: int, environment_mode: str = "🎲 Dynamic / Random Scene Sweep", custom_scene_override: str = "", **kwargs):
        if custom_scene_override and custom_scene_override.strip():
            return (custom_scene_override.strip(),)

        scene_map = _load_vault()
        if environment_mode == "🎲 Dynamic / Random Scene Sweep" or environment_mode not in scene_map:
            keys = list(scene_map.keys())
            idx = (master_seed // 2000) % len(keys)
            env_key = keys[idx]
        else:
            env_key = environment_mode

        prompt = scene_map.get(env_key, list(scene_map.values())[0])
        return (prompt,)
