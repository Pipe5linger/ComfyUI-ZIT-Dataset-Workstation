"""
Node    : DynamicBackboneLoader
Package : ComfyUI-Vespera-ZIT
Purpose : In-Canvas Dynamic UNet & CLIP Model Matrix Loader with Round-Robin Rotation and Dedicated Disk Logging.
"""

import os
import json
import time
import datetime
import random
import torch

class DynamicBackboneLoaderNode:
    _GLOBAL_QUEUE_INDEX = 0

    # HARD BLACKLIST: Models known to cause VRAM hangs, thrashing, or execution halts
    BLACKLISTED_MODELS = {
        "Huihui-Qwen3-VL-4B-Instruct-abliterated-fp8_scaled.safetensors": "Known to cause text encoder hang & 450s+ PCIe thrashing with Lumina2",
    }

    CURATED_PAIRS = [
        {
            "tag": "FP8_KJ_x_Qwen3_Mixed",
            "name": "1️⃣ Z-Image-Turbo (FP8-KJ) + Qwen 3.4B (FP8-Mixed)",
            "unet": "z-image-turbo_fp8_scaled_e4m3fn_KJ.safetensors",
            "clip": "qwen_3_4b_fp8_mixed.safetensors",
            "weight_dtype": "default",
            "clip_type": "lumina2"
        },
        {
            "tag": "BF16_x_Qwen3_Mixed",
            "name": "2️⃣ Z-Image-Turbo (BF16 Master) + Qwen 3.4B (FP8-Mixed)",
            "unet": "z_image_turbo_bf16.safetensors",
            "clip": "qwen_3_4b_fp8_mixed.safetensors",
            "weight_dtype": "default",
            "clip_type": "lumina2"
        },
        {
            "tag": "FP8_KJ_x_HereticQwen3",
            "name": "3️⃣ Z-Image-Turbo (FP8-KJ) + Qwen3-VL-Heretic (v10)",
            "unet": "z-image-turbo_fp8_scaled_e4m3fn_KJ.safetensors",
            "clip": "qwen3VLInstruct4bHeretic_v10.safetensors",
            "weight_dtype": "default",
            "clip_type": "lumina2"
        },
        {
            "tag": "BF16_x_HereticQwen3",
            "name": "4️⃣ Z-Image-Turbo (BF16 Master) + Qwen3-VL-Heretic (v10)",
            "unet": "z_image_turbo_bf16.safetensors",
            "clip": "qwen3VLInstruct4bHeretic_v10.safetensors",
            "weight_dtype": "default",
            "clip_type": "lumina2"
        }
    ]

    @classmethod
    def INPUT_TYPES(s):
        mode_options = [
            "🔄 Sequential Round-Robin (Cycles 1 ➔ 2 ➔ 3 ➔ 4)",
            "🎲 Stochastic Wildcard (50/50 Random Backbone Roll)",
            "1️⃣ Fixed: Z-Image-Turbo (FP8-KJ) + Qwen 3.4B (FP8-Mixed)",
            "2️⃣ Fixed: Z-Image-Turbo (BF16) + Qwen 3.4B (FP8-Mixed)",
            "3️⃣ Fixed: Z-Image-Turbo (FP8-KJ) + Qwen3-Heretic",
            "4️⃣ Fixed: Z-Image-Turbo (BF16) + Qwen3-Heretic",
        ]
        return {
            "required": {
                "rotation_mode": (mode_options, {"default": "🔄 Sequential Round-Robin (Cycles 1 ➔ 2 ➔ 3 ➔ 4)"}),
                "enable_disk_logging": ("BOOLEAN", {"default": True, "label_on": "ON (Logging)", "label_off": "OFF (Disabled)"}),
                "log_directory": ("STRING", {"default": r"D:\AI\Outputs\ZIT_Benchmark_Logs", "multiline": False}),
            },
            "optional": {
                "master_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "active_backbone_tag", "backbone_telemetry")
    FUNCTION = "load_backbone"
    CATEGORY = "Vespera-ZIT/Evaluation"

    @classmethod
    def IS_CHANGED(s, **kwargs):
        # Guarantee dynamic rotation on every queue item
        return time.time_ns()

    def load_backbone(self, rotation_mode, enable_disk_logging, log_directory, master_seed=0):
        import folder_paths
        import comfy.sd

        DynamicBackboneLoaderNode._GLOBAL_QUEUE_INDEX += 1
        queue_idx = DynamicBackboneLoaderNode._GLOBAL_QUEUE_INDEX

        # 1. Select Active Backbone Pair
        if "Round-Robin" in rotation_mode:
            selected_idx = (queue_idx - 1) % len(self.CURATED_PAIRS)
        elif "Stochastic" in rotation_mode:
            prng = random.Random(master_seed if master_seed != 0 else time.time_ns())
            selected_idx = prng.randint(0, len(self.CURATED_PAIRS) - 1)
        elif "1️⃣" in rotation_mode:
            selected_idx = 0
        elif "2️⃣" in rotation_mode:
            selected_idx = 1
        elif "3️⃣" in rotation_mode:
            selected_idx = 2
        else:
            selected_idx = 3

        pair = self.CURATED_PAIRS[selected_idx]
        tag = pair["tag"]
        unet_name = pair["unet"]
        clip_name = pair["clip"]
        weight_dtype = pair["weight_dtype"]
        clip_type_str = pair["clip_type"]

        # 2. Load UNet Model
        model_options = {}
        if weight_dtype == "fp8_e4m3fn":
            model_options["dtype"] = torch.float8_e4m3fn
        elif weight_dtype == "fp8_e5m2":
            model_options["dtype"] = torch.float8_e5m2

        unet_path = folder_paths.get_full_path_or_raise("diffusion_models", unet_name)
        model = comfy.sd.load_diffusion_model(unet_path, model_options=model_options)

        # 3. Load CLIP Model
        clip_type = getattr(comfy.sd.CLIPType, clip_type_str.upper(), comfy.sd.CLIPType.STABLE_DIFFUSION)
        clip_path = folder_paths.get_full_path_or_raise("text_encoders", clip_name)
        clip = comfy.sd.load_clip(
            ckpt_paths=[clip_path],
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
            clip_type=clip_type,
            model_options={}
        )

        telemetry = (
            f"=== 🔄 DYNAMIC BACKBONE MATRIX (Queue #{queue_idx}) ===\n"
            f"• Mode           : {rotation_mode}\n"
            f"• Active Pair    : {pair['name']}\n"
            f"• UNet Checkpoint: {unet_name}\n"
            f"• CLIP Encoder   : {clip_name} ({clip_type_str.upper()})\n"
            f"• Seed Sync      : {master_seed}"
        )

        # 4. Write Benchmark Log to Disk
        if enable_disk_logging and log_directory:
            try:
                os.makedirs(log_directory, exist_ok=True)
                jsonl_path = os.path.join(log_directory, "benchmark_history.jsonl")
                log_entry = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "queue_index": queue_idx,
                    "master_seed": master_seed,
                    "rotation_mode": rotation_mode,
                    "pair_tag": tag,
                    "unet_checkpoint": unet_name,
                    "clip_encoder": clip_name,
                    "clip_type": clip_type_str
                }
                with open(jsonl_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception as e:
                print(f"[DynamicBackboneLoader] Disk logging notice: {e}")

        return (model, clip, tag, telemetry)
