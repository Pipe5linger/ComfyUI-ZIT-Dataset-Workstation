"""
File    : zit_nodes.py
Purpose : Main ComfyUI Node execution engine with dynamic character injection.
"""
from .zit_data import LORA_TIER1_ANCHORS # (and your other arrays)

class ZITMasterPromptWorkstation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # These two new string inputs allow ANY user to use your matrices
                "subject_trigger": ("STRING", {"default": "trigger_word, 1girl", "multiline": False}),
                "subject_anatomy": ("STRING", {"default": "detailed skin texture, specific body type", "multiline": True}),
                
                # Your existing inputs
                "matrix_tier": (["Tier 1 (Anchors)", "Tier 2 (Anatomy)", "Tier 3 (Wardrobe)", "Tier 4 (Spatial)"],),
                "generation_index": ("INT", {"default": 1, "min": 1, "max": 250, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("master_prompt", "filename_prefix")
    FUNCTION = "generate_matrix"
    CATEGORY = "ZIT Dataset Engineering"

    def generate_matrix(self, subject_trigger, subject_anatomy, matrix_tier, generation_index):
        # 1. Select the correct dictionary from your list based on the index
        # (This uses your existing modulo slicing logic)
        
        # Example dummy fetch:
        raw_data = LORA_TIER1_ANCHORS[0] # Fetch actual based on your index logic

        # 2. INJECT the user's custom character into your matrix template
        final_pose = raw_data["pose"].format(subject=subject_trigger)
        final_physics = raw_data["physics"].format(anatomy=subject_anatomy)

        # 3. Assemble the prompt
        master_prompt = f"{final_pose}, {raw_data['expression']}, {raw_data['attire']}, {raw_data['env']}, {raw_data['rig']}, {final_physics}"
        
        # 4. Generate the clean filename prefix
        filename_prefix = f"{subject_trigger.split(',')[0].strip()}_{raw_data['tier']}_{generation_index:05d}"

        return (master_prompt, filename_prefix)

# ComfyUI Registration
NODE_CLASS_MAPPINGS = {
    "ZITMasterPromptWorkstation": ZITMasterPromptWorkstation
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ZITMasterPromptWorkstation": "ZIT Dataset Matrix Workstation"
}