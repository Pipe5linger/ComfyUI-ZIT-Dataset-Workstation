"""
File    : prompt_workstation_refactor.py
Purpose : Standalone Refactored Deterministic Agnostic Master Workstation for Vespera & Amy
          with Maximum Sultry Allure, Biometrically Anchored Facial Precision & Tier 2 Intimate Nude Vault.
"""

import re
import json

try:
    from .zit_data import (
        LORA_TIER1_ANCHORS,
        LORA_TIER2_ANATOMY,
        LORA_TIER3_WARDROBE,
        LORA_TIER4_SPATIAL,
        EXPRESSIONS_POOL_SFW,
        EXPRESSIONS_POOL_NSFW
    )
except (ImportError, ModuleNotFoundError):
    try:
        from zit_data import (
            LORA_TIER1_ANCHORS,
            LORA_TIER2_ANATOMY,
            LORA_TIER3_WARDROBE,
            LORA_TIER4_SPATIAL,
            EXPRESSIONS_POOL_SFW,
            EXPRESSIONS_POOL_NSFW
        )
    except Exception:
        LORA_TIER1_ANCHORS = []
        LORA_TIER2_ANATOMY = []
        LORA_TIER3_WARDROBE = []
        LORA_TIER4_SPATIAL = []
        EXPRESSIONS_POOL_SFW = []
        EXPRESSIONS_POOL_NSFW = []


