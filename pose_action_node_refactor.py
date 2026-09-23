"""
File    : pose_action_node_refactor.py
Purpose : Standalone Refactored Pose & Action Node with full 4-tier matrix sweeps and explicit cinematic poses.
"""

import re
import random

try:
    from .zit_data import (
        LORA_TIER1_ANCHORS,
        LORA_TIER2_ANATOMY,
        LORA_TIER3_WARDROBE,
        LORA_TIER4_SPATIAL,
        DIRECTOR_RIG_CONFIGS,
        POSES_POOL_NSFW,
        POSES_POOL_SFW,
        EXPRESSIONS_POOL_NSFW,
        EXPRESSIONS_POOL_SFW,
    )
except (ImportError, ModuleNotFoundError):
    try:
        from zit_data import (
            LORA_TIER1_ANCHORS,
            LORA_TIER2_ANATOMY,
            LORA_TIER3_WARDROBE,
            LORA_TIER4_SPATIAL,
            DIRECTOR_RIG_CONFIGS,
            POSES_POOL_NSFW,
            POSES_POOL_SFW,
            EXPRESSIONS_POOL_NSFW,
            EXPRESSIONS_POOL_SFW,
        )
    except Exception:
        LORA_TIER1_ANCHORS = []
        LORA_TIER2_ANATOMY = []
        LORA_TIER3_WARDROBE = []
        LORA_TIER4_SPATIAL = []
        DIRECTOR_RIG_CONFIGS = {}
        POSES_POOL_NSFW = []
        POSES_POOL_SFW = []
        EXPRESSIONS_POOL_NSFW = []
        EXPRESSIONS_POOL_SFW = []


