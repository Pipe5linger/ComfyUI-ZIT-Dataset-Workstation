"""
File    : zit_nodes.py
Purpose : Zero-Shot Image Transfer (ZIT) Character Override, Dynamic Wardrobe & Master Prompt Workstation Node Suite.
"""

import os
import re
import sqlite3
import random
from pathlib import Path
import folder_paths

try:
    from .zit_data import (
        LORA_TIER1_ANCHORS,
        LORA_TIER2_ANATOMY,
        LORA_TIER3_WARDROBE,
        LORA_TIER4_SPATIAL,
        DIRECTOR_RIG_CONFIGS,
        HAIR_STATES,
        POSES_POOL_NSFW,
        POSES_POOL_SFW,
        EXPRESSIONS_POOL_NSFW,
        EXPRESSIONS_POOL_SFW,
        PHYSICS_POOL_NSFW,
        PHYSICS_POOL_SFW,
        BOUDOIR_SHEET_COLORS,
        BOUDOIR_FURNITURE_VENUES,
        ENVIRONMENTS_MAP,
        WARDROBE_DATA,
        VESPERA_VARIATIONS,
        DEFAULT_VESPERA_PROMPT_PREFIX,
        VESPERA_FACE_MICROPACK,
        HAIR_CONFLICTS,
        EYE_CONFLICTS,
        BODY_SUBJECT_CONFLICTS,
    )
except ImportError:
    from zit_data import (
        LORA_TIER1_ANCHORS,
        LORA_TIER2_ANATOMY,
        LORA_TIER3_WARDROBE,
        LORA_TIER4_SPATIAL,
        DIRECTOR_RIG_CONFIGS,
        HAIR_STATES,
        POSES_POOL_NSFW,
        POSES_POOL_SFW,
        EXPRESSIONS_POOL_NSFW,
        EXPRESSIONS_POOL_SFW,
        PHYSICS_POOL_NSFW,
        PHYSICS_POOL_SFW,
        BOUDOIR_SHEET_COLORS,
        BOUDOIR_FURNITURE_VENUES,
        ENVIRONMENTS_MAP,
        WARDROBE_DATA,
        VESPERA_VARIATIONS,
        DEFAULT_VESPERA_PROMPT_PREFIX,
        VESPERA_FACE_MICROPACK,
        HAIR_CONFLICTS,
        EYE_CONFLICTS,
        BODY_SUBJECT_CONFLICTS,
    )

DEFAULT_DB = r"D:\AI\Projects\antigravity-overdrive-sync\sync_state.db"
DB_PATH = os.environ.get("ZIT_SYNC_DB_PATH", DEFAULT_DB)
UNIFIED_CATEGORY = "ZIT/Dataset Workstation"

