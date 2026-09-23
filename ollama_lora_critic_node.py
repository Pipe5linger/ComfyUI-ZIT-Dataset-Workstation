import os
import sys
import json
import urllib.request
import time
import subprocess

try:
    import folder_paths
except ImportError:
    folder_paths = None

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_BASE = "http://127.0.0.1:11434"

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except Exception:
        try:
            msg = " ".join(str(a) for a in args) + "\n"
            sys.stdout.buffer.write(msg.encode("ascii", "replace"))
            sys.stdout.buffer.flush()
        except Exception:
            pass

def _ensure_ollama_online(timeout_sec=4.0) -> bool:
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                return True
    except Exception:
        pass
    try:
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NO_WINDOW
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags
        )
        start_t = time.time()
        while time.time() - start_t < timeout_sec:
            time.sleep(0.5)
            try:
                req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    if resp.status == 200:
                        return True
            except Exception:
                continue
    except Exception:
        pass
    return False

class OllamaLoRACriticNode:
    """An advisory LLM node that reads local LoRAs and recommends a stack based on the prompt."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "active": ("BOOLEAN", {"default": True}),
                "prompt": ("STRING", {"multiline": True, "forceInput": True}),
                "current_loras": ("STRING", {"multiline": True, "default": "ZIB_SkinnyVoluptousSlider_v5.1 (1.5)\nZ-Hip-Slider (1.5)\nAntiPlastic_AnalogTexture_v1 (1.0)\nafterdark_v2 (0.8)\nZ-Detail-Slider (0.5)"}),
                "ollama_model": ("STRING", {"default": "qwen2.5:7b-instruct"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("lora_recommendation",)
    FUNCTION = "run"
    CATEGORY = "ZIT/Dataset Workstation"

    def run(self, active: bool, prompt: str, current_loras: str, ollama_model: str):
        if not active:
            return ("CRITIC BYPASSED: Set active=True to enable the LoRA critic.",)
            
        safe_print("[OllamaLoRACriticNode] Fetching available LoRAs from disk...")
        lora_list = []
        if folder_paths is not None:
            lora_list = folder_paths.get_filename_list("loras")
        else:
            lora_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "models", "loras")
            if os.path.exists(lora_dir):
                lora_list = os.listdir(lora_dir)
                
        # Take up to 250 LoRAs to fit within context limits safely
        lora_list_str = "\n".join(lora_list[:250])
        
        system_prompt = (
            "You are an elite AI Diffusion Architect and LoRA (Low-Rank Adaptation) Critic. "
            "Your job is to read the user's prompt, review their current LoRA stack, and scan their "
            "available LoRA library to recommend an optimal 5-LoRA stack (with strength values from 0.1 to 2.0). "
            "Output your recommendation as a clean, highly readable advisory report. Explain why you are keeping, "
            "dropping, or adding specific LoRAs. Ensure any recommended LoRA name exactly matches a file from the library list."
        )
        
        user_msg = (
            f"PROMPT:\n{prompt}\n\n"
            f"CURRENT LORA STACK:\n{current_loras}\n\n"
            f"AVAILABLE LORAS IN LIBRARY:\n{lora_list_str}\n\n"
            "Task: Based on the prompt aesthetics, suggest the perfect 5-LoRA combination from the library. "
            "Format your response with a brief aesthetic analysis, the recommended stack with strengths, and your reasoning."
        )
        
        if not _ensure_ollama_online():
            return ("ERROR: Ollama server is offline or unreachable.",)
            
        safe_print(f"[OllamaLoRACriticNode] Sending critique request to {ollama_model}...")
        
        payload = json.dumps({
            "model": ollama_model,
            "prompt": user_msg,
            "system": system_prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 1024}
        }).encode("utf-8")
        
        req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                result = body.get("response", "").strip()
                # Purge from VRAM
                try:
                    purge_req = urllib.request.Request(OLLAMA_URL, data=json.dumps({"model": ollama_model, "keep_alive": 0}).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
                    urllib.request.urlopen(purge_req, timeout=3)
                except Exception:
                    pass
                return (result,)
        except Exception as e:
            safe_print(f"[OllamaLoRACriticNode] Error: {e}")
            return (f"ERROR: Failed to fetch critique from Ollama: {str(e)}",)
