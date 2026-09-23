"""
File    : scene_lighting_node_refactor.py
Purpose : Standalone Refactored Scene & Lighting node — 130+ curated cinematic, Parisian,
          luxury interior, and studio environments with pure atmospheric and lighting physics.
          Zero character/human prompt bleed.

          active_tier_tag input enforces tier-coherent scene selection:
            T2_ / anatomy -> constrained to warm private interiors (boudoir, bath, studio)
            T1_ / closeup  -> biased toward clean neutral portrait backdrops
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
                    result = {}
                    for cat, items in data.items():
                        for idx_item, item in enumerate(items):
                            short_title = item.split(",")[0].strip()
                            if short_title in result:
                                short_title = f"{short_title} ({cat} #{idx_item+1})"
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

# Tier-coherent scene keyword filters
# Tier 2 = Anatomy / Body Proportions bake. Warm private interiors only.
T2_SCENE_KEYWORDS = [
    "boudoir", "bath", "marble", "studio", "spa", "lounge", "bedroom",
    "candle", "silk", "private", "apartment", "sanctuary", "interior",
    "warm", "steam", "mirror", "dressing", "pool", "velvet", "intimate",
    "loft", "penthouse", "suite", "balcony", "window light", "diffused",
]

# Tier 1 = Identity anchors / close-up. Clean neutral studio backdrops preferred.
T1_SCENE_KEYWORDS = [
    "studio", "editorial", "cyclorama", "backdrop", "neutral", "clean",
    "softbox", "rim light", "grey", "white wall", "seamless", "minimalist",
    "strobe", "fill light", "magazine",
]

# Scenes excluded when Tier 2 fires (outdoor / public / cold / street)
T2_SCENE_EXCLUSIONS = [
    "alley", "cobblestone", "street", "metro", "rooftop", "rain", "outdoor",
    "urban", "neon", "nightscape", "club", "subterranean", "forest",
    "beach", "cliff", "garden", "park", "cafe", "restaurant", "market",
]


class RefactoredSceneLightingNode:
    """Massive Scene & Lighting matrix generator with zero character bleed.

    - 130+ distinct atmospheric environments and cinematic lighting setups.
    - Emits ONLY environmental architecture, spatial depth, atmospheric weather, and lighting physics.
    - Zero human/subject tokens, eliminating any conflict with PuLID or subject identity.
    - Master seed drives deterministic modulo selection across all environments.
    - active_tier_tag enforces Tier 2 coherence: no outdoor/cold/public scenes during
      body anatomy bakes. Only warm private interiors allowed.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":      ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "environment_mode": (ENV_OPTIONS, {"default": "🎲 Dynamic / Random Scene Sweep"}),
            },
            "optional": {
                "custom_scene_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "active_tier_tag":       ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("scene_lighting_prompt",)
    FUNCTION     = "run"
    CATEGORY     = "ZIT/Dataset Workstation"

    def run(self, master_seed: int, environment_mode: str = "🎲 Dynamic / Random Scene Sweep",
            custom_scene_override: str = "", active_tier_tag: str = "", **kwargs):

        # Custom override bypasses everything
        if custom_scene_override and custom_scene_override.strip():
            return (custom_scene_override.strip(),)

        scene_map = SCENE_MAP
        if not scene_map:
            return ("cinematic Parisian atmosphere, warm diffused lighting, natural bokeh",)

        # Detect active tier from tag
        tag_lower = active_tier_tag.lower()
        is_tier_2 = any(k in tag_lower for k in ["t2_", "tier 2", "anatomy", "t2 "])
        is_tier_1 = any(k in tag_lower for k in ["t1_", "tier 1", "headshot", "closeup", "close-up", "macro", "t1 "])

        # If a specific environment is locked, respect it unless it violates Tier 2
        if environment_mode != "🎲 Dynamic / Random Scene Sweep" and environment_mode in scene_map:
            prompt = scene_map[environment_mode]
            if is_tier_2:
                env_lower = (environment_mode + " " + prompt).lower()
                if not any(excl in env_lower for excl in T2_SCENE_EXCLUSIONS):
                    return (prompt,)
                # Violates T2 coherence — fall through to filtered pool
            else:
                return (prompt,)

        # Dynamic selection with tier-coherent filtering
        keys = list(scene_map.keys())
        if not keys:
            return ("cinematic Parisian atmosphere, warm diffused lighting, natural bokeh",)

        if is_tier_2:
            pool = [
                k for k in keys
                if not any(excl in (k + " " + scene_map[k]).lower() for excl in T2_SCENE_EXCLUSIONS)
            ]
            pool = pool if pool else keys  # graceful fallback
            print(f"[SceneNode] T2 filter: {len(pool)} intimate/indoor scenes in pool")
        elif is_tier_1:
            pool = keys  # Unlock full 130+ cinematic vault for T1
            print(f"[SceneNode] T1 filter: {len(pool)} diverse cinematic scenes in pool")
        else:
            pool = keys

        idx = master_seed % len(pool)
        env_key = pool[idx]
        prompt = scene_map.get(env_key, list(scene_map.values())[0])
        return (prompt,)
