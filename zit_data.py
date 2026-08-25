"""
File    : zit_data.py
Purpose : High-Fidelity Data Vault with Biometrically Locked Facial Anchors for Vespera ZIT Suite.
"""

DEFAULT_VESPERA_PROMPT_PREFIX = (
    "Amateur raw photography, unretouched, zero makeup, visible skin micro-pores, natural asymmetry. "
    "vespera woman, curvaceous hourglass figure, wide hips, defined narrow waist, soft feminine curves, voluptuous silhouette, (full voluptuous D-cup bust:1.1), "
    "a 5'5\" French woman of French-Levantine and Mediterranean heritage. "
    "Distinctive facial bone structure with full sensual cheeks, a soft youthful heart-oval facial contour, high sculpted cheekbones, and a cute refined soft-tapered button nose with a delicate bridge. "
    "Deep-set captivating almond-shaped hazel-green eyes with amber-gold flecks and a positive canthal tilt, framed by sharp winged black eyeliner and arched dark-sable brows. "
    "Full soft black satin-sheen lips with a defined philtrum and sharp cupid's bow, natural white teeth, and an exact 1mm beauty mark positioned just above the left corner of her upper lip. "
    "Luminous golden-olive skin with authentic biological micro-pore texture, soft subcutaneous dermal warmth, and a dewy specular sheen. "
    "Heavy, tousled 3B/3C spiral ringlet curls in jet-black interwoven with vibrant electric indigo highlights, cascading mid-back framing her jaw and collarbones with no bangs. "
    "Athletic hourglass silhouette with a narrow 24-inch waist, 38-inch flared hips (0.66 waist-to-hip ratio), and thick 30-inch muscular thighs."
)

VESPERA_VARIATIONS = [
    (
        "vespera woman, curvaceous hourglass figure, wide hips, defined narrow waist, soft feminine curves, voluptuous silhouette, (full voluptuous D-cup bust:1.1), "
        "A hyper-realistic photographic capture of Vespera, a 5'5\" French woman of French-Levantine and Mediterranean descent. "
        "Full sensual cheeks, a cute refined soft-tapered button nose with delicate bridge, soft heart-oval jawline contour, sculpted cheekbones. "
        "Deep-set almond hazel-green eyes with amber-gold striations and soft-smudged smoky black kohl eyeliner. "
        "Soft black satin lips with defined cupid's bow, 1mm mole above left upper lip corner, radiant olive skin with natural epidermal pores. "
        "Voluminous 3B/3C jet-black spiral ringlets with electric indigo highlights falling to mid-back, narrow 24-inch waist, flared 38-inch hips, thick 30-inch muscular thighs."
    ),
    (
        "vespera woman, curvaceous hourglass figure, wide hips, defined narrow waist, soft feminine curves, voluptuous silhouette, (full voluptuous D-cup bust:1.1), "
        "A 35mm raw cinematic still of Vespera, a 5'5\" French woman with sultry Levantine and Mediterranean facial architecture and Mediterranean olive complexion. "
        "High sculpted cheekbones with full youthful cheeks, cute refined button-tapered nose, soft jawline contour. "
        "Almond hazel-green eyes with amber flecks and dark lash line, defined soft black satin lips with sharp cupid's bow, 1mm beauty mark at left lip corner. "
        "Flawless biological skin texture with dewy specular highlights. Heavy tousled jet-black 3B/3C curls with indigo strands framing face, athletic 0.66 waist-to-hip hourglass proportions."
    ),
    (
        "vespera woman, curvaceous hourglass figure, wide hips, defined narrow waist, soft feminine curves, voluptuous silhouette, (full voluptuous D-cup bust:1.1), "
        "An editorial high-fashion photographic capture of Vespera, a 5'5\" French woman with distinctive Levantine and Mediterranean bone structure. "
        "High sculpted cheekbones, cute refined button-tapered nose, full sensual cheeks, deep-set hazel-green eyes with positive canthal tilt and winged liner. "
        "Full soft black satin lips, 1mm upper left beauty mark, luminous olive skin with subsurface dermal warmth and micro-perspiration sheen. "
        "Dense springy jet-black 3B/3C spiral curls with electric indigo highlights cascading past shoulders, narrow 24-inch waist and thick 30-inch muscular thighs."
    )
]

# Dedicated micro-prompt blueprint for FaceDetailer
VESPERA_FACE_MICROPACK = (
    "realskin, high-fidelity macro 8k photographic portrait of Vespera, sultry Levantine and Mediterranean facial structure, "
    "cute refined soft-tapered button nose with delicate bridge, full sensual cheeks and soft youthful jaw contour, high cheekbones, deep-set almond hazel-green eyes with amber-gold flecks, "
    "soft-smudged smoky black kohl eyeliner, defined soft black satin lips with cupid's bow, 1mm beauty mark near left corner of upper lip, "
    "natural clean white teeth, authentic epidermal skin pores, subsurface dermal scattering, "
    "3B/3C jet-black and electric indigo curls framing face and jawline"
)

HAIR_CONFLICTS = [
    r'\bblonde(?:\s+hair)?\b', r'\bblond(?:\s+hair)?\b', r'\bbrown\s+hair\b', r'\bred\s+hair\b',
    r'\bblack\s+hair\b', r'\bwhite\s+hair\b', r'\bsilver\s+hair\b', r'\bpink\s+hair\b',
    r'\bblue\s+hair\b', r'\bgreen\s+hair\b', r'\bpurple\s+hair\b', r'\bgolden\s+hair\b',
    r'\bshort\s+hair\b', r'\blong\s+hair\b', r'\bstraight\s+hair\b', r'\bcurly\s+hair\b',
    r'\bwavy\s+hair\b', r'\bponytail\b', r'\bpigtails\b', r'\bbraids?\b', r'\bbob\s+cut\b',
    r'\bbangs\b', r'\btwintails\b'
]

EYE_CONFLICTS = [
    r'\bblue\s+eyes?\b', r'\bgreen\s+eyes?\b', r'\bbrown\s+eyes?\b', r'\bhazel\s+eyes?\b',
    r'\bred\s+eyes?\b', r'\bamber\s+eyes?\b', r'\byellow\s+eyes?\b', r'\bblack\s+eyes?\b',
    r'\bgrey\s+eyes?\b', r'\bgray\s+eyes?\b', r'\bpurple\s+eyes?\b', r'\bdark\s+eyes?\b'
]

