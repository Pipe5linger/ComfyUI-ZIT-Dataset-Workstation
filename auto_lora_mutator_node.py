import os
import json
import torch
import folder_paths
import comfy.sd
from comfy.utils import load_torch_file

class AutoLoRAMutatorNode:
    """
    Acts as the 'Daemon / Mutator' that takes the Critic's advice (formatted as JSON) 
    and dynamically applies the recommended LoRAs directly to the MODEL and CLIP.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "critic_advice": ("STRING", {"multiline": True, "forceInput": True}),
                "active": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "applied_log")
    FUNCTION = "run"
    CATEGORY = "ZIT/Dataset Workstation"

    def run(self, model, clip, critic_advice, active):
        if not active:
            return (model, clip, "MUTATOR BYPASSED: Active is False.")

        # 1. Parse the JSON payload from the critic advice
        # We look for a JSON array block inside the text.
        json_str = None
        try:
            if "[" in critic_advice and "]" in critic_advice:
                start = critic_advice.rindex("[")
                end = critic_advice.rindex("]") + 1
                json_str = critic_advice[start:end]
                lora_list = json.loads(json_str)
            else:
                lora_list = []
        except Exception as e:
            return (model, clip, f"MUTATOR PARSE ERROR: Could not find valid JSON array in critic advice.\n{e}")

        if not lora_list:
            return (model, clip, "MUTATOR WARNING: No LoRAs parsed from critic advice.")

        log_lines = ["👑 [AUTO LORA MUTATOR - DYNAMIC INJECTION]"]
        
        # 2. Iteratively load and apply each LoRA
        current_model = model
        current_clip = clip
        
        for lora_item in lora_list:
            lora_name = lora_item.get("name")
            strength = float(lora_item.get("strength", 1.0))
            
            if not lora_name:
                continue
                
            lora_path = folder_paths.get_full_path("loras", lora_name)
            if not lora_path or not os.path.exists(lora_path):
                log_lines.append(f"❌ FAILED: '{lora_name}' not found on disk.")
                continue

            try:
                lora_weights = load_torch_file(lora_path, safe_load=True)
                current_model, current_clip = comfy.sd.load_lora_for_models(
                    current_model, current_clip, lora_weights, strength, strength
                )
                log_lines.append(f"✅ APPLIED: {lora_name} @ {strength:.2f}")
            except Exception as e:
                log_lines.append(f"❌ ERROR loading {lora_name}: {str(e)}")

        return (current_model, current_clip, "\n".join(log_lines))

