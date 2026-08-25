"""
File    : prompt_workstation_refactor.py
Purpose : Standalone Refactored Prompt Workstation node — complete feature agnosticism
          with 14 curly hairstyles, 10 lip shades, 12 synchronized manicures,
          and locked canonical Vespera photographic baseline.
"""

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None


class RefactoredPromptWorkstation:
    """Prompt Workstation for Vespera character dataset synthesis with full feature agnosticism.

    - Rotates 14 hairstyles, 10 lip colors, and 12 nail colors across seeds to prevent LoRA overbaking.
    - Hair states preserve curly ringlet physics (up-dos, high ponytails, wet looks, messy bedhead,
      side-swept, half-up half-down, pinned finger waves) to maintain perfect harmony with PuLID
      facial embeddings without cross-attention warping.
    - Synchronizes fingernail and toenail colors per render.
    - Direct export prefixes, negative prompt, and biometric face detailer wildcards.
    """

    DEFAULT_SUBJECT_CORE = (
        "photorealistic 8k portrait of Vespera, gorgeous woman of French-Levantine heritage in late-30s, "
        "luminous warm olive skin with natural micro-pores and golden undertones, "
        "captivating deep hazel-green almond-shaped eyes with soft-smudged smoky black kohl eyeliner, "
        "tiny beauty mark at upper-left lip corner, athletic hourglass figure, narrow defined waist, toned curves"
    )

    DEFAULT_NEGATIVE = (
        "blurry, out of focus, low quality, deformed, extra limbs, bad anatomy, bad hands, "
        "missing fingers, plastic smooth skin, oversaturated, cartoon, 3d render, illustration, "
        "blonde hair, blue eyes, Asian, pale white skin, tattoo, piercing, straight flat hair"
    )

    DEFAULT_FACE_DETAILER = (
        "hyper-detailed 8k photograph of Vespera, hazel-green almond eyes with amber striations, "
        "soft-smudged smoky kohl eyeliner, tiny beauty mark above left lip corner, "
        "sculpted high cheekbones, natural epidermal micro-pores and golden undertones, pristine eye focus"
    )

    # ────────────────────────── 14 Expanded Hair Styles ──────────────────────────
    HAIR_STYLES = [
        "voluminous jet-black 3B/3C spiral corkscrew curls with fine electric-indigo highlights cascading past shoulders",
        "elegant high curly up-do pinned atop head with loose spiral tendrils framing face and collarbones",
        "sleek high ponytail with tight jet-black spiral ringlets spilling down back",
        "wet slicked-back spiral ringlets glistening with moisture and cascading over shoulders",
        "messy tousled bedhead corkscrew curls framing face with voluminous natural texture",
        "side-swept spiral corkscrew ringlets draped elegantly over one shoulder",
        "half-up half-down spiral curls with top section pinned neatly at the crown",
        "voluminous natural afro-textured 3C ringlets with deep indigo sheen framing facial structure",
        "loose relaxed corkscrew waves falling naturally around collarbones with soft volume",
        "pinned retro finger-wave curls at front with voluminous spiral ringlets at back",
        "high curly topknot bun with face-framing curly ringlet tendrils",
        "double high curly pigtails with tight spiral ringlets bouncing around shoulders",
        "wind-blown dynamic spiral ringlets with natural movement and separation",
        "low nape-of-neck curly chignon bun with delicate spiral curls escaping at temples",
    ]

    # ────────────────────────── 10 Expanded Lip Finishes ──────────────────────────
    LIP_COLORS = [
        "soft black satin lipstick",
        "deep berry matte lips",
        "nude mauve satin lips",
        "natural bare rosy lips with subtle sheen",
        "rich dark oxblood lipstick",
        "deep crimson velvet matte lipstick",
        "metallic blackberry gloss lips",
        "subtle warm nude tinted lip balm",
        "high-gloss clear lacquer over natural rosy lips",
        "dark plum satin lipstick",
    ]

    # ────────────────────────── 12 Expanded Nail Colors ──────────────────────────
    NAIL_COLORS = [
        "glossy black matching fingernails and toenails",
        "deep oxblood red matching fingernails and toenails",
        "clean classic French manicure on fingernails and toenails",
        "natural clean unpolished manicured fingernails and toenails",
        "metallic chrome matching fingernails and toenails",
        "nude mauve matching fingernails and toenails",
        "deep burgundy matching fingernails and toenails",
        "matte charcoal matching fingernails and toenails",
        "dark emerald green matching fingernails and toenails",
        "rich plum matching fingernails and toenails",
        "pearl white iridescent matching fingernails and toenails",
        "subtle gold foil accent matching fingernails and toenails",
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":     ("INT",    {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "subject_core":    ("STRING", {"multiline": True, "default": cls.DEFAULT_SUBJECT_CORE}),
            },
            "optional": {
                "pose_prompt":           ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "active_tier_tag":       ("STRING", {"default": "", "forceInput": True}),
                "wardrobe_prompt":       ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "scene_lighting_prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "hair_override":         (["🎲 Dynamic Rotation"] + cls.HAIR_STYLES, {"default": "🎲 Dynamic Rotation"}),
                "lip_override":          (["🎲 Dynamic Rotation"] + cls.LIP_COLORS, {"default": "🎲 Dynamic Rotation"}),
                "nail_override":         (["🎲 Dynamic Rotation"] + cls.NAIL_COLORS, {"default": "🎲 Dynamic Rotation"}),
                "custom_prompt":         ("STRING", {"multiline": True, "default": ""}),
                "custom_negative":       ("STRING", {"multiline": True, "default": cls.DEFAULT_NEGATIVE}),
            }
        }

    RETURN_TYPES  = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES  = (
        "fused_prompt",
        "negative_prompt",
        "face_detailer_prompt",
        "image_filename_prefix",
        "mask_filename_prefix",
        "upscale_filename_prefix",
        "telemetry_summary"
    )
    FUNCTION      = "run"
    CATEGORY      = "ZIT/Dataset Workstation"

    def run(
        self,
        master_seed: int,
        subject_core: str = DEFAULT_SUBJECT_CORE,
        pose_prompt: str = "",
        active_tier_tag: str = "",
        wardrobe_prompt: str = "",
        scene_lighting_prompt: str = "",
        hair_override: str = "🎲 Dynamic Rotation",
        lip_override: str = "🎲 Dynamic Rotation",
        nail_override: str = "🎲 Dynamic Rotation",
        custom_prompt: str = "",
        custom_negative: str = DEFAULT_NEGATIVE,
        **kwargs
    ):
        # 1. Feature Agnosticism Selection (deterministic modulo rotation)
        if hair_override == "🎲 Dynamic Rotation" or hair_override not in self.HAIR_STYLES:
            hair = self.HAIR_STYLES[master_seed % len(self.HAIR_STYLES)]
        else:
            hair = hair_override

        if lip_override == "🎲 Dynamic Rotation" or lip_override not in self.LIP_COLORS:
            lip = self.LIP_COLORS[(master_seed // 2) % len(self.LIP_COLORS)]
        else:
            lip = lip_override

        if nail_override == "🎲 Dynamic Rotation" or nail_override not in self.NAIL_COLORS:
            nail = self.NAIL_COLORS[(master_seed // 3) % len(self.NAIL_COLORS)]
        else:
            nail = nail_override

        parts = []

        # 1. Subject Core Baseline (Locked identity)
        if subject_core and subject_core.strip():
            parts.append(subject_core.strip().rstrip(","))

        # 2. Dynamic Identity Features (Hair, Lips, Nails)
        parts.append(hair)
        parts.append(lip)
        parts.append(nail)

        # 3. Pose & Action
        if pose_prompt and pose_prompt.strip():
            parts.append(pose_prompt.strip().rstrip(","))

        # 4. Wardrobe
        if wardrobe_prompt and wardrobe_prompt.strip():
            parts.append(wardrobe_prompt.strip().rstrip(","))

        # 5. Scene & Lighting
        if scene_lighting_prompt and scene_lighting_prompt.strip():
            parts.append(scene_lighting_prompt.strip().rstrip(","))

        # 6. User Custom Prompt
        if custom_prompt and custom_prompt.strip():
            parts.append(custom_prompt.strip().rstrip(","))

        fused = ", ".join(parts)
        negative = custom_negative.strip() if custom_negative and custom_negative.strip() else self.DEFAULT_NEGATIVE

        # Face detailer gets matched lip token
        face_detailer = f"{self.DEFAULT_FACE_DETAILER}, {lip}"

        tag_clean = active_tier_tag.strip() if active_tier_tag and active_tier_tag.strip() else f"seed_{master_seed}"
        image_prefix = f"dataset_images/vespera_{tag_clean}"
        mask_prefix = f"dataset_masks/vespera_{tag_clean}"
        upscale_prefix = f"dataset_upscaled/vespera_{tag_clean}"

        telemetry = f"[Agnostic Engine] Seed: {master_seed} | Tag: {tag_clean} | Hair: {hair[:25]}... | Lip: {lip} | Nail: {nail[:25]}..."

        return (
            fused,
            negative,
            face_detailer,
            image_prefix,
            mask_prefix,
            upscale_prefix,
            telemetry
        )