class RefactoredPoseActionNode:
    """Refactored Pose & Action Node: Deterministic modulo sweeps (Tier 1-4) and explicit cinematic poses."""

    POSE_MODES = [
        "🔄 Full Master Sweep (1 Round: Tier 1 to Tier 4 - 50 Poses)",
        "🔁 Mega Dataset Sweep (5 Rounds - 250 Batch)",
        "🔁 Foundation Sweep (10 Rounds - 500 Batch)",
        "🔁 Enterprise Sweep (20 Rounds - 1000 Batch)",
        "🔁 Odyssey Sweep (30 Rounds - 1500 Batch)",
        "🔁 Matrix Sweep (40 Rounds - 2000 Batch)",
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

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "pose_action_mode": (cls.POSE_MODES, {"default": "🎯 Tier 1: Sequential Sweep (15 Identity Anchors)"}),
            },
            "optional": {
                "custom_pose_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("pose_prompt", "active_tier_tag", "camera_framing", "wardrobe_prompt", "scene_lighting_prompt", "expression_prompt")
    FUNCTION = "run"
    CATEGORY = "ZIT/Dataset Workstation"

    ROUND_MODULATIONS = {
        1: {
            "theme": "Pristine Editorial Studio",
            "lighting": "balanced neutral studio key lighting with soft directional wrap-around fill, 5600K daylight balance, subtle specular hair light, authentic spatial separation",
            "camera_85": "shot on 85mm prime portrait lens at f/1.4, razor-sharp eyelash plane, creamy background bokeh, distinct catchlights",
            "camera_50": "shot on 50mm f/1.4 prime lens, natural direct perspective, pristine optical acutance, authentic depth falloff",
            "exp_nuance": "calm, intense direct gaze with steady focus",
            "env_tone": "minimalist high-fashion studio with seamless warm-grey cyclorama wall"
        },
        2: {
            "theme": "Chiaroscuro & Low-Key Drama",
            "lighting": "dramatic low-key chiaroscuro lighting, deep sculptural directional shadow falloff, subtle warm 3200K tungsten edge rim, rich atmospheric density",
            "camera_85": "shot on 85mm f/1.4 cinema lens, subtle low-angle tilt, authentic micro-tonal gradation",
            "camera_50": "shot on 50mm f/1.4 cinema lens, intimate low-key angle, authentic filmic contrast",
            "exp_nuance": "penetrating focused stare with subtle parted lips and deep intensity",
            "env_tone": "atmospheric dark architectural interior with rich charcoal shadows and subtle practical tungsten glow"
        },
        3: {
            "theme": "Cool High-Key Daylight & Window Ambient",
            "lighting": "cool overcast natural daylight, soft diffused North-facing window bounce, luminous skin reflection with organic micro-tonal gradation",
            "camera_85": "shot on 85mm f/1.8 prime lens, natural eye-level framing, delicate organic depth falloff",
            "camera_50": "shot on 50mm f/1.8 prime lens, natural eye-level framing, delicate organic focal falloff",
            "exp_nuance": "contemplative, relaxed expression with softened gaze and natural composure",
            "env_tone": "high-ceiling Parisian atelier apartment with tall French windows and airy soft daylight"
        },
        4: {
            "theme": "Editorial Dual-Tone & Chromatic Edge",
            "lighting": "high-contrast editorial dual-tone lighting, soft warm key with subtle electric-violet rim backlight catching curl contours, razor-sharp optical acutance",
            "camera_85": "shot on 85mm f/1.2 lens, dynamic slight angle, ultra-shallow depth of field",
            "camera_50": "shot on 50mm f/1.2 lens, dynamic three-quarter framing, crisp edge separation",
            "exp_nuance": "knowing confident expression with slight eyebrow arch and subtle micro-smirk",
            "env_tone": "sleek contemporary gallery with dark brushed surfaces and dramatic accent beams"
        },
        5: {
            "theme": "Warm Golden Hour & Sunset Rake",
            "lighting": "warm golden hour rake lighting, low-angle late-afternoon sunbeam catching cheekbones and collarbones, rich golden skin undertones with delicate lens flare",
            "camera_85": "shot on 85mm portrait prime, warm organic falloff, fine photographic grain, subtle lens flare",
            "camera_50": "shot on 50mm portrait prime, warm organic focal falloff, fine photographic grain",
            "exp_nuance": "radiant magnetic expression with soft parted lips catching warm sun highlights",
            "env_tone": "luxury penthouse terrace at sunset with golden amber horizon and warm ambient glow"
        }
    }

    def run(self, master_seed: int, pose_action_mode: str, custom_pose_override: str = "", **kwargs):
        if custom_pose_override and custom_pose_override.strip():
            return (custom_pose_override.strip(), "custom_override", "custom framing", "", "", "")

        rng = random.Random(master_seed)

        def clean_slug(text: str) -> str:
            slug = re.sub(r'[^a-zA-Z0-9]', '_', text)
            return re.sub(r'_+', '_', slug).strip('_')

        active_tier_tag = "dynamic_pose"
        camera_framing = "85mm portrait lens, shallow depth of field"

        if "Sweep" in pose_action_mode and "Batch" in pose_action_mode or "Round" in pose_action_mode:
            all_tiers = (
                [("T1", i, cfg) for i, cfg in enumerate(LORA_TIER1_ANCHORS)] +
                [("T2", i, cfg) for i, cfg in enumerate(LORA_TIER2_ANATOMY)] +
                [("T3", i, cfg) for i, cfg in enumerate(LORA_TIER3_WARDROBE)] +
                [("T4", i, cfg) for i, cfg in enumerate(LORA_TIER4_SPATIAL)]
            )
            total_slots = len(all_tiers) if all_tiers else 1
            
            # Parse max rounds from the mode string
            rmatch = re.search(r'\((\d+)\s+Rounds?', pose_action_mode)
            max_rounds = int(rmatch.group(1)) if rmatch else 1
            
            round_num = ((master_seed // total_slots) % max_rounds) + 1
            
            # To ensure seeds > 250 are mathematically distinct, we shuffle the modulo baseline for poses in higher rounds
            if round_num > 5:
                slot_idx = (master_seed + (round_num * 17)) % total_slots
            else:
                slot_idx = master_seed % total_slots
                
            tier_prefix, sub_idx, cfg = all_tiers[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            
            if max_rounds > 1:
                active_tier_tag = f"R{round_num}_{tier_prefix}_{sub_idx+1:02d}_{slug_name}"
            else:
                active_tier_tag = f"{tier_prefix}_{sub_idx+1:02d}_{slug_name}"

            mod_idx = ((round_num - 1) % 5) + 1
            mod = self.ROUND_MODULATIONS.get(mod_idx, self.ROUND_MODULATIONS[1])
            
            # Cross-pollinate environments for extreme rounds so they are genuinely new
            if round_num > 5:
                env_mod_idx = ((round_num * 3) % 5) + 1
                mod = dict(mod) # create a copy
                mod['env_tone'] = self.ROUND_MODULATIONS.get(env_mod_idx, mod)['env_tone']
            camera_framing = mod["camera_85"] if tier_prefix == "T1" else mod["camera_50"]

            base_exp = cfg.get('expression', '').strip()
            if round_num == 1 or not base_exp:
                active_exp = base_exp if base_exp else mod["exp_nuance"]
            else:
                active_exp = f"{base_exp}, {mod['exp_nuance']}"

            base_env = cfg.get('env', '').strip()
            if base_env:
                scene_lighting = f"{base_env}, {mod['lighting']}"
            else:
                scene_lighting = f"{mod['env_tone']}, {mod['lighting']}"

            selected_pose = cfg.get('pose', '').strip()
            selected_physics = cfg.get('physics', '').strip()
            pose_prompt = ", ".join(p for p in [selected_pose, active_exp, selected_physics] if p)
            return (pose_prompt, active_tier_tag, camera_framing, cfg.get('attire', ''), scene_lighting, active_exp)

        elif "Tier 1" in pose_action_mode and LORA_TIER1_ANCHORS:
            total = len(LORA_TIER1_ANCHORS)
            round_num = ((master_seed // total) % 5) + 1
            slot_idx = master_seed % total
            cfg = LORA_TIER1_ANCHORS[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            prefix_round = f"R{round_num}_" if round_num > 1 else ""
            active_tier_tag = f"{prefix_round}T1_{slot_idx+1:02d}_{slug_name}"

            mod = self.ROUND_MODULATIONS.get(round_num, self.ROUND_MODULATIONS[1])
            camera_framing = mod["camera_85"]

            base_exp = cfg.get('expression', '').strip()
            active_exp = base_exp if round_num == 1 or not base_exp else f"{base_exp}, {mod['exp_nuance']}"
            base_env = cfg.get('env', '').strip()
            scene_lighting = f"{base_env}, {mod['lighting']}" if base_env else f"{mod['env_tone']}, {mod['lighting']}"

            selected_pose = cfg.get('pose', '').strip()
            selected_physics = cfg.get('physics', '').strip()
            pose_prompt = ", ".join(p for p in [selected_pose, active_exp, selected_physics] if p)
            return (pose_prompt, active_tier_tag, camera_framing, cfg.get('attire', ''), scene_lighting, active_exp)

        elif "Tier 2" in pose_action_mode and LORA_TIER2_ANATOMY:
            total = len(LORA_TIER2_ANATOMY)
            round_num = ((master_seed // total) % 5) + 1
            slot_idx = master_seed % total
            cfg = LORA_TIER2_ANATOMY[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            prefix_round = f"R{round_num}_" if round_num > 1 else ""
            active_tier_tag = f"{prefix_round}T2_{slot_idx+1:02d}_{slug_name}"

            mod = self.ROUND_MODULATIONS.get(round_num, self.ROUND_MODULATIONS[1])
            camera_framing = mod["camera_50"]

            base_exp = cfg.get('expression', '').strip()
            active_exp = base_exp if round_num == 1 or not base_exp else f"{base_exp}, {mod['exp_nuance']}"
            base_env = cfg.get('env', '').strip()
            scene_lighting = f"{base_env}, {mod['lighting']}" if base_env else f"{mod['env_tone']}, {mod['lighting']}"

            selected_pose = cfg.get('pose', '').strip()
            selected_physics = cfg.get('physics', '').strip()
            pose_prompt = ", ".join(p for p in [selected_pose, active_exp, selected_physics] if p)
            return (pose_prompt, active_tier_tag, camera_framing, cfg.get('attire', ''), scene_lighting, active_exp)

        elif "Tier 3" in pose_action_mode and LORA_TIER3_WARDROBE:
            total = len(LORA_TIER3_WARDROBE)
            round_num = ((master_seed // total) % 5) + 1
            slot_idx = master_seed % total
            cfg = LORA_TIER3_WARDROBE[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            prefix_round = f"R{round_num}_" if round_num > 1 else ""
            active_tier_tag = f"{prefix_round}T3_{slot_idx+1:02d}_{slug_name}"

            mod = self.ROUND_MODULATIONS.get(round_num, self.ROUND_MODULATIONS[1])
            camera_framing = mod["camera_50"]

            base_exp = cfg.get('expression', '').strip()
            active_exp = base_exp if round_num == 1 or not base_exp else f"{base_exp}, {mod['exp_nuance']}"
            base_env = cfg.get('env', '').strip()
            scene_lighting = f"{base_env}, {mod['lighting']}" if base_env else f"{mod['env_tone']}, {mod['lighting']}"

            selected_pose = cfg.get('pose', '').strip()
            selected_physics = cfg.get('physics', '').strip()
            pose_prompt = ", ".join(p for p in [selected_pose, active_exp, selected_physics] if p)
            return (pose_prompt, active_tier_tag, camera_framing, cfg.get('attire', ''), scene_lighting, active_exp)

        elif "Tier 4" in pose_action_mode and LORA_TIER4_SPATIAL:
            total = len(LORA_TIER4_SPATIAL)
            round_num = ((master_seed // total) % 5) + 1
            slot_idx = master_seed % total
            cfg = LORA_TIER4_SPATIAL[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            prefix_round = f"R{round_num}_" if round_num > 1 else ""
            active_tier_tag = f"{prefix_round}T4_{slot_idx+1:02d}_{slug_name}"

            mod = self.ROUND_MODULATIONS.get(round_num, self.ROUND_MODULATIONS[1])
            camera_framing = mod["camera_50"]

            base_exp = cfg.get('expression', '').strip()
            active_exp = base_exp if round_num == 1 or not base_exp else f"{base_exp}, {mod['exp_nuance']}"
            base_env = cfg.get('env', '').strip()
            scene_lighting = f"{base_env}, {mod['lighting']}" if base_env else f"{mod['env_tone']}, {mod['lighting']}"

            selected_pose = cfg.get('pose', '').strip()
            selected_physics = cfg.get('physics', '').strip()
            pose_prompt = ", ".join(p for p in [selected_pose, active_exp, selected_physics] if p)
            return (pose_prompt, active_tier_tag, camera_framing, cfg.get('attire', ''), scene_lighting, active_exp)

        elif pose_action_mode == "🎲 Dynamic Random Pose":
            all_poses = (POSES_POOL_SFW or ["standing confidently"]) + (POSES_POOL_NSFW or [])
            all_exps = (EXPRESSIONS_POOL_SFW or ["focused intense gaze"]) + (EXPRESSIONS_POOL_NSFW or [])
            chosen_pose = rng.choice(all_poses)
            chosen_exp = rng.choice(all_exps)
            active_tier_tag = "dynamic_random"
            camera_framing = "cinematic 50mm framing"
            return (f"{chosen_pose}, {chosen_exp}", active_tier_tag, camera_framing, "", "")

        else:
            all_exps = (EXPRESSIONS_POOL_SFW or ["focused gaze"])
            chosen_exp = rng.choice(all_exps)
            active_tier_tag = clean_slug(pose_action_mode[:30])
            camera_framing = "cinematic framing with full headroom"
            return (f"{pose_action_mode}, {chosen_exp}", active_tier_tag, camera_framing, "", "")

