"""
Node    : ExecutionWatchdog
Package : ComfyUI-Vespera-ZIT
Purpose : In-Canvas Execution Watchdog & Kill Order Circuit Breaker with Generous Headroom.
"""

import time
import torch

class ExecutionWatchdogNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "enable_watchdog": ("BOOLEAN", {"default": True, "label_on": "ON (Active)", "label_off": "OFF (Disabled)"}),
                "max_render_seconds": ("FLOAT", {"default": 45.0, "min": 5.0, "max": 180.0, "step": 1.0}),
                "abort_on_latent_explosion": ("BOOLEAN", {"default": True, "label_on": "ON", "label_off": "OFF"}),
            }
        }

    RETURN_TYPES = ("MODEL", "STRING")
    RETURN_NAMES = ("MODEL", "watchdog_status")
    FUNCTION = "apply_watchdog"
    CATEGORY = "Vespera-ZIT/Evaluation"

    def apply_watchdog(self, model, enable_watchdog, max_render_seconds, abort_on_latent_explosion):
        if not enable_watchdog:
            return (model, "⏸️ Watchdog is disabled. Standard execution.")

        try:
            import comfy.model_management
        except Exception:
            comfy = None

        m = model.clone()
        start_time = [time.time()]
        status_msg = [f"🛡️ Watchdog Armed (Max Timeout: {max_render_seconds:.1f}s | Latent Defense: ON)"]

        def watchdog_callback(step, x0, x, total_steps):
            # DEFECT 3 FIX: Reset timer on first sampling step so model load time is excluded
            if step == 0:
                start_time[0] = time.time()
            elapsed = time.time() - start_time[0]
            
            if elapsed > max_render_seconds:
                print(f"\n🔥 [WATCHDOG KILL ORDER FIRED]: Render exceeded timeout limit ({elapsed:.2f}s > {max_render_seconds:.1f}s)! Aborting...")
                if comfy is not None:
                    try:
                        comfy.model_management.interrupt_current_processing()
                    except Exception:
                        pass
                raise Exception(f"🔥 Watchdog Timeout ({elapsed:.2f}s > {max_render_seconds:.1f}s) - Advancing to next queue item.")

            if abort_on_latent_explosion and x0 is not None:
                if torch.isnan(x0).any() or torch.isinf(x0).any():
                    print(f"\n🔥 [WATCHDOG KILL ORDER FIRED]: NaN/Inf anomaly detected at step {step}/{total_steps}! Aborting...")
                    if comfy is not None:
                        try:
                            comfy.model_management.interrupt_current_processing()
                        except Exception:
                            pass
                    raise Exception(f"🔥 Latent NaN/Inf Anomaly Detected at step {step} - Advancing to next queue item.")

        # DEFECT 1 FIX: Removed m.set_model_sampler_post_cfg_function(None) — it was erasing PAG hooks
        if not hasattr(m, "model_options"):
            m.model_options = {}
        
        existing_callback = m.model_options.get("sampler_callback", None)
        
        def combined_callback(step, x0, x, total_steps):
            watchdog_callback(step, x0, x, total_steps)
            if existing_callback is not None:
                existing_callback(step, x0, x, total_steps)

        m.model_options["sampler_callback"] = combined_callback

        return (m, status_msg[0])