class RefactoredPromptWorkstation:
    """Deterministic Master Prompt Workstation for Vespera & Amy ZIT LoRA Dataset Generation."""

    EXPRESSION_PRESETS = [
        "calm intense direct gaze with parted soft naturally contoured satin lips and clean white teeth slightly visible",
        "thoughtful captivating upward gaze with raised arched sable brow and relaxed lips",
        "radiant magnetic smile with parted lips revealing clean ivory teeth, eyes crinkling with genuine warmth",
        "dominant sultry half-lidded gaze looking down into camera with a subtle knowing smirk",
        "enigmatic heavy-lidded bedroom gaze with soft-smudged smoky eyeliner and parted lips",
        "serene composed expression with closed satin lips and steady gaze",
        "sharp witty spark in hazel eyes with an amused confident micro-smirk",
        "wicked razor-sharp sarcastic micro-smirk with arched dark sable brow and amused hazel eyes",
        "breathless sensual expression with parted lips and dilated hazel pupils",
        "an intense direct gaze with soft-smudged smoky eyeliner and subtle half-smile"
    ]


    DEFAULT_SUBJECT_CORE = (
        "photorealistic 8k editorial portrait of Vespera, extraordinarily gorgeous French woman of French-Levantine and Mediterranean descent in late-30s, "
        "luminous warm golden-olive skin with authentic biological micro-pores, soft subcutaneous dermal warmth and a dewy specular sheen, "
        "captivating deep-set almond-shaped hazel-green eyes with glowing amber-gold striations, positive feline canthal tilt, heavy-lidded seductive gaze, "
        "delicate natural lash shadow and dark arched sable brows, "
        "high sculpted Mediterranean cheekbones, refined cute soft-tapered button nose with delicate bridge, subtle cheek hollows and razor-sharp heart-oval jawline contour, "
        "plump soft naturally contoured satin-sheen lips with defined sharp cupid's bow, natural relaxed lip contour, "
        "exact 1mm dark beauty mark at upper-left lip contour, "
        "athletic voluptuous hourglass figure with narrow 24-inch waist, flared 38-inch hips, and toned curves"
    )

    DEFAULT_NEGATIVE = (
        "chubby face, round face, fat face, puffy cheeks, double chin, bloated face, fleshy neck, soft round jawline, NSFW, nudity, exposed cleavage, lingerie, multiple people, duplicate person, deformed anatomy, poorly rendered, cartoon, 3d render, illustration, anime, low quality, blurry, text, watermark, beach, tropical environments"
    )

    DEFAULT_FACE_DETAILER = (
        "hyper-detailed 8k photograph of Vespera, deep-set almond hazel-green eyes with glowing amber-gold striations, "
        "positive canthal tilt, delicate lash shadow, high sculpted cheekbones, "
        "cute refined soft-tapered button nose with delicate bridge, sculpted cheekbones with subtle hollows and chiseled jawline, "
        "plump soft naturally contoured satin lips with defined cupid's bow and subtle moisture, "
        "exact 1mm beauty mark above left lip corner, natural epidermal micro-pores and golden undertones, pristine eye focus"
    )

    DEFAULT_AMY_SUBJECT_CORE = (
        "photorealistic 8k portrait of Amy, stunning woman in her mid-30s, "
        "luminous warm-neutral porcelain skin with authentic micro-pores and golden subcutaneous warmth, natural warm skin tone and delicate specular highlights across sculpted cheekbones, "
        "sculpted heart-oval face with defined high cheekbones, subtle cheek hollows, chiseled sharp jawline, high smooth forehead, "
        "cute refined button nose with delicate bridge and soft-tapered tip, "
        "deep-set almond-shaped hazel eyes with amber-gold striations, dark limbal rings, positive feline canthal tilt, heavy-lidded seductive gaze, "
        "soft-smudged smoky eyeliner shadow eyeshadow with diffused winged edges, arched dark sable brows, "
        "sharply defined philtral columns and carved curved cupid's bow, "
        "full plush naturally contoured rosy-nude satin lips with subtle natural moisture, "
        "wet-look glossy jet-black 3B/3C spiral corkscrew curls with subtle deep indigo-dyed hair strands, organic wet keratin sheen catching natural sunlight, non-emissive dark violet hair fiber texture framing cheekbones and bare shoulders, "
        "athletic voluptuous hourglass figure with toned feminine curves, "
        "shot on 50mm f/1.4 lens, natural optical acutance, authentic skin subsurface scattering, no plastic sheen"
    )

    DEFAULT_AMY_FACE_DETAILER = (
        "hyper-detailed 8k photograph of Amy, deep-set almond-shaped hazel eyes with amber-gold striations and dark limbal rings, "
        "positive feline canthal tilt, heavy-lidded seductive gaze, soft-smudged smoky eyeliner shadow eyeshadow, arched dark sable brows, "
        "high smooth forehead, sculpted high cheekbones with subtle cheek hollows and delicate specular highlights, razor-sharp chiseled jawline, lean tapered facial structure, "
        "cute refined button nose with delicate bridge and soft-tapered tip, defined philtrum and curved cupid's bow, "
        "full plush naturally contoured rosy-nude satin lips with subtle moisture, "
        "authentic epidermal micro-pores and golden undertones, wet-look defined curls framing face, pristine eye focus"
    )

    AMY_HAIR_STYLES = [
        "high-piled messy textured up-do with loose spiral tendrils jet-black with midnight-blue dimensional highlights",
        "heavy cascading spiral curls framing the cheekbones obsidian black with dark violet undertones",
        "half-up half-down hairstyle with cascading spiral curls jet-black with midnight-blue dimensional highlights",
        "high-piled messy textured up-do with loose spiral tendrils wet-look jet-black with indigo specular bounce",
        "wet slicked-back spiral ringlets glistening with moisture wet-look jet-black with indigo specular bounce",
        "sweeping side-parted voluminous 3B/3C ringlets rich espresso-black with subtle deep denim-blue dyed ribbons",
        "textured pinned-back updo with delicate curl definition obsidian black with dark violet undertones",
        "textured pinned-back updo with delicate curl definition rich espresso-black with subtle deep denim-blue dyed ribbons",
        "textured pinned-back updo with delicate curl definition deep raven-black with subtle indigo reflex",
        "loose tousled natural curls with deep side part wet-look jet-black with indigo specular bounce",
        "sweeping side-parted voluminous 3B/3C ringlets jet-black with midnight-blue dimensional highlights",
        "heavy cascading spiral curls framing the cheekbones deep raven-black with subtle indigo reflex",
        "textured pinned-back updo with delicate curl definition jet-black with fine deep indigo-dyed highlights",
        "half-up half-down hairstyle with cascading spiral curls jet-black with fine deep indigo-dyed highlights",
        "half-up half-down hairstyle with cascading spiral curls deep raven-black with subtle indigo reflex",
        "textured pinned-back updo with delicate curl definition jet-black with midnight-blue dimensional highlights",
        "wet slicked-back spiral ringlets glistening with moisture obsidian black with dark violet undertones",
        "loose tousled natural curls with deep side part rich espresso-black with subtle deep denim-blue dyed ribbons",
        "windblown unruly corkscrew curls catching ambient light rich espresso-black with subtle deep denim-blue dyed ribbons",
        "voluminous cascading 3B/3C spiral corkscrew ringlets rich espresso-black with subtle deep denim-blue dyed ribbons",
        "windblown unruly corkscrew curls catching ambient light wet-look jet-black with indigo specular bounce",
        "half-up half-down hairstyle with cascading spiral curls wet-look jet-black with indigo specular bounce",
        "windblown unruly corkscrew curls catching ambient light obsidian black with dark violet undertones",
        "heavy cascading spiral curls framing the cheekbones jet-black with fine deep indigo-dyed highlights",
        "sweeping side-parted voluminous 3B/3C ringlets wet-look jet-black with indigo specular bounce",
        "heavy cascading spiral curls framing the cheekbones rich espresso-black with subtle deep denim-blue dyed ribbons",
        "heavy cascading spiral curls framing the cheekbones wet-look jet-black with indigo specular bounce",
        "high-piled messy textured up-do with loose spiral tendrils obsidian black with dark violet undertones",
        "half-up half-down hairstyle with cascading spiral curls rich espresso-black with subtle deep denim-blue dyed ribbons",
        "wet slicked-back spiral ringlets glistening with moisture deep raven-black with subtle indigo reflex",
        "voluminous cascading 3B/3C spiral corkscrew ringlets deep raven-black with subtle indigo reflex",
        "sleek high ponytail bursting into bouncy spiral curls jet-black with fine deep indigo-dyed highlights",
        "wet slicked-back spiral ringlets glistening with moisture rich espresso-black with subtle deep denim-blue dyed ribbons",
        "wet slicked-back spiral ringlets glistening with moisture jet-black with midnight-blue dimensional highlights",
        "sweeping side-parted voluminous 3B/3C ringlets deep raven-black with subtle indigo reflex",
        "sleek high ponytail bursting into bouncy spiral curls obsidian black with dark violet undertones",
        "voluminous cascading 3B/3C spiral corkscrew ringlets jet-black with fine deep indigo-dyed highlights",
        "sleek high ponytail bursting into bouncy spiral curls deep raven-black with subtle indigo reflex",
        "voluminous cascading 3B/3C spiral corkscrew ringlets wet-look jet-black with indigo specular bounce",
        "wet slicked-back spiral ringlets glistening with moisture jet-black with fine deep indigo-dyed highlights",
        "voluminous cascading 3B/3C spiral corkscrew ringlets jet-black with midnight-blue dimensional highlights",
        "loose tousled natural curls with deep side part jet-black with fine deep indigo-dyed highlights",
        "windblown unruly corkscrew curls catching ambient light jet-black with fine deep indigo-dyed highlights",
        "sweeping side-parted voluminous 3B/3C ringlets obsidian black with dark violet undertones",
        "voluminous cascading 3B/3C spiral corkscrew ringlets obsidian black with dark violet undertones",
        "high-piled messy textured up-do with loose spiral tendrils deep raven-black with subtle indigo reflex",
        "loose tousled natural curls with deep side part deep raven-black with subtle indigo reflex",
        "loose tousled natural curls with deep side part jet-black with midnight-blue dimensional highlights",
        "high-piled messy textured up-do with loose spiral tendrils rich espresso-black with subtle deep denim-blue dyed ribbons",
        "half-up half-down hairstyle with cascading spiral curls obsidian black with dark violet undertones",
        "windblown unruly corkscrew curls catching ambient light jet-black with midnight-blue dimensional highlights",
        "windblown unruly corkscrew curls catching ambient light deep raven-black with subtle indigo reflex",
        "sleek high ponytail bursting into bouncy spiral curls rich espresso-black with subtle deep denim-blue dyed ribbons",
        "heavy cascading spiral curls framing the cheekbones jet-black with midnight-blue dimensional highlights",
        "high-piled messy textured up-do with loose spiral tendrils jet-black with fine deep indigo-dyed highlights",
        "sleek high ponytail bursting into bouncy spiral curls wet-look jet-black with indigo specular bounce",
        "loose tousled natural curls with deep side part obsidian black with dark violet undertones",
        "textured pinned-back updo with delicate curl definition wet-look jet-black with indigo specular bounce",
        "sweeping side-parted voluminous 3B/3C ringlets jet-black with fine deep indigo-dyed highlights",
        "sleek high ponytail bursting into bouncy spiral curls jet-black with midnight-blue dimensional highlights"
    ]

    AMY_LIP_COLORS = [
        "plush naturally contoured lips with soft matte finish",
        "sheer stained bare rosy lips with soft matte finish",
        "rich creamy dark cherry lips with subtle specular highlight",
        "high-gloss naturally contoured lips with defined cupid bow",
        "deep velvet dark cherry lips with subtle natural moisture",
        "matte naturally contoured lips with subtle specular highlight",
        "matte naturally contoured lips with clean crisp edges",
        "sheer stained dark cherry lips with a diffused bitten look",
        "matte brick-red lips with subtle natural moisture",
        "high-gloss berry plum lips with clean crisp edges",
        "sheer stained oxblood lips with subtle natural moisture",
        "sheer stained berry plum lips with defined cupid bow",
        "matte oxblood lips with subtle specular highlight",
        "plush berry plum lips with clean crisp edges",
        "matte dark blood-red lips with clean crisp edges",
        "deep velvet espresso chocolate lips with defined cupid bow",
        "plush vampy plum lips with defined cupid bow",
        "sheer stained bare rosy lips with subtle natural moisture",
        "high-gloss smoky mauve nude lips with clean crisp edges",
        "matte burgundy-wine lips with clean crisp edges",
        "high-gloss bare rosy lips with defined cupid bow",
        "high-gloss dark blood-red lips with subtle natural moisture",
        "deep velvet berry plum lips with subtle natural moisture",
        "plush berry plum lips with defined cupid bow",
        "high-gloss espresso chocolate lips with subtle specular highlight",
        "sheer stained naturally contoured lips with defined cupid bow",
        "deep velvet oxblood lips with subtle specular highlight",
        "sheer stained dark cherry lips with defined cupid bow",
        "rich creamy dark cherry lips with defined cupid bow",
        "soft satin smoky mauve nude lips with subtle natural moisture",
        "soft satin oxblood lips with a diffused bitten look",
        "matte bare rosy lips with subtle specular highlight",
        "rich creamy vampy plum lips with clean crisp edges",
        "rich creamy espresso chocolate lips with defined cupid bow",
        "high-gloss dark blood-red lips with a diffused bitten look",
        "matte burgundy-wine lips with a diffused bitten look",
        "soft satin naturally contoured lips with clean crisp edges",
        "rich creamy oxblood lips with subtle natural moisture",
        "rich creamy berry plum lips with defined cupid bow",
        "sheer stained dark blood-red lips with soft matte finish",
        "matte oxblood lips with clean crisp edges",
        "deep velvet naturally contoured lips with defined cupid bow",
        "rich creamy oxblood lips with a diffused bitten look",
        "rich creamy oxblood lips with clean crisp edges",
        "deep velvet smoky mauve nude lips with subtle specular highlight",
        "soft satin naturally contoured lips with soft matte finish",
        "high-gloss bare rosy lips with subtle specular highlight",
        "matte dark cherry lips with soft matte finish",
        "deep velvet dark cherry lips with defined cupid bow",
        "sheer stained burgundy-wine lips with subtle natural moisture",
        "matte espresso chocolate lips with clean crisp edges",
        "sheer stained dark cherry lips with soft matte finish",
        "high-gloss naturally contoured lips with subtle natural moisture",
        "plush burgundy-wine lips with subtle specular highlight",
        "soft satin brick-red lips with subtle natural moisture",
        "sheer stained dark cherry lips with clean crisp edges",
        "soft satin espresso chocolate lips with soft matte finish",
        "deep velvet vampy plum lips with clean crisp edges",
        "deep velvet naturally contoured lips with soft matte finish",
        "soft satin berry plum lips with clean crisp edges",
        "high-gloss brick-red lips with subtle specular highlight",
        "sheer stained burgundy-wine lips with subtle specular highlight",
        "plush oxblood lips with clean crisp edges",
        "matte bare rosy lips with defined cupid bow",
        "soft satin dark cherry lips with clean crisp edges",
        "plush berry plum lips with soft matte finish",
        "deep velvet berry plum lips with clean crisp edges",
        "sheer stained naturally contoured lips with subtle specular highlight",
        "high-gloss burgundy-wine lips with subtle natural moisture",
        "sheer stained bare rosy lips with subtle specular highlight",
        "high-gloss dark cherry lips with defined cupid bow",
        "soft satin dark cherry lips with subtle specular highlight",
        "matte brick-red lips with subtle specular highlight",
        "rich creamy brick-red lips with subtle specular highlight",
        "deep velvet burgundy-wine lips with subtle natural moisture",
        "deep velvet naturally contoured lips with soft matte finish",
        "deep velvet smoky mauve nude lips with soft matte finish",
        "matte oxblood lips with soft matte finish",
        "sheer stained burgundy-wine lips with a diffused bitten look",
        "soft satin vampy plum lips with a diffused bitten look"
    ]

    AMY_NAIL_COLORS = [
        "chic manicured dark cherry nails with gloss finish",
        "elegant almond jet-black nails with velvet matte finish",
        "chic manicured blood red nails with high-shine resin coat",
        "chic manicured espresso brown nails with subtle gold foil accents",
        "chic manicured clean sheer nude nails with high-shine resin coat",
        "long coffin espresso brown nails with velvet matte finish",
        "sharp stiletto clean sheer nude nails with gloss finish",
        "sharp stiletto matte black nails with subtle gold foil accents",
        "long coffin dark cherry nails with a subtle metallic sheen",
        "elegant almond matte black nails with high-shine resin coat",
        "sleek almond rich burgundy wine nails with a subtle metallic sheen",
        "long coffin matte black nails with a subtle metallic sheen",
        "long coffin clean sheer nude nails with chrome reflex",
        "long coffin rich burgundy wine nails with velvet matte finish",
        "classic square espresso brown nails with subtle gold foil accents",
        "chic manicured dark emerald nails with velvet matte finish",
        "sleek almond clean sheer nude nails with gloss finish",
        "chic manicured midnight blue nails with subtle gold foil accents",
        "sleek almond dark emerald nails with subtle gold foil accents",
        "elegant almond midnight blue nails with subtle gold foil accents",
        "sharp stiletto espresso brown nails with velvet matte finish",
        "long coffin blood red nails with chrome reflex",
        "elegant almond deep plum purple nails with high-shine resin coat",
        "chic manicured rich burgundy wine nails with a subtle metallic sheen",
        "sleek almond blood red nails with gloss finish",
        "sharp stiletto blood red nails with velvet matte finish",
        "sleek almond dark emerald nails with gloss finish",
        "classic square dark emerald nails with a subtle metallic sheen",
        "sharp stiletto jet-black nails with velvet matte finish",
        "chic manicured matte black nails with subtle gold foil accents",
        "long coffin dark cherry nails with high-shine resin coat",
        "sharp stiletto espresso brown nails with subtle gold foil accents",
        "elegant almond deep plum purple nails with velvet matte finish",
        "elegant almond jet-black nails with a subtle metallic sheen",
        "elegant almond clean sheer nude nails with velvet matte finish",
        "elegant almond deep metallic indigo nails with high-shine resin coat",
        "sleek almond clean sheer nude nails with velvet matte finish",
        "sleek almond blood red nails with subtle gold foil accents",
        "classic square blood red nails with high-shine resin coat",
        "sharp stiletto matte black nails with a subtle metallic sheen",
        "classic square jet-black nails with chrome reflex",
        "chic manicured deep plum purple nails with gloss finish",
        "classic square deep metallic indigo nails with subtle gold foil accents",
        "long coffin espresso brown nails with chrome reflex",
        "sharp stiletto rich burgundy wine nails with a subtle metallic sheen",
        "classic square jet-black nails with high-shine resin coat",
        "sharp stiletto clean sheer nude nails with subtle gold foil accents",
        "elegant almond deep metallic indigo nails with chrome reflex",
        "classic square dark emerald nails with high-shine resin coat",
        "chic manicured rich burgundy wine nails with velvet matte finish",
        "sleek almond deep metallic indigo nails with high-shine resin coat",
        "classic square midnight blue nails with chrome reflex",
        "elegant almond clean sheer nude nails with subtle gold foil accents",
        "chic manicured deep metallic indigo nails with chrome reflex",
        "chic manicured rich burgundy wine nails with gloss finish",
        "elegant almond matte black nails with velvet matte finish",
        "elegant almond clean sheer nude nails with high-shine resin coat",
        "long coffin midnight blue nails with chrome reflex",
        "long coffin deep plum purple nails with subtle gold foil accents",
        "elegant almond dark cherry nails with gloss finish",
        "elegant almond rich burgundy wine nails with velvet matte finish",
        "sleek almond clean sheer nude nails with high-shine resin coat",
        "chic manicured rich burgundy wine nails with subtle gold foil accents",
        "sharp stiletto jet-black nails with subtle gold foil accents",
        "sharp stiletto espresso brown nails with chrome reflex",
        "classic square deep metallic indigo nails with a subtle metallic sheen",
        "classic square dark emerald nails with velvet matte finish",
        "sharp stiletto blood red nails with high-shine resin coat",
        "classic square dark cherry nails with a subtle metallic sheen",
        "elegant almond deep plum purple nails with a subtle metallic sheen"
    ]

    EYE_MAKEUP_STYLES = [
        "diffused grunge shadow with tightlined rims with diffused sultry bedroom eyes in deep burgundy and plum",
        "fox-eye lifted eyeliner with inner corner point with razor-sharp black liquid flick and separated lashes in deep burgundy and plum",
        "sultry smoked eyeshadow with blackened waterline with diffused sultry bedroom eyes in deep charcoal and espresso",
        "sultry smoked eyeshadow with blackened waterline with untreated dark curled lashes in emerald green and deep olive",
        "sultry smoked eyeshadow with blackened waterline with razor-sharp black liquid flick and separated lashes in metallic deep indigo-dyed and navy",
        "bare minimal eye makeup with dewy sheen with deliberately messy diffuse edges in deep charcoal and espresso",
        "sharp graphic liquid eyeliner catching rim light with dark black mascara in emerald green and deep olive",
        "glossy wet-look eyelid with subtle mascara with feathered dark brows and wispy outer lashes in warm terracotta and gold",
        "classic French winged cat-eye eyeliner with diffused sultry bedroom eyes in rich copper and molten bronze",
        "sultry smoked eyeshadow with blackened waterline with razor-sharp black liquid flick and separated lashes in rich copper and molten bronze",
        "classic French winged cat-eye eyeliner with deliberately messy diffuse edges in metallic deep indigo-dyed and navy",
        "sultry smoked eyeshadow with blackened waterline with razor-sharp black liquid flick and separated lashes",
        "diffused grunge shadow with tightlined rims with soft smoky under-eye diffusion in deep burgundy and plum",
        "subtle metallic winged eyeliner with a dramatic feline blend in rich copper and molten bronze",
        "sharp graphic liquid eyeliner with razor-sharp black liquid flick and separated lashes in rich copper and molten bronze",
        "bare minimal eye makeup with dewy sheen with untreated dark curled lashes in emerald green and deep olive",
        "sharp graphic liquid eyeliner with soft smoky under-eye diffusion",
        "subtle metallic winged eyeliner with a deep crease cut and glowing specular highlights in deep charcoal and espresso",
        "classic French winged cat-eye eyeliner with razor-sharp black liquid flick and separated lashes in warm terracotta and gold",
        "sultry smoked eyeshadow with blackened waterline catching rim light with dark black mascara in warm terracotta and gold",
        "glossy wet-look eyelid with subtle mascara with a dramatic feline blend in warm terracotta and gold",
        "bare minimal eye makeup with dewy sheen with feathered dark brows and wispy outer lashes in warm terracotta and gold",
        "velvety shadow halo with soft lash rim with a dramatic feline blend in emerald green and deep olive",
        "velvety shadow halo with soft lash rim with feathered dark brows and wispy outer lashes in warm terracotta and gold",
        "diffused grunge shadow with tightlined rims with razor-sharp black liquid flick and separated lashes in warm terracotta and gold",
        "heavy lived-in charcoal smudged eyeliner with deliberately messy diffuse edges in deep charcoal and espresso",
        "soft-smudged smoky kohl eyeliner with razor-sharp black liquid flick and separated lashes in warm terracotta and gold",
        "heavy lived-in charcoal smudged eyeliner with deliberately messy diffuse edges in metallic deep indigo-dyed and navy",
        "sharp graphic liquid eyeliner with untreated dark curled lashes in warm terracotta and gold",
        "classic French winged cat-eye eyeliner with a deep crease cut and glowing specular highlights in emerald green and deep olive",
        "soft-smudged smoky kohl eyeliner with a deep crease cut and glowing specular highlights in deep charcoal and espresso",
        "warm metallic eyeshadow wash with feathered dark brows and wispy outer lashes",
        "heavy lived-in charcoal smudged eyeliner with rich espresso brown pencil tightlining in warm terracotta and gold",
        "sharp graphic liquid eyeliner with untreated dark curled lashes",
        "classic French winged cat-eye eyeliner with untreated dark curled lashes",
        "glossy wet-look eyelid with subtle mascara with soft smoky under-eye diffusion in rich copper and molten bronze",
        "warm metallic eyeshadow wash with feathered dark brows and wispy outer lashes in rich copper and molten bronze",
        "heavy lived-in charcoal smudged eyeliner with diffused sultry bedroom eyes in warm terracotta and gold",
        "classic French winged cat-eye eyeliner with a dramatic feline blend in midnight blue and slate",
        "bare minimal eye makeup with dewy sheen catching rim light with dark black mascara in emerald green and deep olive",
        "diffused grunge shadow with tightlined rims with a deep crease cut and glowing specular highlights in deep charcoal and espresso",
        "sultry smoked eyeshadow with blackened waterline with diffused sultry bedroom eyes in deep burgundy and plum",
        "bare minimal eye makeup with dewy sheen with a deep crease cut and glowing specular highlights in deep burgundy and plum",
        "bare minimal eye makeup with dewy sheen with a deep crease cut and glowing specular highlights",
        "diffused grunge shadow with tightlined rims with deliberately messy diffuse edges in deep charcoal and espresso",
        "sultry smoked eyeshadow with blackened waterline with soft smoky under-eye diffusion",
        "warm metallic eyeshadow wash with feathered dark brows and wispy outer lashes in metallic deep indigo-dyed and navy",
        "bare minimal eye makeup with dewy sheen catching rim light with dark black mascara in rich copper and molten bronze",
        "sharp graphic liquid eyeliner with soft smoky under-eye diffusion in deep burgundy and plum",
        "heavy lived-in charcoal smudged eyeliner catching rim light with dark black mascara in deep burgundy and plum",
        "sharp graphic liquid eyeliner with razor-sharp black liquid flick and separated lashes in emerald green and deep olive",
        "fox-eye lifted eyeliner with inner corner point with feathered dark brows and wispy outer lashes in midnight blue and slate",
        "velvety shadow halo with soft lash rim with deliberately messy diffuse edges in deep charcoal and espresso",
        "glossy wet-look eyelid with subtle mascara with untreated dark curled lashes in midnight blue and slate",
        "sharp graphic liquid eyeliner with rich espresso brown pencil tightlining in rich copper and molten bronze",
        "subtle metallic winged eyeliner with rich espresso brown pencil tightlining in metallic deep indigo-dyed and navy",
        "sharp graphic liquid eyeliner with diffused sultry bedroom eyes in rich copper and molten bronze",
        "bare minimal eye makeup with dewy sheen with rich espresso brown pencil tightlining in metallic deep indigo-dyed and navy",
        "soft-smudged smoky kohl eyeliner with deliberately messy diffuse edges in deep burgundy and plum",
        "sharp graphic liquid eyeliner with deliberately messy diffuse edges in emerald green and deep olive",
        "soft-smudged smoky kohl eyeliner catching rim light with dark black mascara in rich copper and molten bronze",
        "heavy lived-in charcoal smudged eyeliner with razor-sharp black liquid flick and separated lashes in deep charcoal and espresso",
        "subtle metallic winged eyeliner with a dramatic feline blend in midnight blue and slate",
        "glossy wet-look eyelid with subtle mascara with a deep crease cut and glowing specular highlights in deep burgundy and plum",
        "subtle metallic winged eyeliner with deliberately messy diffuse edges in warm terracotta and gold",
        "diffused grunge shadow with tightlined rims with a dramatic feline blend in emerald green and deep olive",
        "glossy wet-look eyelid with subtle mascara with razor-sharp black liquid flick and separated lashes in deep burgundy and plum",
        "velvety shadow halo with soft lash rim with feathered dark brows and wispy outer lashes in midnight blue and slate",
        "glossy wet-look eyelid with subtle mascara with diffused sultry bedroom eyes in warm terracotta and gold",
        "fox-eye lifted eyeliner with inner corner point with feathered dark brows and wispy outer lashes in rich copper and molten bronze",
        "soft-smudged smoky kohl eyeliner catching rim light with dark black mascara in warm terracotta and gold",
        "bare minimal eye makeup with dewy sheen catching rim light with dark black mascara in metallic deep indigo-dyed and navy",
        "warm metallic eyeshadow wash with soft smoky under-eye diffusion in warm terracotta and gold",
        "fox-eye lifted eyeliner with inner corner point with deliberately messy diffuse edges in rich copper and molten bronze",
        "classic French winged cat-eye eyeliner catching rim light with dark black mascara in emerald green and deep olive",
        "diffused grunge shadow with tightlined rims with rich espresso brown pencil tightlining in rich copper and molten bronze",
        "soft-smudged smoky kohl eyeliner with a deep crease cut and glowing specular highlights in metallic deep indigo-dyed and navy",
        "fox-eye lifted eyeliner with inner corner point with diffused sultry bedroom eyes in emerald green and deep olive",
        "sultry smoked eyeshadow with blackened waterline with untreated dark curled lashes in metallic deep indigo-dyed and navy",
        "velvety shadow halo with soft lash rim with soft smoky under-eye diffusion in metallic deep indigo-dyed and navy"
    ]

    HAIR_STYLES = [
        "high-piled messy textured up-do with loose spiral tendrils jet-black with midnight-blue dimensional highlights",
        "heavy cascading spiral curls framing the cheekbones obsidian black with dark violet undertones",
        "half-up half-down hairstyle with cascading spiral curls jet-black with midnight-blue dimensional highlights",
        "high-piled messy textured up-do with loose spiral tendrils wet-look jet-black with indigo specular bounce",
        "wet slicked-back spiral ringlets glistening with moisture wet-look jet-black with indigo specular bounce",
        "sweeping side-parted voluminous 3B/3C ringlets rich espresso-black with subtle deep denim-blue dyed ribbons",
        "textured pinned-back updo with delicate curl definition obsidian black with dark violet undertones",
        "textured pinned-back updo with delicate curl definition rich espresso-black with subtle deep denim-blue dyed ribbons",
        "textured pinned-back updo with delicate curl definition deep raven-black with subtle indigo reflex",
        "loose tousled natural curls with deep side part wet-look jet-black with indigo specular bounce",
        "sweeping side-parted voluminous 3B/3C ringlets jet-black with midnight-blue dimensional highlights",
        "heavy cascading spiral curls framing the cheekbones deep raven-black with subtle indigo reflex",
        "textured pinned-back updo with delicate curl definition jet-black with fine deep indigo-dyed highlights",
        "half-up half-down hairstyle with cascading spiral curls jet-black with fine deep indigo-dyed highlights",
        "half-up half-down hairstyle with cascading spiral curls deep raven-black with subtle indigo reflex",
        "textured pinned-back updo with delicate curl definition jet-black with midnight-blue dimensional highlights",
        "wet slicked-back spiral ringlets glistening with moisture obsidian black with dark violet undertones",
        "loose tousled natural curls with deep side part rich espresso-black with subtle deep denim-blue dyed ribbons",
        "windblown unruly corkscrew curls catching ambient light rich espresso-black with subtle deep denim-blue dyed ribbons",
        "voluminous cascading 3B/3C spiral corkscrew ringlets rich espresso-black with subtle deep denim-blue dyed ribbons",
        "windblown unruly corkscrew curls catching ambient light wet-look jet-black with indigo specular bounce",
        "half-up half-down hairstyle with cascading spiral curls wet-look jet-black with indigo specular bounce",
        "windblown unruly corkscrew curls catching ambient light obsidian black with dark violet undertones",
        "heavy cascading spiral curls framing the cheekbones jet-black with fine deep indigo-dyed highlights",
        "sweeping side-parted voluminous 3B/3C ringlets wet-look jet-black with indigo specular bounce",
        "heavy cascading spiral curls framing the cheekbones rich espresso-black with subtle deep denim-blue dyed ribbons",
        "heavy cascading spiral curls framing the cheekbones wet-look jet-black with indigo specular bounce",
        "high-piled messy textured up-do with loose spiral tendrils obsidian black with dark violet undertones",
        "half-up half-down hairstyle with cascading spiral curls rich espresso-black with subtle deep denim-blue dyed ribbons",
        "wet slicked-back spiral ringlets glistening with moisture deep raven-black with subtle indigo reflex",
        "voluminous cascading 3B/3C spiral corkscrew ringlets deep raven-black with subtle indigo reflex",
        "sleek high ponytail bursting into bouncy spiral curls jet-black with fine deep indigo-dyed highlights",
        "wet slicked-back spiral ringlets glistening with moisture rich espresso-black with subtle deep denim-blue dyed ribbons",
        "wet slicked-back spiral ringlets glistening with moisture jet-black with midnight-blue dimensional highlights",
        "sweeping side-parted voluminous 3B/3C ringlets deep raven-black with subtle indigo reflex",
        "sleek high ponytail bursting into bouncy spiral curls obsidian black with dark violet undertones",
        "voluminous cascading 3B/3C spiral corkscrew ringlets jet-black with fine deep indigo-dyed highlights",
        "sleek high ponytail bursting into bouncy spiral curls deep raven-black with subtle indigo reflex",
        "voluminous cascading 3B/3C spiral corkscrew ringlets wet-look jet-black with indigo specular bounce",
        "wet slicked-back spiral ringlets glistening with moisture jet-black with fine deep indigo-dyed highlights",
        "voluminous cascading 3B/3C spiral corkscrew ringlets jet-black with midnight-blue dimensional highlights",
        "loose tousled natural curls with deep side part jet-black with fine deep indigo-dyed highlights",
        "windblown unruly corkscrew curls catching ambient light jet-black with fine deep indigo-dyed highlights",
        "sweeping side-parted voluminous 3B/3C ringlets obsidian black with dark violet undertones",
        "voluminous cascading 3B/3C spiral corkscrew ringlets obsidian black with dark violet undertones",
        "high-piled messy textured up-do with loose spiral tendrils deep raven-black with subtle indigo reflex",
        "loose tousled natural curls with deep side part deep raven-black with subtle indigo reflex",
        "loose tousled natural curls with deep side part jet-black with midnight-blue dimensional highlights",
        "high-piled messy textured up-do with loose spiral tendrils rich espresso-black with subtle deep denim-blue dyed ribbons",
        "half-up half-down hairstyle with cascading spiral curls obsidian black with dark violet undertones",
        "windblown unruly corkscrew curls catching ambient light jet-black with midnight-blue dimensional highlights",
        "windblown unruly corkscrew curls catching ambient light deep raven-black with subtle indigo reflex",
        "sleek high ponytail bursting into bouncy spiral curls rich espresso-black with subtle deep denim-blue dyed ribbons",
        "heavy cascading spiral curls framing the cheekbones jet-black with midnight-blue dimensional highlights",
        "high-piled messy textured up-do with loose spiral tendrils jet-black with fine deep indigo-dyed highlights",
        "sleek high ponytail bursting into bouncy spiral curls wet-look jet-black with indigo specular bounce",
        "loose tousled natural curls with deep side part obsidian black with dark violet undertones",
        "textured pinned-back updo with delicate curl definition wet-look jet-black with indigo specular bounce",
        "sweeping side-parted voluminous 3B/3C ringlets jet-black with fine deep indigo-dyed highlights",
        "sleek high ponytail bursting into bouncy spiral curls jet-black with midnight-blue dimensional highlights"
    ]

    LIP_COLORS = [
        "plush naturally contoured lips with soft matte finish",
        "sheer stained bare rosy lips with soft matte finish",
        "rich creamy dark cherry lips with subtle specular highlight",
        "high-gloss naturally contoured lips with defined cupid bow",
        "deep velvet dark cherry lips with subtle natural moisture",
        "matte naturally contoured lips with subtle specular highlight",
        "matte naturally contoured lips with clean crisp edges",
        "sheer stained dark cherry lips with a diffused bitten look",
        "matte brick-red lips with subtle natural moisture",
        "high-gloss berry plum lips with clean crisp edges",
        "sheer stained oxblood lips with subtle natural moisture",
        "sheer stained berry plum lips with defined cupid bow",
        "matte oxblood lips with subtle specular highlight",
        "plush berry plum lips with clean crisp edges",
        "matte dark blood-red lips with clean crisp edges",
        "deep velvet espresso chocolate lips with defined cupid bow",
        "plush vampy plum lips with defined cupid bow",
        "sheer stained bare rosy lips with subtle natural moisture",
        "high-gloss smoky mauve nude lips with clean crisp edges",
        "matte burgundy-wine lips with clean crisp edges",
        "high-gloss bare rosy lips with defined cupid bow",
        "high-gloss dark blood-red lips with subtle natural moisture",
        "deep velvet berry plum lips with subtle natural moisture",
        "plush berry plum lips with defined cupid bow",
        "high-gloss espresso chocolate lips with subtle specular highlight",
        "sheer stained naturally contoured lips with defined cupid bow",
        "deep velvet oxblood lips with subtle specular highlight",
        "sheer stained dark cherry lips with defined cupid bow",
        "rich creamy dark cherry lips with defined cupid bow",
        "soft satin smoky mauve nude lips with subtle natural moisture",
        "soft satin oxblood lips with a diffused bitten look",
        "matte bare rosy lips with subtle specular highlight",
        "rich creamy vampy plum lips with clean crisp edges",
        "rich creamy espresso chocolate lips with defined cupid bow",
        "high-gloss dark blood-red lips with a diffused bitten look",
        "matte burgundy-wine lips with a diffused bitten look",
        "soft satin naturally contoured lips with clean crisp edges",
        "rich creamy oxblood lips with subtle natural moisture",
        "rich creamy berry plum lips with defined cupid bow",
        "sheer stained dark blood-red lips with soft matte finish",
        "matte oxblood lips with clean crisp edges",
        "deep velvet naturally contoured lips with defined cupid bow",
        "rich creamy oxblood lips with a diffused bitten look",
        "rich creamy oxblood lips with clean crisp edges",
        "deep velvet smoky mauve nude lips with subtle specular highlight",
        "soft satin naturally contoured lips with soft matte finish",
        "high-gloss bare rosy lips with subtle specular highlight",
        "matte dark cherry lips with soft matte finish",
        "deep velvet dark cherry lips with defined cupid bow",
        "sheer stained burgundy-wine lips with subtle natural moisture",
        "matte espresso chocolate lips with clean crisp edges",
        "sheer stained dark cherry lips with soft matte finish",
        "high-gloss naturally contoured lips with subtle natural moisture",
        "plush burgundy-wine lips with subtle specular highlight",
        "soft satin brick-red lips with subtle natural moisture",
        "sheer stained dark cherry lips with clean crisp edges",
        "soft satin espresso chocolate lips with soft matte finish",
        "deep velvet vampy plum lips with clean crisp edges",
        "deep velvet naturally contoured lips with soft matte finish",
        "soft satin berry plum lips with clean crisp edges",
        "high-gloss brick-red lips with subtle specular highlight",
        "sheer stained burgundy-wine lips with subtle specular highlight",
        "plush oxblood lips with clean crisp edges",
        "matte bare rosy lips with defined cupid bow",
        "soft satin dark cherry lips with clean crisp edges",
        "plush berry plum lips with soft matte finish",
        "deep velvet berry plum lips with clean crisp edges",
        "sheer stained naturally contoured lips with subtle specular highlight",
        "high-gloss burgundy-wine lips with subtle natural moisture",
        "sheer stained bare rosy lips with subtle specular highlight",
        "high-gloss dark cherry lips with defined cupid bow",
        "soft satin dark cherry lips with subtle specular highlight",
        "matte brick-red lips with subtle specular highlight",
        "rich creamy brick-red lips with subtle specular highlight",
        "deep velvet burgundy-wine lips with subtle natural moisture",
        "deep velvet naturally contoured lips with soft matte finish",
        "deep velvet smoky mauve nude lips with soft matte finish",
        "matte oxblood lips with soft matte finish",
        "sheer stained burgundy-wine lips with a diffused bitten look",
        "soft satin vampy plum lips with a diffused bitten look"
    ]

    NAIL_COLORS = [
        "chic manicured dark cherry nails with gloss finish",
        "elegant almond jet-black nails with velvet matte finish",
        "chic manicured blood red nails with high-shine resin coat",
        "chic manicured espresso brown nails with subtle gold foil accents",
        "chic manicured clean sheer nude nails with high-shine resin coat",
        "long coffin espresso brown nails with velvet matte finish",
        "sharp stiletto clean sheer nude nails with gloss finish",
        "sharp stiletto matte black nails with subtle gold foil accents",
        "long coffin dark cherry nails with a subtle metallic sheen",
        "elegant almond matte black nails with high-shine resin coat",
        "sleek almond rich burgundy wine nails with a subtle metallic sheen",
        "long coffin matte black nails with a subtle metallic sheen",
        "long coffin clean sheer nude nails with chrome reflex",
        "long coffin rich burgundy wine nails with velvet matte finish",
        "classic square espresso brown nails with subtle gold foil accents",
        "chic manicured dark emerald nails with velvet matte finish",
        "sleek almond clean sheer nude nails with gloss finish",
        "chic manicured midnight blue nails with subtle gold foil accents",
        "sleek almond dark emerald nails with subtle gold foil accents",
        "elegant almond midnight blue nails with subtle gold foil accents",
        "sharp stiletto espresso brown nails with velvet matte finish",
        "long coffin blood red nails with chrome reflex",
        "elegant almond deep plum purple nails with high-shine resin coat",
        "chic manicured rich burgundy wine nails with a subtle metallic sheen",
        "sleek almond blood red nails with gloss finish",
        "sharp stiletto blood red nails with velvet matte finish",
        "sleek almond dark emerald nails with gloss finish",
        "classic square dark emerald nails with a subtle metallic sheen",
        "sharp stiletto jet-black nails with velvet matte finish",
        "chic manicured matte black nails with subtle gold foil accents",
        "long coffin dark cherry nails with high-shine resin coat",
        "sharp stiletto espresso brown nails with subtle gold foil accents",
        "elegant almond deep plum purple nails with velvet matte finish",
        "elegant almond jet-black nails with a subtle metallic sheen",
        "elegant almond clean sheer nude nails with velvet matte finish",
        "elegant almond deep metallic indigo nails with high-shine resin coat",
        "sleek almond clean sheer nude nails with velvet matte finish",
        "sleek almond blood red nails with subtle gold foil accents",
        "classic square blood red nails with high-shine resin coat",
        "sharp stiletto matte black nails with a subtle metallic sheen",
        "classic square jet-black nails with chrome reflex",
        "chic manicured deep plum purple nails with gloss finish",
        "classic square deep metallic indigo nails with subtle gold foil accents",
        "long coffin espresso brown nails with chrome reflex",
        "sharp stiletto rich burgundy wine nails with a subtle metallic sheen",
        "classic square jet-black nails with high-shine resin coat",
        "sharp stiletto clean sheer nude nails with subtle gold foil accents",
        "elegant almond deep metallic indigo nails with chrome reflex",
        "classic square dark emerald nails with high-shine resin coat",
        "chic manicured rich burgundy wine nails with velvet matte finish",
        "sleek almond deep metallic indigo nails with high-shine resin coat",
        "classic square midnight blue nails with chrome reflex",
        "elegant almond clean sheer nude nails with subtle gold foil accents",
        "chic manicured deep metallic indigo nails with chrome reflex",
        "chic manicured rich burgundy wine nails with gloss finish",
        "elegant almond matte black nails with velvet matte finish",
        "elegant almond clean sheer nude nails with high-shine resin coat",
        "long coffin midnight blue nails with chrome reflex",
        "long coffin deep plum purple nails with subtle gold foil accents",
        "elegant almond dark cherry nails with gloss finish",
        "elegant almond rich burgundy wine nails with velvet matte finish",
        "sleek almond clean sheer nude nails with high-shine resin coat",
        "chic manicured rich burgundy wine nails with subtle gold foil accents",
        "sharp stiletto jet-black nails with subtle gold foil accents",
        "sharp stiletto espresso brown nails with chrome reflex",
        "classic square deep metallic indigo nails with a subtle metallic sheen",
        "classic square dark emerald nails with velvet matte finish",
        "sharp stiletto blood red nails with high-shine resin coat",
        "classic square dark cherry nails with a subtle metallic sheen",
        "elegant almond deep plum purple nails with a subtle metallic sheen"
    ]

    TIER2_INTIMATE_VAULT = [
        "wearing sheer chiffon babydoll unbuttoned to the navel in emerald green with delicate satin strappy back details",
        "wearing sheer chiffon babydoll unbuttoned to the navel in obsidian black catching ray-traced reflections on hip curvature",
        "completely nude, wet bare realskin in obsidian black glistening under soft ambient light with translucent skin depth",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in blush pink with subtle micro-perspiration sheen and biological texture",
        "wearing open silk kimono robe draped loosely in pale champagne with delicate satin strappy back details",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in blush pink glistening under soft ambient light with translucent skin depth",
        "wearing sheer chiffon babydoll unbuttoned to the navel glistening under soft ambient light with translucent skin depth",
        "completely nude, bare unblemished realskin in blush pink exposing narrow waist and athletic hips",
        "wearing silk slip nightdress with eyelash lace trim in sapphire blue with subtle micro-perspiration sheen and biological texture",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in pale champagne with dewy specular highlights across collarbone and thighs",
        "wearing minimalist caged elastic lingerie set in sapphire blue with anatomical precision and natural subcutaneous warmth",
        "completely nude, oiled golden-olive skin in pale champagne catching ray-traced reflections on hip curvature",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in ivory white catching ray-traced reflections on hip curvature",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in dark plum exposing narrow waist and athletic hips",
        "completely nude, oiled golden-olive skin in pale champagne glistening under soft ambient light with translucent skin depth",
        "wearing sheer lace chemise with deep décolletage in pale champagne with anatomical precision and natural subcutaneous warmth",
        "completely nude, oiled golden-olive skin in deep crimson with subtle micro-perspiration sheen and biological texture",
        "wearing sheer lace chemise with deep décolletage in dark plum with dewy specular highlights across collarbone and thighs",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in pale champagne with subtle micro-perspiration sheen and biological texture",
        "wearing minimalist caged elastic lingerie set in sapphire blue glistening under soft ambient light with translucent skin depth",
        "completely nude, bare unblemished realskin with subtle micro-perspiration sheen and biological texture",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in ivory white with dewy specular highlights across collarbone and thighs",
        "wearing sheer floral lace bodysuit with plunging neckline illuminated by soft directional key light and rim light",
        "completely nude, bare unblemished realskin in dark plum with anatomical precision and natural subcutaneous warmth",
        "wearing open silk kimono robe draped loosely with subtle micro-perspiration sheen and biological texture",
        "wearing sheer chiffon babydoll unbuttoned to the navel in dark plum illuminated by soft directional key light and rim light",
        "wearing sheer tulle plunge teddy with satin ribbon ties in ivory white with dewy specular highlights across collarbone and thighs",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in deep crimson catching ray-traced reflections on hip curvature",
        "wearing silk slip nightdress with eyelash lace trim in sapphire blue with exposed side curves and natural shadow gradients",
        "wearing sheer tulle plunge teddy with satin ribbon ties in rich burgundy exposing narrow waist and athletic hips",
        "wearing silk slip nightdress with eyelash lace trim in pale champagne with anatomical precision and natural subcutaneous warmth",
        "wearing minimalist caged elastic lingerie set in deep crimson glistening under soft ambient light with translucent skin depth",
        "wearing silk slip nightdress with eyelash lace trim in pale champagne with delicate satin strappy back details",
        "wearing minimalist silk micro-harness top and sheer strappy bottoms in sapphire blue with dewy specular highlights across collarbone and thighs",
        "wearing silk slip nightdress with eyelash lace trim in sapphire blue illuminated by soft directional key light and rim light",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in pale champagne with anatomical precision and natural subcutaneous warmth",
        "wearing silk slip nightdress with eyelash lace trim in deep crimson with exposed side curves and natural shadow gradients",
        "wearing sheer chiffon babydoll unbuttoned to the navel in emerald green exposing narrow waist and athletic hips",
        "wearing sheer tulle plunge teddy with satin ribbon ties in obsidian black exposing narrow waist and athletic hips",
        "completely nude, bare unblemished realskin with dewy specular highlights across collarbone and thighs",
        "wearing minimalist silk micro-harness top and sheer strappy bottoms in emerald green catching ray-traced reflections on hip curvature",
        "completely nude, oiled golden-olive skin in sapphire blue glistening under soft ambient light with translucent skin depth",
        "wearing sheer lace chemise with deep décolletage in dark plum draped off bare shoulders exposing the clavicle",
        "wearing sheer floral lace bodysuit with plunging neckline in ivory white with delicate satin strappy back details",
        "completely nude, bare unblemished realskin in deep crimson with exposed side curves and natural shadow gradients",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in sapphire blue with exposed side curves and natural shadow gradients",
        "wearing sheer floral lace bodysuit with plunging neckline in obsidian black catching ray-traced reflections on hip curvature",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in obsidian black draped off bare shoulders exposing the clavicle",
        "wearing sheer lace chemise with deep décolletage in obsidian black with delicate satin strappy back details",
        "wearing minimalist silk micro-harness top and sheer strappy bottoms in rich burgundy with exposed side curves and natural shadow gradients",
        "wearing open silk kimono robe draped loosely with exposed side curves and natural shadow gradients",
        "wearing sheer floral lace bodysuit with plunging neckline in ivory white with subtle micro-perspiration sheen and biological texture",
        "completely nude, bare unblemished realskin in obsidian black with subtle micro-perspiration sheen and biological texture",
        "completely nude, bare unblemished realskin in deep crimson with subtle micro-perspiration sheen and biological texture",
        "wearing sheer floral lace bodysuit with plunging neckline in emerald green with delicate satin strappy back details",
        "completely nude, bare unblemished realskin in obsidian black catching ray-traced reflections on hip curvature",
        "completely nude, bare unblemished realskin in obsidian black with delicate satin strappy back details",
        "completely nude, wet bare realskin in dark plum with exposed side curves and natural shadow gradients",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in emerald green with dewy specular highlights across collarbone and thighs",
        "completely nude, oiled golden-olive skin in emerald green catching ray-traced reflections on hip curvature",
        "wearing silk slip nightdress with eyelash lace trim exposing narrow waist and athletic hips",
        "wearing whisper-thin silk bralette with matching garter belt and sheer stockings in rich burgundy catching ray-traced reflections on hip curvature",
        "wearing minimalist caged elastic lingerie set in blush pink with subtle micro-perspiration sheen and biological texture",
        "wearing sheer lace chemise with deep décolletage in ivory white illuminated by soft directional key light and rim light",
        "wearing open silk kimono robe draped loosely in dark plum with dewy specular highlights across collarbone and thighs",
        "completely nude, bare unblemished realskin in pale champagne with subtle micro-perspiration sheen and biological texture",
        "wearing whisper-thin silk bralette with matching garter belt and sheer stockings glistening under soft ambient light with translucent skin depth",
        "wearing sheer lace chemise with deep décolletage in pale champagne with delicate satin strappy back details",
        "completely nude, oiled golden-olive skin in sapphire blue illuminated by soft directional key light and rim light",
        "completely nude, wet bare realskin in deep crimson catching ray-traced reflections on hip curvature",
        "completely nude, bare unblemished realskin in pale champagne catching ray-traced reflections on hip curvature",
        "wearing sheer floral lace bodysuit with plunging neckline in blush pink catching ray-traced reflections on hip curvature",
        "completely nude, bare unblemished realskin in sapphire blue with delicate satin strappy back details",
        "completely nude, wet bare realskin in emerald green with delicate satin strappy back details",
        "wearing sheer lace chemise with deep décolletage in obsidian black with subtle micro-perspiration sheen and biological texture",
        "wearing whisper-thin silk bralette with matching garter belt and sheer stockings in rich burgundy illuminated by soft directional key light and rim light",
        "completely nude, oiled golden-olive skin with exposed side curves and natural shadow gradients",
        "wearing minimalist silk micro-harness top and sheer strappy bottoms in blush pink glistening under soft ambient light with translucent skin depth",
        "wearing whisper-thin silk bralette with matching garter belt and sheer stockings in deep crimson with subtle micro-perspiration sheen and biological texture",
        "wearing open silk kimono robe draped loosely in dark plum with subtle micro-perspiration sheen and biological texture",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in blush pink with exposed side curves and natural shadow gradients",
        "wearing sheer tulle plunge teddy with satin ribbon ties in blush pink with anatomical precision and natural subcutaneous warmth",
        "wearing sheer chiffon babydoll unbuttoned to the navel in sapphire blue exposing narrow waist and athletic hips",
        "wearing sheer floral lace bodysuit with plunging neckline in rich burgundy draped off bare shoulders exposing the clavicle",
        "wearing sheer floral lace bodysuit with plunging neckline in emerald green catching ray-traced reflections on hip curvature",
        "wearing sheer lace chemise with deep décolletage in deep crimson glistening under soft ambient light with translucent skin depth",
        "completely nude, bare unblemished realskin catching ray-traced reflections on hip curvature",
        "wearing whisper-thin silk bralette with matching garter belt and sheer stockings in deep crimson exposing narrow waist and athletic hips",
        "completely nude, bare unblemished realskin exposing narrow waist and athletic hips",
        "wearing minimalist caged elastic lingerie set in rich burgundy with exposed side curves and natural shadow gradients",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in dark plum with anatomical precision and natural subcutaneous warmth",
        "wearing sheer tulle plunge teddy with satin ribbon ties in emerald green with exposed side curves and natural shadow gradients",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in emerald green glistening under soft ambient light with translucent skin depth",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in pale champagne catching ray-traced reflections on hip curvature",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong glistening under soft ambient light with translucent skin depth",
        "wearing sheer tulle plunge teddy with satin ribbon ties in ivory white glistening under soft ambient light with translucent skin depth",
        "wearing open silk kimono robe draped loosely in rich burgundy with delicate satin strappy back details",
        "completely nude, wet bare realskin in deep crimson with delicate satin strappy back details",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong with delicate satin strappy back details",
        "wearing open silk kimono robe draped loosely in rich burgundy catching ray-traced reflections on hip curvature",
        "completely nude, wet bare realskin in sapphire blue illuminated by soft directional key light and rim light",
        "wearing sheer tulle plunge teddy with satin ribbon ties with dewy specular highlights across collarbone and thighs",
        "completely nude, oiled golden-olive skin in obsidian black catching ray-traced reflections on hip curvature",
        "wearing silk satin balconette bra with matching sheer lace-panel string panties in blush pink exposing narrow waist and athletic hips",
        "wearing minimalist caged elastic lingerie set in dark plum illuminated by soft directional key light and rim light",
        "wearing sheer floral lace bodysuit with plunging neckline in blush pink glistening under soft ambient light with translucent skin depth",
        "wearing sheer lace chemise with deep décolletage in pale champagne illuminated by soft directional key light and rim light",
        "wearing sheer chiffon babydoll unbuttoned to the navel in rich burgundy glistening under soft ambient light with translucent skin depth",
        "wearing sheer micro-lace bralette with matching high-cut silk garter thong in pale champagne draped off bare shoulders exposing the clavicle",
        "wearing minimalist caged elastic lingerie set in obsidian black draped off bare shoulders exposing the clavicle",
        "wearing whisper-thin silk bralette with matching garter belt and sheer stockings in sapphire blue with dewy specular highlights across collarbone and thighs",
        "wearing silk slip nightdress with eyelash lace trim in ivory white draped off bare shoulders exposing the clavicle",
        "wearing sheer tulle plunge teddy with satin ribbon ties in obsidian black with dewy specular highlights across collarbone and thighs",
        "wearing sheer lace chemise with deep décolletage in sapphire blue with exposed side curves and natural shadow gradients",
        "wearing open silk kimono robe draped loosely in deep crimson glistening under soft ambient light with translucent skin depth",
        "completely nude, oiled golden-olive skin in obsidian black glistening under soft ambient light with translucent skin depth",
        "wearing minimalist caged elastic lingerie set in blush pink catching ray-traced reflections on hip curvature",
        "wearing sheer tulle plunge teddy with satin ribbon ties in obsidian black with delicate satin strappy back details",
        "wearing open silk kimono robe draped loosely in pale champagne with dewy specular highlights across collarbone and thighs",
        "completely nude, wet bare realskin in obsidian black with anatomical precision and natural subcutaneous warmth"
    ]


    @classmethod
    def _extract_slot_expression(cls, active_tier_tag: str, master_seed: int) -> str:
        tag = (active_tier_tag or "").upper()
        m = re.search(r'(T[1-4])_(\d{2})', tag)
        base_exp = ""
        if m:
            tier_code = m.group(1)
            slot_num = int(m.group(2)) - 1
            tier_map = {
                "T1": LORA_TIER1_ANCHORS,
                "T2": LORA_TIER2_ANATOMY,
                "T3": LORA_TIER3_WARDROBE,
                "T4": LORA_TIER4_SPATIAL
            }
            t_list = tier_map.get(tier_code, [])
            if 0 <= slot_num < len(t_list):
                base_exp = t_list[slot_num].get("expression", "")
        
        if not base_exp:
            idx = master_seed % 50
            if idx < 15 and LORA_TIER1_ANCHORS:
                base_exp = LORA_TIER1_ANCHORS[idx % len(LORA_TIER1_ANCHORS)].get("expression", "")
            elif idx < 25 and LORA_TIER2_ANATOMY:
                base_exp = LORA_TIER2_ANATOMY[(idx - 15) % len(LORA_TIER2_ANATOMY)].get("expression", "")
            elif idx < 40 and LORA_TIER3_WARDROBE:
                base_exp = LORA_TIER3_WARDROBE[(idx - 25) % len(LORA_TIER3_WARDROBE)].get("expression", "")
            elif LORA_TIER4_SPATIAL:
                base_exp = LORA_TIER4_SPATIAL[(idx - 40) % len(LORA_TIER4_SPATIAL)].get("expression", "")
            else:
                base_exp = "calm intense direct gaze with parted soft naturally contoured satin lips"

        round_match = re.search(r'R(\d+)', tag)
        round_num = int(round_match.group(1)) if round_match else (((master_seed // 50) % 40) + 1)
        round_nuances = {
            1: "",
            2: "penetrating focused stare with subtle parted lips and deep intensity",
            3: "contemplative, relaxed expression with softened gaze and natural composure",
            4: "knowing confident expression with slight eyebrow arch and subtle micro-smirk",
            5: "radiant magnetic expression with soft parted lips catching warm sun highlights"
        }
        nuance_idx = ((round_num - 1) % 5) + 1
        nuance = round_nuances.get(nuance_idx, "")
        if nuance and round_num > 1:
            return f"{base_exp}, {nuance}"
        return base_exp

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":           ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "subject_core":          ("STRING", {"multiline": True, "default": cls.DEFAULT_SUBJECT_CORE}),
            },
            "optional": {
                "pose_prompt":           ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "active_tier_tag":       ("STRING", {"default": "", "forceInput": True}),
                "wardrobe_prompt":       ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "scene_lighting_prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "eye_makeup_prompt":     ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "hair_prompt":           ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "lip_prompt":            ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "nail_prompt":           ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "eye_makeup_override":   (["✨ Ollama / LLM Dynamic", "🎲 Dynamic Rotation"] + cls.EYE_MAKEUP_STYLES, {"default": "✨ Ollama / LLM Dynamic"}),
                "hair_override":         (["✨ Ollama / LLM Dynamic", "🎲 Dynamic Rotation"] + cls.HAIR_STYLES, {"default": "✨ Ollama / LLM Dynamic"}),
                "lip_override":          (["✨ Ollama / LLM Dynamic", "🎲 Dynamic Rotation"] + cls.LIP_COLORS, {"default": "✨ Ollama / LLM Dynamic"}),
                "nail_override":         (["✨ Ollama / LLM Dynamic", "🎲 Dynamic Rotation"] + cls.NAIL_COLORS, {"default": "✨ Ollama / LLM Dynamic"}),
                                "expression_override":   (["✨ Pose Engine Matched", "🎲 Dynamic Rotation"] + cls.EXPRESSION_PRESETS, {"default": "✨ Pose Engine Matched"}),
                "expression_prompt":     ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "custom_prompt":         ("STRING", {"multiline": True, "default": ""}),
                "custom_negative":       ("STRING", {"multiline": True, "default": cls.DEFAULT_NEGATIVE}),
            }
        }

    RETURN_TYPES  = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES  = ("fused_prompt", "negative_prompt", "face_detailer_prompt", "image_filename_prefix", "mask_filename_prefix", "upscale_filename_prefix", "telemetry")
    FUNCTION      = "run"
    CATEGORY      = "Vespera/ZIT"

    def run(
        self,
        master_seed: int,
        subject_core: str = DEFAULT_SUBJECT_CORE,
        pose_prompt: str = "",
        active_tier_tag: str = "",
        wardrobe_prompt: str = "",
        scene_lighting_prompt: str = "",
        eye_makeup_prompt: str = "",
        hair_prompt: str = "",
        lip_prompt: str = "",
        nail_prompt: str = "",
        eye_makeup_override: str = "✨ Ollama / LLM Dynamic",
        hair_override: str = "✨ Ollama / LLM Dynamic",
        lip_override: str = "✨ Ollama / LLM Dynamic",
        nail_override: str = "✨ Ollama / LLM Dynamic",
        expression_override: str = "✨ Pose Engine Matched",
        expression_prompt: str = "",
        custom_prompt: str = "",
        custom_negative: str = DEFAULT_NEGATIVE,
        **kwargs
    ):
        is_amy = "amy" in subject_core.lower()
        hair_pool = self.AMY_HAIR_STYLES if is_amy else self.HAIR_STYLES
        lip_pool = self.AMY_LIP_COLORS if is_amy else self.LIP_COLORS
        nail_pool = self.AMY_NAIL_COLORS if is_amy else self.NAIL_COLORS

        # 1. Dynamic Features Selection (deterministic modulo rotation & LLM synthesis)
        if eye_makeup_override == "✨ Ollama / LLM Dynamic":
            if eye_makeup_prompt and eye_makeup_prompt.strip():
                eye_makeup = eye_makeup_prompt.strip()
            else:
                eye_makeup = self.EYE_MAKEUP_STYLES[(master_seed // 4) % len(self.EYE_MAKEUP_STYLES)]
        elif eye_makeup_override == "🎲 Dynamic Rotation" or eye_makeup_override not in self.EYE_MAKEUP_STYLES:
            eye_makeup = self.EYE_MAKEUP_STYLES[(master_seed // 4) % len(self.EYE_MAKEUP_STYLES)]
        else:
            eye_makeup = eye_makeup_override

        if hair_override == "✨ Ollama / LLM Dynamic":
            if hair_prompt and hair_prompt.strip():
                hair = hair_prompt.strip()
            else:
                hair = hair_pool[master_seed % len(hair_pool)]
        elif hair_override == "🎲 Dynamic Rotation" or (hair_override not in self.HAIR_STYLES and hair_override not in self.AMY_HAIR_STYLES):
            hair = hair_pool[master_seed % len(hair_pool)]
        else:
            hair = hair_override

        if lip_override == "✨ Ollama / LLM Dynamic":
            if lip_prompt and lip_prompt.strip():
                lip = lip_prompt.strip()
            else:
                lip = lip_pool[(master_seed // 2) % len(lip_pool)]
        elif lip_override == "🎲 Dynamic Rotation" or (lip_override not in self.LIP_COLORS and lip_override not in self.AMY_LIP_COLORS):
            lip = lip_pool[(master_seed // 2) % len(lip_pool)]
        else:
            lip = lip_override

        if nail_override == "✨ Ollama / LLM Dynamic":
            if nail_prompt and nail_prompt.strip():
                nail = nail_prompt.strip()
            else:
                nail = nail_pool[(master_seed // 3) % len(nail_pool)]
        elif nail_override == "🎲 Dynamic Rotation" or (nail_override not in self.NAIL_COLORS and nail_override not in self.AMY_NAIL_COLORS):
            nail = nail_pool[(master_seed // 3) % len(nail_pool)]
        else:
            nail = nail_override


        # Resolve active expression (Pose Engine Matched, Dynamic Rotation, or Preset)
        if expression_override == "✨ Pose Engine Matched":
            if expression_prompt and expression_prompt.strip():
                active_expression = expression_prompt.strip()
            else:
                active_expression = self._extract_slot_expression(active_tier_tag, master_seed)
        elif expression_override == "🎲 Dynamic Rotation":
            all_exps = EXPRESSIONS_POOL_SFW or ["calm poised expression, natural eye contact"]
            active_expression = all_exps[master_seed % len(all_exps)]
        elif expression_override in self.EXPRESSION_PRESETS:
            active_expression = expression_override
        else:
            active_expression = self._extract_slot_expression(active_tier_tag, master_seed)


        tag_lower = (active_tier_tag + " " + pose_prompt).lower()
        is_tier_2 = "tier 2" in tag_lower or "t2_" in tag_lower or "anatomy" in tag_lower
        is_close_up = any(kw in tag_lower for kw in [
            "macro", "close-up", "closeup", "headshot", "tight focal framing", "face only", "portrait framing"
        ])

        # 2. Wardrobe Enforcement
        if is_tier_2:
            intimate_idx = master_seed % len(self.TIER2_INTIMATE_VAULT)
            cleaned_wardrobe = self.TIER2_INTIMATE_VAULT[intimate_idx]
        else:
            cleaned_wardrobe = wardrobe_prompt.strip() if wardrobe_prompt else ""
            if is_close_up and cleaned_wardrobe:
                garment_parts = [p.strip() for p in cleaned_wardrobe.split(",") if p.strip()]
                upper_garment_parts = []
                for gp in garment_parts:
                    gp_lower = gp.lower()
                    if any(skip_kw in gp_lower for skip_kw in [
                        "trousers", "pants", "skirt", "heels", "shoes", "boots", "stilettos", "pumps", "leggings", "sneakers", "sandals", "loafers", "oxford"
                    ]):
                        continue
                    upper_garment_parts.append(gp)
                if upper_garment_parts:
                    cleaned_wardrobe = ", ".join(upper_garment_parts)
                else:
                    cleaned_wardrobe = wardrobe_prompt.strip()
            
            # Final safety: if wardrobe is still empty, use a safe default
            if not cleaned_wardrobe:
                cleaned_wardrobe = "chic tailored blazer, buttoned silk blouse, fitted trousers"

        # 3. Pose & Subject Sanitization for Clothed Tiers
        active_pose = pose_prompt.strip() if pose_prompt else ""
        active_core = subject_core.strip() if subject_core else ""
        # Sanitize any legacy smirk from active_core
        if active_core:
            active_core = re.sub(r'knowing sensual smirk revealing ivory teeth,?\s*', '', active_core, flags=re.IGNORECASE)
            active_core = re.sub(r'subtle knowing asymmetrical half-smirk,?\s*(clean ivory teeth slightly visible,?)?\s*', '', active_core, flags=re.IGNORECASE)
            active_core = re.sub(r'\s+', ' ', active_core).strip(', ')

        if not is_tier_2:
            # Strip accidental nudity / bare skin triggers from pose prompts
            if active_pose:
                active_pose = re.sub(r'\bbare\s+(left\s+|right\s+)?(shoulder|shoulders|neck|chest|back|spine|skin|midriff)\b', r'\1\2', active_pose, flags=re.IGNORECASE)
                active_pose = re.sub(r'\bbare\b', '', active_pose, flags=re.IGNORECASE)
                active_pose = re.sub(r'\s+', ' ', active_pose).strip(', ')

            # Strip exposed stomach / navel / bust distortion triggers from subject core
            if active_core:
                active_core = re.sub(r'\b(vertical\s+navel|navel|D-cup\s+bust|thick\s+\d+-inch\s+thighs|bare\s+shoulders?)\b', '', active_core, flags=re.IGNORECASE)
                active_core = re.sub(r',\s*,', ',', active_core)
                active_core = re.sub(r'\s+', ' ', active_core).strip(', ')

        parts = []

        # 0. Wardrobe Enforcement (Must be first for FLUX/Lumina to prevent NSFW collapse)
        if cleaned_wardrobe:
            if not is_tier_2:
                parts.append(f"fully clothed woman, modest completely covered chest and torso, wearing elegant {cleaned_wardrobe.rstrip(',')}")
            else:
                parts.append(cleaned_wardrobe.rstrip(","))

        # 1. Subject Core Baseline (Locked identity)
        if active_core:
            parts.append(active_core.rstrip(","))

        # 2. Dynamic Identity Features (Eye Makeup, Hair, Lips, Nails)
        if eye_makeup:
            parts.append(f"({eye_makeup.rstrip(',')}:1.15)")
        parts.append(hair)
        parts.append(f"({lip}:1.2)")
        if not is_close_up:
            parts.append(nail)

        # 3. Pose & Action
        if active_pose:
            parts.append(active_pose.rstrip(","))
        if active_expression and active_expression.lower() not in active_pose.lower():
            parts.append(active_expression.rstrip(","))

        # 4. Built-in Context-Aware Forensic Details (Baked Engine)
        forensic_base = "flawless photographic rendering with true-to-life light absorption, rich tonal depth, and micro-contrast"
        
        if is_close_up:
            forensic_framing = "ultra-detailed micro-epidermis with authentic pores, fine vellus hair along the jawline, complex subsurface scattering revealing natural vascular warmth, highly detailed iris topography with deep corneal specular reflections, sharp individual eyelash definition, subtle moisture on the lips and tear ducts"
        else:
            forensic_framing = "accurate human anatomy and proportions, subtle muscular definition and skin tension over bone structure, realistic center of gravity and postural weight distribution, authentic fabric drape and material physics"
        
        forensic_env = "skin and materials reacting accurately to environmental lighting with correct specular bounce and ambient occlusion" if (scene_lighting_prompt and scene_lighting_prompt.strip()) else "cinematic studio lighting with rich shadows"
        
        # 5. Camera Optics & Sensor Chemistry
        if is_close_up:
            optical_physics = "shot on 85mm prime portrait lens, f/1.4 aperture, razor-sharp focal plane on the eyelashes, anamorphic optical bokeh, physical circle of confusion, distinct ocular catchlights"
        else:
            optical_physics = "shot on 35mm cinematic lens, f/4 aperture, hyper-crisp edge-to-edge optical fidelity, authentic spatial compression, subtle lateral chromatic aberration along high-contrast silhouettes, true 35mm optical glass mechanics"
            
        sensor_chemistry = "raw uncompressed digital sensor capture, high acutance, zero digital airbrushing, subtle natural lens halation, micro-contrast optical imperfections"

        parts.append(f"{forensic_base}, {forensic_framing}, {forensic_env}, {optical_physics}, {sensor_chemistry}")

        # 6. Scene & Lighting
        if scene_lighting_prompt and scene_lighting_prompt.strip():
            parts.append(scene_lighting_prompt.strip().rstrip(","))

        # 6. User Custom Prompt
        if custom_prompt and custom_prompt.strip():
            parts.append(custom_prompt.strip().rstrip(","))

        fused = ", ".join(parts)
        negative = custom_negative.strip() if custom_negative and custom_negative.strip() else self.DEFAULT_NEGATIVE
        
        if not is_tier_2:
            anti_nsfw = (
                "nsfw, nude, naked, topless, bare breasts, nipples, exposed chest, cleavage, deep cleavage, "
                "exposed breasts, bare midriff, exposed navel, bare stomach, unclothed, undressed, "
                "wardrobe malfunction, dress pulled down, open robe, open shirt, open dress, lingerie, see-through"
            )
            for tok in anti_nsfw.split(", "):
                if tok.lower() not in negative.lower():
                    negative = negative + ", " + tok

        pose_slug = active_tier_tag.strip() if active_tier_tag and active_tier_tag.strip() else "pose_unknown"
        tag_clean = f"{pose_slug}_s{master_seed}"

        # Face detailer gets matched eye makeup + lip token + forensic identity anchors
        if is_amy:
            base_detailer = self.DEFAULT_AMY_FACE_DETAILER
            image_prefix = f"dataset_images/amy_{tag_clean}"
            mask_prefix = f"dataset_masks/amy_{tag_clean}"
            upscale_prefix = f"dataset_upscaled/amy_{tag_clean}"
            telemetry = f"[Agnostic Engine] Seed: {master_seed} | Tag: {pose_slug} | Amy Forensic Face Locked | CloseUp: {is_close_up}"
        else:
            base_detailer = self.DEFAULT_FACE_DETAILER
            image_prefix = f"dataset_images/vespera_{tag_clean}"
            mask_prefix = f"dataset_masks/vespera_{tag_clean}"
            upscale_prefix = f"dataset_upscaled/vespera_{tag_clean}"
            telemetry = f"[Agnostic Engine] Seed: {master_seed} | Tag: {pose_slug} | Sultry Face Locked | CloseUp: {is_close_up}"

        face_detailer = f"{base_detailer}, {active_expression}, ({eye_makeup}:1.2), ({lip}:1.35), chiseled razor-sharp jawline, sculpted high cheekbones, subtle cheek hollows, lean delicate bone structure, narrow chin, raw unedited skin texture, visible natural micro-pores, authentic skin imperfections, zero beauty filter, zero airbrushing, crisp dermal grain, natural outdoor ambient pupil reflections, eye catchlights reflecting actual scene lighting, zero studio softbox reflections"

        return (
            fused,
            negative,
            face_detailer,
            image_prefix,
            mask_prefix,
            upscale_prefix,
            telemetry
        )