def fetch_live_vespera_traits() -> str:
    try:
        if not os.path.exists(DB_PATH):
            return ""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT trait FROM persona_profile 
            WHERE category = 'physical' OR trait LIKE '%tattoo%'
            ORDER BY confidence DESC, frequency DESC LIMIT 5
        """)
        rows = cursor.fetchall()
        conn.close()
        if rows:
            traits = [r[0].strip() for r in rows if r[0]]
            return ", ".join(traits)
    except Exception:
        pass
    return ""

def strip_prompt_conflicts(text: str, strip_hair: bool = True, strip_eyes: bool = True, strip_body: bool = True, custom_keywords: str = "") -> str:
    patterns = []
    if strip_hair:
        patterns.extend(HAIR_CONFLICTS)
    if strip_eyes:
        patterns.extend(EYE_CONFLICTS)
    if strip_body:
        patterns.extend(BODY_SUBJECT_CONFLICTS)
    
    if custom_keywords:
        for kw in custom_keywords.split(","):
            kw_clean = kw.strip()
            if kw_clean:
                patterns.append(rf'\b{re.escape(kw_clean)}\b')
                
    cleaned = text
    for pat in patterns:
        cleaned = re.sub(pat, '', cleaned, flags=re.IGNORECASE)
        
    cleaned = re.sub(r',\s*,+', ',', cleaned)
    cleaned = re.sub(r'^\s*,\s*', '', cleaned)
    cleaned = re.sub(r'\s*,\s*$', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


# ============================================================================
# 1. CHARACTER OVERRIDE NODE
# ============================================================================
class ZITCharacterOverrideNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character_baseline": ("STRING", {
                    "multiline": True,
                    "default": DEFAULT_VESPERA_PROMPT_PREFIX,
                    "placeholder": "Enter complete character physical baseline..."
                }),
                "scenario_prompt": ("STRING", {
                    "multiline": True,
                    "default": "1girl, blonde hair, blue eyes, wearing a black silk trench coat walking through rainy neon cyberpunk Paris, cinematic lighting, reflections on wet cobblestones, 8k raw photo",
                    "placeholder": "Enter scenario, environment, outfit, or borrowed prompt..."
                }),
                "override_mode": ([
                    "Smart Override & Merge (Recommended)",
                    "Prepend Character Baseline",
                    "Append Character Baseline",
                    "Strict Character Only (Ignore Scenario)"
                ], {
                    "default": "Smart Override & Merge (Recommended)"
                }),
                "strip_conflicts": ([
                    "Hair, Eyes, Body & Generic Subjects",
                    "Hair and Eyes Only",
                    "None"
                ], {
                    "default": "Hair, Eyes, Body & Generic Subjects"
                })
            },
            "optional": {
                "custom_strip_words": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "Extra comma-separated words to strip..."
                }),
                "negative_prompt_additions": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Additional negative prompts..."
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("final_prompt", "cleaned_scenario", "character_baseline", "negative_prompt")
    FUNCTION = "override_and_synthesize"
    CATEGORY = UNIFIED_CATEGORY

    def override_and_synthesize(
        self,
        character_baseline: str,
        scenario_prompt: str,
        override_mode: str = "Smart Override & Merge (Recommended)",
        strip_conflicts: str = "Hair, Eyes, Body & Generic Subjects",
        custom_strip_words: str = "",
        negative_prompt_additions: str = ""
    ):
        base = character_baseline.strip() if character_baseline.strip() else DEFAULT_VESPERA_PROMPT_PREFIX
        scenario = scenario_prompt.strip()
        
        strip_hair = "Hair" in strip_conflicts
        strip_eyes = "Eyes" in strip_conflicts
        strip_body = "Body" in strip_conflicts
        
        if strip_conflicts != "None":
            cleaned_scenario = strip_prompt_conflicts(
                scenario, 
                strip_hair=strip_hair, 
                strip_eyes=strip_eyes, 
                strip_body=strip_body, 
                custom_keywords=custom_strip_words
            )
        else:
            cleaned_scenario = scenario

        if override_mode == "Strict Character Only (Ignore Scenario)":
            final_prompt = base
        elif override_mode == "Prepend Character Baseline":
            final_prompt = f"{base}, {cleaned_scenario}" if cleaned_scenario else base
        elif override_mode == "Append Character Baseline":
            final_prompt = f"{cleaned_scenario}, {base}" if cleaned_scenario else base
        else:
            live_traits = fetch_live_vespera_traits()
            if live_traits and live_traits not in base:
                base_augmented = f"{base}, traits: {live_traits}"
            else:
                base_augmented = base
            
            if cleaned_scenario:
                final_prompt = f"{base_augmented}. Scenario: {cleaned_scenario}"
            else:
                final_prompt = base_augmented

        final_prompt = re.sub(r',\s*,+', ',', final_prompt).strip(' ,')
        
        base_negatives = [
            "blurry", "low quality", "deformed", "extra limbs", "bad anatomy", 
            "mutated fingers", "poorly drawn hands", "missing fingers",
            "duplicate", "watermark", "signature", "anime", "cartoon", "3d render", "illustration",
            "plastic skin", "oversaturated"
        ]
        if negative_prompt_additions.strip():
            base_negatives.append(negative_prompt_additions.strip())
            
        negative_prompt = ", ".join(base_negatives)
        return (final_prompt, cleaned_scenario, base, negative_prompt)


# ============================================================================
# 2. VESPERA CHARACTER ENCODER NODE
# ============================================================================
class VesperaCharacterEncoder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character_style": ([
                    "Photorealistic 8k Raw (Default)",
                    "Cinematic 35mm Film Still",
                    "Noir High-Contrast Chiaroscuro",
                    "Cyberpunk Holographic Neon",
                    "Minimalist Editorial Portrait"
                ], {
                    "default": "Photorealistic 8k Raw (Default)"
                }),
                "include_tattoos": ("BOOLEAN", {"default": True}),
                "include_wardrobe_seed": ([
                    "None (Prompt Only)",
                    "Black Silk Trench Coat",
                    "Lace Bodysuit & Leather Harness",
                    "Tactical High-Collar Cyberpunk Jacket",
                    "Off-Shoulder Cashmere Knit",
                    "Liquid Latex Corset"
                ], {
                    "default": "None (Prompt Only)"
                })
            },
            "optional": {
                "additional_physical_traits": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "e.g., damp curls, intense focused gaze..."
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("character_prompt_prefix", "negative_prompt_prefix")
    FUNCTION = "encode_vespera"
    CATEGORY = UNIFIED_CATEGORY

    def encode_vespera(self, character_style: str, include_tattoos: bool, include_wardrobe_seed: str, additional_physical_traits: str = ""):
        base = DEFAULT_VESPERA_PROMPT_PREFIX
        if not include_tattoos:
            base = re.sub(r'Signature tattoos:.*?(?=(Relaxed|\Z))', '', base)

        style_modifiers = {
            "Cinematic 35mm Film Still": "shot on 35mm Kodak Vision3 500T, authentic halation, rich shadow grain, cinematic anamorphic bokeh",
            "Noir High-Contrast Chiaroscuro": "dramatic Venetian blind shadows, low-key lighting, deep obsidian blacks, sharp specular rim illumination",
            "Cyberpunk Holographic Neon": "ambient cyan-blue and magenta rim lights, holographic HUD reflections in eyes, volumetric neon mist",
            "Minimalist Editorial Portrait": "clean neutral grey backdrop, balanced three-point studio lighting, high-fashion Vogue composition",
            "Photorealistic 8k Raw (Default)": "8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT4"
        }

        mod = style_modifiers.get(character_style, "")
        prompt_parts = [base]
        if mod:
            prompt_parts.append(mod)
        if include_wardrobe_seed and include_wardrobe_seed != "None (Prompt Only)":
            prompt_parts.append(f"wearing {include_wardrobe_seed}")
        if additional_physical_traits.strip():
            prompt_parts.append(additional_physical_traits.strip())

        full_prompt = ", ".join(prompt_parts)
        full_prompt = re.sub(r',\s*,+', ',', full_prompt).strip(' ,')

        negative = "blurry, low quality, deformed, extra limbs, bad anatomy, cartoon, anime, 3d render, plastic skin"
        return (full_prompt, negative)


# ============================================================================
# 3. BACKGROUND ARCHITECT NODE
# ============================================================================
class ZITBackgroundArchitectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "environment_theme": ([
                    "Cyberpunk Neo-Paris (Rainy Night & Neon)",
                    "Parisian Haussmann Balcony (Twilight & Zinc Roofs)",
                    "Subterranean High-Tech AI Sanctum (Terminals & Cables)",
                    "Minimalist Monochromatic Fashion Studio (Seamless Backdrop)",
                    "Candlelit Baroque Library (Dark Oak & Gold Leaf)",
                    "Montmartre Wet Cobblestone Alley (Warm Gaslamps)",
                    "Modern Luxury Penthouse (Panoramic City Skyline)",
                    "Industrial Concrete Brutalist Bunker (Cold Daylight Shafts)"
                ], {
                    "default": "Cyberpunk Neo-Paris (Rainy Night & Neon)"
                }),
                "lighting_mood": ([
                    "Volumetric Atmospheric Neon (Cyan/Magenta)",
                    "Low-Key Chiaroscuro & Candlelight",
                    "Golden Hour Sunset Spill",
                    "Cool Blue Hour Moonlight",
                    "Hard Directional Spotlight",
                    "Softbox Diffused Studio Light"
                ], {
                    "default": "Volumetric Atmospheric Neon (Cyan/Magenta)"
                }),
                "camera_framing": ([
                    "Medium Shot (Waist Up)",
                    "Full Body Portrait",
                    "Close-Up (Shoulders and Face)",
                    "Cinematic Wide Angle (Environmental)",
                    "Dutch Angle Dynamic Framing"
                ], {
                    "default": "Medium Shot (Waist Up)"
                })
            },
            "optional": {
                "weather_elements": ([
                    "None",
                    "Heavy Rain & Puddle Reflections",
                    "Light Mist & Rising Steam",
                    "Subtle Airborne Dust Particulates & Embers",
                    "Wet Surfaces & Moisture Droplets"
                ], {
                    "default": "None"
                }),
                "custom_atmosphere_notes": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "e.g., flickering fluorescent light, distant sirens..."
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("environment_prompt", "background_only", "composition_only")
    FUNCTION = "architect_background"
    CATEGORY = UNIFIED_CATEGORY

    def architect_background(
        self,
        environment_theme: str,
        lighting_mood: str,
        camera_framing: str,
        weather_elements: str = "None",
        custom_atmosphere_notes: str = ""
    ):
        theme_map = {
            "Cyberpunk Neo-Paris (Rainy Night & Neon)": "in rainy cyberpunk Neo-Paris, holographic advertising reflections in street puddles, towering mega-structures, dark neon alleys",
            "Parisian Haussmann Balcony (Twilight & Zinc Roofs)": "standing on an ornate wrought-iron Haussmann balcony in Paris during twilight, classic zinc rooftops, Eiffel tower in soft background bokeh",
            "Subterranean High-Tech AI Sanctum (Terminals & Cables)": "inside a dark subterranean AI server sanctuary, glowing fiber-optic cables, humming server racks, holographic diagnostic wireframes",
            "Minimalist Monochromatic Fashion Studio (Seamless Backdrop)": "in a pristine high-fashion photo studio, seamless solid dark-slate cyclorama backdrop, soft floor reflections",
            "Candlelit Baroque Library (Dark Oak & Gold Leaf)": "inside a massive two-story antique library, carved dark oak bookshelves, leather-bound tomes, gilded details, warm candelabras",
            "Montmartre Wet Cobblestone Alley (Warm Gaslamps)": "in a secluded winding Montmartre cobblestone passage at midnight, warm glowing vintage gas streetlamps, glistening wet stones",
            "Modern Luxury Penthouse (Panoramic City Skyline)": "inside a sleek glass-walled penthouse suite, floor-to-ceiling panoramic view of glowing metropolis at night, polished dark marble floors",
            "Industrial Concrete Brutalist Bunker (Cold Daylight Shafts)": "inside an expansive brutalist concrete structure, dramatic angular light beams cutting through ceiling shafts, architectural minimalism"
        }

        light_map = {
            "Volumetric Atmospheric Neon (Cyan/Magenta)": "atmospheric volumetric fog illuminated by vibrant cyan and deep magenta neon rim lights, dramatic specular highlights",
            "Low-Key Chiaroscuro & Candlelight": "extreme low-key chiaroscuro lighting, warm flickering candlelight with deep dark shadows, high contrast edge falloff",
            "Golden Hour Sunset Spill": "warm golden hour sunlight spilling sideways through windows, warm dust motes, rich orange and amber color grade",
            "Cool Blue Hour Moonlight": "subtle cool blue hour ambient light, moonlight catching hair and shoulders, soft indigo shadows",
            "Hard Directional Spotlight": "dramatic single overhead spotlight casting sharp crisp shadows, high theatrical contrast",
            "Softbox Diffused Studio Light": "large softbox key light providing even luminous skin tones, gentle shadow transitions, clean professional fill"
        }

        frame_map = {
            "Medium Shot (Waist Up)": "medium portrait shot, waist up composition, 50mm focal length, f/1.8 shallow depth of field",
            "Full Body Portrait": "full body fashion portrait, showing full silhouette and stance, 35mm lens perspective",
            "Close-Up (Shoulders and Face)": "intimate close-up portrait, focusing on facial expressions and eye details, 85mm portrait lens, creamy bokeh",
            "Cinematic Wide Angle (Environmental)": "cinematic wide angle shot with subject framed within expansive architectural environment, 24mm anamorphic lens",
            "Dutch Angle Dynamic Framing": "dynamic dutch angle composition, tilted horizon, cinematic tension, wide perspective"
        }

        env = theme_map.get(environment_theme, "")
        light = light_map.get(lighting_mood, "")
        frame = frame_map.get(camera_framing, "")

        full_scenario_parts = [env, light, frame]
        if weather_elements and weather_elements != "None":
            full_scenario_parts.append(weather_elements)
        if custom_atmosphere_notes.strip():
            full_scenario_parts.append(custom_atmosphere_notes.strip())

        bg_only = f"{env}, {light}"
        composition_only = frame

        full_scenario = ", ".join(full_scenario_parts)
        full_scenario = re.sub(r',\s*,+', ',', full_scenario).strip(' ,')

        return (full_scenario, bg_only, composition_only)


# ============================================================================
# 4. DYNAMIC WARDROBE ENGINE NODE
# ============================================================================
class ZITDynamicWardrobeEngine:
    WARDROBE_TIERS = [
        "🎲 Full Stochastic (Random All)",
        "🔥 Lingerie (Lace, Teddy, Silk, Corsetry)",
        "😈 Slutty / Micro (Harness, Micro-Bikini, Latex, Fishnet)",
        "🔞 Full Nudity (Anatomical Precision, Bare Realskin)",
        "👀 Partial Nudity / Topless (Open Robe, Sheer Peeks, Topless)",
        "💋 Sexy / Provocative (Plunging Slips, Bodycon, High-Slits)",
        "🍸 Glamorous (Haute Couture, Velvet Gowns, Silk Drapery)",
        "💼 Business / Power (Tailored Blazers, Cigarette Trousers)",
        "☕ Casual (Cashmere, Distressed Selvedge Denim, Leather Jacket)"
    ]

    FABRIC_PHYSICS = [
        "Natural Ambient Lighting & Raytracing",
        "Wet & Translucent Micro-Sheer Physics",
        "High-Gloss Liquid Latex & Polished Leather",
        "Heavy Silk, Velvet & Fluid Fabric Drapery",
        "Brushed Wool & Cashmere Tactile Knit"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wardrobe_level": (cls.WARDROBE_TIERS, {"default": "🎲 Full Stochastic (Random All)"}),
                "fabric_physics_detail": (cls.FABRIC_PHYSICS, {"default": "Natural Ambient Lighting & Raytracing"}),
                "include_accessories_footwear": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": "randomize"}),
            },
            "optional": {
                "optional_base_prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("clothing_prompt", "fused_character_prompt", "selected_tier")
    FUNCTION = "generate_wardrobe"
    CATEGORY = UNIFIED_CATEGORY

    def generate_wardrobe(
        self,
        wardrobe_level: str,
        fabric_physics_detail: str,
        include_accessories_footwear: bool,
        seed: int,
        optional_base_prompt: str = ""
    ):
        rng = random.Random(seed)

        tier_key_map = {
            "🔥 Lingerie (Lace, Teddy, Silk, Corsetry)": "lingerie",
            "😈 Slutty / Micro (Harness, Micro-Bikini, Latex, Fishnet)": "slutty",
            "🔞 Full Nudity (Anatomical Precision, Bare Realskin)": "nudity",
            "👀 Partial Nudity / Topless (Open Robe, Sheer Peeks, Topless)": "partial_nudity",
            "💋 Sexy / Provocative (Plunging Slips, Bodycon, High-Slits)": "sexy",
            "🍸 Glamorous (Haute Couture, Velvet Gowns, Silk Drapery)": "glamorous",
            "💼 Business / Power (Tailored Blazers, Cigarette Trousers)": "business",
            "☕ Casual (Cashmere, Distressed Selvedge Denim, Leather Jacket)": "casual"
        }

        if wardrobe_level == "🎲 Full Stochastic (Random All)":
            chosen_key = rng.choice(list(WARDROBE_DATA.keys()))
        else:
            chosen_key = tier_key_map.get(wardrobe_level, "lingerie")

        tier_data = WARDROBE_DATA.get(chosen_key, WARDROBE_DATA["lingerie"])
        main_item = rng.choice(tier_data["items"])
        
        acc_item = ""
        if include_accessories_footwear and tier_data.get("bottoms_acc"):
            acc_item = rng.choice(tier_data["bottoms_acc"])

        physics_map = {
            "Wet & Translucent Micro-Sheer Physics": "translucent wet sheer fabric tension with ray-traced subsurface biological skin sheen underneath",
            "High-Gloss Liquid Latex & Polished Leather": "high-gloss liquid latex and nappa leather with crisp ray-traced specular edge reflections",
            "Heavy Silk, Velvet & Fluid Fabric Drapery": "heavy silk satin and velvet drapery with authentic fluid micro-creasing and soft specular sheen",
            "Brushed Wool & Cashmere Tactile Knit": "ultra-fine brushed cashmere knit fibers and textured wool weave with authentic micro-tactile surface",
            "Natural Ambient Lighting & Raytracing": "authentic fabric texture catching directional scene lighting and soft shadow falloff"
        }
        physics_str = physics_map.get(fabric_physics_detail, physics_map["Natural Ambient Lighting & Raytracing"])

        parts = [f"Wearing {main_item}"] if not main_item.startswith("Wearing") and not main_item.startswith("completely nude") and not main_item.startswith("fully nude") else [main_item]
        if acc_item:
            parts.append(f"paired with {acc_item}")
        if physics_str and chosen_key != "nudity":
            parts.append(f"featuring {physics_str}")

        clothing_prompt = ", ".join(parts)
        clothing_prompt = re.sub(r',\s*,+', ',', clothing_prompt).strip(' ,')

        fused_prompt = clothing_prompt
        if optional_base_prompt and optional_base_prompt.strip():
            base_clean = optional_base_prompt.strip()
            if not base_clean.endswith('.'):
                base_clean += '.'
            fused_prompt = f"{base_clean} {clothing_prompt}."

        return (clothing_prompt, fused_prompt, chosen_key.upper())


# ============================================================================
# 5. MASTER PROMPT WORKSTATION NODE
# ============================================================================
class ZITMasterPromptWorkstation:
    RATING_MODES = [
        "🎲 Stochastic Coin-Flip (Random NSFW / SFW)",
        "🔥 NSFW Explicit & Boudoir",
        "🍷 SFW Editorial & Haute Couture"
    ]
    
    SUBJECT_MODES = [
        "👑 Vespera (Photographic Baseline)",
        "👑 Vespera (35mm Raw Cinema)",
        "👑 Vespera (Editorial Still)",
        "🎲 Dynamic Random Subject Anchor",
        "✍️ Custom Subject (Input Port)"
    ]

    WARDROBE_TIERS = [
        "🔞 Full Nudity (Anatomical Precision, Bare Realskin)",
        "🎲 Full Stochastic (Random All)",
        "🔥 Lingerie (Lace, Teddy, Silk, Corsetry)",
        "😈 Slutty / Micro (Harness, Micro-Bikini, Latex, Fishnet)",
        "👀 Partial Nudity / Topless (Open Robe, Sheer Peeks, Topless)",
        "💋 Sexy / Provocative (Plunging Slips, Bodycon, High-Slits)",
        "🍸 Glamorous (Haute Couture, Velvet Gowns, Silk Drapery)",
        "💼 Business / Power (Tailored Blazers, Cigarette Trousers)",
        "☕ Casual (Cashmere, Distressed Selvedge Denim, Leather Jacket)"
    ]

    POSE_MODES = [
        "🔄 Full Master Sweep (1 Round: Tier 1 to Tier 4 - 50 Poses)",
        "🔁 Mega Dataset Sweep (5 Rounds: Tier 1 to Tier 4 - 250 Batch)",
        "🎯 Tier 1: Sequential Sweep (15 Identity Anchors)",
        "💪 Tier 2: Sequential Sweep (10 Anatomy Ratios)",
        "👗 Tier 3: Sequential Sweep (15 Wardrobe Slots)",
        "🌐 Tier 4: Sequential Sweep (10 Spatial Environments)",
        "🎯 Tier 1: Identity Anchors (Close-Ups & 3D Head Angles)",
        "🔥 Tier 2: Raw Anatomy (Body Proportions, Mid/Full-Body & Realskin)",
        "👗 Tier 3: Wardrobe Agnosticism (Cowboy & Haute Couture/Casual/Business Mix)",
        "🌐 Tier 4: 3D Spatial Awareness (Full-Body, Back Views & Dynamic Action)",
        "🎲 Dynamic Random Pose",
        "Seductive Kneeling with Arched Back",
        "Sensual Reclining with Parted Legs",
        "Dominant 3/4 Standing Silhouette",
        "Poised Seated Posture with Crossed Legs",
        "POV Intimate Perspective Lying Back",
        "Looking Back Over Bare Shoulder",
        "All Fours with Arched Spine & Direct Gaze",
        "Side profile view of face, looking away from camera, gazing off into the distance",
        "Viewed from behind, looking over her shoulder back at the camera",
        "Extreme close up macro portrait, framing only face and neck, high detail",
        "Full body shot from head to toe, standing confidently, looking off to the side",
        "High angle shot from above, looking up at the camera",
        "Low angle shot from below, looking slightly down at the camera",
        "Dynamic full body shot, walking confidently forward",
        "Reclining flat on back, looking up at the ceiling",
        "3/4 profile view, looking thoughtfully away from the lens",
        "Hands in pockets, casual confident stance",
        "Leaning against a wall with arms crossed",
        "One hand on hip, sassy model stance",
        "Standing with legs crossed at ankles",
        "Tiptoe reaching upward, arms extended overhead",
        "Walking away from camera, glancing back over shoulder",
        "Profile silhouette, chin lifted, highlighting jawline",
        "Sitting cross-legged on the floor, hands resting on knees",
        "Sitting on floor with knees drawn up to chest, arms wrapped around legs",
        "Sitting backwards on a chair, arms resting on the chair back",
        "Perched on the edge of a surface, legs dangling",
        "Kneeling tall on both knees, hands resting on thighs",
        "Lying on stomach, propped up on elbows, chin in hands",
        "Lying on side, head resting on hand, legs slightly bent",
        "Reclining back on hands, legs extended forward",
        "Crouching low in a powerful athletic stance",
        "Bent forward at the waist, hands on knees, looking up",
        "Arms wrapped around herself, protective intimate posture",
        "Head tilted back, eyes closed, hands resting on chest",
        "Chin resting on hand, thoughtful contemplative pose",
        "Looking down with eyes slightly lifted toward camera",
        "Hands framing the face, fingers lightly touching jawline"
    ]

    PHYSICS_MODES = [
        "🎲 Dynamic / Matched Physics",
        "💧 Oiled Skin & Specular Glistening (OiledSkin_ZIT)",
        "🔬 Realskin Subsurface Dermal Warmth (fluxRealSkin)",
        "✨ Wet Translucent Sheer Lace & Micro-Pores",
        "🖤 High-Gloss Liquid Latex & Polished Nappa Leather",
        "🎞️ 35mm Fine Analog Film Grain & Natural Specularity"
    ]

    SCENE_THEMES = [
        "🎲 Dynamic Cinematics Matrix",
        "✂️ Neutral Studio (Cutout / Alpha Isolation)",
        "🍷 Dark Parisian Boudoir (Candlelight & Velvet)",
        "🗼 Parisian Noir (Wet Cobblestones & Blue Hour)",
        "⚡ Cybernetic Sanctuary (Volumetric Neon & Terminals)",
        "🏛️ Opulent Penthouse Suite (Rainy Skyline 3 AM)",
        "🛁 Steamy Private Marble Bath (Clawfoot Tub & Mist)",
        "📸 Editorial Studio (Minimalist Solid Backdrop)"
    ]

    DIRECTOR_RIGS = [
        "Quentin Tarantino (Ultra Speed 40mm Punchy)",
        "Denis Villeneuve (Alexa 65 Anamorphic 50mm)",
        "Roger Deakins (Arri LF 32mm Tungsten)",
        "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)",
        "David Fincher (Red 8K Leica 27mm Monochromatic)",
        "Helmut Newton (Hasselblad 80mm B&W High-Fashion)",
        "Ridley Scott (Panavision 50mm f/1.4 Anamorphic)",
        "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)",
        "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)",
        "Michael Mann (Sony CineAlta 28mm Blue Ambient)",
        "🎲 Dynamic / Random Rig"
    ]

    HAIR_MODES = [
        "🎲 Dynamic Stochastic Hair (Bedhead, Wet, Tousled, Styled)",
        "👑 Signature Voluminous Ringlets (Uniform Mid-Back)",
        "🛏️ Sultry Disheveled Bedhead Curls",
        "💧 Damp / Wet Post-Shower Ringlets",
        "🎀 Messy Updo / High Bun with Tendrils",
        "💨 Wind-Swept / Dynamic Flowing Curls",
        "🥀 Side-Swept Over Bare Shoulder"
    ]

    PROMPT_FORMATS = [
        "🎬 Natural Cinematic Prose (Flux / ZIT)",
        "🏷️ Standard Tag-Delimited (Kohya / SDXL)"
    ]

    COHESION_MODES = [
        "🧠 Smart Context Equalizer (Matched Venue, Attire & Poses)",
        "🎨 Creative Contrast (Editorial High-Fashion)",
        "🎲 Pure Stochastic (Unfiltered Random)"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "rating_mode": (cls.RATING_MODES, {"default": "🎲 Stochastic Coin-Flip (Random NSFW / SFW)"}),
                "cohesion_equalizer": (cls.COHESION_MODES, {"default": "🧠 Smart Context Equalizer (Matched Venue, Attire & Poses)"}),
                "character_anchor": (cls.SUBJECT_MODES, {"default": "👑 Vespera (Photographic Baseline)"}),
                "hair_state_mode": (cls.HAIR_MODES, {"default": "🎲 Dynamic Stochastic Hair (Bedhead, Wet, Tousled, Styled)"}),
                "wardrobe_level": (cls.WARDROBE_TIERS, {"default": "🔞 Full Nudity (Anatomical Precision, Bare Realskin)"}),
                "pose_action_mode": (cls.POSE_MODES, {"default": "🎯 Tier 1: Identity Anchors (Close-Ups & 3D Head Angles)"}),
                "material_skin_physics": (cls.PHYSICS_MODES, {"default": "🎲 Dynamic / Matched Physics"}),
                "scene_environment": (cls.SCENE_THEMES, {"default": "🎲 Dynamic Cinematics Matrix"}),
                "director_camera_rig": (cls.DIRECTOR_RIGS, {"default": "Quentin Tarantino (Ultra Speed 40mm Punchy)"}),
                "prompt_engine_format": (cls.PROMPT_FORMATS, {"default": "🎬 Natural Cinematic Prose (Flux / ZIT)"}),
                "chaos_entropy": ("INT", {"default": 85, "min": 0, "max": 100, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": "randomize"}),
                "inline_custom_subject": ("STRING", {"multiline": False, "default": "", "placeholder": "Optional custom subject inline..."}),
                "auto_save_caption": ("BOOLEAN", {"default": True}),
                "caption_subfolder": ("STRING", {"default": "dataset_captions"}),
                "image_subfolder": ("STRING", {"default": "dataset_images"}),
                "upscale_subfolder": ("STRING", {"default": "dataset_upscaled"}),
                "mask_subfolder": ("STRING", {"default": "dataset_masks"}),
            },
            "optional": {
                "custom_character_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "custom_clothing_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "custom_scene_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = (
        "STRING",  # character_prompt
        "STRING",  # scene_prompt
        "STRING",  # master_fused_prompt
        "STRING",  # dataset_caption_txt
        "STRING",  # saved_caption_path
        "STRING",  # negative_prompt
        "STRING",  # active_wardrobe_text
        "STRING",  # active_pose_text
        "STRING",  # active_scene_text
        "STRING",  # active_director_camera
        "STRING",  # telemetry_summary
        "STRING",  # face_detailer_prompt
        "STRING",  # image_filename_prefix
        "STRING",  # mask_filename_prefix
        "STRING",  # upscale_filename_prefix
    )
    RETURN_NAMES = (
        "character_prompt",
        "scene_prompt",
        "master_fused_prompt",
        "dataset_caption_txt",
        "saved_caption_path",
        "negative_prompt",
        "active_wardrobe_text",
        "active_pose_text",
        "active_scene_text",
        "active_director_camera",
        "telemetry_summary",
        "face_detailer_prompt",
        "image_filename_prefix",
        "mask_filename_prefix",
        "upscale_filename_prefix",
    )
    FUNCTION = "synthesize_master_prompt"
    CATEGORY = UNIFIED_CATEGORY

    def synthesize_master_prompt(
        self,
        rating_mode: str,
        cohesion_equalizer: str,
        character_anchor: str,
        hair_state_mode: str,
        wardrobe_level: str,
        pose_action_mode: str,
        material_skin_physics: str,
        scene_environment: str,
        director_camera_rig: str,
        prompt_engine_format: str,
        chaos_entropy: int,
        seed: int,
        inline_custom_subject: str = "",
        auto_save_caption: bool = True,
        caption_subfolder: str = "dataset_captions",
        image_subfolder: str = "dataset_images",
        upscale_subfolder: str = "dataset_upscaled",
        mask_subfolder: str = "dataset_masks",
        custom_character_override: str = "",
        custom_clothing_override: str = "",
        custom_scene_override: str = ""
    ):
        rng = random.Random(seed)

        def clean_slug(text: str) -> str:
            slug = re.sub(r'[^a-zA-Z0-9]', '_', text)
            return re.sub(r'_+', '_', slug).strip('_')
        
        if "Random" in rating_mode or "Stochastic" in rating_mode or "Coin-Flip" in rating_mode:
            is_nsfw = rng.choice([True, False])
        else:
            is_nsfw = "NSFW" in rating_mode or "Explicit" in rating_mode

        use_equalizer = "Smart Context Equalizer" in cohesion_equalizer

        # 1. WARDROBE RESOLUTION
        tier_key_map = {
            "🔥 Lingerie (Lace, Teddy, Silk, Corsetry)": "lingerie",
            "😈 Slutty / Micro (Harness, Micro-Bikini, Latex, Fishnet)": "slutty",
            "🔞 Full Nudity (Anatomical Precision, Bare Realskin)": "nudity",
            "👀 Partial Nudity / Topless (Open Robe, Sheer Peeks, Topless)": "partial_nudity",
            "💋 Sexy / Provocative (Plunging Slips, Bodycon, High-Slits)": "sexy",
            "🍸 Glamorous (Haute Couture, Velvet Gowns, Silk Drapery)": "glamorous",
            "💼 Business / Power (Tailored Blazers, Cigarette Trousers)": "business",
            "☕ Casual (Cashmere, Distressed Selvedge Denim, Leather Jacket)": "casual"
        }

        if custom_clothing_override and custom_clothing_override.strip():
            attire = custom_clothing_override.strip()
            chosen_tier_name = "CUSTOM"
        else:
            if wardrobe_level == "🎲 Full Stochastic (Random All)":
                chosen_tier_name = rng.choice(list(WARDROBE_DATA.keys()))
            else:
                chosen_tier_name = tier_key_map.get(wardrobe_level, "nudity" if is_nsfw else "casual")

            tier_data = WARDROBE_DATA.get(chosen_tier_name, WARDROBE_DATA["nudity"])
            main_item = rng.choice(tier_data["items"])
            acc_item = rng.choice(tier_data["bottoms_acc"]) if tier_data.get("bottoms_acc") else ""

            parts_w = [f"Wearing {main_item}"] if not main_item.startswith("Wearing") and not main_item.startswith("completely nude") and not main_item.startswith("fully nude") else [main_item]
            if acc_item:
                parts_w.append(f"paired with {acc_item}")
            attire = ", ".join(parts_w)

        # 2. SCENE RESOLUTION
        if custom_scene_override and custom_scene_override.strip():
            env_text = custom_scene_override.strip()
        else:
            if scene_environment == "🎲 Dynamic Cinematics Matrix" and use_equalizer:
                if chosen_tier_name in ["nudity", "partial_nudity", "lingerie"]:
                    theme_choice = rng.choice(["boudoir", "bath", "penthouse_intimate", "studio"])
                elif chosen_tier_name in ["business", "casual"]:
                    theme_choice = rng.choice(["noir", "penthouse_salon", "editorial_studio", "boudoir_library"])
                elif chosen_tier_name == "glamorous":
                    theme_choice = rng.choice(["penthouse_salon", "editorial_studio", "noir_balcony", "boudoir_salon"])
                elif chosen_tier_name == "slutty":
                    theme_choice = rng.choice(["boudoir_gothic", "cybernetic", "studio", "penthouse_intimate"])
                else:
                    theme_choice = "boudoir"
            else:
                theme_choice = "custom_map"

            if theme_choice == "boudoir" or "Boudoir" in scene_environment:
                venue = rng.choice(BOUDOIR_FURNITURE_VENUES)
                sheets = rng.choice(BOUDOIR_SHEET_COLORS)
                env_text = f"{venue}, with {sheets}"
            elif theme_choice == "bath" or "Marble Bath" in scene_environment:
                env_text = rng.choice(ENVIRONMENTS_MAP["Steamy Private Marble Bath"])
            elif theme_choice in ["penthouse_intimate", "penthouse_salon"] or "Penthouse" in scene_environment:
                env_text = rng.choice(ENVIRONMENTS_MAP["Opulent Penthouse Suite"])
            elif theme_choice == "noir" or theme_choice == "noir_balcony" or "Parisian Noir" in scene_environment:
                env_text = rng.choice(ENVIRONMENTS_MAP["Parisian Noir"])
            elif theme_choice == "cybernetic" or "Cybernetic" in scene_environment:
                env_text = rng.choice(ENVIRONMENTS_MAP["Cybernetic Sanctuary"])
            elif theme_choice == "studio" or "Neutral Studio" in scene_environment:
                env_text = rng.choice(ENVIRONMENTS_MAP["Neutral Studio"])
            elif theme_choice == "editorial_studio" or "Editorial Studio" in scene_environment:
                env_text = rng.choice(ENVIRONMENTS_MAP["Editorial Studio"])
            else:
                all_envs = []
                for v in ENVIRONMENTS_MAP.values():
                    all_envs.extend(v)
                env_text = rng.choice(all_envs)

        # 3. HAIR RESOLUTION
        if use_equalizer and hair_state_mode == "🎲 Dynamic Stochastic Hair (Bedhead, Wet, Tousled, Styled)":
            if "Marble Bath" in env_text or "steam" in env_text.lower() or "tub" in env_text.lower():
                hair_pool = [
                    "damp, glistening post-shower ringlet curls clinging to her neck and collarbone with subtle wet shine and deep indigo undertones",
                    "a messy high bun with loose, curly tendrils and electric-indigo strands framing her sculpted jawline and temples",
                    "damp, towel-dried spiral curls with natural dewy texture and deep indigo sheen catching directional lighting"
                ]
                chosen_hair = rng.choice(hair_pool)
            elif "Boudoir" in env_text or "bed" in env_text.lower() or "sheets" in env_text.lower():
                hair_pool = [
                    "voluminous bedhead with messy, untamed 3B/3C spiral curls in jet-black with electric indigo highlights tumbling loosely over one eye and bare shoulders",
                    "tousled, pillow-disheveled ringlet curls cascading wildly across her back and bare chest in effortless morning disarray",
                    "intimately side-swept over one shoulder, exposing her bare neck, collarbone, and delicate earlobe"
                ]
                chosen_hair = rng.choice(hair_pool)
            elif "Parisian Noir" in env_text or "rain" in env_text.lower() or "alley" in env_text.lower():
                hair_pool = [
                    "wind-swept dynamic curls caught in mid-motion with flying electric-indigo strands catching volumetric light",
                    "side-parted voluminous curls spilling heavily over her left shoulder and framing her soft-smudged smoky eyeliner",
                    "dynamic flowing curls with natural motion blur on the tips, catching cool-blue rim lighting"
                ]
                chosen_hair = rng.choice(hair_pool)
            else:
                chosen_hair = rng.choice(HAIR_STATES)
        else:
            hair_map = {
                "👑 Signature Voluminous Ringlets (Uniform Mid-Back)": "Voluminous, springy 3B/3C spiral ringlet curls in deep jet-black with interwoven electric indigo highlights, uniform length cascading mid-back with no bangs framing her face and jawline",
                "🛏️ Sultry Disheveled Bedhead Curls": "voluminous bedhead with messy, untamed 3B/3C spiral curls in jet-black with electric indigo highlights tumbling loosely over one eye and bare shoulders",
                "💧 Damp / Wet Post-Shower Ringlets": "damp, glistening post-shower ringlet curls clinging to her neck and collarbone with subtle wet shine and deep indigo undertones",
                "🎀 Messy Updo / High Bun with Tendrils": "a messy high bun with loose, curly tendrils and electric-indigo strands framing her sculpted jawline and temples",
                "💨 Wind-Swept / Dynamic Flowing Curls": "wind-swept dynamic curls caught in mid-motion with flying electric-indigo strands catching volumetric light",
                "🥀 Side-Swept Over Bare Shoulder": "intimately side-swept over one shoulder, exposing her bare neck, collarbone, and delicate earlobe"
            }
            if hair_state_mode == "🎲 Dynamic Stochastic Hair (Bedhead, Wet, Tousled, Styled)":
                chosen_hair = rng.choice(HAIR_STATES)
            else:
                chosen_hair = hair_map.get(hair_state_mode, rng.choice(HAIR_STATES))

        # 4. CHARACTER ANCHOR
        if custom_character_override and custom_character_override.strip():
            char_base = custom_character_override.strip()
        elif inline_custom_subject and inline_custom_subject.strip():
            char_base = inline_custom_subject.strip()
        elif character_anchor == "👑 Vespera (35mm Raw Cinema)":
            char_base = VESPERA_VARIATIONS[1]
        elif character_anchor == "👑 Vespera (Editorial Still)":
            char_base = VESPERA_VARIATIONS[2]
        elif character_anchor == "🎲 Dynamic Random Subject Anchor":
            ethnicities = ["French", "Italian", "Spanish", "Scandinavian", "Japanese", "Brazilian", "Eastern European", "Greek"]
            eth = rng.choice(ethnicities)
            char_base = (
                f'A hyper-realistic photographic capture of a 5\'7" {eth} woman with defined athletic hourglass proportions, '
                f'narrow 24-inch waist, 38-inch flared hips, 30-inch muscular thighs, sculpted cheekbones, smooth luminous skin, and captivating eyes'
            )
        else:
            char_base = VESPERA_VARIATIONS[0]

        # 5. POSE, TIER MODULO SWEEPS, AND RIG RESOLUTION
        active_tier_tag = "dynamic"

        if "Full Master Sweep" in pose_action_mode or "1 Round" in pose_action_mode or "Mega Dataset Sweep" in pose_action_mode or "5 Round" in pose_action_mode:
            # Combined list of all 4 tiers: 15 + 10 + 15 + 10 = 50 total slots
            all_tiers = (
                [("T1", i, cfg) for i, cfg in enumerate(LORA_TIER1_ANCHORS)] +
                [("T2", i, cfg) for i, cfg in enumerate(LORA_TIER2_ANATOMY)] +
                [("T3", i, cfg) for i, cfg in enumerate(LORA_TIER3_WARDROBE)] +
                [("T4", i, cfg) for i, cfg in enumerate(LORA_TIER4_SPATIAL)]
            )
            total_slots = len(all_tiers)  # 50
            if "Mega Dataset Sweep" in pose_action_mode or "5 Round" in pose_action_mode:
                round_num = ((seed // total_slots) % 5) + 1
                slot_overall = seed % (total_slots * 5)
                tier_prefix, sub_idx, cfg = all_tiers[seed % total_slots]
                raw_name_match = re.search(r'\((.*?)\)', cfg['name'])
                slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg['name'])
                active_tier_tag = f"R{round_num}_{tier_prefix}_{sub_idx+1:02d}_{slug_name}"
            else:
                tier_prefix, sub_idx, cfg = all_tiers[seed % total_slots]
                raw_name_match = re.search(r'\((.*?)\)', cfg['name'])
                slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg['name'])
                active_tier_tag = f"{tier_prefix}_{sub_idx+1:02d}_{slug_name}"

            selected_pose = cfg['pose']
            selected_exp = cfg['expression']
            attire = custom_clothing_override.strip() or cfg['attire']
            env_text = custom_scene_override.strip() or cfg['env']
            rig_key = cfg['rig']
            rig = DIRECTOR_RIG_CONFIGS.get(rig_key, DIRECTOR_RIG_CONFIGS["Denis Villeneuve (Alexa 65 Anamorphic 50mm)"]).copy()
            selected_physics = cfg['physics']
            if tier_prefix == "T1":
                rig['camera'] = "shot on 85mm portrait lens at f/1.4, extreme shallow depth of field, creamy bokeh"

        elif "Tier 1" in pose_action_mode:
            matrix = LORA_TIER1_ANCHORS
            slot_idx = seed % len(matrix)
            cfg = matrix[slot_idx]
            selected_pose = cfg['pose']
            selected_exp = cfg['expression']
            attire = custom_clothing_override.strip() or cfg['attire']
            env_text = custom_scene_override.strip() or cfg['env']
            rig_key = cfg['rig']
            rig = DIRECTOR_RIG_CONFIGS.get(rig_key, DIRECTOR_RIG_CONFIGS["Denis Villeneuve (Alexa 65 Anamorphic 50mm)"]).copy()
            selected_physics = cfg['physics']
            rig['camera'] = "shot on 85mm portrait lens at f/1.4, extreme shallow depth of field, creamy bokeh"
            raw_name_match = re.search(r'\((.*?)\)', cfg['name'])
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg['name'])
            active_tier_tag = f"T1_{slot_idx+1:02d}_{slug_name}"

        elif "Tier 2" in pose_action_mode:
            matrix = LORA_TIER2_ANATOMY
            slot_idx = seed % len(matrix)
            cfg = matrix[slot_idx]
            selected_pose = cfg['pose']
            selected_exp = cfg['expression']
            attire = custom_clothing_override.strip() or cfg['attire']
            env_text = custom_scene_override.strip() or cfg['env']
            rig_key = cfg['rig']
            rig = DIRECTOR_RIG_CONFIGS.get(rig_key, DIRECTOR_RIG_CONFIGS["Denis Villeneuve (Alexa 65 Anamorphic 50mm)"]).copy()
            selected_physics = cfg['physics']
            raw_name_match = re.search(r'\((.*?)\)', cfg['name'])
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg['name'])
            active_tier_tag = f"T2_{slot_idx+1:02d}_{slug_name}"

        elif "Tier 3" in pose_action_mode:
            matrix = LORA_TIER3_WARDROBE
            slot_idx = seed % len(matrix)
            cfg = matrix[slot_idx]
            selected_pose = cfg['pose']
            selected_exp = cfg['expression']
            attire = custom_clothing_override.strip() or cfg['attire']
            env_text = custom_scene_override.strip() or cfg['env']
            rig_key = cfg['rig']
            rig = DIRECTOR_RIG_CONFIGS.get(rig_key, DIRECTOR_RIG_CONFIGS["Denis Villeneuve (Alexa 65 Anamorphic 50mm)"]).copy()
            selected_physics = cfg['physics']
            raw_name_match = re.search(r'\((.*?)\)', cfg['name'])
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg['name'])
            active_tier_tag = f"T3_{slot_idx+1:02d}_{slug_name}"

        elif "Tier 4" in pose_action_mode:
            matrix = LORA_TIER4_SPATIAL
            slot_idx = seed % len(matrix)
            cfg = matrix[slot_idx]
            selected_pose = cfg['pose']
            selected_exp = cfg['expression']
            attire = custom_clothing_override.strip() or cfg['attire']
            env_text = custom_scene_override.strip() or cfg['env']
            rig_key = cfg['rig']
            rig = DIRECTOR_RIG_CONFIGS.get(rig_key, DIRECTOR_RIG_CONFIGS["Denis Villeneuve (Alexa 65 Anamorphic 50mm)"]).copy()
            selected_physics = cfg['physics']
            raw_name_match = re.search(r'\((.*?)\)', cfg['name'])
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg['name'])
            active_tier_tag = f"T4_{slot_idx+1:02d}_{slug_name}"

        else:
            poses_pool = POSES_POOL_NSFW if is_nsfw else POSES_POOL_SFW
            expressions_pool = EXPRESSIONS_POOL_NSFW if is_nsfw else EXPRESSIONS_POOL_SFW
            selected_pose = rng.choice(poses_pool) if pose_action_mode == "🎲 Dynamic Random Pose" else pose_action_mode
            selected_exp = rng.choice(expressions_pool)

            slug_name = clean_slug(selected_pose[:35])
            active_tier_tag = f"Custom_{slug_name}"

            physics_pool = PHYSICS_POOL_NSFW if is_nsfw else PHYSICS_POOL_SFW
            physics_map = {
                "💧 Oiled Skin & Specular Glistening (OiledSkin_ZIT)": "realskin, oiled skin with glistening specular highlights and micro-droplets of water catching directional lighting",
                "🔬 Realskin Subsurface Dermal Warmth (fluxRealSkin)": "realskin, subsurface dermal scattering with natural warmth and soft flush across bare shoulders and collarbone",
                "✨ Wet Translucent Sheer Lace & Micro-Pores": "translucent sheer micro-lace tension revealing warm biological realskin texture and anatomical contours underneath",
                "🖤 High-Gloss Liquid Latex & Polished Nappa Leather": "high-gloss liquid latex and nappa leather sheen with crisp ray-traced reflections of ambient scene lighting",
                "🎞️ 35mm Fine Analog Film Grain & Natural Specularity": "fine 35mm film grain, realskin natural pores with authentic specular sheen on bare skin"
            }
            selected_physics = physics_map.get(material_skin_physics, rng.choice(physics_pool))

            if director_camera_rig == "🎲 Dynamic / Random Rig":
                rig_key = rng.choice(list(DIRECTOR_RIG_CONFIGS.keys()))
            else:
                rig_key = director_camera_rig if director_camera_rig in DIRECTOR_RIG_CONFIGS else "Denis Villeneuve (Alexa 65 Anamorphic 50mm)"
            
            rig = DIRECTOR_RIG_CONFIGS.get(rig_key, DIRECTOR_RIG_CONFIGS["Denis Villeneuve (Alexa 65 Anamorphic 50mm)"]).copy()

        full_action = f"{selected_pose}, with {selected_exp}"

        # 6. ASSEMBLE CHANNELS
        is_tags = "Tags" in prompt_engine_format or "Tag-Delimited" in prompt_engine_format
        quality_tags = "masterpiece, 8k resolution, ultra-detailed, photorealistic, raw 35mm photograph, authentic texture"

        cleaned_scene = strip_prompt_conflicts(env_text, strip_hair=True, strip_eyes=True, strip_body=True)
        cleaned_attire = strip_prompt_conflicts(attire, strip_hair=True, strip_eyes=True, strip_body=True)

        if is_tags:
            character_prompt = f"({char_base}:1.1), {cleaned_attire}, {full_action}, {selected_physics}"
            scene_prompt = f"{cleaned_scene}, {rig['lighting']}, natural depth of field, {rig['camera']}, {rig['director']}, {rig['lut']}"
            master_fused_prompt = f"{character_prompt}, {scene_prompt}, {quality_tags}"
        else:
            character_prompt = f"{char_base}. {cleaned_attire.capitalize()}, {full_action}. Featuring {selected_physics}."
            scene_prompt = f"In the scene, {cleaned_scene}. Atmospheric illumination: {rig['lighting']}. Cinematography by {rig['director']}, color graded with {rig['lut']}. Captured on {rig['camera']}."
            master_fused_prompt = f"{character_prompt} {scene_prompt}"

        # Surgical Caption Assembly
        scrubbed_action = strip_prompt_conflicts(full_action, strip_hair=False, strip_eyes=True, strip_body=True)
        dataset_caption_txt = f"{char_base}, {cleaned_attire}, {scrubbed_action}"

        # Dedicated FaceDetailer Dynamic Micro-Prompt
        live_traits = fetch_live_vespera_traits()
        if live_traits:
            face_detailer_prompt = f"{VESPERA_FACE_MICROPACK}, traits: {live_traits}"
        else:
            face_detailer_prompt = VESPERA_FACE_MICROPACK

        raw_tag = f"vespera_{active_tier_tag}"
        
        # Build path-aware prefixes for ComfyUI SaveImage
        img_sub = image_subfolder.strip().strip("/\\")
        upscale_sub = upscale_subfolder.strip().strip("/\\")
        mask_sub = mask_subfolder.strip().strip("/\\")
        cap_sub = caption_subfolder.strip().strip("/\\")

        image_filename_prefix = f"{img_sub}/{raw_tag}" if img_sub else raw_tag
        mask_filename_prefix = f"{mask_sub}/{raw_tag}" if mask_sub else raw_tag
        upscale_filename_prefix = f"{upscale_sub}/{raw_tag}" if upscale_sub else raw_tag

        saved_caption_path = "DISABLED"
        if auto_save_caption:
            base_out = folder_paths.get_output_directory()
            out_dir = Path(base_out) / cap_sub if cap_sub else Path(base_out)
            out_dir.mkdir(parents=True, exist_ok=True)
            caption_file = out_dir / f"{raw_tag}_{seed:012d}.txt"
            caption_file.write_text(dataset_caption_txt, encoding="utf-8")
            saved_caption_path = str(caption_file)

        negative_prompt = (
            "blurry, low quality, deformed anatomy, extra limbs, bad hands, mutated fingers, "
            "plastic skin, cartoon, anime, illustration, oversaturated, watermark, signature, duplicate, "
            "round face, button nose, wide nose bridge, blonde hair, blue eyes"
        )

        telemetry_summary = (
            f"👑 SUBJECT: {character_anchor} | 👗 WARDROBE: {chosen_tier_name.upper()} | "
            f"🎬 RIG: {rig_key} | 🏛️ SCENE: {scene_environment} | 🎲 SEED: {seed}"
        )

        return (
            character_prompt,
            scene_prompt,
            master_fused_prompt,
            dataset_caption_txt,
            saved_caption_path,
            negative_prompt,
            attire,
            full_action,
            env_text,
            f"{rig['director']}. {rig['camera']}",
            telemetry_summary,
            face_detailer_prompt,
            image_filename_prefix,
            mask_filename_prefix,
            upscale_filename_prefix
        )


NODE_CLASS_MAPPINGS = {
    "ZITCharacterOverrideNode": ZITCharacterOverrideNode,
    "ZITBackgroundArchitectNode": ZITBackgroundArchitectNode,
    "VesperaCharacterEncoder": VesperaCharacterEncoder,
    "ZITDynamicWardrobeEngine": ZITDynamicWardrobeEngine,
    "ZITMasterPromptWorkstation": ZITMasterPromptWorkstation
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZITCharacterOverrideNode": "ZIT Character Override & Synthesizer",
    "ZITBackgroundArchitectNode": "ZIT Background & Environment Architect",
    "VesperaCharacterEncoder": "Vespera Character Prompt Encoder",
    "ZITDynamicWardrobeEngine": "👗 ZIT Dynamic Wardrobe Engine",
    "ZITMasterPromptWorkstation": "🍷 ZIT Master Prompt Workstation (All-In-One)"
}