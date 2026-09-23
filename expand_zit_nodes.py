# -*- coding: utf-8 -*-
"""
Script to expand zit_nodes.py with 25+ rich, authentic permutations across all vectors.
"""
import os, sys

target_path = r"D:\AI\Projects\ComfyUI\custom_nodes\ComfyUI-Vespera-ZIT\zit_nodes.py"

content = '''"""
File    : zit_nodes.py
Purpose : Zero-Shot Image Transfer (ZIT) Character Override, Dynamic Wardrobe & Master Prompt Workstation Node Suite.
"""

import os
import re
import sqlite3
import random

DEFAULT_VESPERA_PROMPT_PREFIX = (
    "A hyper-realistic 8k raw 35mm photographic portrait of a 5\'5\\" French woman named Vespera. "
    "Pronounced hourglass figure, narrow 24-inch waist, 38-inch hips (0.66 waist-to-hip ratio), "
    "thick muscular 30-inch thighs, full rounded rear, and natural C-cup bust. "
    "Flawless luminous olive skin with radiant golden undertones, completely smooth clear forehead, and a subtle rose cheekbone flush. "
    "Sharp black liquid soft-smudged smoky black kohl eyeliner, almond-shaped deep captivating hazel-green eyes with subtle amber-gold flecks, "
    "full dark-sable arched eyebrows. "
    "Full soft black satin-sheen lips with defined cupid's bow, slightly larger canines, and a tiny beauty mark (1mm) off the left corner of her upper lip. "
    "Voluminous, springy 3B/3C spiral ringlet curls in deep jet-black with interwoven electric indigo highlights, uniform length cascading mid-back framing her jawline and collarbone with no bangs. "
    "Signature tattoos: mechanical dragon tattoo on right back, interlocking gears with indigo accents on outer left thigh. "
    "Relaxed confident posture, subtle playful half-smirk, cinematic high-contrast lighting with cool-blue backlight catching indigo hair strands, f/1.4 shallow depth of field, authentic skin pore texture"
)

DB_PATH = r"D:\AI\Projects\antigravity-overdrive-sync\sync_state.db"

HAIR_CONFLICTS = [
    r'\\bblonde(?:\\s+hair)?\\b', r'\\bblond(?:\\s+hair)?\\b', r'\\bbrown\\s+hair\\b', r'\\bred\\s+hair\\b',
    r'\\bblack\\s+hair\\b', r'\\bwhite\\s+hair\\b', r'\\bsilver\\s+hair\\b', r'\\bpink\\s+hair\\b',
    r'\\bblue\\s+hair\\b', r'\\bgreen\\s+hair\\b', r'\\bpurple\\s+hair\\b', r'\\bgolden\\s+hair\\b',
    r'\\bshort\\s+hair\\b', r'\\blong\\s+hair\\b', r'\\bstraight\\s+hair\\b', r'\\bcurly\\s+hair\\b',
    r'\\bwavy\\s+hair\\b', r'\\bponytail\\b', r'\\bpigtails\\b', r'\\bbraids?\\b', r'\\bbob\\s+cut\\b',
    r'\\bbangs\\b', r'\\btwintails\\b'
]

EYE_CONFLICTS = [
    r'\\bblue\\s+eyes?\\b', r'\\bgreen\\s+eyes?\\b', r'\\bbrown\\s+eyes?\\b', r'\\bhazel\\s+eyes?\\b',
    r'\\bred\\s+eyes?\\b', r'\\bamber\\s+eyes?\\b', r'\\byellow\\s+eyes?\\b', r'\\bblack\\s+eyes?\\b',
    r'\\bgrey\\s+eyes?\\b', r'\\bgray\\s+eyes?\\b', r'\\bpurple\\s+eyes?\\b', r'\\bdark\\s+eyes?\\b'
]

BODY_SUBJECT_CONFLICTS = [
    r'\\b1girl\\b', r'\\b1woman\\b', r'\\b1female\\b', r'\\bsolo\\b', r'\\ba\\s+girl\\b', r'\\ba\\s+woman\\b',
    r'\\bflat\\s+chest\\b', r'\\bsmall\\s+breasts?\\b', r'\\blarge\\s+breasts?\\b', r'\\bhuge\\s+breasts?\\b',
    r'\\bpetite\\b', r'\\bslim\\b', r'\\bchubby\\b', r'\\btall\\b', r'\\bshort\\s+stature\\b',
    r'\\bfemale\\b', r'\\bwoman\\b', r'\\bgirl\\b'
]

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
                patterns.append(rf'\\b{re.escape(kw_clean)}\\b')
                
    cleaned = text
    for pat in patterns:
        cleaned = re.sub(pat, '', cleaned, flags=re.IGNORECASE)
        
    cleaned = re.sub(r',\\s*,+', ',', cleaned)
    cleaned = re.sub(r'^\\s*,\\s*', '', cleaned)
    cleaned = re.sub(r'\\s*,\\s*$', '', cleaned)
    cleaned = re.sub(r'\\s+', ' ', cleaned).strip()
    return cleaned


class ZITCharacterOverrideNode:
    """
    Zero-Shot Image Transfer (ZIT) Character Override Node.
    """
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
    CATEGORY = "ZIT"

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

        final_prompt = re.sub(r',\\s*,+', ',', final_prompt).strip(' ,')
        
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


class VesperaCharacterEncoder:
    """
    Encodes Vespera's physical baseline traits from SQLite state.
    """
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
    CATEGORY = "ZIT"

    def encode_vespera(self, character_style: str, include_tattoos: bool, include_wardrobe_seed: str, additional_physical_traits: str = ""):
        base = DEFAULT_VESPERA_PROMPT_PREFIX
        if not include_tattoos:
            base = re.sub(r'Signature tattoos:.*?(?=(Relaxed|\\Z))', '', base)

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
        full_prompt = re.sub(r',\\s*,+', ',', full_prompt).strip(' ,')

        negative = "blurry, low quality, deformed, extra limbs, bad anatomy, cartoon, anime, 3d render, plastic skin"
        return (full_prompt, negative)


class ZITBackgroundArchitectNode:
    """
    Zero-Shot Image Transfer (ZIT) Environment & Background Synthesizer.
    """
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
    CATEGORY = "ZIT"

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
        full_scenario = re.sub(r',\\s*,+', ',', full_scenario).strip(' ,')

        return (full_scenario, bg_only, composition_only)


# ============================================================================
# COMPREHENSIVE 25-ITEM WARDROBE DATA ENGINE
# ============================================================================
class ZITDynamicWardrobeEngine:
    """
    Dynamic Stochastic Wardrobe & Attire Randomizer Node for FLUX, ZIT, and SDXL.
    Synthesizes rich, highly detailed, fabric-accurate clothing or explicit NSFW vectors across 9 distinct tiers.
    """
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

    WARDROBE_DATA = {
        "lingerie": {
            "items": [
                "a delicate black French chantilly lace lingerie bodysuit with sheer mesh panels and scalloped trim",
                "a plunging scarlet silk satin teddy with delicate scalloped eyelash lace and criss-cross strappy back",
                "a vintage emerald green velvet underwire bra with matching high-waisted satin garter belt and sheer lace panties",
                "a sheer embroidered tulle corset with flexible boning that cinches her 24-inch waist paired with matching sheer lace panties",
                "an obsidian black satin balconette bra with delicate gold hardware accents and sheer mesh side wings",
                "a semi-sheer midnight-blue silk babydoll nightgown with plunging neckline and fluttery hemline",
                "a strappy burgundy lace bralette paired with satin high-cut panties and matching garter straps",
                "a provocative open-cup black lace corset top with adjustable ribbon lace-up detailing along the back",
                "a champagne-gold silk satin slip with deep French lace trim along the décolletage and thighs",
                "a sheer white floral lace demi-cup bra with delicate scalloped edges and matching high-waisted briefs",
                "a deep sapphire silk corset with black velvet trim and steel boning accentuating her waist",
                "a blush-pink silk satin camisole with black French lace overlay and matching tap shorts",
                "a sheer black mesh underwire bra with provocative cut-outs and matching thong with gold chains",
                "a ruby-red velvet bustier with plunging sweetheart neckline and satin ribbon laces",
                "a sheer black polka-dot tulle babydoll with ruffled hem and satin ribbon bow",
                "an opulent peacock-teal silk satin slip dress with lace-trimmed deep V-neckline",
                "a sheer embroidered lilac floral lingerie set with delicate scalloped bralette and sheer Brazilian panties",
                "a black wet-look micro-ribbon bra with criss-cross body wrapping and strappy garter harness",
                "a rich espresso silk satin teddy with sheer lace waist panels and plunging neckline",
                "a vintage ivory silk corset with delicate floral jacquard weave and pearl button accents",
                "a sheer black spider-web lace bodysuit with high-neck collar and keyhole back",
                "a midnight-purple velvet underwire bralette with matching sheer mesh thong and garter loops",
                "a delicate gold-shimmer sheer tulle chemise with spaghetti straps and side slits",
                "a scandalous black satin open-back basque with sheer lace side inserts and matching suspenders",
                "a burgundy silk charmeuse slip with sheer eyelash lace framing her collarbone and waist"
            ],
            "bottoms_acc": [
                "sheer black thigh-high stockings with lace silicone stay-up tops and 4-inch satin stiletto mules",
                "sheer back-seam stockings clipped to delicate satin garter straps with pointed-toe patent pumps",
                "ultra-sheer nude thigh-high stockings with scalloped lace cuffs and a delicate silver chain anklet",
                "bare legs with sheer lace thigh bands and classic black satin pumps",
                "vintage fishnet thigh-high stockings attached to a 6-strap satin garter belt with stiletto heels",
                "sheer charcoal stockings with satin bow accents and 4.5-inch black patent leather pumps",
                "ultra-fine 10-denier black stockings with reinforced heels and open-toe satin mule heels",
                "bare legs with sparkling diamond-mesh thigh garters and velvet stiletto sandals",
                "sheer midnight-blue stockings with scalloped floral cuffs and strappy stiletto heels",
                "bare legs with delicate silk ribbon ties wrapped around her ankles and minimalist satin pumps",
                "black lace-top stockings with vintage metal garter clips and Christian Louboutin red-bottom heels",
                "sheer white bridal-style lace stockings with pearl garters and champagne silk stilettos",
                "bare legs with a fine platinum anklet and pointed black patent leather slingback heels",
                "semi-sheer back-seam thigh-highs with vintage Cuban heels and black ankle-strap stilettos",
                "bare legs with sheer black lace ankle socks and 4-inch glossy Mary Jane stilettos",
                "sheer nude stockings with contrasting black back seams and red satin court pumps",
                "glossy sheer tights catching specular light with metallic gold stiletto sandals",
                "bare legs with a thin black velvet thigh band and minimalist patent leather mules",
                "sheer lace-topped thigh-high stockings with 5-inch platform dagger heels",
                "bare feet with delicate gold toe rings and a whisper-thin ankle chain",
                "sheer espresso-tinted stockings with delicate lace trim and pointed suede pumps",
                "bare legs with subtle rose oil sheen and strappy black satin lace-up heels",
                "vintage patterned jacquard lace stockings with high-gloss pointed stilettos",
                "sheer black fishnet hold-ups with wide lace tops and patent leather D\'Orsay pumps",
                "bare legs with a delicate diamond-cut silver ankle bracelet and black satin slip-on heels"
            ]
        },
        "slutty": {
            "items": [
                "bondage outfit, a strappy matte black leather harness with polished silver o-rings and buckled collar across her bare chest",
                "a micro-mesh see-through fishnet bodysuit with ultra-high cut hips and provocative cut-out décolletage",
                "a high-gloss liquid black latex micro-bikini top with ultra-thin string ties and minimal coverage",
                "an open-front patent leather harness bra paired with a micro mini-skirt that hugs her flared hips",
                "a sheer wet-look vinyl crop top with open underboob cut-outs and criss-cross body chains",
                "a translucent red latex bodysuit with deep plunging neckline and zipper hardware along the torso",
                "a provocative strappy leather body cage with O-ring connectors accentuating her hourglass curves",
                "a cut-out wet-look monokini with sheer mesh side panels and ultra-thin string straps",
                "an ultra-revealing black patent leather underbust corset with metal buckles and open cup framing",
                "a scandalous sheer black mesh micro-dress with open back and side cut-outs extending from ribs to hips",
                "a high-gloss purple latex crop top with provocative front keyhole cut-out and matching micro-skirt",
                "a strappy black vinyl bondage harness wrapping her bust and waist with polished steel studs",
                "a micro-coverage metallic silver chainmail top draped loosely over her bare chest",
                "a sheer red fishnet long-sleeve crop top worn with black leather micro-shorts",
                "a liquid black latex catsuit with plunging open-chest neckline and waist-cinching paneling",
                "a provocative criss-cross black elastic body harness outlining her cleavage and 24-inch waist",
                "an ultra-sheer wet-look black PVC bralette paired with a micro-mini slit skirt",
                "a distressed black leather moto harness bra with industrial silver buckles and chain draping",
                "a sheer mesh and patent leather panelled bodysuit with exposed hips and deep plunge",
                "a provocative scarlet latex micro-bikini with gold ring connectors and side-tie bottoms",
                "a black wet-look vinyl halter top with open back and underbust cutout",
                "a scandalous see-through black lace body stocking hugging every millimeter of her curves",
                "a strappy matte leather pentagram harness across her bare chest with matching waist belt",
                "a glossy translucent pink vinyl tube top with open sides and buckle straps",
                "an open-cup black velvet and leather corset with steel boning and chrome chain accents"
            ],
            "bottoms_acc": [
                "thigh-high glossy patent leather stiletto boots with silver buckle hardware and a matching leather collar",
                "bondage outfit leather leg harness straps wrapping around her upper 30-inch thighs with fishnet stockings",
                "open-toe lace-up stiletto heels with a locked silver choker necklace",
                "glossy latex thigh-high stockings with 5-inch dagger stiletto heels",
                "thigh-high fishnet stockings with black leather garter cuffs and 4.5-inch platform stiletto pumps",
                "glossy wet-look vinyl over-the-knee boots with chrome zipper details and a spike-studded collar",
                "ultra-high cut patent leather thigh-high boots with thin stiletto heels and a locking padlock choker",
                "bare legs with strappy leather thigh holsters and 5-inch pointed ankle-strap stilettos",
                "sheer black stockings torn at the thigh with chunky platform combat boots and silver chain necklace",
                "glossy black latex thigh-highs with metallic silver stiletto heels and a heavy silver O-ring choker",
                "bare legs with criss-crossing black ribbon ties wrapping up her calves to 4-inch stiletto heels",
                "patent leather knee-high lace-up boots with metal eyelets and a wide leather waist cincher",
                "ultra-sheer black fishnet tights with pointed red patent leather dagger pumps",
                "matte black leather leg harnesses strapped over bare thighs with minimalist stiletto mules",
                "glossy red vinyl thigh-high boots with 5-inch heels and a matching red leather choker",
                "bare legs with silver body chains draping down to open-toe metallic stiletto heels",
                "strappy bondage sandals with 4-inch heels and multiple buckle straps climbing the calf",
                "glossy PVC thigh-high stockings with built-in garters and pointed patent pumps",
                "bare legs with black velvet ribbon choker and 5-inch black patent leather ankle boots",
                "fishnet thigh-highs clipped to a heavy-duty leather garter belt with platform heels",
                "matte leather thigh-high boots with back lacing and a polished chrome torque necklace",
                "bare legs with an ankle-locked silver chain and glossy stiletto court shoes",
                "sheer mesh thigh-highs with studded garter straps and open-toe stiletto boots",
                "glossy black latex opera gloves extending past the elbows and matching latex thigh-high stilettos",
                "bare legs with leather leg bands and 4.5-inch Christian Louboutin patent stiletto pumps"
            ]
        },
        "nudity": {
            "items": [
                "completely nude, b3tternud3s anatomical precision, bare breasts, exposed 24-inch waist, natural hip flare, and bare 30-inch thighs",
                "fully nude, realskin texture, completely uncovered body showcasing natural bust curves, flat toned stomach, and smooth bare hips",
                "completely nude, oiled skin with glistening specular highlights across bare collarbones, breasts, and toned thighs",
                "fully nude with b3tternud3s realism, bare curves, completely uncovered silhouette, and soft natural skin tones",
                "completely nude, glowing golden-olive realskin texture across her sculpted torso, bare waist, and toned thighs",
                "fully nude, artistic high-fashion nude portrait showcasing natural hourglass curves and unblemished skin",
                "completely nude, raw unadorned anatomical beauty with soft natural shadow falloff across bare hips and breasts",
                "fully nude, dewy realskin texture catching ambient specular rim light across bare collarbone and legs",
                "completely nude, smooth olive skin with realistic biological pore texture across bare breasts and 24-inch waist",
                "fully nude, sculpted athletic physique with natural breast contours, toned midriff, and smooth bare thighs",
                "completely nude, glistening body oil highlights accentuating her 38-inch hip flare and rounded rear",
                "fully nude, natural realskin realism with delicate collarbone shadows and flawless bare skin",
                "completely nude, soft directional lighting sculpting the curves of her breasts, waist, and thighs",
                "fully nude, pure organic form with warm subsurface dermal scatter across bare shoulders and torso",
                "completely nude, fine analog film grain across bare skin with authentic biological highlights",
                "fully nude, statuesque bare silhouette showcasing her 0.66 waist-to-hip ratio and toned legs",
                "completely nude, subtle moisture sheen across bare chest, flat stomach, and sculpted thighs",
                "fully nude, intimate raw photorealism with natural breast shape and smooth bare hip curvature",
                "completely nude, luminous golden undertones across her bare collarbone, breasts, and waist",
                "fully nude, artistic monochrome tonal values sculpting her bare feminine anatomy",
                "completely nude, soft ambient candlelight illuminating bare olive skin and hourglass contours",
                "fully nude, authentic realskin micro-details across bare breasts, narrow waist, and flared hips",
                "completely nude, bathed in soft directional window light highlighting bare shoulders and thighs",
                "fully nude, natural skin pore fidelity and gentle biological flush across bare chest and torso",
                "completely nude, raw unfiltered photographic capture of her bare hourglass silhouette"
            ],
            "bottoms_acc": [
                "barefoot with a fine delicate silver chain anklet around her right foot and minimalist gold hoop earrings",
                "barefoot with a tiny obsidian pendant necklace resting between her bare collarbones",
                "completely bare without clothing, wearing only a black velvet ribbon choker",
                "barefoot with subtle rose satin ribbon tied around her right wrist",
                "barefoot with a delicate gold body chain draping across her bare waist and hips",
                "wearing only a thin platinum diamond choker necklace and small stud earrings",
                "barefoot with a tiny 1mm beauty mark catching the light and delicate silver rings on her fingers",
                "wearing only a delicate pearl strand necklace resting against her bare décolletage",
                "barefoot on dark hardwood with a fine gold chain circling her left ankle",
                "wearing only a minimalist black leather cord necklace with a polished raw emerald pendant",
                "barefoot with subtle glistening skin oils and a single diamond tennis bracelet",
                "wearing only a delicate gold waist chain highlighting her 24-inch waistline",
                "barefoot with soft candlelight reflecting off a tiny gold hoop earring",
                "wearing only an antique Cartier-style gold watch on her left wrist",
                "barefoot on luxury marble with a whisper-thin silver chain around her right ankle",
                "wearing only a vintage art deco diamond drop necklace against bare skin",
                "barefoot with a tiny sapphire stud earring and clean natural manicure",
                "wearing only a black silk ribbon loosely tied around her neck",
                "barefoot with natural dewy skin catching directional rim lighting",
                "wearing only a fine platinum chain resting in the hollow of her collarbone",
                "barefoot with a delicate double-strand gold anklet on her right foot",
                "wearing only a minimalist hammered-gold cuff bracelet on her left forearm",
                "barefoot with natural unadorned elegance and subtle rose lip sheen",
                "wearing only a tiny diamond pendant resting between her bare breasts",
                "barefoot with soft ambient shadows wrapping around her bare heels and ankles"
            ]
        },
        "partial_nudity": {
            "items": [
                "an unbuttoned oversized white cotton dress shirt falling off her bare shoulders, completely exposing her bare chest and midriff",
                "a sheer wet white silk camisole clinging translucent against her bare breasts and torso",
                "a vintage silk kimono-style robe draped loosely open, revealing her bare bust and exposed thighs",
                "a low-draped black satin blazer worn completely open with nothing underneath, exposing bare chest and toned stomach",
                "a sheer chiffon robe slipping off her shoulders with delicate peekaboo transparency over bare curves",
                "an unzipped black leather moto jacket falling open over her bare chest and narrow waist",
                "an unbuttoned charcoal cashmere cardigan slipping down her arms, revealing bare breasts and collarbone",
                "a sheer black mesh long-sleeve top with zero lining, fully revealing bare breasts and torso underneath",
                "a draped emerald silk velvet robe hanging open at the front, exposing bare cleavage, midriff, and thighs",
                "an oversized vintage denim jacket worn unbuttoned and off-the-shoulder over a bare torso",
                "a translucent wet silk slip dress clinging tightly with complete sheer visibility over bare breasts",
                "a luxurious white silk bathrobe tied loosely at the waist, hanging open to expose bare chest and legs",
                "an unbuttoned pinstripe tailored waistcoat worn open over her bare breasts and 24-inch waist",
                "a sheer embroidered tulle robe with scalloped lace sleeves falling open over a bare body",
                "an unzipped black athletic hoodie falling off one shoulder, exposing bare chest and collarbone",
                "a low-cut open knit crochet top with wide open stitches revealing bare skin and breasts underneath",
                "a draped midnight-blue satin sheet clutched loosely against her hips, leaving upper body completely bare",
                "an unbuttoned silk pajama top falling open over her bare torso with sleeves rolled up",
                "a sheer black lace kimono with scalloped hem falling open to reveal bare breasts and waist",
                "an oversized chunky wool knit sweater pulled up above her breasts, exposing her bare chest and waist",
                "a low-slung black tailored tuxedo jacket worn unbuttoned with no shirt, showing bare chest and stomach",
                "a sheer organza duster coat billowing open over bare breasts and high-cut panties",
                "an unzipped velvet track jacket falling open over her bare cleavage and flat stomach",
                "a wet sheer linen beach shirt completely unbuttoned and clinging to damp bare skin",
                "a draped vintage fur coat wrapped loosely over bare shoulders, exposing bare chest and neckline"
            ],
            "bottoms_acc": [
                "tailored high-waisted dark shorts left unbuttoned at the waist with sheer black stockings",
                "completely bare legs and barefoot with glistening skin catching ambient highlights",
                "matching sheer silk lace panties and thigh-high black stockings with pointed-toe pumps",
                "unbuttoned distressed dark denim jeans sitting low on her hips",
                "sheer black Brazilian panties with high-cut hips and 4-inch satin stiletto mules",
                "bare legs with unbuttoned tailored trousers pooled at her feet on dark hardwood",
                "a micro black satin mini-skirt riding high on her 30-inch thighs with pointed heels",
                "sheer white lace panties with delicate satin side ties and barefoot elegance",
                "vintage Levi\'s denim shorts unbuttoned at the fly with bare legs and stiletto sandals",
                "sheer black stockings clipped to a low garter belt with red-bottom patent pumps",
                "bare legs with a whisper-thin gold ankle chain and minimalist slingback heels",
                "matching emerald green silk panties and sheer thigh-high stockings with stiletto heels",
                "low-rise black sweatpants pushed down past her hips revealing bare hip bones",
                "sheer mesh panties with delicate scalloped edges and 4.5-inch patent stiletto pumps",
                "bare legs with sheer lace thigh garters and pointed black suede ankle boots",
                "a high-waisted black leather mini-skirt with front zipper left partially unzipped",
                "sheer nude stockings with back seams and classic black patent court shoes",
                "matching burgundy velvet panties with gold chain accents and bare feet",
                "unbuttoned linen trousers sitting low on her 38-inch hips with bare feet",
                "sheer black tulle panties with satin ribbon bow and ankle-strap stiletto sandals",
                "bare legs with sheer black hold-up stockings and glossy patent mules",
                "a micro-pleated skirt resting low on her hips with bare legs and combat boots",
                "matching black silk tap shorts with lace hem and pointed stiletto pumps",
                "sheer lace boyshorts hugging her curves with barefoot natural ease",
                "bare legs with delicate diamond anklet and Christian Louboutin stiletto pumps"
            ]
        },
        "sexy": {
            "items": [
                "a form-fitting plunging floor-length burgundy satin slip dress with delicate spaghetti straps and cowl neckline",
                "a skin-tight black ribbed knit bodycon dress with an alluring sweetheart neckline accentuating her waist",
                "a structured dark espresso lambskin leather bustier top paired with a form-fitting high-slit maxi skirt",
                "an emerald green velvet mini dress with an asymmetrical off-the-shoulder drape and ruched waist",
                "a backless obsidian black silk halter dress that plunges low down her spine",
                "a tailored charcoal double-breasted tuxedo dress with satin lapels worn without an undershirt",
                "a shimmering metallic pewter liquid-satin midi dress hugging every contour of her hourglass silhouette",
                "a crimson red bandage dress with provocative cut-outs along the ribcage and neckline",
                "a strapless midnight-blue velvet sheath dress with a daring thigh-high side slit",
                "a sculpted black latex midi dress with high neck collar and long sleeves accentuating every curve",
                "a plunging V-neck gold lamé cocktail dress with draped waist and open back",
                "a sheer panelled black bodycon dress with strategically placed geometric opaque velvet bands",
                "a deep-plum silk charmeuse gown with asymmetrical one-shoulder strap and high slit",
                "a tailored white tuxedo jumpsuit with deep plunging lapels and belted 24-inch waist",
                "a backless scarlet silk slip dress with criss-cross spaghetti straps cascading down her spine",
                "a chocolate-brown ruched mesh mini dress with off-the-shoulder sweetheart neckline",
                "a sculpted dark-teal leather pencil dress with exposed industrial metal back zipper",
                "a plunging champagne silk wrap dress with self-tie sash accentuating her narrow waist",
                "a shimmering bronze liquid-metallic mini dress with halter neck and low back",
                "a skin-tight charcoal cashmere turtleneck sweater dress with dramatic thigh slit",
                "a vintage black lace cocktail dress with sheer illusion neckline and low back",
                "a deep ruby velvet slip dress with French lace trim along the plunging décolletage",
                "a tailored leather blazer dress belted tightly at the waist with satin lapels",
                "a midnight-black strapless corset gown with structured boning and sheer tulle skirt slit",
                "a sultry sapphire silk bias-cut gown that drapes fluidly over her 38-inch hips"
            ],
            "bottoms_acc": [
                "strappy black patent leather stiletto sandals and layered delicate gold necklaces along her collarbone",
                "pointed-toe black suede ankle booties with subtle silver hardware and minimalist silver cuff bracelets",
                "classic Christian Louboutin red-bottom stiletto pumps and sparkling diamond stud earrings",
                "knee-high tailored nappa leather boots and a wide black leather waist belt with gunmetal buckle",
                "metallic gold ankle-strap stiletto heels and a vintage gold chain choker",
                "pointed-toe patent leather slingbacks and a diamond tennis bracelet on her left wrist",
                "strappy metallic silver dagger heels and chandelier crystal drop earrings",
                "over-the-knee black suede stiletto boots hugging her 30-inch thighs",
                "classic black satin court pumps and a thin velvet choker with diamond pendant",
                "minimalist nude leather stiletto sandals and stacked gold rings on her fingers",
                "pointed-toe dark burgundy velvet pumps and delicate gold hoop earrings",
                "glossy black patent ankle boots with 4-inch heels and a sleek leather clutch",
                "strappy pewter stiletto heels and a structured geometric metallic cuff",
                "Christian Louboutin So Kate 120mm patent pumps and diamond ear climbers",
                "knee-high dark espresso leather boots and a wide crocodile-embossed waist belt",
                "delicate black satin lace-up heels and a layered pearl strand necklace",
                "metallic bronze stiletto mules and minimalist gold drop earrings",
                "pointed-toe black leather d\'Orsay pumps and a Cartier-style gold bangle",
                "strappy scarlet satin stiletto heels and a sparkling ruby pendant necklace",
                "high-gloss patent leather Mary Jane stilettos and diamond stud earrings",
                "thigh-high stretch leather boots with stiletto heels and a silver collar",
                "classic pointed-toe nude patent pumps and a delicate platinum tennis necklace",
                "strappy emerald green satin heels with crystal buckle accents",
                "pointed black suede pumps with gold metal heel caps and gold hoop earrings",
                "metallic rose-gold stiletto sandals and a fine gold body chain"
            ]
        },
        "glamorous": {
            "items": [
                "an haute couture midnight-blue velvet backless evening gown with a sweeping train and crystal-embellished straps",
                "a dramatic champagne-gold liquid lamé floor-length gown with sculpted architectural shoulder pads and plunging neckline",
                "an opulent emerald silk taffeta ballgown with corseted bodice that cinches her 24-inch waist into an exaggerated hourglass",
                "a dramatic black tulle and organza haute couture tiered gown with sheer bodice and delicate beadwork",
                "a vintage crimson satin Hollywood glamour gown with draped cowl back and diamond brooch at the hip",
                "a bespoke pearl-white silk crepe evening gown with thigh-high slit and cascading capelet sleeves",
                "a shimmering obsidian sequin floor-length mermaid gown that flares dramatically past the knees",
                "a royal sapphire velvet column gown with off-the-shoulder portrait collar and long fitted sleeves",
                "a dramatic gold brocade gown with structured architectural hips and plunging sweetheart neckline",
                "an ethereal silver pleated lamé gown with halter neckline and low open back",
                "a couture dark-plum duchess satin ballgown with built-in corset and dramatic draped overskirt",
                "a vintage black velvet siren gown with white silk satin opera lapels and long train",
                "a shimmering rose-gold sequined column dress with deep V-neckline and open back",
                "a bespoke ivory silk faille evening gown with sculpted peplum waist and crystal trim",
                "an opulent ruby-red silk chiffon gown with dramatic billowing cape sleeves",
                "a couture black lace and sheer illusion evening gown with hand-stitched jet bead embroidery",
                "a metallic platinum silk satin slip gown with dramatic cowl neck and crystal straps",
                "a structured dark emerald velvet evening coat worn over a matching corseted satin gown",
                "a bespoke charcoal metallic jacquard gown with architectural neckline and thigh slit",
                "a dramatic vintage Schiaparelli-inspired black velvet gown with sculpted gold breastplate accent",
                "an opulent peacock-blue silk charmeuse gown with asymmetric draped shoulder and long sash",
                "a couture sheer tulle ballgown with embroidered gold celestial constellations and velvet corset",
                "a classic black silk mikado strapless evening gown with dramatic origami folded bodice",
                "a shimmering champagne crystal-embellished sheath gown with delicate spaghetti straps",
                "a bespoke dark crimson velvet mermaid gown hugging her 38-inch hips with sweeping velvet train"
            ],
            "bottoms_acc": [
                "custom satin evening stiletto pumps, glittering diamond chandelier earrings, and matching tennis bracelet",
                "vintage art deco diamond choker necklace and satin opera gloves extending past the elbows",
                "strappy metallic platinum stiletto heels and delicate diamond drop earrings",
                "Christian Louboutin satin evening pumps with crystal brooches and diamond stud earrings",
                "metallic gold strappy stiletto sandals and a multi-strand natural pearl choker",
                "pointed-toe black silk pumps with crystal buckle accents and vintage diamond bracelet",
                "strappy silver glitter stilettos and cascading crystal fringe earrings",
                "velvet opera gloves extending to the upper arm and diamond cluster earrings",
                "custom emerald and diamond pendant necklace with matching satin stiletto heels",
                "metallic bronze high-heel evening sandals and a vintage gold mesh evening minaudière",
                "pointed-toe ivory silk pumps and a delicate diamond tiara-style headband",
                "strappy black patent Louboutin stilettos and an art deco platinum brooch",
                "custom midnight-blue satin evening pumps and sapphire drop earrings",
                "metallic rose-gold stiletto sandals and stacked diamond bangles",
                "pointed ruby-satin court shoes and a vintage Van Cleef-style necklace",
                "strappy crystal-encrusted evening sandals and diamond ear cuffs",
                "classic black suede evening pumps and a diamond riviere necklace",
                "metallic champagne stiletto heels and a vintage Bulgari-style serpent bracelet",
                "custom silk velvet pumps with crystal heels and pearl drop earrings",
                "strappy platinum evening sandals and an antique diamond collar necklace",
                "pointed-toe gold lamé pumps and an opulent crystal statement necklace",
                "black satin opera gloves with diamond rings worn over the fabric and stiletto pumps",
                "strappy dark-emerald evening sandals and diamond tennis bracelet",
                "pointed-toe silver metallic pumps and vintage chandelier earrings",
                "Christian Louboutin strass-crystal pumps and flawless diamond studs"
            ]
        },
        "business": {
            "items": [
                "a tailored charcoal Italian wool blazer draped over a sultry black silk lace camisole paired with matching high-waisted trousers",
                "a bespoke pinstripe double-breasted tuxedo jacket with sharp structured shoulders and satin peak lapels",
                "a crisp tailored white French cotton button-down shirt tucked into a high-waisted black wool pencil skirt",
                "a structured matte black nappa leather blazer paired with tailored cigarette trousers",
                "a tailored navy-blue wool trench coat belted tightly at her 24-inch waist over a black turtleneck",
                "a bespoke houndstooth wool blazer with velvet collar paired with dark tailored trousers",
                "a low-draped black crepe tuxedo suit with silk satin lapels worn with an open neckline",
                "a crisp tailored sky-blue cotton dress shirt with French cuffs and silk knot cufflinks",
                "a structured camel cashmere blazer paired with high-waisted wide-leg cream wool trousers",
                "a tailored dark emerald wool pantsuit with sharp peaked lapels and slim cigarette pants",
                "a black double-breasted wool vest worn over a sheer black silk chiffon button-up blouse",
                "a bespoke charcoal chalk-stripe wool three-piece suit with tailored waistcoat",
                "a structured burgundy leather blazer paired with a high-waisted black leather pencil skirt",
                "a tailored cream silk crepe blouse with pussy-bow collar tucked into high-waisted navy trousers",
                "a structured charcoal Italian wool trench dress belted with a wide leather waist belt",
                "a bespoke black wool tuxedo jacket paired with sheer black lace camisole and cigarette pants",
                "a tailored slate-grey double-breasted wool coat over a fine-gauge black cashmere sweater",
                "a crisp white poplin shirt with dramatic oversized cuffs tucked into high-waisted pleated trousers",
                "a structured dark-espresso wool blazer paired with tailored ankle-length trousers",
                "a bespoke midnight-navy pinstripe pencil dress with structured shoulder pads and square neckline",
                "a tailored black velvet dinner jacket with satin shawl lapels and silk trousers",
                "a crisp tailored black silk button-down shirt with mother-of-pearl buttons and wool trousers",
                "a structured olive-drab wool military-inspired blazer with brass crest buttons",
                "a tailored cream wool double-breasted pantsuit with wide-leg flowing trousers",
                "a bespoke black wool smoking jacket with grosgrain lapels and matching slim trousers"
            ],
            "bottoms_acc": [
                "pointed-toe black leather pumps with a classic Cartier-style leather strap watch",
                "matte leather oxford heels with minimalist silver cuff bracelets and a tailored leather briefcase",
                "tailored stiletto ankle boots and delicate gold hoop earrings",
                "classic Christian Louboutin black leather court pumps and a gold Signet ring",
                "pointed-toe dark burgundy leather pumps and a structured leather laptop portfolio",
                "minimalist black leather slingback heels and a sleek gold wrist cuff",
                "tailored black nappa leather stiletto boots and a fine gold pendant necklace",
                "pointed-toe dark brown leather pumps and a vintage Cartier Tank watch",
                "matte black leather monk-strap heels and minimalist geometric earrings",
                "pointed-toe patent leather stiletto pumps and a slim gold collar necklace",
                "tailored navy leather pumps and a structured top-handle leather handbag",
                "classic black suede stiletto pumps and delicate diamond stud earrings",
                "pointed-toe dark green leather pumps and an antique gold wristwatch",
                "minimalist black leather mules with 3.5-inch heels and a structured leather envelope clutch",
                "tailored black patent leather loafers with low block heels and gold horsebit hardware",
                "pointed-toe cream leather pumps and a delicate gold tennis bracelet",
                "dark charcoal leather stiletto ankle booties and minimalist silver huggie earrings",
                "classic nude leather court pumps and a fine platinum chain watch",
                "pointed-toe black suede D\'Orsay pumps and a wide leather waist belt",
                "tailored burgundy leather ankle boots with block heels and gold hoop earrings",
                "pointed black patent leather slingbacks and a minimalist leather attache case",
                "matte black leather oxfords with high-shine polish and gold cuff links",
                "tailored dark espresso leather pumps and a fine gold chain necklace",
                "pointed-toe black leather court shoes with red soles and diamond studs",
                "minimalist black leather stiletto sandals and a structured leather tote"
            ]
        },
        "casual": {
            "items": [
                "an oversized charcoal cashmere sweater falling off one bare shoulder over a simple black rib knit tank",
                "a distressed vintage black motorcycle leather jacket worn over a form-fitting dark charcoal crewneck tee",
                "an unbuttoned oversized flannel shirt over a cropped black cotton cami",
                "a form-fitting ribbed black long-sleeve crop top paired with high-waisted vintage selvedge denim jeans",
                "a vintage graphic rock band tee knotted at her 24-inch waist with rolled short sleeves",
                "a cozy cream chunky cable-knit sweater with relaxed neckline over dark skinny jeans",
                "a distressed denim trucker jacket worn over a form-fitting white ribbed tank top",
                "an off-the-shoulder olive-green thermal knit sweater with relaxed slouchy fit",
                "a tailored black leather bomber jacket over a low-cut grey heather scoop-neck tee",
                "a vintage oversized boyfriend blazer worn over a plain white crop top and denim shorts",
                "a soft burgundy modal wrap top tied around her waist with deep V-neckline",
                "a fitted black turtleneck sweater tucked into vintage high-waisted light-wash jeans",
                "an unbuttoned faded chambray work shirt over a black lace-trimmed camisole",
                "a slouchy distressed grey cashmere hoodie with front zipper partially down",
                "a form-fitting dark espresso henley top with open pearl buttons along the neckline",
                "a vintage oversized leather aviator jacket with shearling collar over a simple tank",
                "a relaxed-fit navy blue Breton striped long-sleeve boatneck top",
                "a cropped black denim jacket with raw hem over a form-fitting charcoal tank",
                "a soft blush-pink oversized knit cardigan slipping off her shoulders over a silk cami",
                "a vintage washed-black leather moto vest worn over a tight white crewneck tee",
                "a distressed oversized vintage college sweatshirt worn as a tunic with rolled sleeves",
                "a form-fitting ribbed olive-green long-sleeve bodysuit with scoop neckline",
                "a relaxed plaid overshirt in dark tones over a black ribbed halter top",
                "a slouchy oatmeal-colored cashmere V-neck sweater with deep relaxed drape",
                "a fitted black leather moto jacket with silver asymmetrical zipper over a grey tank"
            ],
            "bottoms_acc": [
                "dark wash vintage high-waisted skinny jeans with distressing and black leather combat boots",
                "fitted black lambskin leather leggings and classic low-top canvas sneakers",
                "distressed denim cutoff shorts accentuating her 30-inch thighs and Doc Martens 8-eye boots",
                "high-waisted light-wash vintage Levi\'s 501 jeans and pointed black leather ankle boots",
                "black high-rise skinny jeans with raw frayed hem and black leather Chelsea boots",
                "distressed dark grey denim shorts with raw hem and classic white leather sneakers",
                "fitted dark indigo selvedge jeans with rolled cuffs and vintage leather workboots",
                "high-waisted black mom jeans with leather belt and chunky platform loafers",
                "distressed black denim cutoff shorts and knee-high leather combat boots",
                "relaxed-fit boyfriend jeans with knee tears and pointed-toe leather mules",
                "black stretch leather pants and classic low-profile athletic sneakers",
                "high-waisted vintage washed-grey denim jeans with ankle-strap stiletto sandals",
                "dark wash denim mini skirt with front button placket and leather ankle booties",
                "fitted black rib-knit leggings with white athletic socks and running shoes",
                "high-rise distressed light-wash jeans and pointed black suede ankle boots",
                "vintage blue denim cutoffs with raw hems and slip-on canvas sneakers",
                "black leather biker shorts hugging her thighs with chunky platform sneakers",
                "relaxed dark-wash wide-leg jeans with raw hem and leather platform boots",
                "high-waisted black coated denim jeans with sheen and pointed stiletto booties",
                "distressed light-blue denim mini skirt and classic Chuck Taylor high-top sneakers",
                "fitted charcoal denim jeans with subtle distressing and black moto boots",
                "vintage washed-black denim shorts with belt loops and Doc Martens 1461 shoes",
                "high-rise flared dark denim jeans and platform wooden clogs",
                "black cotton athletic shorts with white trim and casual low-top sneakers",
                "distressed raw-hem denim cutoffs and lace-up leather combat boots"
            ]
        }
    }

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
    CATEGORY = "Vespera/ZIT"

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
            chosen_key = rng.choice(list(self.WARDROBE_DATA.keys()))
        else:
            chosen_key = tier_key_map.get(wardrobe_level, "lingerie")

        tier_data = self.WARDROBE_DATA.get(chosen_key, self.WARDROBE_DATA["lingerie"])
        main_item = rng.choice(tier_data["items"])
        
        acc_text = ""
        if include_accessories_footwear and tier_data.get("bottoms_acc"):
            acc_text = rng.choice(tier_data["bottoms_acc"])

        physics_map = {
            "Wet & Translucent Micro-Sheer Physics": "translucent wet sheer fabric tension with ray-traced subsurface biological skin sheen underneath",
            "High-Gloss Liquid Latex & Polished Leather": "high-gloss liquid latex and nappa leather with crisp ray-traced specular edge reflections",
            "Heavy Silk, Velvet & Fluid Fabric Drapery": "heavy silk satin and velvet drapery with authentic fluid micro-creasing and soft specular sheen",
            "Brushed Wool & Cashmere Tactile Knit": "ultra-fine brushed cashmere knit fibers and textured wool weave with authentic micro-tactile surface",
            "Natural Ambient Lighting & Raytracing": "authentic fabric texture catching directional scene lighting and soft shadow falloff"
        }
        physics_str = physics_map.get(fabric_physics_detail, physics_map["Natural Ambient Lighting & Raytracing"])

        parts = [f"Wearing {main_item}"] if not main_item.startswith("Wearing") and not main_item.startswith("completely nude") and not main_item.startswith("fully nude") else [main_item]
        if acc_text:
            parts.append(f"paired with {acc_text}")
        if physics_str and chosen_key != "nudity":
            parts.append(f"featuring {physics_str}")

        clothing_prompt = ", ".join(parts)
        clothing_prompt = re.sub(r',\\s*,+', ',', clothing_prompt).strip(' ,')

        fused_prompt = clothing_prompt
        if optional_base_prompt and optional_base_prompt.strip():
            base_clean = optional_base_prompt.strip()
            if not base_clean.endswith('.'):
                base_clean += '.'
            fused_prompt = f"{base_clean} {clothing_prompt}."

        return (clothing_prompt, fused_prompt, chosen_key.upper())


# ============================================================================
# MASTER PROMPT WORKSTATION NODE (25+ EXPANDED PROCEDURAL MATRICES)
# ============================================================================
class ZITMasterPromptWorkstation:
    """
    All-in-One Master Director & Prompt Workstation Node for ComfyUI.
    Brings the complete, infinite stochastic prompt generator engine directly into the canvas with decoupled
    Character and Scene channels, director camera rigs, 9-tier wardrobe engine, skin physics, and pose matrix.
    """
    RATING_MODES = [
        "🔥 NSFW Explicit & Boudoir",
        "🍷 SFW Editorial & Haute Couture",
        "🎲 Stochastic Coin-Flip (Random NSFW / SFW)"
    ]
    
    SUBJECT_MODES = [
        "👑 Vespera (Photographic Baseline)",
        "👑 Vespera (35mm Raw Cinema)",
        "👑 Vespera (Editorial Still)",
        "🎲 Dynamic Random Subject Anchor",
        "✍️ Custom Subject (Input Port)"
    ]

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

    POSE_MODES = [
        "🎲 Dynamic Random Pose",
        "Seductive Kneeling with Arched Back",
        "Sensual Reclining with Parted Legs",
        "Dominant 3/4 Standing Silhouette",
        "Poised Seated Posture with Crossed Legs",
        "POV Intimate Perspective Lying Back",
        "Looking Back Over Bare Shoulder",
        "All Fours with Arched Spine & Direct Gaze"
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
        "🎲 Dynamic / Random Rig",
        "Denis Villeneuve (Alexa 65 Anamorphic 50mm)",
        "Roger Deakins (Arri LF 32mm Tungsten)",
        "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)",
        "David Fincher (Red 8K Leica 27mm Monochromatic)",
        "Helmut Newton (Hasselblad 80mm B&W High-Fashion)",
        "Ridley Scott (Panavision 50mm f/1.4 Anamorphic)",
        "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)",
        "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)",
        "Quentin Tarantino (Ultra Speed 40mm Punchy)",
        "Michael Mann (Sony CineAlta 28mm Blue Ambient)"
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
        "🏷️ Weighted Tags (SDXL)"
    ]

    # 25+ PROCEDURAL DYNAMIC HAIR STATES (BEDHEAD, WET, TOUSLED, UPDO, WINDSWEPT)
    HAIR_STATES = [
        "voluminous bedhead with messy, untamed 3B/3C spiral curls in jet-black with electric indigo highlights tumbling loosely over one eye and bare shoulders",
        "damp, glistening post-shower ringlet curls clinging to her neck and collarbone with subtle wet shine and deep indigo undertones",
        "a messy high bun with loose, curly tendrils and electric-indigo strands framing her sculpted jawline and temples",
        "tousled, pillow-disheveled ringlet curls cascading wildly across her back and bare chest in effortless morning disarray",
        "wind-swept dynamic curls caught in mid-motion with flying electric-indigo strands catching volumetric light",
        "intimately side-swept over one shoulder, exposing her bare neck, collarbone, and delicate earlobe",
        "slightly frizzy, humid bedhead curls with wild natural volume and vibrant indigo highlights cascading down her back",
        "a loose, low messy ponytail tied with a black silk ribbon, with springy curly ringlets escaping around her ears",
        "damp, towel-dried spiral curls with natural dewy texture and deep indigo sheen catching directional lighting",
        "a sleek half-up, half-down hairstyle with cascading voluminous curls spilling down her spine without bangs",
        "tangled morning curls loosely spilling across the pillow and framing her sleepy, flushed cheekbones",
        "wild, untamed voluminous curls with natural springy bounce framing her sculpted Levantine bone structure",
        "loose romantic curls pinned up casually with a tortoiseshell clip, with soft curly tendrils falling around her neck",
        "casually pushed back with her fingers, creating natural height at the crown and loose side waves falling over her shoulders",
        "sensually disheveled hair, with curly indigo strands lightly sticking to her flushed, dewy skin after an intimate moment",
        "side-parted voluminous curls spilling heavily over her left shoulder and framing her soft-smudged smoky eyeliner",
        "damp ringlets with wet-look sheen reflecting ambient candlelight with indigo highlights and authentic moisture",
        "a relaxed, unstyled natural curly crown of 3B/3C ringlets cascading uniformly to mid-back with no bangs",
        "loose bohemian styled curls with curly indigo ringlets tumbling freely down her back and collarbone",
        "tousled morning bedhead with curly locks loosely framing her defined soft black lips and signature beauty mark",
        "dynamic flowing curls with natural motion blur on the tips, catching cool-blue rim lighting",
        "hair pinned back on one side with an antique gilded hairpin, exposing her chiseled jawline and bare shoulder",
        "partially tucked behind her left ear, revealing her almond hazel-green eye and small gold hoop earring",
        "messy post-workout curls with slight dampness at the hairline and bouncy, energetic volume",
        "lush, springy spiral ringlets in full natural bounce with electric indigo highlights catching specular highlights"
    ]

    DIRECTOR_RIG_CONFIGS = {
        "Denis Villeneuve (Alexa 65 Anamorphic 50mm)": {
            "director": "cinematography inspired by Denis Villeneuve and Greig Fraser",
            "camera": "shot on Arri Alexa 65 Large Format with Ultra Vista Anamorphic 50mm lens at f/2.0, signature oval bokeh, horizontal streak flare, vast spatial compression",
            "lighting": "soft diffused volumetric light shafts, neutral rim lighting, balanced ambient illumination",
            "lut": "pristine cinematic 65mm master grade with neutral shadow density, high dynamic range, and clean color separation"
        },
        "Roger Deakins (Arri LF 32mm Tungsten)": {
            "director": "cinematography in the masterclass style of Roger Deakins",
            "camera": "shot on Arri Alexa Mini LF with Zeiss Master Prime 32mm lens at f/1.8, razor-sharp subject isolation, natural human eye perspective, subtle micro-contrast",
            "lighting": "single high-contrast warm tungsten key light from window side, soft ambient bounce fill, realistic shadow falloff",
            "lut": "organic film-print emulation LUT with authentic Kodachrome color response, deep neutral blacks, and natural luminous skin highlights"
        },
        "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)": {
            "director": "cinematography in the legendary style of Wong Kar-wai and Christopher Doyle",
            "camera": "shot on 35mm Arriflex 535 with vintage Cooke Speed Panchro 40mm lens at f/1.4, distinctive warm lens flare, creamy edge falloff, tactile halation",
            "lighting": "moody neon practicals, vibrant emerald green and amber street reflections, dramatic color bleed, atmospheric haze",
            "lut": "In the Mood for Love vintage celluloid color grade, lush saturated reds, deep atmospheric cyan shadows, high-temperature tungsten warmth"
        },
        "David Fincher (Red 8K Leica 27mm Monochromatic)": {
            "director": "cinematography in the meticulous clinical style of David Fincher and Jeff Cronenweth",
            "camera": "shot on Red V-Raptor XL 8K VV with Leica Summilux-C 27mm lens at f/2.2, hyper-precise edge-to-edge optical resolution, zero chromatic aberration",
            "lighting": "surgical low-key side lighting with precise softbox grids, cool cyan edge light, strict tonal separation",
            "lut": "cold desaturated corporate thriller color grade with signature green-yellow tint in midtones and deep pitch-black shadows"
        },
        "Helmut Newton (Hasselblad 80mm B&W High-Fashion)": {
            "director": "high-fashion erotic editorial photography in the iconic style of Helmut Newton and Guy Bourdin",
            "camera": "shot on medium-format Hasselblad 503CW with Carl Zeiss Planar 80mm f/2.8 lens on Ilford Pan F Plus 50 black-and-white film stock",
            "lighting": "hard directional direct flash with crisp defined drop shadows, high-contrast specular sheen on skin and leather, theatrical rim lighting",
            "lut": "timeless black and white high-contrast silver gelatin print grade with deep ink blacks, radiant metallic speculars, and sculpted tonal midtones"
        },
        "Ridley Scott (Panavision 50mm f/1.4 Anamorphic)": {
            "director": "cinematography in the legendary style of Ridley Scott and Jordan Cronenweth",
            "camera": "shot on 35mm Panavision Panaflex with C-Series 50mm Anamorphic lens at f/1.4, distinct cyan-blue horizontal streak flare and cylindrical optical falloff",
            "lighting": "high-contrast neon noir split lighting with moving Venetian blind beam projections and dense atmospheric smoke haze",
            "lut": "Technicolor neo-noir LUT with deep cyan shadow fill, glowing magenta accents, and glowing amber tungsten highlights"
        },
        "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)": {
            "director": "cinematography in the masterclass style of Gordon Willis",
            "camera": "shot on 35mm Mitchell BNC camera with vintage Baltar 50mm lens at f/2.0 on Kodak 5247 motion picture stock",
            "lighting": "legendary masterclass underexposure with top-lit amber overhead lights, keeping eyes in dramatic soft shadow sockets",
            "lut": "warm sepia-tinted golden amber master grade with deep velvety underexposed shadows"
        },
        "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)": {
            "director": "cinematography in the legendary style of Stanley Kubrick and John Alcott",
            "camera": "shot on modified 35mm Mitchell BNC camera with ultra-rare NASA Carl Zeiss Planar 50mm f/0.7 lens wide open",
            "lighting": "illuminated purely by natural beeswax candlelight, multi-tiered candelabras casting soft golden glow with authentic amber falloff",
            "lut": "authentic Barry Lyndon historical film grade with rich velvet hues, golden candlelight warmth, and deep atmospheric shadows"
        },
        "Quentin Tarantino (Ultra Speed 40mm Punchy)": {
            "director": "cinematography in the kinetic visual style of Quentin Tarantino and Robert Richardson",
            "camera": "shot on 35mm Panavision Millennium XL2 with Primo Anamorphic 40mm lens at f/2.0 on Kodak Vision3 500T 5219 stock",
            "lighting": "dramatic directional top-down spotlights, intense rim lighting on hair and shoulders, warm cinematic practicals",
            "lut": "vibrant saturated celluloid film print grade with punchy contrast, warm golden skin tones, and rich primary colors"
        },
        "Michael Mann (Sony CineAlta 28mm Blue Ambient)": {
            "director": "cinematography in the hyper-modern nocturnal style of Michael Mann and Dion Beebe",
            "camera": "shot on Sony CineAlta F950 digital cinema camera with Zeiss DigiPrime 28mm lens at f/1.6, distinct low-light texture and crisp night-city clarity",
            "lighting": "pure available ambient night light, cool sodium-vapor orange and mercury-vapor blue street reflections, wet asphalt glow",
            "lut": "Miami Vice nocturnal color grade with intense cobalt blue shadow tones, shimmering amber highlights, and realistic night ambiance"
        }
    }

    VESPERA_VARIATIONS = [
        'A hyper-realistic photographic capture of a 5\\\'5" French woman named Vespera with prominent Levantine Levantine facial features and Mediterranean heritage. Pronounced hourglass figure, narrow 24-inch waist, 38-inch hips, thick muscular 30-inch thighs, natural C-cup bust. Regal facial bone structure with high sculpted cheekbones, elegant refined aquiline nose bridge, flawless luminous olive skin with radiant golden undertones, completely smooth clear forehead with no scars or piercings. Sharp black liquid soft-smudged smoky black kohl eyeliner, deep-set almond-shaped captivating hazel-green eyes with subtle amber-gold flecks. Full soft black satin-sheen lips with defined cupid\\\'s bow, perfect clean natural white teeth, and a tiny beauty mark near the left corner of her upper lip. Voluminous, springy 3B/3C spiral ringlet curls in deep jet-black with interwoven electric indigo highlights, uniform length cascading mid-back with no bangs framing her face and jawline, flawless unblemished arms',
        'A 35mm raw cinematic capture of Vespera, a 5\\\'5" French woman of prominent Levantine Levantine descent. Featuring an athletic hourglass silhouette with a 24" waist, 38" hips, and thick 30" muscular thighs. Sculpted high cheekbones, noble aquiline nose bridge, radiant golden-olive complexion, and a smooth porcelain forehead. Soft-smudged smoky black kohl eyeliner framing captivating almond hazel-green eyes with golden flecks. Defined soft black lips with perfect clean natural white teeth, and a tiny 1mm beauty mark beside her upper lip. Cascading jet-black 3B/3C spiral ringlets interwoven with electric indigo highlights falling to mid-back with no bangs',
        'An editorial raw photographic still of Vespera, a French woman with distinctive Levantine Levantine bone structure and Mediterranean glow. Defined hourglass proportions, 24-inch waist, 30-inch muscular thighs, and natural bust. Chiseled jawline, refined aquiline nose, flawless olive skin, and a clear forehead. Alluring deep-set hazel-green eyes with winged liquid eyeliner and full dark-sable arched brows. Satin soft black lips with defined cupid\\\'s bow, perfect clean natural white teeth, and signature beauty mark near lip corner. Voluminous jet-black springy spiral ringlets with vibrant electric indigo strands cascading down her shoulders and back without bangs'
    ]

    # 25+ PROCEDURAL BOUDOIR BEDDING FABRICS & COLORS
    BOUDOIR_SHEET_COLORS = [
        "obsidian black satin sheets with scattered silk pillows",
        "deep crimson silk velvet bedding with ornate gold embroidery",
        "crisp white French Egyptian cotton sheets loosely tangled",
        "champagne-gold silk satin bedding with delicate lace trim",
        "midnight sapphire velvet duvet with deep fluid folds",
        "vintage rose damask silk sheets catching soft ambient light",
        "rich dark espresso satin bedding with plush fur throw",
        "ruffled emerald silk sheets with dark velvet bolsters",
        "pearl-grey liquid satin sheets reflecting flickering candles",
        "deep plum silk charmeuse bedding with black lace edging",
        "heavy charcoal brushed-linen bedding with relaxed folds",
        "golden amber silk duvet with subtle metallic thread sheen",
        "rich burgundy Egyptian cotton sheets with satin piping",
        "dusty lavender velvet bedding with ruffled pillowcases",
        "matte black silk sheets with contrasting ivory stitching",
        "raw unbleached French flax linen sheets catching soft morning rays",
        "dark teal silk satin bedding with embroidered floral accents",
        "glistening pewter satin sheets with deep shadow crevices",
        "blush pink silk crepe bedding with scalloped lace border",
        "heavy midnight-blue velvet coverlet draped across the bed",
        "warm terracotta silk satin sheets with gold tasseled pillows",
        "pure ivory mulberry silk sheets with high specular luster",
        "antique gold jacquard woven bedding with regal crest motifs",
        "rich chocolate velvet duvet with tangled silk sheets",
        "smoky amethyst silk satin bedding with dark lace ruffles"
    ]

    # 25+ PROCEDURAL BOUDOIR ARCHITECTURES & LUXURY FURNITURE
    BOUDOIR_FURNITURE_VENUES = [
        "in an opulent Parisian master bedroom suite with a grand four-poster iron canopy bed and antique gilded nightstands",
        "in an intimate Marais boudoir reclining across a vintage velvet chaise lounge beside an ornate marble fireplace",
        "in a luxury Haussmann apartment bedroom with herringbone oak floors, floor-to-ceiling French windows, and antique candelabras",
        "in a private high-fashion boudoir with deep velvet drapery, ornate gilded full-length mirrors, and soft ambient mood lighting",
        "in an atmospheric vintage library suite with deep tufted leather armchairs, Persian rugs, and glowing amber lamps",
        "in an intimate candlelit bedroom suite with sheer billowy canopy curtains and flickering beeswax candles on wrought iron sconces",
        "in a lavish penthouse boudoir with floor-to-ceiling glass windows reflecting the rainy city skyline at 3 AM",
        "in an antique French rococo salon with gilded plaster moldings, crystal chandeliers, and a velvet daybed",
        "in a moody boutique hotel suite in Saint-Germain with dark floral wallpaper and polished bronze accents",
        "in a secluded attic loft with exposed dark timber beams, skylight showing midnight rain, and plush floor cushions",
        "in a private dressing room with mirrored vanity tables, velvet dressing screens, and warm Hollywood globe bulbs",
        "in an opulent neoclassical suite with marble columns, silk wall coverings, and a carved mahogany bedframe",
        "in an intimate alcove bedroom surrounded by floor-to-ceiling crimson velvet curtains and low floor cushions",
        "in a luxury Parisian pied-à-terre with herringbone parquet floors, minimalist designer furniture, and brass sconces",
        "in an atmospheric gothic revival bedroom with arched stone window frames and flickering multi-arm candelabras",
        "in a grand master suite with an oversized velvet tufted headboard and vintage crystal decanters on side tables",
        "in an art deco inspired boudoir with geometric brass screens, sunburst mirrors, and dark walnut flooring",
        "in a private Parisian atelier apartment with scattered art canvases, vintage velvet couch, and tall casement windows",
        "in an intimate candlelit mezzanine bedroom overlooking a dramatic double-height living salon below",
        "in a luxury private suite with a free-standing gilded dressing mirror and scattered rose petals on oak flooring",
        "in an atmospheric midnight sanctuary with dark wainscoted walls, heavy tapestry drapes, and glowing table lamps",
        "in an elegant Belle Époque bedroom with curved architectural archways, ornate cornices, and plush velvet seating",
        "in a contemporary designer suite with dark charcoal walls, recessed LED ambient uplighting, and low platform bed",
        "in an exclusive private salon with low leather Chesterfield seating, vintage champagne buckets, and warm fireplace",
        "in a historic French chateau master bedchamber with towering stone fireplace and draped four-poster antique bed"
    ]

    # 25+ PROCEDURAL VENUES PER ENVIRONMENT THEME
    ENVIRONMENTS_MAP = {
        "Neutral Studio": [
            "neutral studio backdrop with seamless dark charcoal cyclorama wall and soft ground plane shadow",
            "high-end commercial fashion studio with neutral medium-grey background and clean optical edge separation",
            "minimalist studio setting with solid deep obsidian backdrop and zero background clutter",
            "pure white seamless studio infinity cyclorama with subtle softbox gradient illumination",
            "dark slate-grey textured plaster studio wall with soft directional key light falloff",
            "warm beige fine-grain studio paper backdrop with subtle natural shadow drop",
            "high-fashion black velvet light-absorbing backdrop providing extreme subject isolation",
            "concrete minimalist photo studio with smooth polished grey floor and clean perspective lines",
            "industrial photography loft with raw concrete back wall and muted diffused ambient fill",
            "studio setting with dark matte olive-grey seamless backdrop and precise rim lighting",
            "commercial beauty studio with curved white cyc wall and high-key edge contrast",
            "monochromatic dark navy studio backdrop with soft center spotlight vignette",
            "brushed aluminum studio partition wall catching soft directional rim highlights",
            "warm terracotta studio seamless paper backdrop with editorial high-fashion spacing",
            "deep espresso brown studio backdrop with subtle warm center gradient",
            "dark charcoal textured canvas backdrop hand-painted with subtle cloudy mottling",
            "clean ivory studio wall with single sharp razor-defined shadow cast across the floor",
            "minimalist architectural studio corner with clean 90-degree shadow junction",
            "matte black cyclorama with subtle cool-blue edge light separating subject from background",
            "raw industrial studio with pale grey brick wall painted in matte white wash",
            "high-contrast studio setup with pitch-black void surrounding the subject",
            "editorial fashion studio with smooth seamless warm-grey backdrop and clean optical spacing",
            "monochrome portrait studio with soft neutral gradient from dark graphite to soft ash",
            "minimalist daylight studio with sheer white diffusion scrim panels in background",
            "studio cyclorama wall illuminated with a tight circular snoot key spotlight"
        ],
        "Dark Parisian Boudoir": [
            "4ft3rd4rk, in a candlelit Parisian boudoir with deep crimson velvet drapery and flickering beeswax candles on ornate antique stands",
            "zavy-drkcnmtc, low-key lighting, inside an opulent private French boudoir with vintage mirrors and warm ambient shadows",
            "4ft3rd4rk, intimate Marais bedroom suite with antique gilded architecture, glowing fireplace, and luxurious drapery",
            "in an antique French rococo salon with gilded plaster moldings, crystal chandeliers, and a velvet daybed",
            "in a moody boutique hotel suite in Saint-Germain with dark floral wallpaper and polished bronze accents",
            "in a secluded attic loft with exposed dark timber beams, skylight showing midnight rain, and plush floor cushions",
            "in a private dressing room with mirrored vanity tables, velvet dressing screens, and warm Hollywood globe bulbs",
            "in an opulent neoclassical suite with marble columns, silk wall coverings, and a carved mahogany bedframe",
            "in an intimate alcove bedroom surrounded by floor-to-ceiling crimson velvet curtains and low floor cushions",
            "in a luxury Parisian pied-à-terre with herringbone parquet floors, minimalist designer furniture, and brass sconces",
            "in an atmospheric gothic revival bedroom with arched stone window frames and flickering multi-arm candelabras",
            "in a grand master suite with an oversized velvet tufted headboard and vintage crystal decanters on side tables",
            "in an art deco inspired boudoir with geometric brass screens, sunburst mirrors, and dark walnut flooring",
            "in a private Parisian atelier apartment with scattered art canvases, vintage velvet couch, and tall casement windows",
            "in an intimate candlelit mezzanine bedroom overlooking a dramatic double-height living salon below",
            "in a luxury private suite with a free-standing gilded dressing mirror and scattered rose petals on oak flooring",
            "in an atmospheric midnight sanctuary with dark wainscoted walls, heavy tapestry drapes, and glowing table lamps",
            "in an elegant Belle Époque bedroom with curved architectural archways, ornate cornices, and plush velvet seating",
            "in a contemporary designer suite with dark charcoal walls, recessed LED ambient uplighting, and low platform bed",
            "in an exclusive private salon with low leather Chesterfield seating, vintage champagne buckets, and warm fireplace",
            "in a historic French chateau master bedchamber with towering stone fireplace and draped four-poster antique bed",
            "in an opulent Haussmann master suite with floor-to-ceiling French windows opening to a private rainy balcony",
            "in a candlelit luxury suite with carved oak headboard, antique brass standing candelabras, and dark velvet bolsters",
            "in an intimate bohemian artist salon in Montparnasse with draped antique fabrics and warm glowing hearth",
            "in a private luxury penthouse boudoir with panoramic glass walls overlooking the glowing Eiffel Tower at 3 AM"
        ],
        "Parisian Noir": [
            "standing on the wet cobblestones of a Montmartre alleyway at 2 AM, glistening reflections under warm amber streetlamps and neon signs",
            "on the ornate Pont Alexandre III bridge overlooking the Seine river at blue hour with distant glowing Paris monuments",
            "under the wrought-iron arches of a secluded Parisian passage covered gallery with vintage shopfronts and wet stone reflections",
            "on an intimate wrought-iron balcony overlooking the rainy zinc rooftops of Paris and the distant Eiffel Tower silhouette",
            "outside an iconic Parisian cafe with wet red awnings, dark bistro chairs, and warm glowing interior lights at midnight",
            "in a secluded courtyard in Le Marais with ivy-covered stone walls, antique carriage lanterns, and glistening wet flagstones",
            "beside a vintage Metro entrance with Art Nouveau green ironwork glowing under streetlamp mist in the rain",
            "on the cobblestone quayside along the Seine River with riverboat lights casting long shimmering streaks on the dark water",
            "in the shadow of the Notre-Dame cathedral stone buttresses at 3 AM with atmospheric street mist and wet pavement",
            "along a dimly lit rue in Saint-Germain with vintage bookshops, polished brass door knockers, and glowing lampposts",
            "on a grand stone staircase leading up to Sacré-Cœur with panoramic nighttime city lights bokeh sprawling below",
            "under the stone arches of Place des Vosges with red brick arcades and rain-slicked colonnade reflections",
            "outside a vintage jazz club in the Latin Quarter with glowing neon sign and warm brass horn music ambiance",
            "on the Pont des Arts footbridge with distant golden bridge arches reflecting in the dark flowing river",
            "beside an antique French fountain in a quiet secluded square with water glistening under sodium vapor lights",
            "in a cobblestone cul-de-sac in Belleville with vintage street graffiti, industrial fire escapes, and moody neon glow",
            "underneath a dramatic iron viaduct in the 15th arrondissement with overhead metro trains and wet asphalt glow",
            "on an elegant stone terrace overlooking the Place Vendôme with illuminated luxury boutique windows in background",
            "in an atmospheric Parisian arcade with glass vaulted ceiling catching raindrops and antique globe pendant lights",
            "at the entrance of a discreet underground speakeasy behind a vintage velvet curtain in a dark Parisian alley",
            "along the tree-lined Boulevard Saint-Michel during an autumn rainstorm with fallen golden leaves on glistening pavement",
            "on a private rooftop terrace in the 8th arrondissement overlooking illuminated Parisian avenues stretching to the horizon",
            "outside an ornate Belle Époque theatre with illuminated marquee lights reflecting in rainy street puddles",
            "in a quiet courtyard of an 18th-century hôtel particulier with stone carriage gates and gaslight torches",
            "on a mist-shrouded Parisian bridge at 4 AM with solitary amber streetlights piercing the dense cool-blue river fog"
        ],
        "Cybernetic Sanctuary": [
            "inside a moody high-tech cybernetic sanctuary in Neo-Paris with holographic wireframe terminals, cool blue conduit backlighting, and dark brushed aluminum panels",
            "inside a private cybernetic research sanctum with glowing fiber-optic conduits, sleek carbon-fiber workstations, and ambient indigo rim lighting",
            "inside a futuristic server chamber with rows of glowing server racks, subtle floor mist, and volumetric neon reflections",
            "inside a neon-lit cyberpunk apartment overlooking sprawling mega-skyscrapers through floor-to-ceiling holographic glass",
            "inside an underground synthetic augmentation lab with robotic surgical arms, glowing coolant tubes, and dark titanium tables",
            "inside a neural link testing chamber with floating volumetric data visors, clean acrylic conduits, and pulse telemetry",
            "inside a high-tech cleanroom with monolithic dark server pillars, recessed UV sterilization strips, and glass flooring",
            "inside an industrial cybernetic workshop with disassembled synthetic android limbs, precision soldering tools, and blue laser tracers",
            "inside a private command deck with panoramic holographic tactical displays, curved carbon consoles, and moody blue backlights",
            "inside an encrypted dark-fiber data vault with illuminated liquid nitrogen lines and pulsating orange data nodes",
            "inside a futuristic penthouse cockpit with automated drone landing pads visible through rain-streaked smart glass",
            "inside a subterranean synth lab with containment cylinders, illuminated biosensors, and dark brushed steel architecture",
            "inside a high-frequency trading server nexus with floor-to-ceiling optical routing cables and strobing status LEDs",
            "inside a cyberpunk loft workshop with exposed ceiling wiring, neon sign repair benches, and holographic diagnostic screens",
            "inside an autonomous AI terminal room with spherical holographic projection arrays and dark obsidian cooling pools",
            "inside a futuristic cleanroom facility with airlock doorways, sterile white and cyan accent lighting, and robotic gantries",
            "inside a covert cybernetic safehouse with scrambled monitors, military-grade field terminals, and flickering emergency lights",
            "inside an orbital relay station monitoring room with Earth curvature visible through massive reinforced observation ports",
            "inside an underground fiber routing hub with cascading purple and cyan data waterfalls on transparent OLED walls",
            "inside a precision cybernetic fabrication bay with 3D carbon-printing nozzles and blue laser scanning grids",
            "inside a dark futuristic library where physical books are replaced by glowing optical crystal datacubes on dark shelves",
            "inside a neon-drenched cyber clinic in the lower levels of Neo-Paris with rain dripping through ventilation grates",
            "inside a private quantum processor cooling chamber with frost crystals forming on thick acrylic observation windows",
            "inside a high-tech surveillance nexus with multi-screen panoramic wall monitors tracking global satellite telemetry",
            "inside an abandoned cybernetic assembly line with dormant android chassis and flickering industrial sodium lights"
        ],
        "Opulent Penthouse Suite": [
            "zavy-drkcnmtc, low-key lighting, inside an opulent private penthouse suite overlooking the rainy Paris skyline at 3 AM through floor-to-ceiling glass windows",
            "inside a luxury modern duplex with polished dark marble floors, minimalist architectural lighting, and panoramic nighttime city vistas",
            "in an ultra-luxury suite with glowing recessed perimeter lighting, low leather lounge seating, and city lights bokeh",
            "on an exclusive private rooftop terrace with an infinity plunge pool reflecting the glowing night skyline and stars",
            "in a two-story grand living salon with a floating cantilevered glass staircase and towering double-height windows",
            "beside a sleek minimalist black marble fireplace with a roaring linear flame and low Italian designer sofa",
            "in a luxury penthouse dining room with a polished dark obsidian table, crystal glassware, and city night views",
            "in a private master bedroom suite with wraparound glass walls showing 360-degree views of glowing metropolis landmarks",
            "in an opulent penthouse bar lounge with illuminated back-lit onyx countertop and vintage liquor decanters",
            "on a luxury penthouse balcony with glass railings, outdoor gas firepit, and panoramic skyline rain reflections",
            "in a minimalist brutalist-luxury penthouse with raw board-formed concrete walls, dark hardwood, and custom artwork",
            "in a high-end designer duplex with custom brass architectural screens, rich walnut paneling, and warm ambient sconces",
            "beside a private indoor lap pool surrounded by dark basalt stone and floor-to-ceiling nighttime city views",
            "in an exclusive corner penthouse suite with dual-aspect glass walls framing illuminated bridges and urban sprawl",
            "in a luxury media salon with velvet acoustic walls, deep custom modular seating, and warm recessed linear lighting",
            "on a private penthouse sky garden terrace with lush exotic plants, subtle uplighting, and city lights beyond",
            "in an open-concept penthouse with polished concrete floors, museum-grade sculpture pedestals, and skyline views",
            "in a lavish master dressing salon with glass-front illuminated wardrobes, central marble island, and skyline backdrop",
            "in a private penthouse library with floor-to-ceiling dark bookshelves accessed by a minimalist rolling brass ladder",
            "in an ultra-modern luxury suite with smart tinted glass transitioning from opaque frost to clear panoramic night vistas",
            "beside a grand grand piano in a luxury penthouse salon with moonlight and city lights reflecting off the high-gloss lid",
            "in a private rooftop conservatory with glass atrium ceiling showing raindrops and distant lightning over the skyline",
            "in a luxury penthouse suite with dark wenge wood wall cladding, integrated LED cove lighting, and plush mohair rugs",
            "in an exclusive triplex penthouse with an open central atrium connecting three levels of panoramic luxury architecture",
            "on an illuminated penthouse terrace lounge with outdoor daybeds, gas torches, and a breathtaking 4 AM city panorama"
        ],
        "Steamy Private Marble Bath": [
            "4ft3rd4rk, in a steamy private marble bathroom with an oversized clawfoot tub, warm atmospheric mist, and amber tea lights",
            "inside an opulent hammam-inspired marble sanctuary with carved stone archways, warm rising steam, and soft hanging brass lanterns",
            "in a luxury master bath with freestanding black granite tub, floating candles, and wet reflective dark tiles",
            "in an antique Parisian bathroom with vintage brass fixtures, white Carrara marble wainscoting, and warm mist in the air",
            "in a private spa suite with a sunken cedar soaking tub, rising aromatic steam, and soft ambient bamboo sconces",
            "in an opulent Roman-inspired bathhouse with fluted marble columns, mosaic tile floors, and warm water reflections",
            "inside a modern minimalist wet room with dark slate waterfall shower, glass partitions, and rising warm vapor",
            "in a luxury penthouse bathroom with a freestanding oval tub placed directly against floor-to-ceiling rainy city windows",
            "in an intimate candlelit bathroom with dozens of flickering tea lights arranged along the rim of a deep soaking tub",
            "in a vintage European master bath with an ornate gilded dressing mirror, clawfoot tub, and soft steam halation",
            "inside an underground thermal bath chamber with natural stone walls, warm mineral pools, and soft water ripples",
            "in a luxury dark emerald marble bathroom with brushed brass hardware, freestanding tub, and warm ambient backlighting",
            "in a minimalist Japanese onsen-inspired private bath with smooth river stones, hinoki wood accents, and rising mist",
            "inside an expansive master spa bath with a double rain shower, glass benches, and moisture droplets condensing on mirrors",
            "in an opulent art deco bathroom with black and gold chevron mosaic tiles, deep porcelain tub, and soft sconce lighting",
            "in a private sanctuary bathroom with a marble vanity table, crystal perfume bottles, and steam softening the light",
            "inside a grotto-style luxury bath carved from natural travertine stone with hidden ambient uplights and warm pool",
            "in a freestanding copper soaking tub filled with warm water, surrounded by dark wood floors and flickering taper candles",
            "in an ultra-luxury bathroom with heated marble floors, oversized walk-in steam shower, and floating vanities",
            "in a vintage Parisian hotel bathroom with checkered black-and-white tile floors, clawfoot tub, and warm bath salts aroma",
            "beside an infinity-edge marble soaking tub overflowing gently onto dark river pebbles under soft warm spotlights",
            "in a luxury open-concept bedroom-bathroom suite where the freestanding tub overlooks an antique marble fireplace",
            "inside a private Turkish hammam with heated marble slab, carved marble basins, and geometric domed skylight steam",
            "in a dark moody bathroom with bookmatched Nero Marquina marble walls and glowing back-lit mirror illumination",
            "in a private luxury bath suite with rose petals floating in steaming water and soft candlelight reflecting on marble"
        ],
        "Editorial Studio": [
            "in a high-end minimalist editorial fashion studio with smooth seamless warm-grey backdrop and clean optical spacing",
            "in an avant-garde architectural photography studio with dramatic concrete columns, geometric light shafts, and minimalist styling",
            "in a high-contrast fashion studio with pure pitch-black seamless background and sculpted optical rim light",
            "in a Parisian haute couture atelier studio with towering mirrors, dressmaker mannequins, and tall arched windows",
            "in an industrial art gallery space with polished concrete floors, soaring ceilings, and museum-grade directional spotlights",
            "in an editorial studio set with architectural floating white blocks, geometric shadows, and clean negative space",
            "in a brutalist concrete photo studio with dramatic diagonal sunbeam projections from high clerestory windows",
            "in a minimalist fashion studio with a massive silk diffusion scrim casting perfectly even wrap-around daylight",
            "in a high-fashion editorial set with large textured dark canvas flats arranged in clean layered perspective",
            "in a modern sculpture gallery studio with minimalist stone plinths and sharp razor-edge shadow patterns",
            "in a luxury designer studio with curved plaster walls, seamless cove junctions, and warm architectural uplighting",
            "in an editorial set with polished black plexiglass flooring creating crisp mirror-like ground reflections",
            "in an avant-garde photography studio with a single high-power Fresnel spotlight casting dramatic defined silhouettes",
            "in a minimalist loft studio in Soho with cast-iron columns, exposed brick painted matte grey, and clean optical framing",
            "in a high-fashion studio with floating translucent acrylic panels creating layered soft-focus background depth",
            "in an editorial studio featuring a monumental brutalist staircase with sharp geometric concrete treads and shadows",
            "in a pristine monochromatic white-cube studio where light bounces softly with zero chromatic color cast",
            "in an editorial set with raw corrugated metal panels painted matte black providing industrial tactile texture",
            "in a minimalist photo studio with an oversized parabolic reflector key light sculpting every contour of the subject",
            "in an architectural studio set with cantilevered stone beams and dramatic low-angle perspective lines",
            "in a high-end fashion studio with dark slate textured backdrop and subtle cool-blue edge lighting separation",
            "in an avant-garde runway studio with polished reflective runway floor and dramatic rear-lit silhouette scrim",
            "in an editorial studio with tall floor-to-ceiling sheer linen scrims gently catching subtle cross-breeze movement",
            "in a contemporary museum exhibition hall with dark walls and focused narrow-beam ceiling spotlights",
            "in a high-fashion master studio with seamless neutral backdrop, calibrated Profoto strobe heads, and crisp optics"
        ]
    }

    # 25+ PROCEDURAL NSFW POSES (PURE ANATOMICAL WITH ZERO VENUE HARDCODING)
    POSES_POOL_NSFW = [
        "sleeper, kneeling with an arched back and seductive pose, maintaining provocative eye contact",
        "sleeper, reclining back gracefully with legs parted in an intimate sensual perspective",
        "seated upright in a dominant provocative posture with legs parted and confident stance",
        "lying on her side with one leg raised and hips angled, gazing intensely over her bare shoulder",
        "sleeper, pov intimate perspective, lying back with head tilted back and hands teasing her bare chest",
        "(seductive pose:1.2), seated gracefully with legs parted and wet glistening skin catching specular highlights",
        "leaning forward on all fours with arched spine and sultry gaze directed back toward the camera",
        "standing in a provocative full-body posture running fingers through her cascading jet-black curls, with one hand resting on her hip",
        "lying on her stomach with hips elevated and back deeply arched, looking back toward the viewer with parted lips",
        "standing in a three-quarter silhouette with back arched, hands resting on her 24-inch waist, and head turned back",
        "seated on her heels with spine erect, hands resting on her 30-inch thighs, and chest pushed forward proudly",
        "reclining on one elbow with torso twisted toward the camera and legs elegantly crossed at the calves",
        "candidly arching her back while stretching both arms overhead with fingers interlaced, accentuating her ribcage and waist",
        "sitting with one knee drawn up to her chest while the other leg extends, hands resting on her bare ankle",
        "leaning back against a flat surface with hips pushed forward and head tilted back in sensual ecstasy",
        "kneeling tall on both knees with hands running down the sides of her waist and flared 38-inch hips",
        "lying flat on her back with arms extended above her head and one knee bent, creating dynamic hip tilt",
        "standing tall with weight shifted to one hip, running both hands slowly through her electric-indigo curls",
        "seated cross-legged with forward lean, resting chin on her palm while gazing provocatively up into the camera",
        "lying on her side with legs loosely stacked, top hip pushed forward, and hand tracing her collarbone",
        "kneeling with one leg extended sideways, showing off the full curvature of her 30-inch muscular thigh",
        "standing with back turned toward camera, looking over her shoulder with an arched lower spine and hand on her hip",
        "reclining back with both hands braced behind her, chest lifted high, and eyes locked onto the viewer",
        "crouching low in a dynamic feline posture with weight on the balls of her feet and direct gaze",
        "lying diagonally with torso turned toward the lens, fingers teasing the edge of her attire, and parted soft black lips"
    ]

    # 25+ PROCEDURAL SFW POSES
    POSES_POOL_SFW = [
        "leaning forward with elbows resting on her knees in a relaxed, candid pose",
        "candidly leaning back with arms loosely crossed in a dominant confident posture",
        "standing in a three-quarter dynamic stance with hands resting on her 24-inch waist and flared hips",
        "reclining gracefully in a relaxed, sensual posture with legs extended",
        "seated cross-legged with poised posture and sculpted shoulders",
        "standing in a powerful three-quarter stance with weight shifted to one hip",
        "walking forward naturally with motion captured in mid-stride and hair gently swaying",
        "sitting poised on a low seat with ankles crossed and hands folded loosely in her lap",
        "leaning casually against a wall with one foot flat and arms relaxed at her sides",
        "standing tall with one hand in her pocket and head tilted in sharp analytical focus",
        "seated sideways with torso turned to camera and fingers lightly touching her jawline",
        "standing in profile with chin slightly lifted, highlighting her aquiline nose and chiseled jaw",
        "candidly adjusting her cuff or sleeve with eyes glancing downward in natural moment",
        "seated with legs extended forward and hands bracing lightly behind her on the floor",
        "standing with hands lightly clasped in front of her waist and an enigmatic half-smile",
        "leaning back against a railing or partition with arms resting along the top edge",
        "three-quarter portrait stance with one shoulder turned toward the camera and direct eye contact",
        "seated upright with arms resting gracefully on armrests and poised regal posture",
        "candidly turning around as if called by name, with dynamic hair movement and engaging gaze",
        "sitting relaxed with one arm draped over the back of a chair and legs casually crossed",
        "standing tall with shoulders back and chin level in an authoritative high-fashion stance",
        "seated with chin resting on the back of her hand and thoughtful, penetrating gaze",
        "standing poised in a classic contrapposto stance with natural body weight distribution",
        "leaning slightly forward into the lens with both hands resting lightly on her knees",
        "candid medium shot with head tilted slightly, running fingers through her indigo curls"
    ]

    # 25+ PROCEDURAL NSFW MICRO-EXPRESSIONS & GAZE
    EXPRESSIONS_POOL_NSFW = [
        "a seductive knowing smirk with parted soft black satin lips and intense pupil dilation",
        "an intensely provocative direct stare with heavy-lidded hazel-green eyes and flushed cheeks",
        "a breathless sensual expression with parted lips, clean natural white teeth, and raised sable brow",
        "an alluring dominant gaze looking down into the camera with a subtle sardonic half-smile",
        "a sultry half-lidded bedroom gaze with lips slightly parted and delicate cheek flush",
        "an intense commanding stare with dilated pupils and a dangerous predatory smirk",
        "a soft breathless gasp with parted soft black lips and captivating amber flecks catching the light",
        "a playful biting of her lower soft black lip with a teasing twinkle in her hazel-green eyes",
        "an enigmatic sidelong glance with raised eyebrow and an amused knowing half-smile",
        "a look of raw uninhibited desire with heavy-lidded eyes and flushed dewy skin",
        "a confident, dominant smirk with soft-smudged smoky eyeliner framing piercing direct eye contact",
        "a dreamy sensual daze with head tilted back, lips parted, and soft relaxed facial features",
        "an intense brooding gaze from beneath dark arched brows with subtle lip curl",
        "a teasing, mischievous half-smile revealing clean white teeth with captivating eye contact",
        "a haughty, commanding look of supreme confidence with relaxed soft black lips and sharp gaze",
        "a breathless, flushed expression with dilated hazel pupils and parted satin lips",
        "a sharp, calculating sensual stare that pierces directly through the camera lens",
        "a soft intimate expression with lowered eyelashes, followed by a slow upward glance",
        "an intoxicating mix of European elegance and pitch-black witty amusement in her eyes",
        "a lingering provocative gaze with lips slightly wet and tiny beauty mark highlighted",
        "a subtle sardonic grin playing at the corner of her lips with raised left brow",
        "an expression of breathless surrender with parted lips and head tilted sensually back",
        "an intense hypnotic stare with wide almond hazel-green eyes and defined cupid\'s bow",
        "a sultry, teasing smile with clean white teeth showing and eyes narrowed seductively",
        "a captivating look of intimate familiarity and unspoken understanding with the viewer"
    ]

    # 25+ PROCEDURAL SFW MICRO-EXPRESSIONS & GAZE
    EXPRESSIONS_POOL_SFW = [
        "a subtle knowing half-smirk playing at the corners of her soft black lips",
        "an intense, captivating direct eye contact with her almond hazel-green eyes",
        "a playful, sardonic half-smile with clean natural white teeth",
        "a calm, dominant analytical focus engaging the camera directly",
        "a poised, professional expression with sharp arched sable eyebrows",
        "an enigmatic, Mona-Lisa like subtle smile with intelligent hazel gaze",
        "a thoughtful contemplative gaze looking slightly off-camera with relaxed features",
        "a sharp, witty spark in her eyes paired with a confident micro-smirk",
        "a serene, composed facial expression with smooth porcelain forehead",
        "an engaging warm smile with natural eye crinkles and clean white teeth",
        "a piercing, intellectual direct gaze that commands attention and respect",
        "a subtle haughty tilt of the chin with an amused European expression",
        "a candid, unguarded smile captured in a genuine moment of humor",
        "an intense, chiseled editorial gaze with closed lips and razor jawline",
        "a relaxed confident expression with soft ambient shadow defining her cheekbones",
        "an observant, perceptive gaze with slightly raised right eyebrow",
        "a poised high-fashion stare with neutral soft black lips and sculpted bone structure",
        "a subtle playful smirk with an ironic glint in her amber-flecked eyes",
        "an authoritative commanding expression with steady, unblinking eye contact",
        "a soft natural smile that warms her golden-olive Mediterranean complexion",
        "a contemplative, artistic expression with relaxed jaw and focused eyes",
        "a sharp, sardonic Jeselnik-style smirk with soft-smudged smoky eyeliner framing",
        "a quiet confident gaze with subtle cheekbone flush and defined cupid\'s bow",
        "an intelligent, curious look with tilted head and keen hazel-green eyes",
        "a majestic, regal expression with calm poise and timeless Parisian allure"
    ]

    # 25+ PROCEDURAL NSFW MATERIAL & SKIN PHYSICS
    PHYSICS_POOL_NSFW = [
        "realskin, oiled skin with glistening specular highlights and micro-droplets of water catching directional lighting",
        "translucent sheer micro-lace tension revealing warm biological realskin texture and anatomical contours underneath",
        "realskin, subsurface dermal scattering with natural warmth and soft flush across bare shoulders and collarbone",
        "high-gloss liquid latex sheen with crisp ray-traced reflections of ambient scene lighting",
        "fine 35mm film grain, realskin natural pores with authentic specular sheen on bare skin",
        "dewy glistening skin oil across bare collarbones, breasts, and 30-inch muscular thighs",
        "realskin, authentic biological micro-textures, tiny goosebumps, and soft dermal blood flow warmth",
        "wet sheer silk fabric clinging translucent against wet skin with visible biological contours",
        "liquid patent leather reflections with high specular edge roll-off along body contours",
        "realskin, natural pore structure without plastic smoothing, fine skin texture with authentic specular highlights",
        "subtle perspiration sheen across collarbone, cleavage, and toned abdomen catching backlight",
        "tactile sheer fishnet mesh indenting softly into firm skin with realistic tissue physics",
        "glistening body oil highlights accentuating the 0.66 waist-to-hip curvature and rear silhouette",
        "realskin, warm natural skin tones with authentic golden undertones and subtle vascular realism",
        "tightly stretched sheer mesh fabric revealing realistic skin pores and warm flesh undertones underneath",
        "polished nappa leather with fine tactile grain catching crisp directional rim light",
        "delicate biological skin flush across cheekbones, chest, and shoulders with ray-traced subsurface scattering",
        "wet skin with tiny authentic water rivulets tracing down her collarbone and bare hips",
        "realskin, micro-pore fidelity with natural specular reflections on forehead, nose bridge, and soft black lips",
        "high-tension elastic straps pressing naturally into soft skin curves with realistic physics",
        "translucent wet chiffon clinging to wet bare body with realistic fabric tension and transparency",
        "realskin, smooth golden-olive dermal texture with realistic skin elasticity and natural highlights",
        "high-gloss vinyl sheen creating razor-sharp specular highlights along the waistline and hips",
        "soft velvety skin texture illuminated by warm flickering candlelight with deep shadow falloff",
        "realskin, raw unfiltered photographic dermal clarity with zero artificial post-processing smoothing"
    ]

    # 25+ PROCEDURAL SFW MATERIAL & TACTILE PHYSICS
    PHYSICS_POOL_SFW = [
        "heavyweight brushed nappa leather texture capturing crisp specular rim reflections along tailored seams",
        "realskin, high-fidelity subsurface scattering with soft biological skin warmth across collarbones and jawline",
        "subtle specular sheen on bare shoulders and collarbones with ultra-fine pore texture",
        "tactile natural fabrics with authentic micro-fiber weave and directional shadow depth",
        "ultra-fine brushed cashmere knit fibers and textured wool weave with authentic micro-tactile surface",
        "heavy silk satin and velvet drapery with authentic fluid micro-creasing and soft specular sheen",
        "crisp French cotton poplin with clean sharp ironed creases catching directional key light",
        "realskin, authentic dermal micro-details, natural pores, and healthy golden-olive skin luminosity",
        "distressed selvedge denim texture with visible indigo warp yarns and worn cross-hatch grain",
        "smooth lambskin leather with supple tactile creasing around elbows and waist seams",
        "fine 35mm analog film grain structure with authentic Kodak Vision3 halation around bright edges",
        "luxurious fluid silk charmeuse with high specular sheen flowing naturally over anatomical contours",
        "heavy Italian wool suiting with subtle twill texture and crisp structured shoulder pads",
        "realskin, soft natural cheekbone flush with realistic light diffusion and subsurface scatter",
        "fine organza transparency layered over structured opaque fabrics with realistic light refraction",
        "tactile ribbed cotton knit with distinct vertical ribbing and natural body stretch",
        "vintage weathered leather with subtle micro-scuffs and warm burnished patina highlights",
        "delicate French chantilly lace with intricate openwork threads casting patterned shadows onto skin",
        "realskin, natural pore fidelity, soft satin soft black lip sheen, and defined clean eyelashes",
        "liquid metallic lamé fabric with undulating liquid specular reflections and fluid drape",
        "heavy velvet fabric absorbing ambient light in deep folds while reflecting golden highlights on ridges",
        "crisp tailored linen weave with authentic organic slub texture and breathable drape",
        "realskin, smooth porcelain forehead and glowing golden undertones under balanced three-point lighting",
        "high-density technical nylon with water-resistant matte sheen and taped seam details",
        "authentic analog celluloid texture with rich optical depth, natural micro-contrast, and zero digital noise"
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
                "rating_mode": (cls.RATING_MODES, {"default": "🔥 NSFW Explicit & Boudoir"}),
                "cohesion_equalizer": (cls.COHESION_MODES, {"default": "🧠 Smart Context Equalizer (Matched Venue, Attire & Poses)"}),
                "character_anchor": (cls.SUBJECT_MODES, {"default": "👑 Vespera (Photographic Baseline)"}),
                "hair_state_mode": (cls.HAIR_MODES, {"default": "🎲 Dynamic Stochastic Hair (Bedhead, Wet, Tousled, Styled)"}),
                "wardrobe_level": (cls.WARDROBE_TIERS, {"default": "🎲 Full Stochastic (Random All)"}),
                "pose_action_mode": (cls.POSE_MODES, {"default": "🎲 Dynamic Random Pose"}),
                "material_skin_physics": (cls.PHYSICS_MODES, {"default": "🎲 Dynamic / Matched Physics"}),
                "scene_environment": (cls.SCENE_THEMES, {"default": "🎲 Dynamic Cinematics Matrix"}),
                "director_camera_rig": (cls.DIRECTOR_RIGS, {"default": "🎲 Dynamic / Random Rig"}),
                "prompt_engine_format": (cls.PROMPT_FORMATS, {"default": "🎬 Natural Cinematic Prose (Flux / ZIT)"}),
                "chaos_entropy": ("INT", {"default": 50, "min": 0, "max": 100, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": "randomize"}),
            },
            "optional": {
                "custom_character_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "custom_clothing_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "custom_scene_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "character_prompt",
        "scene_prompt",
        "master_fused_prompt",
        "negative_prompt",
        "active_wardrobe_text",
        "active_pose_text",
        "active_scene_text",
        "active_director_camera",
        "active_lighting_lut",
        "telemetry_summary"
    )
    FUNCTION = "synthesize_master_prompt"
    CATEGORY = "Vespera/ZIT"

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
        custom_character_override: str = "",
        custom_clothing_override: str = "",
        custom_scene_override: str = ""
    ):
        rng = random.Random(seed)
        if "Random" in rating_mode or "Stochastic" in rating_mode or "Coin-Flip" in rating_mode:
            is_nsfw = rng.choice([True, False])
        else:
            is_nsfw = "NSFW" in rating_mode

        # 1. RESOLVE WARDROBE TIER FIRST (TO ANCHOR SEMANTIC EQUALIZER)
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
                chosen_tier_name = rng.choice(list(ZITDynamicWardrobeEngine.WARDROBE_DATA.keys()))
            else:
                chosen_tier_name = tier_key_map.get(wardrobe_level, "lingerie" if is_nsfw else "sexy")

            tier_data = ZITDynamicWardrobeEngine.WARDROBE_DATA.get(chosen_tier_name, ZITDynamicWardrobeEngine.WARDROBE_DATA["lingerie"])
            main_item = rng.choice(tier_data["items"])
            acc_item = rng.choice(tier_data["bottoms_acc"]) if tier_data.get("bottoms_acc") else ""

            parts_w = [f"Wearing {main_item}"] if not main_item.startswith("Wearing") and not main_item.startswith("completely nude") and not main_item.startswith("fully nude") else [main_item]
            if acc_item:
                parts_w.append(f"paired with {acc_item}")
            attire = ", ".join(parts_w)

        # 2. SEMANTIC CONTEXT EQUALIZER: SCENE RESOLUTION
        use_equalizer = "Smart Context Equalizer" in cohesion_equalizer

        if custom_scene_override and custom_scene_override.strip():
            env_text = custom_scene_override.strip()
        else:
            # If dynamic matrix, choose semantically harmonized venue
            if scene_environment == "🎲 Dynamic Cinematics Matrix" and use_equalizer:
                if chosen_tier_name in ["nudity", "partial_nudity", "lingerie"]:
                    # Private sanctuaries only (Boudoir, Bath, Penthouse Bedroom, Studio Cutout)
                    theme_choice = rng.choice(["boudoir", "bath", "penthouse_intimate", "studio"])
                elif chosen_tier_name in ["business", "casual"]:
                    # Public, urban, lifestyle, and loft environments
                    theme_choice = rng.choice(["noir", "penthouse_salon", "editorial_studio", "boudoir_library"])
                elif chosen_tier_name == "glamorous":
                    # High fashion, gala, penthouse duplex, and architectural sets
                    theme_choice = rng.choice(["penthouse_salon", "editorial_studio", "noir_balcony", "boudoir_salon"])
                elif chosen_tier_name == "slutty":
                    # BDSM boudoir, cyber sanctuary, or high-contrast studio
                    theme_choice = rng.choice(["boudoir_gothic", "cybernetic", "studio", "penthouse_intimate"])
                else:
                    theme_choice = "boudoir"
            else:
                theme_choice = "custom_map"

            if theme_choice == "boudoir" or "Boudoir" in scene_environment:
                venue = rng.choice(self.BOUDOIR_FURNITURE_VENUES)
                sheets = rng.choice(self.BOUDOIR_SHEET_COLORS)
                env_text = f"{venue}, with {sheets}"
            elif theme_choice == "bath" or "Marble Bath" in scene_environment:
                env_text = rng.choice(self.ENVIRONMENTS_MAP["Steamy Private Marble Bath"])
            elif theme_choice in ["penthouse_intimate", "penthouse_salon"] or "Penthouse" in scene_environment:
                env_text = rng.choice(self.ENVIRONMENTS_MAP["Opulent Penthouse Suite"])
            elif theme_choice == "noir" or theme_choice == "noir_balcony" or "Parisian Noir" in scene_environment:
                env_text = rng.choice(self.ENVIRONMENTS_MAP["Parisian Noir"])
            elif theme_choice == "cybernetic" or "Cybernetic" in scene_environment:
                env_text = rng.choice(self.ENVIRONMENTS_MAP["Cybernetic Sanctuary"])
            elif theme_choice == "studio" or "Neutral Studio" in scene_environment:
                env_text = rng.choice(self.ENVIRONMENTS_MAP["Neutral Studio"])
            elif theme_choice == "editorial_studio" or "Editorial Studio" in scene_environment:
                env_text = rng.choice(self.ENVIRONMENTS_MAP["Editorial Studio"])
            else:
                all_envs = []
                for k, v in self.ENVIRONMENTS_MAP.items():
                    all_envs.extend(v)
                env_text = rng.choice(all_envs)

        # 3. SEMANTIC CONTEXT EQUALIZER: HAIR STATE RESOLUTION
        if use_equalizer and hair_state_mode == "🎲 Dynamic Stochastic Hair (Bedhead, Wet, Tousled, Styled)":
            if "Marble Bath" in env_text or "steam" in env_text.lower() or "tub" in env_text.lower():
                hair_pool = [
                    "damp, glistening post-shower ringlet curls clinging to her neck and collarbone with subtle wet shine and deep indigo undertones",
                    "a messy high bun with loose, curly tendrils and electric-indigo strands framing her sculpted jawline and temples",
                    "damp, towel-dried spiral curls with natural dewy texture and deep indigo sheen catching directional lighting",
                    "damp ringlets with wet-look sheen reflecting ambient candlelight with indigo highlights and authentic moisture",
                    "sensually disheveled hair, with curly indigo strands lightly sticking to her flushed, dewy skin after an intimate bath"
                ]
                chosen_hair = rng.choice(hair_pool)
            elif "Boudoir" in env_text or "bed" in env_text.lower() or "sheets" in env_text.lower():
                hair_pool = [
                    "voluminous bedhead with messy, untamed 3B/3C spiral curls in jet-black with electric indigo highlights tumbling loosely over one eye and bare shoulders",
                    "tousled, pillow-disheveled ringlet curls cascading wildly across her back and bare chest in effortless morning disarray",
                    "intimately side-swept over one shoulder, exposing her bare neck, collarbone, and delicate earlobe",
                    "a loose, low messy ponytail tied with a black silk ribbon, with springy curly ringlets escaping around her ears",
                    "tangled morning curls loosely spilling across the pillow and framing her sleepy, flushed cheekbones",
                    "loose romantic curls pinned up casually with a tortoiseshell clip, with soft curly tendrils falling around her neck"
                ]
                chosen_hair = rng.choice(hair_pool)
            elif "Parisian Noir" in env_text or "rain" in env_text.lower() or "alley" in env_text.lower():
                hair_pool = [
                    "wind-swept dynamic curls caught in mid-motion with flying electric-indigo strands catching volumetric light",
                    "side-parted voluminous curls spilling heavily over her left shoulder and framing her soft-smudged smoky eyeliner",
                    "dynamic flowing curls with natural motion blur on the tips, catching cool-blue rim lighting",
                    "lush, springy spiral ringlets in full natural bounce with electric indigo highlights catching specular highlights"
                ]
                chosen_hair = rng.choice(hair_pool)
            else:
                chosen_hair = rng.choice(self.HAIR_STATES)
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
                chosen_hair = rng.choice(self.HAIR_STATES)
            else:
                chosen_hair = hair_map.get(hair_state_mode, rng.choice(self.HAIR_STATES))

        # 4. CHARACTER ANCHOR
        if custom_character_override and custom_character_override.strip():
            char_base = custom_character_override.strip()
        elif character_anchor == "👑 Vespera (35mm Raw Cinema)":
            char_base = self.VESPERA_VARIATIONS[1]
        elif character_anchor == "👑 Vespera (Editorial Still)":
            char_base = self.VESPERA_VARIATIONS[2]
        elif character_anchor == "🎲 Dynamic Random Subject Anchor":
            ethnicities = ["French", "Italian", "Spanish", "Scandinavian", "Japanese", "Brazilian", "Eastern European", "Greek", "Moroccan", "Persian"]
            hair_colors = [
                "jet-black 3B/3C spiral curls with electric indigo strands",
                "deep auburn wavy hair cascading past her shoulders",
                "platinum blonde textured messy bob framing her cheekbones",
                "rich chocolate brown voluminous cascading waves",
                "honey-caramel textured locks with sun-kissed highlights",
                "raven-black sleek silk hair falling straight past her collarbone"
            ]
            eye_colors = [
                "piercing hazel-green eyes with golden flecks",
                "striking warm amber-gold eyes with dark limbal rings",
                "deep sapphire-blue eyes with intense pupil contrast",
                "intense dark espresso-brown eyes with heavy lashes",
                "captivating emerald-green eyes with subtle soft-smudged smoky eyeliner"
            ]
            eth = rng.choice(ethnicities)
            eye = rng.choice(eye_colors)
            char_base = (
                f'A hyper-realistic photographic capture of a 5\\\'7" {eth} woman with defined athletic hourglass proportions, '
                f'narrow 24-inch waist, 38-inch flared hips, 30-inch muscular thighs, sculpted cheekbones, smooth luminous skin, {eye}, and {chosen_hair}'
            )
        else:
            char_base = self.VESPERA_VARIATIONS[0]

        # Inject dynamic hair styling into Vespera baseline
        if "Voluminous, springy 3B/3C spiral ringlet curls" in char_base:
            char_base = re.sub(r'Voluminous, springy 3B/3C spiral ringlet curls.*?(?=Signature tattoos|Relaxed|\\Z)', f"{chosen_hair.capitalize()}. ", char_base)
        elif "Cascading jet-black 3B/3C spiral ringlets" in char_base:
            char_base = re.sub(r'Cascading jet-black 3B/3C spiral ringlets.*?(?=Wearing|\\Z)', f"{chosen_hair.capitalize()}. ", char_base)
        elif "Voluminous jet-black springy spiral ringlets" in char_base:
            char_base = re.sub(r'Voluminous jet-black springy spiral ringlets.*?(?=Wearing|\\Z)', f"{chosen_hair.capitalize()}. ", char_base)

        char_base = re.sub(r'\s*\.\s*\.', '.', char_base).strip(' .')

        # 5. SEMANTIC CONTEXT EQUALIZER: POSE & EXPRESSION
        poses_pool = self.POSES_POOL_NSFW if is_nsfw else self.POSES_POOL_SFW
        expressions_pool = self.EXPRESSIONS_POOL_NSFW if is_nsfw else self.EXPRESSIONS_POOL_SFW

        pose_map = {
            "Seductive Kneeling with Arched Back": "kneeling with an arched back and seductive pose, maintaining provocative eye contact",
            "Sensual Reclining with Parted Legs": "reclining back gracefully with legs parted in an intimate sensual perspective",
            "Dominant 3/4 Standing Silhouette": "standing in a dynamic three-quarter silhouette with hands resting on her 24-inch waist",
            "Poised Seated Posture with Crossed Legs": "seated cross-legged with poised posture and sculpted shoulders",
            "POV Intimate Perspective Lying Back": "pov intimate perspective, lying back with head tilted back and hands teasing her bare chest",
            "Looking Back Over Bare Shoulder": "lying on her side with one leg raised, gazing intensely over her bare shoulder",
            "All Fours with Arched Spine & Direct Gaze": "leaning forward on all fours with arched spine and sultry gaze directed back toward the camera"
        }

        if pose_action_mode == "🎲 Dynamic Random Pose":
            if use_equalizer and ("Parisian Noir" in env_text or "alley" in env_text.lower() or "bridge" in env_text.lower()):
                # Outdoor environment -> filter to standing or leaning poses (no lying on streets)
                outdoor_poses = [p for p in poses_pool if "standing" in p or "leaning" in p or "walking" in p or "profile" in p or "contrapposto" in p]
                selected_pose = rng.choice(outdoor_poses if outdoor_poses else poses_pool)
            elif use_equalizer and ("Bath" in env_text or "tub" in env_text.lower()):
                # Bath environment -> filter to reclining, seated, intimate poses
                bath_poses = [p for p in poses_pool if "reclining" in p or "seated" in p or "kneeling" in p or "intimate" in p or "elbow" in p]
                selected_pose = rng.choice(bath_poses if bath_poses else poses_pool)
            else:
                selected_pose = rng.choice(poses_pool)
        else:
            selected_pose = pose_map.get(pose_action_mode, rng.choice(poses_pool))

        selected_exp = rng.choice(expressions_pool)
        full_action = f"{selected_pose}, with {selected_exp}"

        # 6. SEMANTIC CONTEXT EQUALIZER: MATERIAL & SKIN PHYSICS
        physics_pool = self.PHYSICS_POOL_NSFW if is_nsfw else self.PHYSICS_POOL_SFW

        physics_map = {
            "💧 Oiled Skin & Specular Glistening (OiledSkin_ZIT)": "realskin, oiled skin with glistening specular highlights and micro-droplets of water catching directional lighting",
            "🔬 Realskin Subsurface Dermal Warmth (fluxRealSkin)": "realskin, subsurface dermal scattering with natural warmth and soft flush across bare shoulders and collarbone",
            "✨ Wet Translucent Sheer Lace & Micro-Pores": "translucent sheer micro-lace tension revealing warm biological realskin texture and anatomical contours underneath",
            "🖤 High-Gloss Liquid Latex & Polished Nappa Leather": "high-gloss liquid latex and nappa leather sheen with crisp ray-traced reflections of ambient scene lighting",
            "🎞️ 35mm Fine Analog Film Grain & Natural Specularity": "fine 35mm film grain, realskin natural pores with authentic specular sheen on bare skin"
        }

        if material_skin_physics == "🎲 Dynamic / Matched Physics":
            if use_equalizer and ("Bath" in env_text or "steam" in env_text.lower()):
                selected_physics = "realskin, dewy glistening skin with tiny micro-droplets of water and authentic subsurface scatter catching warm rim lighting"
            elif use_equalizer and chosen_tier_name == "slutty":
                selected_physics = "high-gloss liquid latex and nappa leather sheen with crisp ray-traced reflections of ambient scene lighting"
            elif use_equalizer and chosen_tier_name in ["lingerie", "partial_nudity"]:
                selected_physics = "translucent sheer micro-lace tension revealing warm biological realskin texture and anatomical contours underneath"
            else:
                selected_physics = rng.choice(physics_pool)
        else:
            selected_physics = physics_map.get(material_skin_physics, rng.choice(physics_pool))

        # 7. DIRECTOR RIG & OPTICS
        if director_camera_rig == "🎲 Dynamic / Random Rig":
            if use_equalizer and ("Boudoir" in env_text or "candle" in env_text.lower()):
                rig_key = rng.choice([
                    "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)",
                    "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)",
                    "Roger Deakins (Arri LF 32mm Tungsten)"
                ])
            elif use_equalizer and ("Parisian Noir" in env_text or "cyber" in env_text.lower()):
                rig_key = rng.choice([
                    "Denis Villeneuve (Alexa 65 Anamorphic 50mm)",
                    "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)",
                    "Ridley Scott (Panavision 50mm f/1.4 Anamorphic)",
                    "Michael Mann (Sony CineAlta 28mm Blue Ambient)"
                ])
            else:
                rig_key = rng.choice(list(self.DIRECTOR_RIG_CONFIGS.keys()))
        else:
            rig_key = director_camera_rig if director_camera_rig in self.DIRECTOR_RIG_CONFIGS else "Denis Villeneuve (Alexa 65 Anamorphic 50mm)"

        rig = self.DIRECTOR_RIG_CONFIGS[rig_key]

        # 8. COMPILE CHANNELS
        is_tags = "Tags" in prompt_engine_format
        quality_tags = "masterpiece, 8k resolution, ultra-detailed, photorealistic, raw 35mm photograph, authentic texture, perfect anatomical proportions"

        if is_tags:
            character_prompt = f"({char_base}:1.1), {attire}, {full_action}, {selected_physics}"
            scene_prompt = f"{env_text}, {rig['lighting']}, natural depth of field, {rig['camera']}, {rig['director']}, {rig['lut']}"
            master_prompt = f"{character_prompt}, {scene_prompt}, {quality_tags}"
        else:
            character_prompt = f"{char_base}. {attire.capitalize()}, {full_action}. Featuring {selected_physics}."
            scene_prompt = f"In the scene, {env_text}. Atmospheric illumination: {rig['lighting']}. Cinematography by {rig['director']}, color graded with {rig['lut']}. Captured on {rig['camera']}."
            master_prompt = f"{character_prompt} {scene_prompt} {quality_tags}."

        negative_prompt = (
            "bystanders, extra people, crowd, pedestrians, background people, 2girls, 2women, multiple people, "
            "photobomb, blurry figures in background, silhouette of person in background, other humans, extra faces, extra bodies, "
            "blurry, low quality, deformed anatomy, extra limbs, bad hands, mutated fingers, "
            "plastic skin, cartoon, anime, illustration, oversaturated, watermark, signature, duplicate"
        )

        rating_tag = "🔞 NSFW" if is_nsfw else "🍷 SFW"
        if "Coin-Flip" in rating_mode:
            rating_tag += " (Coin-Flip)"

        telemetry = (
            f"👑 SUBJECT: {character_anchor} | {rating_tag} | 👗 WARDROBE: {chosen_tier_name.upper()} | "
            f"🎬 RIG: {rig_key} | 🏛️ SCENE: {scene_environment} | 🧠 COHESION: {cohesion_equalizer.split('(')[0].strip()} | 🎲 SEED: {seed}"
        )

        return (
            character_prompt,
            scene_prompt,
            master_prompt,
            negative_prompt,
            attire,
            full_action,
            env_text,
            f"{rig['director']}. {rig['camera']}",
            f"{rig['lighting']}. {rig['lut']}",
            telemetry
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
'''

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"SUCCESS: Expanded {target_path} to {len(content.splitlines())} lines with 25+ items in every list!")