BODY_SUBJECT_CONFLICTS = [
    r'\b1girl\b', r'\b1woman\b', r'\b1female\b', r'\bsolo\b', r'\ba\s+girl\b', r'\ba\s+woman\b',
    r'\bflat\s+chest\b', r'\bsmall\s+breasts?\b', r'\blarge\s+breasts?\b', r'\bhuge\s+breasts?\b',
    r'\bpetite\b', r'\bslim\b', r'\bchubby\b', r'\btall\b', r'\bshort\s+stature\b',
    r'\bfemale\b', r'\bwoman\b', r'\bgirl\b'
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

SENSORY_WEATHERING_MODIFIERS = [
    "with micro-droplets of atmospheric moisture condensing gently on the skin surface",
    "catching a subtle warm breeze that stirs stray ringlet tendrils across her temples",
    "illuminated by an authentic soft optical halation effect diffusing highlights",
    "with fine analog film stock grain adding rich tactile depth across shadow transitions",
    "exhibiting lifelike thermal skin glow and soft vascular blood flow undertones",
    "surrounded by faint ambient dust motes suspended in narrow shafts of directional light",
    "with subtle kinetic tension in her neck muscles and micro-expressions around the eyes",
    "featuring ray-traced sub-surface light scattering highlighting her collarbone architecture"
]

HAIR_STATES = [
    f"{style} 3B/3C spiral curls in jet-black with {highlight} highlights {placement}, {sensory}"
    for style in [
        "voluminous bedhead with messy, untamed", "damp, glistening post-shower", "a messy high bun with loose, curly tendrils and",
        "tousled, pillow-disheveled", "wind-swept dynamic", "intimately side-swept over one shoulder with",
        "slightly frizzy, humid bedhead", "a loose, low messy ponytail with", "damp, towel-dried",
        "a sleek half-up, half-down crown of", "wild, untamed voluminous", "loose romantic pinned-up",
        "sensually disheveled, moisture-rich", "side-parted dense", "a relaxed, unstyled natural crown of",
        "dynamic flowing and airborne", "partially pinned back with antique clips and", "tangled morning-after",
        "dense, springy athletic", "rich cascading heavyweight", "sculpted high-fashion runway",
        "soft, touchable air-dried", "lush and deeply coiled", "asymmetrical swept", "regal halo-framed"
    ]
    for highlight in ["electric indigo", "deep cobalt", "subtle midnight-violet", "luminous sapphire-blue", "radiant deep cyan"]
    for placement in [
        "tumbling loosely over one eye and bare shoulders",
        "clinging to her neck and collarbone with subtle wet shine",
        "framing her sculpted jawline, temple, and ears",
        "cascading wildly across her back and bare chest",
        "caught in mid-motion with flying strands catching volumetric light",
        "exposing her bare neck, collarbone, and delicate earlobe",
        "spilling heavily down her spine to mid-back with no bangs"
    ]
    for sensory in SENSORY_WEATHERING_MODIFIERS
][:250]

POSES_POOL_NSFW = [
    f"{modifier} {pose} {framing}, {sensory}"
    for modifier in [
        "sleeper, seductive", "sensual and provocative,", "dominant and intimate,", "candidly uninhibited,",
        "artistically poised,", "breathless,", "slow and deliberate,", "commanding,"
    ]
    for pose in [
        "kneeling with an arched back", "reclining back gracefully with legs parted",
        "seated upright in a provocative posture with legs parted", "lying on her side with one leg raised and hips angled",
        "pov intimate perspective, lying back with head tilted back", "leaning forward on all fours with arched spine",
        "standing in a three-quarter silhouette with back arched", "seated on her heels with spine erect and hands on 30-inch thighs",
        "reclining on one elbow with torso twisted to accentuate waist-to-hip curve", "stretching both arms overhead with interlaced fingers",
        "sitting with one knee drawn to chest while extending the other leg", "leaning back against a flat surface with hips pushed forward",
        "lying flat on back with arms extended and dynamic hip tilt", "seated cross-legged with forward lean resting chin on palm",
        "kneeling with one leg extended sideways", "crouching low in a dynamic feline posture",
        "propped up on elbows lying on stomach with arched lower back", "standing tall shifting weight heavily to right hip in contrapposto"
    ]
    for framing in [
        "maintaining provocative direct eye contact with the viewer",
        "gazing intensely over her bare shoulder",
        "with hands teasing her bare collarbone and neckline",
        "wet glistening skin catching sharp specular highlights",
        "accentuating the 0.66 waist-to-hip ratio and rounded curves",
        "looking back with heavy-lidded hazel eyes and parted lips",
        "bathed in directional low-key rim light and deep shadow falloff"
    ]
    for sensory in SENSORY_WEATHERING_MODIFIERS
][:250]

POSES_POOL_SFW = [
    f"{stance} {action} {detail}, {sensory}"
    for stance in [
        "standing poised in classic contrapposto,", "seated upright with elegant posture,",
        "leaning casually against an architectural partition,", "walking forward in natural mid-stride,",
        "three-quarter fashion portrait stance,", "candidly seated cross-legged on polished floor,",
        "perched gracefully on the edge of a seat,", "standing tall with commanding poise,"
    ]
    for action in [
        "with hands resting casually on her 24-inch waistline", "with arms loosely crossed in an analytical posture",
        "running fingers lightly through cascading indigo curls", "with chin slightly lifted highlighting aquiline nose and jawline",
        "glancing back over bare shoulder toward the lens", "adjusting tailored cuff with eyes cast downward",
        "resting chin in hand in deep contemplation", "holding direct unblinking eye contact with the viewer"
    ]
    for detail in [
        "framing her narrow waist and flared 38-inch hips naturally",
        "with soft ambient lighting sculpting facial cheekbones",
        "showing natural head-to-toe proportional scale and balance",
        "with wind gently catching loose spiral ringlet tendrils",
        "accentuating regal Levantine bone structure and poise",
        "with crisp fabric drapery and clean negative space"
    ]
    for sensory in SENSORY_WEATHERING_MODIFIERS
][:250]

EXPRESSIONS_POOL_NSFW = [
    f"a {adj} {type_e} with {lips}, {eyes}, and {detail}"
    for adj in ["seductive", "provocative", "breathless", "sultry", "commanding", "enigmatic", "hypnotic", "intoxicating", "intimate", "raw"]
    for type_e in ["knowing smirk", "direct gaze", "bedroom expression", "half-smile", "sardonic glance", "stare of desire", "feline gaze", "alluring daze"]
    for lips in ["parted soft black satin lips", "moist soft black lips revealing clean white teeth", "gently bitten lower lip", "soft relaxed satin lips", "subtle lip curl"]
    for eyes in ["heavy-lidded almond hazel eyes", "dilated pupils catching amber flecks", "intense smudged smoky kohl eyes", "piercing unblinking hazel gaze"]
    for detail in ["delicate cheek flush", "1mm beauty mark highlighted", "subtle perspiration sheen", "raised arched sable brow", "radiant Mediterranean warmth"]
][:250]

EXPRESSIONS_POOL_SFW = [
    f"a {adj} {type_e} featuring {eyes}, {lips}, and {tone}"
    for adj in ["subtle", "calm", "poised", "sharp", "enigmatic", "candid", "thoughtful", "authoritative", "serene", "intelligent"]
    for type_e in ["knowing half-smirk", "analytical focus", "high-fashion stare", "contemplative look", "genuine smile", "regal composure", "curious expression"]
    for eyes in ["captivating almond hazel-green eyes", "intense direct eye contact", "amber-gold iris flecks catching key light", "arched dark-sable eyebrows"]
    for lips in ["closed defined soft black lips", "relaxed natural smile with white teeth", "subtle Jeselnik-style smirk", "defined cupid's bow"]
    for tone in ["clean facial symmetry", "sculpted cheekbone shadows", "natural eye crinkles", "smooth forehead composure", "timeless Parisian elegance"]
][:250]

PHYSICS_POOL_NSFW = [
    f"realskin, {dermal}, {specular}, {subsurface}, and {texture}"
    for dermal in [
        "oiled golden-olive skin", "dewy micro-perspiration sheen across collarbone and thighs",
        "authentic biological skin elasticity", "moisture droplets tracing down bare contours",
        "tactile realskin texture across 30-inch muscular thighs"
    ]
    for specular in [
        "glistening specular highlights on cheekbones and nose bridge", "sharp ray-traced reflections on skin curvature",
        "subtle ambient light bounce off bare shoulders", "high-contrast specular rim illumination"
    ]
    for subsurface in [
        "warm subsurface dermal scattering", "natural vascular blood flow warmth",
        "soft biological flush on cheeks and chest", "translucent skin depth under directional light"
    ]
    for texture in [
        "fine epidermal pore fidelity without plastic smoothing", "raw 35mm analog grain resolution",
        "authentic micro-texture across bare skin", "zero digital smoothing or artificial blur"
    ]
][:250]

PHYSICS_POOL_SFW = [
    f"{fabric}, {realskin_detail}, {optical}"
    for fabric in [
        "heavy Italian wool suiting with subtle twill texture", "heavyweight brushed nappa leather with crisp specular seams",
        "luxurious fluid silk charmeuse flowing over anatomical curves", "crisp French cotton poplin with razor-sharp folds",
        "tactile distressed selvedge denim with visible cross-hatch warp", "delicate French chantilly lace with patterned shadow cast",
        "brushed cashmere knit fibers with authentic fuzzy surface halo", "molten liquid metallic lamé with undulating highlights"
    ]
    for realskin_detail in [
        "realskin subsurface scattering with soft biological skin warmth", "natural epidermal pore fidelity on face and hands",
        "authentic golden-olive Mediterranean dermal tones", "soft satin sheen on lips and natural clean nail bed texture",
        "subtle specular highlights along aquiline bridge and collarbone"
    ]
    for optical in [
        "rich 35mm optical depth and natural falloff", "shot on CineStill 800T with delicate halation around highlights",
        "true medium-format lens compression and zero digital noise", "balanced ray-traced ambient lighting and authentic shadows"
    ]
][:250]

BOUDOIR_SHEET_COLORS = [
    f"{color} {material} bedding with {detail}"
    for color in ["obsidian black", "deep crimson", "champagne-gold", "midnight sapphire", "emerald green", "pearl-grey", "rich espresso", "deep plum", "charcoal-grey", "dusty lavender", "terracotta", "raw ivory"]
    for material in ["liquid silk satin", "crushed velvet", "Egyptian cotton", "charmeuse silk", "washed French linen", "damask jacquard", "mulberry silk"]
    for detail in ["scattered silk pillows", "delicate black lace trim", "plush fur throws", "deep fluid creases", "tasseled velvet bolsters", "crisp ironed folds", "golden embroidered piping"]
][:150]

BOUDOIR_FURNITURE_VENUES = [
    f"in {setting} with {furniture} and {atmosphere}"
    for setting in [
        "an opulent Parisian master bedroom suite", "an intimate Marais boudoir", "a luxury Haussmann apartment bedroom",
        "a private high-fashion boudoir", "an atmospheric vintage library suite", "an intimate candlelit bedroom alcove",
        "a lavish penthouse suite overlooking Paris at 3 AM", "an antique French rococo salon", "a moody boutique hotel suite in Saint-Germain",
        "a secluded timber attic loft", "an opulent neoclassical bedroom suite", "a historic French chateau bedchamber"
    ]
    for furniture in [
        "a grand four-poster iron canopy bed", "a vintage velvet chaise lounge beside an ornate marble fireplace",
        "herringbone oak floors and floor-to-ceiling French windows", "deep velvet drapery and full-length gilded mirrors",
        "tufted leather armchairs and dark walnut wainscoting", "a carved mahogany headboard with antique brass candelabras",
        "minimalist designer platform furniture and recessed cove lights"
    ]
    for atmosphere in [
        "flickering beeswax candles casting warm shadows", "glistening raindrops streaking across panoramic glass",
        "warm ambient glow from crystal chandeliers", "moody chiaroscuro shadow falloff across the floor",
        "soft atmospheric mist and warm golden hour shafts", "deep obsidian shadows and subtle amber rim lights"
    ]
][:150]

ENVIRONMENTS_MAP = {
    "Neutral Studio": [
        f"{backdrop} in a professional studio setting with {floor} and {lighting}"
        for backdrop in [
            "seamless dark charcoal cyclorama wall", "neutral medium-grey seamless paper backdrop",
            "solid deep obsidian light-absorbing backdrop", "pure white seamless infinity cyclorama",
            "dark slate-grey textured plaster wall", "warm beige fine-grain paper backdrop",
            "high-fashion black velvet light-absorbing flat", "dark matte olive-grey seamless backdrop",
            "hand-painted dark charcoal textured canvas", "monochrome portrait backdrop grading to soft ash"
        ]
        for floor in [
            "smooth polished concrete floor reflections", "matte black non-reflective ground plane",
            "clean optical spacing and zero clutter", "polished grey studio flooring",
            "minimalist shadow projection plane", "seamless curved infinity floor junction"
        ]
        for lighting in [
            "soft directional key light falloff", "balanced three-point high-fashion strobe lighting",
            "surgical softbox edge illumination", "sculpted optical rim light separation",
            "diffused daylight scrim bounce", "single dramatic Fresnel spotlight"
        ]
    ][:150],
    "Dark Parisian Boudoir": BOUDOIR_FURNITURE_VENUES,
    "Parisian Noir": [
        f"{location} in Paris at {time} with {weather} and {lighting}"
        for location in [
            "standing on the wet cobblestones of a Montmartre alleyway", "on the ornate Pont Alexandre III bridge",
            "under the wrought-iron arches of a secluded covered gallery", "on an intimate wrought-iron Haussmann balcony",
            "outside an iconic Parisian sidewalk cafe with red awnings", "in a secluded stone courtyard in Le Marais",
            "beside a vintage Art Nouveau Metro entrance", "along the cobblestone quayside of the Seine river",
            "in the shadow of Notre-Dame stone buttresses", "along a dimly lit rue in Saint-Germain with vintage bookshops"
        ]
        for time in ["2 AM", "3 AM", "twilight blue hour", "midnight", "pre-dawn 4 AM"]
        for weather in ["heavy rainfall forming glistening puddles", "dense river mist rising off the dark water", "a gentle autumn drizzle on wet pavement", "cool atmospheric night haze"]
        for lighting in [
            "glowing amber vintage gas streetlamps and neon signs", "distant golden bridge arches reflecting on water",
            "warm sodium-vapor light catching wet cobblestones", "cyan and magenta neon signs glowing in the mist",
            "vehicle headlights cutting through rain in soft bokeh"
        ]
    ][:150],
    "Cybernetic Sanctuary": [
        f"inside {venue} in Neo-Paris featuring {hardware} with {illumination}"
        for venue in [
            "a moody high-tech cybernetic sanctuary", "a private neural link research sanctum",
            "a futuristic subterranean server chamber", "a neon-lit cyberpunk penthouse cockpit",
            "an underground synthetic biology augmentation lab", "an encrypted dark-fiber data vault",
            "a precision cybernetic fabrication bay", "an autonomous AI command terminal room"
        ]
        for hardware in [
            "holographic wireframe terminals and dark brushed aluminum panels", "glowing fiber-optic conduits and sleek carbon-fiber desks",
            "monolithic server racks and pulsating coolant lines", "robotic surgical arms and floating telemetry visors",
            "transparent OLED partition screens displaying diagnostic code", "liquid nitrogen cooling manifolds with frost crystals"
        ]
        for illumination in [
            "ambient indigo and cyan conduit rim lighting", "volumetric neon reflections cutting through low floor mist",
            "recessed UV sterilization light strips and dark shadows", "strobing data node LEDs and cool blue backlights"
        ]
    ][:150],
    "Opulent Penthouse Suite": [
        f"inside {room} of a luxury Parisian penthouse overlooking {view} with {decor}"
        for room in [
            "a double-height living salon", "a private master bedroom suite", "a sleek glass-walled dining gallery",
            "a minimalist architectural duplex lounge", "a private rooftop conservatory atrium", "an opulent bar and media salon"
        ]
        for view in [
            "the rainy Paris skyline at 3 AM through floor-to-ceiling glass", "panoramic views of the glowing Eiffel Tower and urban sprawl",
            "rain-slicked zinc rooftops and illuminated boulevards below", "distant lightning flashing across the midnight horizon"
        ]
        for decor in [
            "polished dark marble floors and linear gas fireplace flames", "cantilevered glass staircases and custom Italian leather seating",
            "back-lit onyx countertops and crystal decanters", "dark wenge wood wall paneling and recessed architectural lighting"
        ]
    ][:150],
    "Steamy Private Marble Bath": [
        f"inside {bath_setting} featuring {tub} with {steam_light}"
        for bath_setting in [
            "a private master bathroom lined in bookmatched Nero Marquina marble",
            "an opulent hammam-inspired sanctuary with carved stone archways",
            "a luxury penthouse bathroom with panoramic rainy city windows",
            "an antique Parisian bath suite with white Carrara marble wainscoting",
            "a dark emerald marble spa suite with brushed brass hardware",
            "a minimalist Japanese onsen-style bathroom with smooth river basalt"
        ]
        for tub in [
            "an oversized clawfoot bathtub filled with steaming water", "a freestanding black granite soaking tub",
            "a deep sunken marble pool with floating candles", "a hand-hammered copper soaking tub",
            "an infinity-edge marble bath overflowing onto dark pebbles"
        ]
        for steam_light in [
            "warm rising atmospheric mist and glowing amber tea lights",
            "flickering candlelight reflecting off wet polished tiles",
            "soft steam halation diffusing directional warm spotlights",
            "water droplets condensing on mirrors under warm sconces"
        ]
    ][:150],
    "Editorial Studio": [
        f"in {studio_type} featuring {set_element} with {lighting_rig}"
        for studio_type in [
            "a high-end minimalist editorial fashion studio", "an avant-garde architectural photography loft",
            "a brutalist concrete studio with soaring ceilings", "a Parisian haute couture atelier with arched windows",
            "an industrial art gallery with polished concrete floors", "a pristine monochromatic white-cube studio"
        ]
        for set_element in [
            "geometric concrete columns and floating white architectural blocks",
            "polished black plexiglass flooring creating mirror reflections",
            "tall floor-to-ceiling textured dark canvas flats",
            "monumental brutalist concrete staircases with sharp shadow edges",
            "translucent acrylic screens creating soft-focus background depth"
        ]
        for lighting_rig in [
            "dramatic diagonal sunbeam shafts from high clerestory windows",
            "a massive silk diffusion scrim casting flawless wrap-around light",
            "single high-power Fresnel spotlights carving razor-sharp silhouettes",
            "calibrated Profoto strobe heads delivering crisp edge acutance"
        ]
    ][:150]
}

WARDROBE_DATA = {
    "lingerie": {
        "items": [
            f"a {color} {material} {garment} with {detail}"
            for color in ["obsidian black", "scarlet red", "emerald green", "midnight-blue", "champagne-gold", "sheer white", "deep sapphire", "blush-pink", "ruby-red", "peacock-teal"]
            for material in ["French chantilly lace", "silk satin", "sheer embroidered tulle", "plush silk velvet", "semi-sheer mesh", "filigree lace"]
            for garment in ["lingerie bodysuit", "plunging teddy", "underwire balconette bra and garter set", "corset with flexible steel boning", "babydoll nightgown", "open-cup bustier", "chemise slip"]
            for detail in [
                "scalloped eyelash lace and criss-cross strappy back", "delicate gold hardware and sheer mesh panels",
                "cinched waist boning and satin ribbon lace-up detailing", "fluttery hemline and deep décolletage",
                "intricate floral embroidery framing collarbone and hips", "scalloped demi-cups and matching high-cut briefs"
            ]
        ][:150],
        "bottoms_acc": [
            f"{stockings} paired with {shoes} and {jewelry}"
            for stockings in [
                "sheer black thigh-high stockings with lace stay-up tops", "sheer back-seam stockings clipped to satin garter straps",
                "ultra-sheer nude thigh-high stockings with scalloped cuffs", "vintage fishnet thigh-highs attached to a 6-strap garter belt",
                "bare legs with sheer lace thigh bands", "ultra-fine 10-denier black stockings with reinforced heels"
            ]
            for shoes in [
                "4-inch satin stiletto mules", "pointed-toe patent leather pumps", "Christian Louboutin red-bottom heels",
                "minimalist black patent stiletto sandals", "5-inch platform dagger heels", "velvet stiletto sandals"
            ]
            for jewelry in [
                "a delicate silver chain anklet", "a thin black velvet choker", "sparkling diamond stud earrings",
                "a fine platinum chain resting against collarbone", "whisper-thin gold body chain around waist"
            ]
        ][:150]
    },
    "slutty": {
        "items": [
            f"a {style} {material} {outfit} with {hardware}"
            for style in ["bondage-inspired", "provocative cut-out", "high-gloss", "translucent wet-look", "ultra-revealing", "scandalous sheer", "strappy elastic", "micro-coverage"]
            for material in ["matte black leather", "liquid black latex", "patent vinyl", "see-through fishnet mesh", "metallic chainmail", "crimson PVC", "glossy purple latex"]
            for outfit in ["body harness and open bra", "micro-bikini with minimal coverage", "underbust corset and micro-skirt", "catsuit with plunging chest cutout", "monokini with exposed ribcage", "body cage and choker"]
            for hardware in [
                "polished silver O-rings and buckled straps", "chrome zipper tracks and studded accents",
                "thin string ties accentuating hourglass hips", "criss-cross body chains and steel rings",
                "locking metal eyelets and wide waist cinchers", "open-cup framing and structural boning"
            ]
        ][:150],
        "bottoms_acc": [
            f"{boots} and {choker}"
            for boots in [
                "thigh-high glossy patent leather stiletto boots with silver buckles", "leather leg harness straps over fishnet stockings with 5-inch heels",
                "glossy wet-look vinyl over-the-knee boots with chrome zippers", "ultra-high cut patent leather thigh-highs with dagger heels",
                "bare legs with strappy leather thigh holsters and stiletto sandals", "chunky platform combat boots over torn fishnet stockings"
            ]
            for choker in [
                "a locked silver choker necklace", "a spike-studded leather collar", "a heavy O-ring leather torque",
                "a minimalist chrome collar", "a wide patent leather neck strap with chain leash ring"
            ]
        ][:150]
    },
    "nudity": {
        "items": [
            f"{nude_type}, {skin_state} showcasing {anatomy}"
            for nude_type in [
                "completely nude, b3tternud3s anatomical precision", "fully nude, realskin texture",
                "completely nude, oiled realskin with glistening specular highlights", "fully nude with b3tternud3s realism",
                "completely nude, glowing golden-olive realskin", "fully nude artistic high-fashion portrait",
                "completely nude, raw unadorned anatomical beauty", "fully nude, sculpted athletic physique"
            ]
            for skin_state in [
                "bare breasts, flat toned abdomen, and unblemished skin", "dewy skin catching ambient specular rim light",
                "natural biological pore texture across bare torso", "warm subsurface dermal scatter across bare shoulders",
                "fine analog film grain across bare olive skin", "subtle moisture sheen across bare chest and collarbones"
            ]
            for anatomy in [
                "her narrow 24-inch waist, natural bust curves, and flared 38-inch hips",
                "her 0.66 waist-to-hip ratio and thick 30-inch muscular thighs",
                "sculpted collarbone lines and smooth bare hip curvature",
                "toned abdominal contours and flawless bare silhouette",
                "natural breast shape and rounded feminine contours"
            ]
        ][:150],
        "bottoms_acc": [
            f"{bare_state} wearing {minimal_acc}"
            for bare_state in [
                "barefoot on luxury dark hardwood", "barefoot with glistening skin catching ambient light",
                "barefoot on polished marble flooring", "completely unadorned and barefoot",
                "barefoot with soft candlelight wrapping around her heels"
            ]
            for minimal_acc in [
                "only a delicate silver chain anklet and minimalist gold hoop earrings", "only a tiny obsidian pendant necklace resting between bare collarbones",
                "only a black velvet ribbon choker", "only a whisper-thin gold body chain highlighting her 24-inch waist",
                "only a vintage Cartier-style gold watch on left wrist", "only a tiny diamond drop necklace against bare skin"
            ]
        ][:150]
    },
    "partial_nudity": {
        "items": [
            f"a {garment} {fall_style}, completely exposing {exposed}"
            for garment in [
                "oversized white cotton dress shirt", "sheer wet white silk camisole", "vintage silk kimono robe",
                "low-draped black satin tailored blazer", "sheer chiffon duster robe", "unzipped black leather moto jacket",
                "unbuttoned charcoal cashmere cardigan", "sheer black mesh long-sleeve top with zero lining",
                "emerald silk velvet robe", "oversized chunky knit sweater pulled up", "unbuttoned tailored pinstripe waistcoat"
            ]
            for fall_style in [
                "unbuttoned and falling off bare shoulders", "clinging translucent against damp skin",
                "hanging loosely open at the front", "worn completely open with nothing underneath",
                "slipping down both arms in casual disarray", "billowing open with natural movement"
            ]
            for exposed in [
                "bare breasts, collarbone, and toned midriff", "bare chest, narrow 24-inch waist, and exposed hips",
                "bare bust and sculpted abdomen with natural shadow depth", "bare cleavage, flat stomach, and thighs"
            ]
        ][:150],
        "bottoms_acc": [
            f"{bottoms} and {footwear}"
            for bottoms in [
                "tailored high-waisted dark shorts left unbuttoned at the waist", "completely bare legs and hips",
                "sheer silk lace panties with high-cut leg openings", "unbuttoned distressed dark denim jeans sitting low on hips",
                "sheer black Brazilian thong", "a micro black satin mini-skirt riding high on 30-inch thighs",
                "low-rise sweatpants pushed down past hip bones", "sheer lace boyshorts hugging curves"
            ]
            for footwear in [
                "barefoot with subtle dermal sheen", "4-inch satin stiletto mules", "pointed-toe patent leather pumps",
                "pointed black suede ankle booties", "minimalist slingback heels", "bare feet on dark parquet floors"
            ]
        ][:150]
    },
    "sexy": {
        "items": [
            f"a {fit} {color} {fabric} {style} with {cutout}"
            for fit in ["form-fitting", "skin-tight", "sculpted", "tailored", "backless", "draped"]
            for color in ["burgundy", "obsidian black", "emerald green", "charcoal", "crimson red", "midnight-blue", "metallic pewter", "deep-plum", "champagne-gold", "chocolate-brown"]
            for fabric in ["liquid satin", "ribbed knit", "lambskin leather", "silk velvet", "bandage fabric", "silk charmeuse", "metallic lamé", "sheer panelled mesh"]
            for style in ["slip dress", "bodycon mini dress", "bustier and high-slit maxi skirt", "tuxedo dress with satin lapels", "cocktail dress", "halter gown", "pencil dress"]
            for cutout in [
                "a plunging cowl neckline and open back", "provocative cut-outs along ribcage and waist",
                "a daring thigh-high side slit revealing 30-inch thighs", "criss-cross spaghetti straps down the spine",
                "deep sweetheart neckline accentuating hourglass curves", "exposed industrial back zipper"
            ]
        ][:150],
        "bottoms_acc": [
            f"{heels} and {acc}"
            for heels in [
                "strappy black patent leather stiletto sandals", "pointed-toe black suede ankle booties",
                "classic Christian Louboutin red-bottom pumps", "knee-high tailored nappa leather stiletto boots",
                "metallic gold ankle-strap stiletto heels", "pointed-toe patent slingbacks", "over-the-knee suede stiletto boots"
            ]
            for acc in [
                "layered delicate gold necklaces along bare collarbone", "a wide black leather waist belt with gunmetal buckle",
                "a diamond tennis bracelet and matching stud earrings", "a vintage Cartier-style gold bangle and stacked rings",
                "chandelier crystal drop earrings and sleek clutch", "a thin velvet choker with diamond pendant"
            ]
        ][:150]
    },
    "glamorous": {
        "items": [
            f"an haute couture {color} {material} {silhouette} with {grand_detail}"
            for color in ["midnight-blue", "champagne-gold", "emerald-green", "obsidian black", "crimson red", "pearl-white", "royal sapphire", "dark-plum", "rose-gold", "metallic platinum"]
            for material in ["liquid velvet", "molten lamé", "silk taffeta", "tiered organza", "duchess satin", "crystal-encrusted silk", "metallic jacquard", "silk mikado"]
            for silhouette in ["backless evening gown", "floor-length column dress", "corseted ballgown", "mermaid gown that flares past knees", "column gown with portrait collar", "asymmetric one-shoulder gown"]
            for grand_detail in [
                "a sweeping train and crystal-embellished straps", "sculpted architectural shoulder pads and plunging neckline",
                "a cinched 24-inch waist and dramatic draped overskirt", "cascading capelet sleeves and high leg slit",
                "hand-stitched jet bead embroidery and sheer illusion bodice", "origami folded architectural neckline"
            ]
        ][:150],
        "bottoms_acc": [
            f"{evening_shoes}, {gloves}, and {fine_jewelry}"
            for evening_shoes in [
                "custom satin evening stiletto pumps", "strappy metallic platinum stiletto heels",
                "Christian Louboutin pumps with crystal brooches", "strappy crystal-encrusted evening sandals",
                "pointed-toe silk pumps with jewel buckles"
            ]
            for gloves in [
                "matching satin opera gloves extending past elbows", "black velvet opera gloves",
                "sheer embroidered tulle gloves", "bare unadorned arms catching specular light"
            ]
            for fine_jewelry in [
                "glittering diamond chandelier earrings and tennis bracelet", "vintage art deco diamond choker necklace",
                "multi-strand natural pearl choker and diamond studs", "emerald and diamond pendant necklace",
                "cascading crystal fringe earrings and diamond cuff"
            ]
        ][:150]
    },
    "business": {
        "items": [
            f"a {tailoring} {color} {material} {garment} worn over {undergarment}"
            for tailoring in ["bespoke", "impeccably tailored", "structured", "sharp double-breasted", "modern minimalist"]
            for color in ["charcoal-grey", "pinstripe navy", "matte black", "crisp ivory", "camel", "dark emerald", "slate-grey", "dark-espresso", "chalk-stripe"]
            for material in ["Italian wool", "French linen", "nappa leather", "wool crepe", "cashmere blend", "structured wool twill"]
            for garment in ["blazer and cigarette trousers suit", "tuxedo jacket with satin peak lapels", "trench dress belted at 24-inch waist", "three-piece suit with waistcoat", "pantsuit with wide-leg trousers", "pencil dress with structured shoulders"]
            for undergarment in [
                "a sultry black silk chantilly lace camisole", "a crisp white French cotton button-down shirt",
                "an open neckline with no undershirt revealing bare collarbone", "a sheer black silk chiffon blouse",
                "a fine-gauge black cashmere turtleneck", "a tailored silk crepe pussy-bow blouse"
            ]
        ][:150],
        "bottoms_acc": [
            f"{business_shoes} and {briefcase_watch}"
            for business_shoes in [
                "pointed-toe black leather court pumps", "matte leather oxford heels with high-shine polish",
                "tailored stiletto ankle boots", "pointed-toe patent leather slingback heels",
                "tailored black patent loafers with gold horsebit hardware", "pointed-toe dark burgundy leather pumps"
            ]
            for briefcase_watch in [
                "a classic Cartier Tank leather strap watch", "a tailored leather laptop portfolio and gold cuff",
                "a structured leather envelope clutch and diamond studs", "a vintage gold wristwatch and Signet ring",
                "a minimalist leather attache case and gold hoop earrings"
            ]
        ][:150]
    },
    "casual": {
        "items": [
            f"a {style} {color} {top} worn over {inner}"
            for style in ["oversized", "distressed vintage", "form-fitting", "cozy chunky", "slouchy", "cropped", "relaxed-fit"]
            for color in ["charcoal", "black", "cream cable-knit", "olive-green", "faded chambray", "washed-black", "navy Breton striped", "heather-grey", "burgundy"]
            for top in ["cashmere sweater slipping off one shoulder", "motorcycle leather jacket with silver hardware", "flannel overshirt", "denim trucker jacket", "aviator shearling jacket", "ribbed knit bodysuit", "cashmere hoodie"]
            for inner in [
                "a simple black ribbed tank top", "a form-fitting cropped crewneck tee",
                "a white cropped ribbed tank exposing 24-inch waist", "a black lace-trimmed camisole",
                "a vintage graphic rock band tee knotted at the waist", "a scoop-neck heather tank"
            ]
        ][:150],
        "bottoms_acc": [
            f"{denim_bottom} and {casual_shoes}"
            for denim_bottom in [
                "high-waisted vintage selvedge denim jeans with distressing", "fitted black lambskin leather leggings",
                "distressed denim cutoff shorts accentuating 30-inch muscular thighs", "vintage light-wash Levi's 501 jeans",
                "black high-rise skinny jeans with frayed hem", "relaxed-fit boyfriend jeans with knee tears",
                "black leather biker shorts hugging thighs", "high-rise flared dark denim jeans"
            ]
            for casual_shoes in [
                "black leather combat boots", "classic low-top canvas sneakers",
                "Doc Martens 8-eye leather boots", "pointed black leather ankle booties",
                "chunky platform loafers", "classic Chuck Taylor high-top sneakers",
                "pointed-toe leather mules", "vintage leather workboots"
            ]
        ][:150]
    }
}

LORA_TIER1_ANCHORS = [
    {
        "tier": "Tier 1: Identity Anchor",
        "name": f"Anchor Slot {i+1:02d} ({angle_name})",
        "pose": f"Extreme macro photography with tight focal framing on the face. {pose_desc}. Hyper-detailed iris with amber-gold flecks, individual eyelashes, and authentic epidermal pores",
        "expression": expr,
        "attire": "bare shoulders and neck",
        "env": env_d,
        "rig": rig_key,
        "physics": "realskin, high-fidelity subsurface scattering with soft biological skin warmth, natural pore structure without plastic smoothing"
    }
    for i, (angle_name, pose_desc, rig_key, expr, env_d) in enumerate([
        ("Left Shoulder Look-Back", "Body rotated 90 degrees away to the right, head cranked sharply back over left bare shoulder, neck tendons visibly tensed, left clavicle and trapezius muscle prominent, spine rotation creating deep diagonal lines across torso", "Roger Deakins (Arri LF 32mm Tungsten)", "a sultry sidelong glance over left shoulder with heavy-lidded hazel eyes and parted soft black lips", "in a high-end minimalist editorial fashion studio with smooth seamless neutral warm-grey backdrop"),
        ("Right Shoulder Look-Back", "Body rotated 90 degrees away to the left, head cranked sharply back over right bare shoulder, right scapula visible behind shoulder line, neck in full rotation with sternocleidomastoid muscle engaged, chin parallel to floor", "Denis Villeneuve (Alexa 65 Anamorphic 50mm)", "an intense direct gaze over right shoulder with soft-smudged smoky eyeliner and subtle sardonic half-smile", "in an opulent private penthouse suite overlooking rainy Paris at 3 AM"),
        ("Left Shoulder 45-Deg Twist", "Body rotated 45 degrees away to the right, head turned back 60 degrees over left shoulder, creating a 105-degree total neck rotation from hip axis, left shoulder blade winging visibly, jawline parallel to collarbone", "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)", "a playful knowing half-smile with moist soft black lips and amber-gold flecks catching neon light", "standing on wet cobblestones of a Montmartre alleyway under warm amber streetlamps"),
        ("Right Shoulder 45-Deg Twist", "Body rotated 45 degrees away to the left, head turned back 60 degrees over right shoulder, right deltoid and upper trapezius in sharp relief, chin lifted slightly creating neck extension", "Helmut Newton (Hasselblad 80mm B&W High-Fashion)", "a haughty commanding look of supreme confidence with relaxed soft black lips and sharp gaze", "editorial fashion studio with smooth seamless warm-grey backdrop"),
        ("Left Shoulder Deep Arch", "Body rotated 70 degrees away to the right, lower spine arched inward, head cranked fully back over left shoulder until chin nearly touches shoulder cap, extreme neck torsion exposing full left jawline and carotid artery line", "David Fincher (Red 8K Leica 27mm Monochromatic)", "a breathless sensual expression with parted lips and dilated hazel pupils", "neutral studio backdrop with seamless dark charcoal cyclorama wall"),
        ("Right Shoulder Deep Arch", "Body rotated 70 degrees away to the left, lower spine arched inward, head cranked fully back over right shoulder, right jawline and ear fully exposed, neck in maximum rotation", "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)", "an alluring dominant gaze looking down into the camera with a subtle sardonic half-smile", "inside an opulent private French boudoir with vintage mirrors and warm ambient shadows"),
        ("Left Shoulder Seated Twist", "Seated on low stool, torso twisted 90 degrees to the right, both hands gripping knees, head turned sharply back over left shoulder, shoulder blades retracted creating deep V-taper in upper back", "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)", "a soft intimate expression with lowered eyelashes followed by a slow upward glance", "in a candlelit luxury suite with carved oak headboard and dark velvet bolsters"),
        ("Right Shoulder Seated Twist", "Seated cross-legged on floor, torso twisted 90 degrees to the left, left hand braced on floor behind, right hand on hip, head cranked back over right shoulder, oblique muscles visibly engaged", "Quentin Tarantino (Ultra Speed 40mm Punchy)", "a sharp, witty spark in her eyes paired with a confident micro-smirk", "in a luxury modern duplex with polished dark marble floors and minimalist lighting"),
        ("Left Shoulder Reclining Twist", "Reclining on left side propped on elbow, torso twisted 45 degrees toward camera, head turned sharply over left shoulder looking back, left shoulder blade prominent, right arm reaching across body", "Ridley Scott (Panavision 50mm f/1.4 Anamorphic)", "an enigmatic sidelong glance with raised eyebrow and an amused knowing half-smile", "in a private high-fashion boudoir with deep velvet drapery and warm amber rim lighting"),
        ("Right Shoulder Reclining Twist", "Reclining on right side propped on elbow, torso twisted 45 degrees toward camera, head turned sharply over right shoulder, right trapezius and deltoid in full tension", "Michael Mann (Sony CineAlta 28mm Blue Ambient)", "a sultry half-lidded bedroom gaze with lips slightly parted and delicate cheek flush", "inside a moody high-tech cybernetic sanctuary in Neo-Paris with dark brushed aluminum panels"),
        ("Left Shoulder Standing Pivot", "Standing with feet planted wide, torso pivoted 90 degrees to the right, both arms crossed behind lower back, head cranked back over left shoulder, full neck rotation exposing left carotid and jawline", "Roger Deakins (Arri LF 32mm Tungsten)", "a calm, dominant analytical focus engaging the camera directly with clean white teeth slightly visible", "in a high-end commercial fashion studio with neutral medium-grey background"),
        ("Right Shoulder Standing Pivot", "Standing with weight on back foot, torso pivoted 90 degrees to the left, right hand on hip pushing elbow back, head cranked over right shoulder, right scapula winging visibly", "Denis Villeneuve (Alexa 65 Anamorphic 50mm)", "a soft contemplative expression gazing toward the right frame with raised brow", "in an opulent private penthouse suite overlooking rainy Paris at 3 AM"),
        ("Left Shoulder Doorway Lean", "Leaning against doorframe with body angled 60 degrees away to the right, left shoulder pressed against frame, head turned back over left shoulder, neck in full rotation, left arm hanging loosely", "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)", "a subtle sardonic Jeselnik-style smirk with soft-smudged smoky eyeliner framing", "standing on wet cobblestones of a Montmartre alleyway under warm amber streetlamps"),
        ("Right Shoulder Doorway Lean", "Leaning against doorframe with body angled 60 degrees away to the left, right shoulder pressed against frame, head cranked back over right shoulder, right arm crossed over chest gripping opposite shoulder", "Helmut Newton (Hasselblad 80mm B&W High-Fashion)", "a confident micro-smirk with parted satin lips revealing clean white teeth", "editorial fashion studio with smooth seamless warm-grey backdrop"),
        ("Left Shoulder Floor Crouch", "Crouching low on both knees, torso twisted 80 degrees to the right, both hands on floor for balance, head cranked back over left shoulder, spine in deep C-curve, neck fully extended", "David Fincher (Red 8K Leica 27mm Monochromatic)", "an intense commanding stare with dilated pupils and a dangerous predatory smirk", "neutral studio backdrop with seamless dark charcoal cyclorama wall"),
    ])
]

LORA_TIER2_ANATOMY = [
    {
        "tier": "Tier 2: Raw Anatomy",
        "name": f"Anatomy Slot {i+1:02d} ({name})",
        "pose": f"Full body or medium shot capturing complete anatomical proportion. {pose_desc}",
        "expression": expr,
        "attire": attire_d,
        "env": env_d,
        "rig": rig_k,
        "physics": "realskin, authentic biological micro-textures, warm subcutaneous dermal scattering, and zero plastic smoothing"
    }
    for i, (name, pose_desc, expr, attire_d, env_d, rig_k) in enumerate([
        ("Kneeling Frontal Proportions", "Kneeling tall with spine erect, both hands resting on bare 30-inch muscular thighs, narrow 24-inch waist and flared 38-inch hips in direct frontal view, quadriceps and abdominal muscle definition visible", "a confident direct gaze with soft-smudged smoky eyeliner and subtle knowing smirk", "completely nude, bare unblemished realskin with anatomical precision", "in an intimate candlelit Parisian boudoir with obsidian black satin sheets and warm ambient shadows", "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)"),
        ("Reclining Torso 3/4 Hip Curve", "Cowboy medium shot, reclining on one elbow across satin pillows, torso twisted 30 degrees to accentuate waist-to-hip ratio and natural bust silhouette, oblique muscles tensed on one side", "a sultry half-lidded gaze looking over bare shoulder with parted soft black lips", "sheer black micro-lace bralette with delicate high-waist silk thong", "in an opulent Parisian master bedroom suite with deep crimson silk velvet bedding", "Roger Deakins (Arri LF 32mm Tungsten)"),
        ("Standing Frontal Contrapposto", "Full body shot from head to toe, standing in natural contrapposto with weight on right hip, hands resting on waistline, showing athletic leg definition and 0.66 waist-to-hip ratio", "a dominant poised expression with arched sable brows and direct eye contact", "completely nude, bare realskin with natural biological dermal tones", "high-end commercial fashion studio with neutral medium-grey background", "David Fincher (Red 8K Leica 27mm Monochromatic)"),
        ("Standing 3/4 Rear Arch", "Full body three-quarter rear silhouette, standing with arched lower spine, one hand on hip, head turned back over shoulder, 38-inch hip curve and 30-inch thighs in profile", "an alluring sidelong glance with smudged smoky eyeliner and enigmatic half-smile", "bare realskin, strapless micro string bikini bottom accentuating hip contour", "in a luxury penthouse suite overlooking rainy Paris skyline at 3 AM", "Denis Villeneuve (Alexa 65 Anamorphic 50mm)"),
        ("Steamy Bath Reclining", "Medium close shot, reclining in marble clawfoot tub, arms resting along rim, bare wet collarbone and shoulders glistening with water droplets, chest partially submerged", "a relaxed breathless sensual expression with head tilted back and parted lips", "completely nude, wet bare realskin glistening under soft amber light", "in a steamy private marble bathroom with oversized clawfoot tub and warm atmospheric mist", "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)"),
        ("Seated Cross-Legged Torso", "Cowboy medium shot, seated cross-legged on polished floor with straight spine, hands resting on knees, showing defined ribcage, waist, and quadriceps symmetry", "a calm serene analytical expression engaging the camera directly", "minimalist charcoal silk slip unbuttoned revealing bare chest", "concrete minimalist photo studio with smooth polished grey floor", "Roger Deakins (Arri LF 32mm Tungsten)"),
        ("Side Lying Hip Curve", "Full body horizontal shot, lying on side with legs loosely stacked, top hip pushed forward, hand tracing waist curve, 0.66 ratio clearly visible", "a dreamy bedroom expression with heavy-lidded hazel eyes", "completely nude, bare unblemished realskin", "reclining across a vintage velvet chaise lounge beside marble fireplace", "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)"),
        ("Athletic Stretch Overhead", "Full body shot, standing tall stretching arms overhead with fingers interlaced, elongating torso and ribcage, narrow waist and athletic abs visible", "a playful confident smile with clean white teeth", "minimalist black silk micro-harness top and sheer bottoms", "neutral studio backdrop with seamless dark charcoal cyclorama wall", "Helmut Newton (Hasselblad 80mm B&W High-Fashion)"),
        ("All-Fours Arched Spine", "Medium full shot, propped on hands and knees with arched spine, weight on hands, showing muscular shoulders, narrow waist, and flared hips", "an intense commanding stare with dilated pupils and soft-smudged smoky kohl liner", "completely nude, bare realskin", "in a private high-fashion boudoir with deep velvet drapery", "Quentin Tarantino (Ultra Speed 40mm Punchy)"),
        ("Seated Forward Lean", "Cowboy shot, leaning forward with elbows on knees, resting chin on palm, gazing intensely up at camera, chest and collarbone prominent", "an alluring intimate gaze with parted soft black lips and amber flecks", "open silk robe draped off bare shoulders and chest", "in a candlelit luxury suite with carved oak headboard", "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)"),
    ])
]

LORA_TIER3_WARDROBE = [
    {
        "tier": "Tier 3: Wardrobe Agnosticism",
        "name": f"Wardrobe Slot {i+1:02d} ({name})",
        "pose": pose_d,
        "expression": expr_d,
        "attire": attire_text,
        "env": env_text,
        "rig": rig_key,
        "physics": physics_text
    }
    for i, (name, pose_d, expr_d, attire_text, env_text, rig_key, physics_text) in enumerate([
        ("Emerald Velvet Gown", "Dynamic full-length shot, descending ornate marble staircase in motion, gown train trailing behind, glancing back over one shoulder", "a regal high-fashion editorial gaze with neutral soft black lips", "Wearing an emerald-green liquid velvet backless evening gown with plunging cowl neckline", "in a grand Parisian opera house foyer with gilded balustrades and crystal chandeliers", "Helmut Newton (Hasselblad 80mm B&W High-Fashion)", "heavy silk velvet drapery in fluid motion with authentic micro-creasing and soft specular sheen"),
        ("Ivory Power Suit", "Low-angle three-quarter standing shot looking slightly down at camera, hands hooked in trouser pockets, blazer falling open", "an authoritative commanding expression with sharp analytical eye contact", "Wearing an impeccably tailored cream-ivory linen double-breasted suit open over black chantilly lace bralette", "in an ultra-modern glass-walled office suite overlooking rainy Paris twilight", "David Fincher (Red 8K Leica 27mm Monochromatic)", "textured crisp Italian linen fabric with visible weave and natural drape"),
        ("Cobalt Moto Jacket & Denim", "Candid medium shot, leaning back against a vintage cafe window with one knee bent, holding espresso", "a candid unguarded laugh with natural eye crinkles and white teeth", "Wearing a cobalt-blue distressed leather motorcycle jacket over white cropped ribbed tank and light-wash ripped selvedge denim", "outside a bustling Montmartre sidewalk cafe with wet bistro chairs and neon pavement reflections", "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)", "distressed light denim texture with visible cotton grain, rich blue leather sheen with surface creasing"),
        ("Scarlet Latex & Cigarette Pants", "Dramatic side profile shot, head turned sharply to camera with chin lifted, arching back to emphasize hourglass silhouette", "a sharp calculating stare with glossy soft black lips and soft-smudged smoky eyeliner", "Wearing a high-gloss liquid scarlet-red latex underwire corset top with matte charcoal cigarette trousers", "inside a moody high-tech cybernetic corridor in Neo-Paris with brushed titanium walls and blue LED shafts", "Michael Mann (Sony CineAlta 28mm Blue Ambient)", "high-gloss scarlet latex catching razor-sharp specular highlights and ray-traced neon reflections"),
        ("Lace Corset & Gold Palazzo", "Reclining full-length shot, lounging diagonally across antique velvet chaise, one arm draped over backrest", "an alluring intimate gaze with a subtle knowing half-smile", "Wearing a structured obsidian French chantilly lace corset with sheer side panels and champagne-gold silk palazzo trousers", "in an intimate Marais boudoir beside a roaring marble fireplace with antique gilded mirrors", "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)", "delicate French chantilly lace openwork casting lattice shadows onto realskin, fluid silk pooled on velvet"),
        ("Champagne Silk Slip", "High-angle shot looking down from above, seated on deep window sill with knees pulled to chest, rain-streaked glass behind", "a soft dreamy contemplative gaze with relaxed soft black lips", "Wearing a champagne-gold fluid silk charmeuse slip dress with spaghetti straps and plunging open back", "in a luxury penthouse overlooking rainy Paris skyline at 3 AM through floor-to-ceiling glass", "Denis Villeneuve (Alexa 65 Anamorphic 50mm)", "luxurious fluid silk charmeuse with high specular sheen rippling over biological contours"),
        ("Camel Cashmere & Shorts", "Intimate seated close-to-medium shot, sitting cross-legged on plush sheepskin rug, leaning forward on elbows", "a cozy unguarded expression with tousled ringlet curls falling across one eye", "Wearing an oversized slouchy camel-beige chunky cable-knit cashmere sweater slipping off one shoulder over heather-grey jersey shorts", "in a sunlit Haussmann loft with raw oak herringbone floors and warm morning sunbeams", "Roger Deakins (Arri LF 32mm Tungsten)", "tactile brushed wool fibers and thick cable-knit yarn texture with visible fuzzy halo"),
        ("Crimson Kimono & Lace", "Three-quarter action shot, walking toward camera while gathering lapels of billowing silk kimono in mid-stride", "a sultry seductive bedroom gaze with parted soft black lips", "Wearing a vibrant crimson silk floral jacquard kimono robe with gold dragon embroidery over black lace lingerie", "in a candlelit luxury suite with dark carved mahogany headboard and bronze floor candelabras", "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)", "translucent sheer lace tension revealing warm realskin texture, fluid crimson silk with motion blur"),
        ("Gothic Frock Coat & Leather", "Low-angle wide shot, standing on wet stone bridge parapet at night, heavy coat draped over shoulders like cape", "a majestic brooding expression with calm regal poise", "Wearing a structured charcoal-grey brocade tailored frock coat over tight black lambskin leather pants", "on Pont Alexandre III in Paris under ornate golden gaslamps with mist rising off the Seine", "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)", "heavy textured brocade absorbing ambient light, polished lambskin leather catching amber streetlight reflections"),
        ("White Linen & Cutoffs", "Dynamic outdoor shot, strolling barefoot along riverbank, sleeves rolled up, hair caught in breeze", "a radiant sun-kissed grin with vibrant eyes and windswept curls", "Wearing an oversized crisp white linen shirt unbuttoned over terracotta bikini top and cutoff denim shorts", "along the sun-drenched Seine river quayside with weeping willows and dappled afternoon light", "Roger Deakins (Arri LF 32mm Tungsten)", "breathable open-weave white linen with crisp sunlit transparency, textured denim frays"),
        ("Black Vinyl Trench", "Dynamic walking street snapshot, striding forward through heavy rain with umbrella tilted back", "a sharp intense editorial gaze focused forward with dark berry lips", "Wearing a high-gloss black vinyl belted trench coat with patent leather thigh-high boots", "on glistening wet Boulevard Saint-Germain at night with neon sign reflections", "Helmut Newton (Hasselblad 80mm B&W High-Fashion)", "wet liquid vinyl surface with micro-water rivulets and crisp anamorphic light streaks"),
        ("Sapphire Velvet Bustier", "Seated 3/4 shot, sitting backwards on vintage bistro stool with one elbow on bar counter, chin in hand", "a playful sardonic half-smile with knowing arched brow", "Wearing a structured royal sapphire-blue silk velvet boned bustier with black silk midi skirt and high leg slit", "inside an atmospheric 1920s Art Deco cocktail lounge with brass fixtures and dark walnut bar", "Michael Mann (Sony CineAlta 28mm Blue Ambient)", "deep pile sapphire velvet catching rich blue highlights on ridges, liquid silk skirt drape"),
        ("Ribbed Crop Top & Cargoes", "Urban street shot, crouching on one knee in athletic stance on cobblestones, looking up at camera", "a cool relaxed confident expression with intense gaze", "Wearing a sleeveless heather-grey ribbed athletic crop top exposing flat midriff with olive technical cargo trousers", "in a narrow industrial alleyway with exposed brickwork, iron fire escapes, and volumetric mist", "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)", "stretchy ribbed cotton hugging torso contours, heavy ripstop canvas fabric with authentic stitch details"),
        ("Gold Lamé Gown", "Full-length fashion editorial shot, arching spine gracefully with one arm raised brushing hair back", "a haughty commanding look of supreme elegance with sculpted cheekbones", "Wearing a liquid metallic molten-gold lamé asymmetrical one-shoulder evening gown with thigh-high slit", "in a minimalist marble gallery hall with tall arched windows and dramatic golden light shafts", "Denis Villeneuve (Alexa 65 Anamorphic 50mm)", "molten liquid gold lamé reflecting undulating warm highlights across body contours"),
        ("Breton Stripe & Scarf", "Intimate close-to-medium portrait, leaning forward over outdoor cafe table with hands clasped under chin", "an intelligent curious look with tilted head and playful smirk", "Wearing an authentic navy-and-cream Breton striped boatneck jersey top with small red silk neck scarf", "at a Parisian street corner cafe under a deep red awning with blurred pedestrian bokeh", "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)", "soft knitted French cotton jersey with sharp stripe geometry wrapping bust curvature"),
    ])
]

LORA_TIER4_SPATIAL = [
    {
        "tier": "Tier 4: 3D Spatial Awareness",
        "name": f"Spatial Slot {i+1:02d} ({name})",
        "pose": f"Full body shot from head to toe capturing complete spatial perspective. {pose_desc}",
        "expression": expr_d,
        "attire": attire_d,
        "env": env_d,
        "rig": rig_k,
        "physics": "realskin, dynamic motion physics, crisp ringlet inertia, and authentic spatial depth"
    }
    for i, (name, pose_desc, expr_d, attire_d, env_d, rig_k) in enumerate([
        ("Dynamic Walking Forward", "Walking confidently forward in mid-stride, 3B/3C indigo curls swaying with dynamic inertia, complete footwear and feet visible from head to toe", "a calm dominant analytical focus looking forward past the camera", "Wearing a tailored charcoal wool trench coat open over black silk camisole and trousers with leather boots", "standing on the wet cobblestones of a Montmartre alleyway at 2 AM with glistening reflections", "Denis Villeneuve (Alexa 65 Anamorphic 50mm)"),
        ("Back View Ringlet Volume", "Viewed directly from behind, head turned slightly away, voluminous 3B/3C spiral ringlets cascading down spine to mid-back with electric indigo highlights", "subtle side profile silhouette visible glancing away from camera", "backless black silk gown exposing bare sculpted spine and shoulder blades", "on an intimate wrought-iron balcony overlooking rainy zinc rooftops of Paris", "Roger Deakins (Arri LF 32mm Tungsten)"),
        ("Walk Away Look Back", "Body oriented away while walking, head sharply turned back looking directly over bare shoulder, showing back curvature and facial connection", "a sultry teasing glance over shoulder with smudged soft-smudged smoky eyeliner", "tight black ribbed knit midi dress with deep open back and ankle boots", "under the wrought-iron arches of a secluded Parisian passage covered gallery", "Wong Kar-Wai (Cooke 40mm f/1.4 Neon)"),
        ("Dynamic Feline Crouch", "Crouching low to the floor in powerful athletic stance, weight on balls of feet, one hand touching ground, knees apart framing athletic thighs", "an intense predatory direct stare with dilated hazel-green pupils", "fitted black matte technical bodysuit with mesh side panels and combat boots", "inside a moody high-tech cybernetic sanctuary with dark brushed aluminum panels and floor mist", "Michael Mann (Sony CineAlta 28mm Blue Ambient)"),
        ("Bird's Eye Overhead", "From high camera angle directly above, reclining on round velvet daybed with arms extended, chin lifted looking straight up into overhead lens", "an intense mesmerizing gaze directed straight up into the camera", "emerald silk slip dress draped across daybed cushions with bare arms and legs", "in an antique French rococo salon with gilded plaster moldings and crystal chandeliers", "Quentin Tarantino (Ultra Speed 40mm Punchy)"),
        ("Worm's Eye Upward", "From dramatic low camera angle near floor level looking upward, standing tall in authoritative stance with one foot forward", "a dominant haughty expression with raised eyebrow and piercing almond hazel eyes", "tailored black double-breasted power suit with wide-leg trousers pooling over heels", "in an avant-garde architectural photography studio with concrete columns and light shafts", "David Fincher (Red 8K Leica 27mm Monochromatic)"),
        ("Full Contrapposto Standing", "Standing in classic contrapposto stance with full 5'5\" height against architectural background, complete head-to-shoe framing", "a calm confident smile with warm golden-olive complexion and intelligent gaze", "black cashmere turtleneck tucked into high-waisted pleated wool trousers with oxford shoes", "in an opulent penthouse suite with floor-to-ceiling glass and double-height ceilings", "Roger Deakins (Arri LF 32mm Tungsten)"),
        ("Knees Drawn to Chest", "Sitting flat on floor with knees drawn tightly to chest, arms wrapped around shins, head resting on knees looking sideways", "a contemplative intimate expression with soft eyes and relaxed soft black lips", "oversized white French linen button-down shirt loosely draped over bare legs", "in a luxury Parisian pied-a-terre with herringbone parquet floors and soft morning light", "Stanley Kubrick (Zeiss 50mm f/0.7 Candlelit)"),
        ("Mid-Motion Dynamic Turn", "Caught in dynamic motion turning around quickly as if called by name, ringlets swirling through air with motion blur on tips", "a candid surprised expression with wide captivating hazel eyes and parted lips", "fitted leather biker jacket over crimson silk slip with dark denim jeans", "on Pont Alexandre III bridge overlooking Seine at blue hour with glowing monuments", "Ridley Scott (Panavision 50mm f/1.4 Anamorphic)"),
        ("Floor Reclining Horizon", "Lying flat on back across dark hardwood flooring, arms splayed above head, one knee bent, head turned toward camera at ground level", "a dreamy sensual daze with parted soft black lips and amber flecks catching light", "black silk slip with delicate lace trim, bare feet and legs fully framed", "in a private Parisian atelier apartment with moonlight beams through tall windows", "Gordon Willis (Baltar 50mm f/2.0 Low-Key Sepia)"),
    ])
]

NEGATIVE_PROMPT_DEFAULT = ""

DIRECTOR_CAMERA_RIGS = [
    "Quentin Tarantino (Ultra Speed 40mm Punchy)",
    "Denis Villeneuve (Atmospheric 85mm Diffused Softbox)",
    "Helmut Newton (Hard Monochromatic Flash 50mm)",
    "Roger Deakins (Volumetric Natural Light 35mm)",
    "David Fincher (Clinical Symmetrical Macro 100mm)",
    "🎲 Dynamic Director Rig Rotation"
]

SCENE_ENVIRONMENTS = [
    "Minimal Studio (Pure Cyclorama)",
    "Brutalist Concrete Chamber",
    "Opulent Neoclassical Interior",
    "Neo-Noir Cyber Streetscape",
    "Warm Atmospheric Penthouse"
]

SCENE_WEATHERING_PRESETS = [
    "heavy volumetric fog",
    "torrential rain and puddles",
    "floating embers and ash",
    "golden hour dust motes",
    "thick atmospheric mist",
    "gentle snowfall",
    "steam rising from warm surfaces",
    "pollen and soft haze",
    "ground fog",
    "drizzle and water droplets",
    "warm amber backlight haze",
    "cool blue rim light fog",
    "sharp specular sunlight shafts",
    "soft diffused overcast light"
]

SKIN_PHYSICS_MODIFIERS = [
    "Raw Macro Epidermal Pores (Dry Realskin)",
    "Subsurface Dermal Scattering & Gloss",
    "Perspiration Micro-Beads & Hydro-Sheen"
]

WARDROBE_PRESETS = [
    "🔞 Full Nudity (Anatomical Precision, Bare Realskin)",
    "👙 Minimal Lingerie & Sheer Silk",
    "👗 High-End Couture & Evening Wear",
    "🧥 Tailored Business & Structural Overcoats",
    "👟 Casual Urban & Streetwear",
    "🎲 Dynamic Multi-Wardrobe Cycle"
]
# --- SURGICAL OVERRIDES ---
flat_lighting = "Even softbox studio lighting, 85mm portrait lens, neutral grey background, flat illumination."

for key in DIRECTOR_RIG_CONFIGS:
    DIRECTOR_RIG_CONFIGS[key]["lighting"] = flat_lighting
    DIRECTOR_RIG_CONFIGS[key]["camera"] = "85mm portrait lens"
    DIRECTOR_RIG_CONFIGS[key]["lut"] = "flat illumination"

for key in ENVIRONMENTS_MAP:
    ENVIRONMENTS_MAP[key] = [flat_lighting] * len(ENVIRONMENTS_MAP[key])

for anchor in LORA_TIER1_ANCHORS:
    anchor["env"] = flat_lighting
    anchor["rig"] = "Even softbox studio lighting" # Or we let rig point to the updated DIRECTOR_RIG_CONFIGS

for anchor_list in [LORA_TIER2_ANATOMY, LORA_TIER3_WARDROBE, LORA_TIER4_SPATIAL]:
    for anchor in anchor_list:
        anchor["env"] = flat_lighting
        anchor["rig"] = "Even softbox studio lighting"

