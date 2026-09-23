"""
Node    : QwenVisionCritic
Package : ComfyUI-Vespera-ZIT
Purpose : In-Canvas Multimodal Quality Critic & Parameter Tuning Advisor with Cross-Queue Memory.
"""

import os
import re
import io
import json
import base64
import urllib.request
import numpy as np
import torch
from PIL import Image

def _ensure_ollama_online(ollama_url="http://127.0.0.1:11434", timeout_sec=5.0) -> bool:
    try:
        urllib.request.urlopen(ollama_url.rstrip("/") + "/", timeout=timeout_sec)
        return True
    except:
        return False

def _purge_ollama_vram(ollama_url, ollama_model):
    try:
        url = ollama_url.rstrip("/") + "/api/generate"
        payload = {"model": ollama_model, "prompt": "", "keep_alive": 0}
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=2.0)
    except:
        pass

class QwenVisionCriticNode:
    _GLOBAL_ITERATION_COUNT = 0
    _GLOBAL_LAST_SCORE = 0.0
    _GLOBAL_LAST_ADVICE = "Baseline initialized."
    _GLOBAL_BEST_SCORE = 0.0

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enable_critic": ("BOOLEAN", {"default": True}),
                "rubric_mode": (["👑 Vespera Biometric Fidelity", "🤚 Hands & Anatomical Precision", "⚙️ Custom Rubric"],),
                "ollama_model": (["qwen2.5vl:3b", "qwen2.5:7b-instruct"], {"default": "qwen2.5vl:3b"}),
                "ollama_url": ("STRING", {"default": "http://127.0.0.1:11434"}),
                "custom_rubric_prompt": ("STRING", {"multiline": True, "default": ""}),
                "image": ("IMAGE",),
            },
            "optional": {
                "reference_image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING", "FLOAT", "STRING")
    RETURN_NAMES = ("diagnostic_report", "quality_score", "parameter_advice")
    FUNCTION = "evaluate_render"
    CATEGORY = "Vespera ZIT Autonomous"

    def evaluate_render(self, enable_critic, rubric_mode, ollama_model, ollama_url, custom_rubric_prompt, image, reference_image=None):
        if not enable_critic:
            return ("Critic Disabled", 0.0, "Critic Disabled")
        
        QwenVisionCriticNode._GLOBAL_ITERATION_COUNT += 1
        iter_num = QwenVisionCriticNode._GLOBAL_ITERATION_COUNT

        try:
            if not _ensure_ollama_online(ollama_url, timeout_sec=4.0):
                return (
                    f"⚠️ [Ollama Offline]: Unable to reach Ollama at {ollama_url}. "
                    "Skipping vision critique this frame to protect render pipeline.",
                    0.0,
                    "Ollama service offline. No adjustments made."
                )

            # Convert active image
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img.thumbnail((512, 512)) # VRAM/CONTEXT OPTIMIZATION
            
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            ref_b64_list = []
            if reference_image is not None:
                for idx in range(reference_image.shape[0]):
                    ref_i = 255.0 * reference_image[idx].cpu().numpy()
                    ref_img = Image.fromarray(np.clip(ref_i, 0, 255).astype(np.uint8))
                    ref_img.thumbnail((512, 512)) # VRAM/CONTEXT OPTIMIZATION
                    ref_buffered = io.BytesIO()
                    ref_img.save(ref_buffered, format="JPEG", quality=85)
                    ref_b64_list.append(base64.b64encode(ref_buffered.getvalue()).decode("utf-8"))

            if rubric_mode == "👑 Vespera Biometric Fidelity":
                system_prompt = (
                    "You are an elite visual quality critic for photorealistic AI diffusion portraits of Vespera Neal. "
                    "Evaluate the generated image strictly against these ground-truth biometric traits:\n"
                    "- Hair: Voluminous jet-black 3B/3C spiral corkscrew curls with fine electric-indigo highlights.\n"
                    "- Face: Warm olive skin, sculpted cheekbones, soft-smudged smoky kohl eyeliner, full dark satin lips, tiny beauty mark near upper-left lip corner.\n"
                    "- Anatomy: Athletic hourglass proportions.\n"
                    "- Lighting & Exposure: CRITICAL - Heavily penalize any image with crushed black shadows, severe underexposure, or blown-out contrast.\n"
                )
            elif rubric_mode == "🤚 Hands & Anatomical Precision":
                system_prompt = "Evaluate anatomical integrity, focusing strictly on fingers, knuckles, nails, hand pose naturalism, limb proportions, and facial symmetry."
            elif rubric_mode == "⚙️ Custom Rubric":
                system_prompt = custom_rubric_prompt if custom_rubric_prompt.strip() else "Evaluate the quality of this image in detail."
            else:
                system_prompt = "Evaluate the overall aesthetic quality, composition, lighting, and artifact absence in this image."

            images_list = ref_b64_list + [img_b64] if ref_b64_list else [img_b64]

            if ref_b64_list:
                num_refs = len(ref_b64_list)
                user_prompt = (
                    f"Analyze the attached {num_refs + 1} images (Iteration #{iter_num}). The first {num_refs} image(s) are the Ground-Truth Reference(s). The LAST image is the Generated Render. Under this rubric:\n{system_prompt}\n\n"
                    "Compare the Generated Render (last image) against the Ground-Truth Reference image(s). Respond in this clean format:\n"
                    "### 📊 Visual Diagnostic Report\n"
                    "- **Overall Score (1-10):** <score>\n"
                    "- **Key Strengths:** <bullet points>\n"
                    "- **Flaws / Artifacts Detected:** <bullet points>\n"
                    "- **Recommended Parameter Adjustments:** <specific suggestions for LoRA weight, PAG, CFG, Denoise>"
                )
            else:
                user_prompt = (
                    f"Analyze the attached image (Iteration #{iter_num}) under this rubric:\n{system_prompt}\n\n"
                    "Respond in this clean format:\n"
                    "### 📊 Visual Diagnostic Report\n"
                    "- **Overall Score (1-10):** <score>\n"
                    "- **Key Strengths:** <bullet points>\n"
                    "- **Flaws / Artifacts Detected:** <bullet points>\n"
                    "- **Recommended Parameter Adjustments:** <specific suggestions for LoRA weight, PAG, CFG, Denoise>"
                )

            import requests
            url = f"{ollama_url.rstrip('/')}/api/generate"
            payload = {
                "model": ollama_model,
                "prompt": user_prompt,
                "images": images_list,
                "stream": False,
                "keep_alive": 0,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 512,
                    "num_ctx": 8192
                }
            }

            response_text = "No evaluation returned."
            try:
                resp = requests.post(url, json=payload, timeout=60)
                if resp.status_code != 200:
                    raise Exception(f"HTTP {resp.status_code}: {resp.text}")
                result = resp.json()
                response_text = result.get("response", "No evaluation returned.")
            finally:
                _purge_ollama_vram(ollama_url, ollama_model)

            score = 0.0
            for line in response_text.splitlines():
                if "score" in line.lower() and (":" in line or "(" in line):
                    score_match = re.search(r"(\d+(?:\.\d+)?)", line.split(":")[-1] if ":" in line else line)
                    if score_match:
                        candidate = float(score_match.group(1))
                        if 0.0 <= candidate <= 10.0:
                            score = candidate
                            break

            advice = "Maintain current trajectory."
            advice_match = re.search(
                r"(?:recommended\s+parameter\s+adjustments|parameter\s+adjustments)\s*[:\-]\s*(.*)",
                response_text,
                re.IGNORECASE | re.DOTALL
            )
            if advice_match:
                advice = advice_match.group(1).strip()

            with open(r"D:\AI\Outputs\critic_debug.txt", "a", encoding="utf-8") as df:
                df.write(f"SUCCESS Score={score} Advice={advice}\nRAW={response_text}\n")
            
            QwenVisionCriticNode._GLOBAL_LAST_SCORE = score
            QwenVisionCriticNode._GLOBAL_LAST_ADVICE = advice
            if score > QwenVisionCriticNode._GLOBAL_BEST_SCORE:
                QwenVisionCriticNode._GLOBAL_BEST_SCORE = score

            return (response_text, score, advice)

        except Exception as e:
            err_details = str(e)
            with open(r"D:\AI\Outputs\critic_debug.txt", "a", encoding="utf-8") as df:
                df.write(f"ERROR: {err_details}\n")
            
            _purge_ollama_vram(ollama_url, ollama_model)
            err_msg = f"⚠️ [QwenVisionCritic Note]: {str(e)}"
            
            QwenVisionCriticNode._GLOBAL_LAST_SCORE = 0.0
            QwenVisionCriticNode._GLOBAL_LAST_ADVICE = f"Evaluation failed: {str(e)}"
            
            return (err_msg, 0.0, "Maintain optimal baseline parameters.")
