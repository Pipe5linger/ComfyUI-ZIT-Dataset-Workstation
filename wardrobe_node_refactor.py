"""
File    : wardrobe_node_refactor.py
Purpose : Standalone Refactored Dynamic Wardrobe node — 270+ curated high-fashion outfits
          across 10 distinct aesthetic tiers. Pure garment/attire tokens only.
          Zero character/body prompt bleed to guarantee pristine LoRA agnosticism.
"""

import json
import os

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None

# Locate data vault
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_PATH = os.path.join(CURRENT_DIR, "data", "wardrobe_vault.json")

def _load_vault():
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data and isinstance(data, dict):
                    return data
        except Exception:
            pass
    return {
        "🖤 Haute Couture & Evening Gowns": [
            "wearing structured black velvet evening gown with deep side slit, patent leather stiletto pumps, minimalist diamond pendant",
            "wearing silk taffeta tailored corset dress, sheer opera gloves, black pointed ankle boots, delicate silver drop earrings",
            "wearing plunging midnight-blue silk slip dress, sheer stockings, strappy designer stiletto sandals, platinum choker",
            "wearing backless satin column gown in rich emerald, delicate gold chain accent, black patent pumps",
        ],
        "⚡ Techwear, Cyberpunk & Moto Armor": [
            "wearing matte black asymmetric cropped tactical jacket, high-waisted techwear cargo trousers, reinforced combat boots, utility harness",
            "wearing metallic iridescent cropped hoodie, reflective black nylon joggers, chunky high-top cybernetic sneakers, chrome cuff",
            "wearing dark vinyl cropped moto jacket, holographic accent leggings, platform stiletto boots, minimalist leather choker",
            "wearing fitted neoprene sleeveless bodysuit under sheer mesh overlay, matte black combat trousers, heavy-tread boots",
        ],
        "🍷 Parisian Gothic, Dark Romance & Noir": [
            "wearing fitted black leather biker jacket over sheer lace camisole, high-waisted distressed black denim, pointed ankle boots",
            "wearing structured Victorian-inspired black lace corset top, layered dark tulle midi skirt, platform lace-up leather boots",
            "wearing dark tailored charcoal trench coat belted tightly, sheer black stockings, patent leather stiletto pumps",
            "wearing sheer black mesh long-sleeve top over silk bralette, high-waisted fitted leather trousers, pointed heels",
        ],
        "☕ Casual Luxe, Denim & Streetwear": [
            "wearing oversized charcoal cashmere turtleneck sweater, dark wash selvedge skinny jeans, suede Chelsea boots, layered silver chains",
            "wearing cropped vintage washed denim jacket over fitted black ribbed tank, dark grey cargo pants, clean white leather sneakers",
            "wearing soft ribbed knit sweater dress in charcoal grey, knee-high black leather riding boots, subtle gold hoop earrings",
            "wearing relaxed linen button-down shirt unbuttoned over dark bralette, tailored high-rise trousers, minimalist loafers",
        ],
        "💼 Power Tailoring, Suiting & Business Noir": [
            "wearing sharp double-breasted black wool blazer, tailored cigarette trousers, polished patent stilettos, slim leather belt",
            "wearing crisp structured white poplin dress shirt, high-waisted charcoal pinstripe suit trousers, black oxford heels",
            "wearing deep navy tailored tuxedo blazer over silk camisole, slim-fit suit pants, pointed-toe high heels",
            "wearing fitted houndstooth cropped blazer, high-waisted black pencil skirt, dark sheer tights, classic black pumps",
        ],
        "🔥 Intimate Boudoir, Lace & Haute Lingerie": [
            "wearing sheer floral black lace bodysuit, delicate strappy satin accents, sheer thigh-high stockings, black velvet heels",
            "wearing silk satin balconette bra with matching high-waist lace-panel panties, sheer silk kimono robe loosely draped",
            "wearing intricate black strapping harness over sheer mesh bralette, satin boy-shorts, delicate silver hardware accents",
            "wearing dark crimson silk slip nightdress with eyelash lace trim, sheer draped silk robe",
        ],
    }

WARDROBE_DATA = _load_vault()
STYLE_OPTIONS = ["🎲 Dynamic / Random Style Sweep"] + list(WARDROBE_DATA.keys())


class RefactoredWardrobeNode:
    """Massive Dynamic Wardrobe matrix generator with zero character bleed.

    - 270+ distinct high-fashion outfits across 10 aesthetic tiers.
    - Emits ONLY garment, fabric, footwear, and accessory tokens.
    - Zero human/body/character tokens, eliminating any conflict with PuLID or subject identity.
    - Master seed drives deterministic modulo selection across all categories.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "style_mode":  (STYLE_OPTIONS, {"default": "🎲 Dynamic / Random Style Sweep"}),
            },
            "optional": {
                "custom_wardrobe_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("wardrobe_prompt",)
    FUNCTION     = "run"
    CATEGORY     = "ZIT/Dataset Workstation"

    def run(self, master_seed: int, style_mode: str = "🎲 Dynamic / Random Style Sweep", custom_wardrobe_override: str = "", **kwargs):
        if custom_wardrobe_override and custom_wardrobe_override.strip():
            return (custom_wardrobe_override.strip(),)

        vault = _load_vault()
        if style_mode == "🎲 Dynamic / Random Style Sweep" or style_mode not in vault:
            categories = list(vault.keys())
            cat_idx = (master_seed // 1000) % len(categories)
            cat = categories[cat_idx]
        else:
            cat = style_mode

        options = vault[cat]
        opt_idx = master_seed % len(options)
        return (options[opt_idx],)
