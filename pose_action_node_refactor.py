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

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("pose_prompt", "active_tier_tag", "camera_framing")
    FUNCTION = "run"
    CATEGORY = "ZIT/Dataset Workstation"

    def run(self, master_seed: int, pose_action_mode: str, custom_pose_override: str = "", **kwargs):
        if custom_pose_override and custom_pose_override.strip():
            return (custom_pose_override.strip(), "custom_override", "custom framing")

        rng = random.Random(master_seed)

        def clean_slug(text: str) -> str:
            slug = re.sub(r'[^a-zA-Z0-9]', '_', text)
            return re.sub(r'_+', '_', slug).strip('_')

        active_tier_tag = "dynamic_pose"
        camera_framing = "85mm portrait lens, shallow depth of field"

        if "Full Master Sweep" in pose_action_mode or "1 Round" in pose_action_mode or "Mega Dataset Sweep" in pose_action_mode or "5 Round" in pose_action_mode:
            all_tiers = (
                [("T1", i, cfg) for i, cfg in enumerate(LORA_TIER1_ANCHORS)] +
                [("T2", i, cfg) for i, cfg in enumerate(LORA_TIER2_ANATOMY)] +
                [("T3", i, cfg) for i, cfg in enumerate(LORA_TIER3_WARDROBE)] +
                [("T4", i, cfg) for i, cfg in enumerate(LORA_TIER4_SPATIAL)]
            )
            total_slots = len(all_tiers) if all_tiers else 1
            if "Mega Dataset Sweep" in pose_action_mode or "5 Round" in pose_action_mode:
                round_num = ((master_seed // total_slots) % 5) + 1
                tier_prefix, sub_idx, cfg = all_tiers[master_seed % total_slots]
                raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
                slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
                active_tier_tag = f"R{round_num}_{tier_prefix}_{sub_idx+1:02d}_{slug_name}"
            else:
                tier_prefix, sub_idx, cfg = all_tiers[master_seed % total_slots]
                raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
                slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
                active_tier_tag = f"{tier_prefix}_{sub_idx+1:02d}_{slug_name}"

            selected_pose = cfg.get('pose', '')
            selected_exp = cfg.get('expression', '')
            selected_physics = cfg.get('physics', '')
            camera_framing = "shot on 85mm portrait lens at f/1.4, extreme shallow depth of field" if tier_prefix == "T1" else "50mm prime lens, natural perspective"
            pose_prompt = f"{selected_pose}, {selected_exp}, {selected_physics}".strip(", ")
            return (pose_prompt, active_tier_tag, camera_framing)

        elif "Tier 1" in pose_action_mode and LORA_TIER1_ANCHORS:
            slot_idx = master_seed % len(LORA_TIER1_ANCHORS)
            cfg = LORA_TIER1_ANCHORS[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            active_tier_tag = f"T1_{slot_idx+1:02d}_{slug_name}"
            camera_framing = "shot on 85mm portrait lens at f/1.4, extreme shallow depth of field, creamy bokeh"
            pose_prompt = f"{cfg.get('pose', '')}, {cfg.get('expression', '')}, {cfg.get('physics', '')}".strip(", ")
            return (pose_prompt, active_tier_tag, camera_framing)

        elif "Tier 2" in pose_action_mode and LORA_TIER2_ANATOMY:
            slot_idx = master_seed % len(LORA_TIER2_ANATOMY)
            cfg = LORA_TIER2_ANATOMY[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            active_tier_tag = f"T2_{slot_idx+1:02d}_{slug_name}"
            camera_framing = "50mm portrait lens, sharp anatomical ratios"
            pose_prompt = f"{cfg.get('pose', '')}, {cfg.get('expression', '')}, {cfg.get('physics', '')}".strip(", ")
            return (pose_prompt, active_tier_tag, camera_framing)

        elif "Tier 3" in pose_action_mode and LORA_TIER3_WARDROBE:
            slot_idx = master_seed % len(LORA_TIER3_WARDROBE)
            cfg = LORA_TIER3_WARDROBE[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            active_tier_tag = f"T3_{slot_idx+1:02d}_{slug_name}"
            camera_framing = "full-length 50mm fashion framing"
            pose_prompt = f"{cfg.get('pose', '')}, {cfg.get('expression', '')}, {cfg.get('physics', '')}".strip(", ")
            return (pose_prompt, active_tier_tag, camera_framing)

        elif "Tier 4" in pose_action_mode and LORA_TIER4_SPATIAL:
            slot_idx = master_seed % len(LORA_TIER4_SPATIAL)
            cfg = LORA_TIER4_SPATIAL[slot_idx]
            raw_name_match = re.search(r'\((.*?)\)', cfg.get('name', ''))
            slug_name = clean_slug(raw_name_match.group(1)) if raw_name_match else clean_slug(cfg.get('name', ''))
            active_tier_tag = f"T4_{slot_idx+1:02d}_{slug_name}"
            camera_framing = "wide 35mm environmental angle"
            pose_prompt = f"{cfg.get('pose', '')}, {cfg.get('expression', '')}, {cfg.get('physics', '')}".strip(", ")
            return (pose_prompt, active_tier_tag, camera_framing)

        elif pose_action_mode == "🎲 Dynamic Random Pose":
            all_poses = (POSES_POOL_SFW or ["standing confidently"]) + (POSES_POOL_NSFW or [])
            all_exps = (EXPRESSIONS_POOL_SFW or ["focused intense gaze"]) + (EXPRESSIONS_POOL_NSFW or [])
            chosen_pose = rng.choice(all_poses)
            chosen_exp = rng.choice(all_exps)
            active_tier_tag = "dynamic_random"
            camera_framing = "cinematic 50mm framing"
            return (f"{chosen_pose}, {chosen_exp}", active_tier_tag, camera_framing)

        else:
            all_exps = (EXPRESSIONS_POOL_SFW or ["focused gaze"])
            chosen_exp = rng.choice(all_exps)
            active_tier_tag = clean_slug(pose_action_mode[:30])
            camera_framing = "cinematic framing with full headroom"
            return (f"{pose_action_mode}, {chosen_exp}", active_tier_tag, camera_framing)
