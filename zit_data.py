"""
File    : zit_data.py
Purpose : Universal 4-Tier Dataset Generation Matrices.
"""

# We remove hardcoded character traits and replace them with {subject} and {anatomy}
# These will be dynamically filled by the ComfyUI node during execution.

LORA_TIER1_ANCHORS = [
    {
        "tier": "tier1_anchor",
        "name": f"Anchor {i+1:03d}",
        "pose": "looking over bare shoulder, extreme 90-degree side profile, {subject} head turned sharply back toward the camera",
        "expression": "neutral intense gaze, focused macro eye contact, detailed micro-expressions",
        "attire": "bare shoulders, minimal framing",
        "env": "studio softbox lighting, absolute black background",
        "rig": "Denis Villeneuve cinematic lighting, 85mm lens, tight macro focus",
        "physics": "soft light falloff, visible skin texture, {anatomy}"
    }
    for i in range(75) # (Note: You will paste your 75 unique poses here, just swap your character details for {subject} and {anatomy})
]

LORA_TIER2_ANATOMY = [
    {
        "tier": "tier2_anatomy",
        "name": f"Anatomy {i+1:03d}",
        "pose": "full body standing, 45-degree angle, {subject} shifting weight onto one leg",
        "expression": "relaxed",
        "attire": "athletic activewear, tight-fitting form reference",
        "env": "bright clinical studio, white infinite cyclorama",
        "rig": "Helmut Newton high-contrast strobe, 50mm lens",
        "physics": "clear structural ratios, sharp shadow definition, {anatomy}"
    }
    for i in range(50) # (Paste your 50 unique anatomy tuples here)
]

# Do the same for Tier 3 (Wardrobe) and Tier 4 (Spatial)