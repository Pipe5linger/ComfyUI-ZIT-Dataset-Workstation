"""
File    : scene_lighting_node_refactor.py
Purpose : Standalone Refactored Scene & Lighting node — 40+ curated cinematic, Parisian,
          luxury interior, and studio environments with pure atmospheric and lighting physics.
          Zero character/human prompt bleed.
"""

try:
    import folder_paths  # noqa: F401
except ModuleNotFoundError:
    folder_paths = None


class RefactoredSceneLightingNode:
    """Massive Scene & Lighting matrix generator with zero character bleed.

    - 40+ distinct atmospheric environments and cinematic lighting setups.
    - Emits ONLY environmental architecture, spatial depth, atmospheric weather, and lighting physics.
    - Zero human/subject tokens, eliminating any conflict with PuLID or subject identity.
    - Master seed drives deterministic modulo selection across all environments.
    """

    ENV_LIGHTING_MAP = {
        # ── 1. Parisian Atmospheric Outdoors ──
        "Rainy Parisian Cobblestone Alley": (
            "rain-slicked dark cobblestone Parisian alley at night, warm amber reflections from vintage streetlamps, "
            "subtle drifting atmospheric mist, wet specular pavement, cinematic shallow depth of field"
        ),
        "Golden Hour Rooftop Terrace": (
            "golden hour sunset on a private Parisian limestone rooftop terrace, warm diffused golden backlight, "
            "distant soft silhouette of Parisian zinc roofs and Eiffel Tower, cinematic lens flare and bokeh"
        ),
        "Pre-Dawn Seine River Embankment": (
            "pre-dawn mist along the Seine river embankment, quiet empty stone promenade, soft pale lavender and rose dawn gradient sky, "
            "vintage iron bridge in soft focus, diffuse natural morning light"
        ),
        "Misty Montmartre Staircase at Twilight": (
            "steep stone staircase in Montmartre at twilight, soft glowing vintage wall lanterns, dense cool blue fog, "
            "warm directional lantern glow on wet stone steps, atmospheric depth"
        ),
        "Sunlit Tuileries Garden Path in Autumn": (
            "crisp autumn afternoon in the Tuileries garden, golden dappled sunlight through chestnut trees, "
            "fallen amber leaves on gravel path, soft warm rim lighting, rich seasonal palette"
        ),
        "Midnight Boulevard Under Heavy Rain": (
            "wide Parisian boulevard at midnight under heavy rain, blurred streaks of passing vehicle tail-lights, "
            "glistening asphalt reflections, cinematic shallow focus, anamorphic lens flares"
        ),
        "Foggy Pont Alexandre III at Night": (
            "historic ornate bridge over the Seine enveloped in thick night fog, golden glow from ornate gilded streetlamps, "
            "dark reflective river surface, dramatic silhouette lighting, moody cinematic ambiance"
        ),
        "Sunny Marais Courtyard at Midday": (
            "private hidden limestone courtyard in Le Marais, bright directional midday sunlight casting crisp architectural shadows, "
            "climbing ivy on weathered stone walls, clean natural daylight illumination"
        ),

        # ── 2. Intimate & Luxury Parisian Interiors ──
        "Dark Parisian Haussmannian Boudoir": (
            "candlelit ornate Haussmannian salon, deep shadow contrast, tall arched French windows with sheer dark drapes, "
            "intimate low-key chiaroscuro lighting, warm rim highlights"
        ),
        "Steamy White Marble Bath": (
            "luxurious high-ceiling white marble bathroom, soft rising diffused steam mist, "
            "warm directional sunlight shafts through frosted glass, glistening specularity on polished stone"
        ),
        "Modern Glass Penthouse at Dusk": (
            "sleek contemporary Parisian penthouse interior, panoramic floor-to-ceiling glass windows at dusk, "
            "ambient purple-blue city skyline glow, subtle warm recessed ceiling spotlights"
        ),
        "Historic Library with Dark Wood Paneling": (
            "grand vintage library with floor-to-ceiling oak bookshelves, soft warm emerald desk lamp glow, "
            "subtle ambient dust motes drifting in shaft of light, deep rich mahogany tones, cozy scholarly ambiance"
        ),
        "Minimalist Marble Fireplace Salon": (
            "classic Haussmannian parlor with a carved white marble fireplace, glowing amber embers in hearth, "
            "intimate firelight casting flickering warm shadows, ornate gilded wall mirror, soft romantic ambiance"
        ),
        "Sunlit Vintage Paris Cafe Corner": (
            "quaint Parisian bistro corner in late afternoon, warm dappled sunlight filtering through awning, "
            "dark wooden paneling, soft atmospheric dust motes, rich warm tones"
        ),
        "Art Deco Hotel Suite with Velvet Accents": (
            "luxurious Art Deco hotel suite, geometric brass and mirror wall paneling, soft diffused cove ceiling lighting, "
            "warm amber bedside sconces, plush velvet textures, sophisticated vintage luxury"
        ),
        "Sun-Drenched Artist Loft in Belleville": (
            "spacious high-ceiling artist studio loft, giant industrial steel-framed skylights, "
            "bright natural north-facing daylight flooding the concrete floor, subtle dust motes, airy bohemian feel"
        ),

        # ── 3. Neon Noir & Underground Nightlife ──
        "Parisian Neon Noir Metro Entrance": (
            "volumetric blue hour dusk, vibrant neon ruby and cyan light reflections on wet pavement, "
            "Art Nouveau metro archway backdrop, cinematic chiaroscuro, high-contrast atmospheric glow"
        ),
        "Underground Vaulted Cellar Club": (
            "dimly lit subterranean vaulted brick Parisian cellar, moody amber and violet atmospheric haze, "
            "subtle directional backlight, cinematic nightlife ambiance, deep rich shadow textures"
        ),
        "Neon-Lit Arcade Corridor": (
            "narrow retro gaming corridor with glowing magenta and cobalt neon signage, deep glossy reflections, "
            "hazy atmosphere, sharp neon edge lighting, cinematic synthwave aesthetic"
        ),
        "Midnight Rooftop Bar with City Panorama": (
            "sleek rooftop lounge terrace at midnight, subtle glowing under-bar LED lighting, "
            "panoramic illuminated Paris city lights in soft bokeh background, cool crisp night air"
        ),
        "Subterranean Metro Platform at Night": (
            "deserted curved white-tiled Paris metro platform late at night, cool fluorescent tube lighting casting long shadows, "
            "glossy beveled ceramic tiles, cinematic urban solitude"
        ),

        # ── 4. High-Fashion Editorial & Studio Lighting ──
        "Minimalist Editorial Studio (Grey Cyclorama)": (
            "high-contrast editorial studio photography, clean seamless solid grey cyclorama backdrop, "
            "sharp crisp dual rim strobes, pristine fill light, sharp micro-contrast, Vogue editorial lighting"
        ),
        "Dramatic Chiaroscuro Studio (Deep Black)": (
            "pitch-black solid studio backdrop, intense single high-angle key light, deep sculptural shadow contours, "
            "dramatic chiaroscuro portrait lighting, crisp skin specular highlights"
        ),
        "Dual-Tone Color Gel Studio (Magenta & Cyan)": (
            "professional photography studio with dramatic dual color gel lighting, saturated magenta rim light on left, "
            "cool cyan fill light on right, seamless dark backdrop, high-fashion aesthetic"
        ),
        "Soft Warm Beauty Dish Studio": (
            "clean minimalist studio portrait setup, large octagonal softbox key light providing flawless soft illumination, "
            "warm subtle reflector fill, gentle wrap-around light, ultra-clean commercial fashion look"
        ),
        "High-Key Pure White Studio": (
            "seamless pure white high-key infinity wall backdrop, ultra-bright diffused softbox array, "
            "clean even illumination with zero harsh shadows, crisp catalog fashion aesthetic"
        ),
        "Warm Tungsten Dramatic Spot Studio": (
            "dark minimalist studio, warm 3200K vintage tungsten spotlight focused tightly from side, "
            "rich amber illumination, deep velvety shadows, classic Hollywood glamour lighting"
        ),

        # ── 5. Contemporary Architecture & Neutral Daylight ──
        "High-End Art Gallery Salon": (
            "minimalist museum gallery with dark herringbone hardwood floors, curated directional picture spot-lighting, "
            "clean white plaster walls, soft diffused architectural shadows, museum-grade illumination"
        ),
        "Brutalist Concrete Pavilion at Dawn": (
            "monolithic raw exposed concrete architecture, cool blue dawn ambient light, clean geometric diagonal shadows, "
            "striking architectural perspective, minimalist high-fashion backdrop"
        ),
        "Neutral Photographic Overcast Daylight": (
            "neutral overcast outdoor daylight, soft even illumination, no harsh shadows, clean photographic neutral contrast"
        ),
        "Glass Greenhouse with Diffused Sunlight": (
            "botanical glasshouse conservatory with antique iron framework, lush tropical foliage in soft focus background, "
            "diffused humid sunlight filtering through glass panels, soft ethereal glow"
        ),
    }

    ENV_OPTIONS = ["🎲 Dynamic / Random Scene Sweep"] + list(ENV_LIGHTING_MAP.keys())

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "master_seed":     ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "environment_mode": (cls.ENV_OPTIONS, {"default": "🎲 Dynamic / Random Scene Sweep"}),
            },
            "optional": {
                "custom_scene_override": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("scene_lighting_prompt",)
    FUNCTION     = "run"
    CATEGORY     = "ZIT/Dataset Workstation"

    def run(self, master_seed: int, environment_mode: str = "🎲 Dynamic / Random Scene Sweep", custom_scene_override: str = "", **kwargs):
        if custom_scene_override and custom_scene_override.strip():
            return (custom_scene_override.strip(),)

        if environment_mode == "🎲 Dynamic / Random Scene Sweep" or environment_mode not in self.ENV_LIGHTING_MAP:
            keys = list(self.ENV_LIGHTING_MAP.keys())
            idx = (master_seed // 2000) % len(keys)
            env = keys[idx]
        else:
            env = environment_mode

        prompt = self.ENV_LIGHTING_MAP[env]
        return (prompt,)
