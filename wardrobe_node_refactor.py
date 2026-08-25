"""
File    : wardrobe_node_refactor.py
Purpose : Standalone Refactored Dynamic Wardrobe node — 60+ curated high-fashion outfits
          across 8 distinct aesthetic tiers. Pure garment/attire tokens only.
          Zero character/body prompt bleed to guarantee pristine LoRA agnosticism.
"""

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None


class RefactoredWardrobeNode:
    """Massive Dynamic Wardrobe matrix generator with zero character bleed.

    - 60+ distinct high-fashion outfits across 8 aesthetic tiers.
    - Emits ONLY garment, fabric, footwear, and accessory tokens.
    - Zero human/body/character tokens, eliminating any conflict with PuLID or subject identity.
    - Master seed drives deterministic modulo selection across all categories.
    """

    WARDROBE_STYLES = {
        "🖤 Haute Couture & Evening Gowns": [
            "wearing structured black velvet evening gown with deep side slit, patent leather stiletto pumps, minimalist diamond pendant",
            "wearing silk taffeta tailored corset dress, sheer opera gloves, black pointed ankle boots, delicate silver drop earrings",
            "wearing plunging midnight-blue silk slip dress, sheer stockings, strappy designer stiletto sandals, platinum choker",
            "wearing backless satin column gown in rich emerald, delicate gold chain accent, black patent pumps",
            "wearing sculptural asymmetric draped black silk chiffon gown, pointed metallic heels, diamond ear cuff",
            "wearing plunging ruby-red silk velvet floor-length gown, sheer black mesh gloves, classic black stilettos",
            "wearing metallic woven champagne lamé evening dress, strappy crystal-embellished heels, pearl drop necklace",
            "wearing tailored black tuxedo dress with satin lapels, black fishnet stockings, patent leather high-heeled pumps",
        ],
        "⚡ Techwear, Cyberpunk & Moto": [
            "wearing matte black asymmetric cropped tactical jacket, high-waisted techwear cargo trousers, reinforced combat boots, utility harness",
            "wearing metallic iridescent cropped hoodie, reflective black nylon joggers, chunky high-top cybernetic sneakers, chrome cuff",
            "wearing dark vinyl cropped moto jacket, holographic accent leggings, platform stiletto boots, minimalist leather choker",
            "wearing fitted neoprene sleeveless bodysuit under sheer mesh overlay, matte black combat trousers, heavy-tread boots",
            "wearing tailored black ballistic nylon cropped vest, high-rise utility trousers, quick-release buckle belt, tactical boots",
            "wearing sleek matte carbon-black armored motorcycle jacket, high-waisted coated denim, reinforced moto riding boots",
            "wearing translucent dark smoke windbreaker over cropped technical tank, articulated knee cargo pants, futuristic runners",
            "wearing modular zip-off techwear jacket, high-waisted strap-accented trousers, platform combat boots, silver link hardware",
        ],
        "🍷 Parisian Gothic & Dark Romance": [
            "wearing fitted black leather biker jacket over sheer lace camisole, high-waisted distressed black denim, pointed ankle boots",
            "wearing structured Victorian-inspired black lace corset top, layered dark tulle midi skirt, platform lace-up leather boots",
            "wearing dark tailored charcoal trench coat belted tightly, sheer black stockings, patent leather stiletto pumps",
            "wearing sheer black mesh long-sleeve top over silk bralette, high-waisted fitted leather trousers, pointed heels",
            "wearing dark burgundy crushed velvet duster coat over black silk camisole, slim tailored trousers, pointed stiletto booties",
            "wearing layered distressed black knit sweater, high-waisted leather pencil skirt, knee-high lace-up combat boots, silver choker",
            "wearing tailored black brocade blazer with silver filigree buttons, dark slim-fit trousers, patent leather ankle boots",
            "wearing romantic sheer chiffon tiered maxi dress in dark charcoal, wide leather corset belt, suede stiletto booties",
        ],
        "☕ Casual Luxe & Minimalist Chic": [
            "wearing oversized charcoal cashmere turtleneck sweater, dark wash selvedge skinny jeans, suede Chelsea boots, layered silver chains",
            "wearing cropped vintage washed denim jacket over fitted black ribbed tank, dark grey cargo pants, clean white leather sneakers",
            "wearing soft ribbed knit sweater dress in charcoal grey, knee-high black leather riding boots, subtle gold hoop earrings",
            "wearing relaxed linen button-down shirt unbuttoned over dark bralette, tailored high-rise trousers, minimalist loafers",
            "wearing tailored camel wool overcoat over fitted black crewneck, high-waisted straight-leg denim, black leather ankle boots",
            "wearing slouchy off-the-shoulder modal knit top, relaxed boyfriend-fit distressed jeans, classic white leather court sneakers",
            "wearing cropped ribbed cardigan sweater, high-waisted wide-leg tailored trousers, minimalist leather slip-on mules",
            "wearing buttery soft lambskin leather bomber jacket, fitted ribbed tank, dark wash relaxed denim, chunky leather loafers",
        ],
        "💼 Power Tailoring & Executive Noir": [
            "wearing sharp double-breasted black wool blazer, tailored cigarette trousers, polished patent stilettos, slim leather belt",
            "wearing crisp structured white poplin dress shirt, high-waisted charcoal pinstripe suit trousers, black oxford heels",
            "wearing deep navy tailored tuxedo blazer over silk camisole, slim-fit suit pants, pointed-toe high heels",
            "wearing fitted houndstooth cropped blazer, high-waisted black pencil skirt, dark sheer tights, classic black pumps",
            "wearing sharp charcoal peak-lapel pantsuit, silk satin camisole, minimalist black leather stiletto pumps, silver watch",
            "wearing belted asymmetrical wrap blazer in dark slate, slim tailored ankle-length trousers, designer pointed pumps",
            "wearing sleeveless tailored vest top, matching wide-leg pleated trousers, pointed-toe heels, structured leather belt",
            "wearing tailored black leather trench dress with double-breasted buttons, sheer black stockings, patent pointed stilettos",
        ],
        "🔥 Intimate Boudoir & Haute Lingerie": [
            "wearing sheer floral black lace bodysuit, delicate strappy satin accents, sheer thigh-high stockings, black velvet heels",
            "wearing silk satin balconette bra with matching high-waist lace-panel panties, sheer silk kimono robe loosely draped",
            "wearing intricate black strapping harness over sheer mesh bralette, satin boy-shorts, delicate silver hardware accents",
            "wearing dark crimson silk slip nightdress with eyelash lace trim, sheer draped silk robe",
            "wearing plunge-front sheer black mesh babydoll with satin ribbon detail, delicate silk panties, sheer stockings",
            "wearing structured black satin basque corset with garters, sheer back-seam stockings, black patent pointed stilettos",
            "wearing emerald green silk charmeuse slip dress with delicate lace edging, draped matching silk robe",
            "wearing semi-sheer modal loungewear set with cropped tank and high-waist boy-shorts, oversized open cashmere cardigan",
        ],
        "🍸 Provocative Slits & Bodycon": [
            "wearing fitted ribbed-knit midi bodycon dress with high thigh slit, strappy stiletto heels, delicate gold pendant",
            "wearing structured bandage-style cutout mini dress in matte black, black leather ankle boots, geometric silver earrings",
            "wearing plunging cowl-neck satin slip dress in deep burgundy, strappy minimalist heels, thin silver chain",
            "wearing asymmetric off-shoulder ruched mesh bodycon dress, pointed stiletto pumps, crystal ear cuffs",
            "wearing liquid-look vinyl mini skirt, cropped fitted mockneck long-sleeve top, knee-high leather stiletto boots",
            "wearing sheer mesh paneled bodycon dress in dark slate, patent leather pointed pumps, minimalist clutch",
            "wearing cross-front halter neck bodycon dress in midnight navy, strappy high heels, delicate bangles",
            "wearing high-neck sleeveless knit bodycon dress with open back, black leather ankle-strap stilettos",
        ],
        "🏃 Modern Athleisure & Activewear": [
            "wearing ribbed seamless compression sports bra and matching high-waisted leggings in slate grey, sleek running sneakers",
            "wearing cropped athletic windbreaker over fitted black workout tank, performance compression shorts, high-top trainers",
            "wearing full-length sculpted matte black activewear unitard, lightweight cropped zip hoodie, clean training shoes",
            "wearing dark olive seamless activewear set with cross-back sports bra and sculpting tights, athletic slip-on sneakers",
        ],
    }

    STYLE_OPTIONS = ["🎲 Dynamic / Random Style Sweep"] + list(WARDROBE_STYLES.keys())

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "style_mode":  (cls.STYLE_OPTIONS, {"default": "🎲 Dynamic / Random Style Sweep"}),
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

        if style_mode == "🎲 Dynamic / Random Style Sweep" or style_mode not in self.WARDROBE_STYLES:
            categories = list(self.WARDROBE_STYLES.keys())
            cat_idx = (master_seed // 1000) % len(categories)
            cat = categories[cat_idx]
        else:
            cat = style_mode

        options = self.WARDROBE_STYLES[cat]
        opt_idx = master_seed % len(options)
        return (options[opt_idx],)
