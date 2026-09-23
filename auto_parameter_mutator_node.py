"""
Node    : AutoParameterMutator
Package : ComfyUI-Vespera-ZIT
Purpose : Hardened Adaptive State Machine Engine (Round-Robin ➔ Freeze ➔ Victory)
          with Taboo Defense, Disk Persistence, Real Critic-Guided Parsing, and Exact Frame-Aligned State Sync.
"""

import os
import json
import time
import random
import re
from pathlib import Path

class AutoParameterMutatorNode:
    # State Persistence Path
    _STATE_DIR = Path(__file__).parent / "data"
    _STATE_FILE = _STATE_DIR / "mutator_state.json"

    # Exact snapshot of parameters that generated the PREVIOUS render (Run N-1)
    _GLOBAL_PREV_ACTIVE_CONFIG = {
        "lora": 1.10,
        "pag": 0.25,
        "cfg": 1.50,
        "steps": 25,
        "denoise": 0.30
    }
    
    # State Machine Memory
    _GLOBAL_QUEUE_INDEX = 0
    _GLOBAL_BEST_SCORE = 0.0
    _GLOBAL_SCORE_HISTORY = []
    _GLOBAL_CURRENT_TWEAK_PARAM_IDX = 0  # 0=cfg, 1=pag, 2=lora
    _GLOBAL_VICTORY_ACHIEVED = False

    # Taboo Search Blacklist Rules
    TABOO_RULES = [
        {"param": "cfg", "op": ">", "val": 8.00, "target": 4.00, "reason": "CFG > 2.2 causes severe latent black-crushing in Lumina FlowMatch"},
        {"param": "cfg", "op": "<", "val": 0.80, "target": 1.10, "reason": "CFG < 0.8 causes zero prompt adherence"},
        {"param": "pag", "op": ">", "val": 2.00, "target": 1.20, "reason": "PAG > 2.0 causes severe cyan background blob artifacts"},
        {"param": "steps", "op": "<", "val": 10, "target": 12, "reason": "Steps < 10 causes facial AI smoothing & missing micro-pores"},
        {"param": "lora", "op": ">", "val": 1.35, "target": 1.15, "reason": "LoRA > 1.35 causes tensor saturation burn"},
        {"param": "lora", "op": "<", "val": 0.70, "target": 0.95, "reason": "LoRA < 0.70 causes identity drift into generic face"},
        {"param": "denoise", "op": "<", "val": 0.15, "target": 0.25, "reason": "Denoise < 0.15 lacks sufficient variance for img2img"},
        {"param": "denoise", "op": ">", "val": 0.60, "target": 0.35, "reason": "Denoise > 0.60 destroys identity & causes anatomical distortion"}
    ]

    @classmethod
    def _load_persisted_state(cls):
        """Loads locked state and high-watermark score from disk if available."""
        try:
            if cls._STATE_FILE.exists():
                with open(cls._STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls._GLOBAL_BEST_SCORE = float(data.get("best_score", 0.0))
                    cls._GLOBAL_SCORE_HISTORY = data.get("score_history", [])
                    cls._GLOBAL_CURRENT_TWEAK_PARAM_IDX = data.get("current_tweak_idx", 0)
                    cls._GLOBAL_VICTORY_ACHIEVED = data.get("victory_achieved", False)
                    cls._GLOBAL_PREV_ACTIVE_CONFIG = data.get("prev_active_config", cls._GLOBAL_PREV_ACTIVE_CONFIG)
        except Exception:
            pass

    @classmethod
    def _save_persisted_state(cls):
        """Saves current state atomically to disk."""
        try:
            cls._STATE_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "best_score": cls._GLOBAL_BEST_SCORE,
                "score_history": cls._GLOBAL_SCORE_HISTORY,
                "current_tweak_idx": cls._GLOBAL_CURRENT_TWEAK_PARAM_IDX,
                "victory_achieved": cls._GLOBAL_VICTORY_ACHIEVED,
                "prev_active_config": cls._GLOBAL_PREV_ACTIVE_CONFIG,
                "timestamp": time.time()
            }
            temp_file = cls._STATE_FILE.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            temp_file.replace(cls._STATE_FILE)
        except Exception:
            pass

    @classmethod
    def _reset_all_state(cls):
        """Hard reset of all in-memory and on-disk state."""
        cls._GLOBAL_BEST_SCORE = 0.0
        cls._GLOBAL_QUEUE_INDEX = 0
        cls._GLOBAL_SCORE_HISTORY = []
        cls._GLOBAL_CURRENT_TWEAK_PARAM_IDX = 0
        cls._GLOBAL_VICTORY_ACHIEVED = False
        cls._GLOBAL_PREV_ACTIVE_CONFIG = {
            "lora": 1.10, "pag": 0.25, "cfg": 1.50, "steps": 25, "denoise": 0.30
        }
        try:
            if cls._STATE_FILE.exists():
                cls._STATE_FILE.unlink()
        except Exception:
            pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enable_mutator": ("BOOLEAN", {"default": True, "label_on": "ON (Active)", "label_off": "OFF (Static)"}),
                "mode": ([
                    "🎯 Strict State Machine (Round-Robin ➔ Freeze ➔ Victory)",
                    "🔒 Static Pass-through"
                ], {"default": "🎯 Strict State Machine (Round-Robin ➔ Freeze ➔ Victory)"}),
                "target_lock_score": ("FLOAT", {"default": 7.0, "min": 5.0, "max": 10.0, "step": 0.1}),
                "enable_taboo_defense": ("BOOLEAN", {"default": True, "label_on": "ON (Block Bad Regions)", "label_off": "OFF (Unrestricted)"}),
                "wildcard_rate": ("FLOAT", {"default": 0.15, "min": 0.0, "max": 1.0, "step": 0.05}),
                "base_lora_strength": ("FLOAT", {"default": 1.10, "min": 0.0, "max": 3.0, "step": 0.05}),
                "base_pag_scale": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 5.0, "step": 0.05}),
                "base_cfg": ("FLOAT", {"default": 1.50, "min": 0.5, "max": 10.0, "step": 0.10}),
                "base_steps": ("INT", {"default": 25, "min": 1, "max": 50, "step": 1}),
                "base_denoise": ("FLOAT", {"default": 0.30, "min": 0.05, "max": 1.0, "step": 0.02}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "reset_state_trigger": ("BOOLEAN", {"default": False, "label_on": "RESET (Wipe Memory)", "label_off": "NORMAL (Retain Memory)"}),
            },
            "optional": {
                "quality_score_in": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.1, "forceInput": True}),
                "tuning_advice_in": ("STRING", {"default": "", "multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT", "INT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "STRING", "STRING")
    RETURN_NAMES = ("lora_strength", "pag_scale", "cfg", "steps", "denoise", "mutation_log", "optimal_matrix_text")
    FUNCTION = "mutate_parameters"
    CATEGORY = "Vespera-ZIT/Evaluation"

    @classmethod
    def IS_CHANGED(s, **kwargs):
        return time.time_ns()

    def check_and_clamp_taboo(self, lora, pag, cfg, steps, denoise):
        """Hard bounds defense: iterates TABOO_RULES dynamically to clamp values out of dead zones."""
        blocked_reasons = []
        params = {"lora": lora, "pag": pag, "cfg": cfg, "steps": steps, "denoise": denoise}
        for rule in self.TABOO_RULES:
            p_name = rule["param"]
            current_val = params[p_name]
            violated = False
            if rule["op"] == "<" and current_val < rule["val"]: violated = True
            elif rule["op"] == ">" and current_val > rule["val"]: violated = True
            if violated:
                blocked_reasons.append(f"Clamped {p_name.upper()} ({current_val} ➔ {rule['target']})")
                params[p_name] = rule["target"]
        return round(params["lora"], 2), round(params["pag"], 2), round(params["cfg"], 2), int(params["steps"]), round(params["denoise"], 2), blocked_reasons

    def mutate_parameters(
        self,
        enable_mutator,
        mode,
        target_lock_score,
        enable_taboo_defense,
        wildcard_rate,
        base_lora_strength,
        base_pag_scale,
        base_cfg,
        base_steps,
        base_denoise,
        seed,
        reset_state_trigger=False,
        quality_score_in=0.0,
        tuning_advice_in=""
    ):
        if reset_state_trigger:
            AutoParameterMutatorNode._reset_all_state()

        AutoParameterMutatorNode._load_persisted_state()
        AutoParameterMutatorNode._GLOBAL_QUEUE_INDEX += 1
        queue_idx = AutoParameterMutatorNode._GLOBAL_QUEUE_INDEX

        last_critic_score = quality_score_in
        last_critic_advice = tuning_advice_in
        critic_active = False

        try:
            from .qwen_vision_critic_node import QwenVisionCriticNode
            if getattr(QwenVisionCriticNode, "_GLOBAL_ITERATION_COUNT", 0) > 0:
                last_critic_score = QwenVisionCriticNode._GLOBAL_LAST_SCORE
                last_critic_advice = QwenVisionCriticNode._GLOBAL_LAST_ADVICE
                critic_active = True
        except Exception:
            critic_active = (quality_score_in > 0.0)

        prev_evaluated_config = dict(AutoParameterMutatorNode._GLOBAL_PREV_ACTIVE_CONFIG)

        # Benchmark Ledger Logging
        if critic_active and last_critic_score > 0.0:
            csv_path = r"D:\AI\Outputs\ZIT_Benchmark_Ledger.csv"
            file_exists = os.path.exists(csv_path)
            try:
                os.makedirs(os.path.dirname(csv_path), exist_ok=True)
                with open(csv_path, "a", encoding="utf-8") as cf:
                    if not file_exists:
                        cf.write("Timestamp,Frame,Score,LoRA,CFG,PAG,Steps,Denoise,Critic_Advice\n")
                    clean_advice = last_critic_advice.replace('"', "'").replace('\n', ' ')
                    cfg_v = prev_evaluated_config.get('cfg', 0)
                    lora_v = prev_evaluated_config.get('lora', 0)
                    pag_v = prev_evaluated_config.get('pag', 0)
                    steps_v = prev_evaluated_config.get('steps', 0)
                    denoise_v = prev_evaluated_config.get('denoise', 0)
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cf.write(f'"{timestamp}",{queue_idx-1},{last_critic_score:.1f},{lora_v:.2f},{cfg_v:.2f},{pag_v:.2f},{steps_v},{denoise_v:.2f},"{clean_advice}"\n')
            except Exception:
                pass

        if not enable_mutator or mode == "🔒 Static Pass-through":
            # STATIC MODE
            out_lora, out_pag, out_cfg, out_steps, out_denoise = base_lora_strength, base_pag_scale, base_cfg, base_steps, base_denoise
            taboo_shields = []
            if enable_taboo_defense:
                out_lora, out_pag, out_cfg, out_steps, out_denoise, taboo_shields = self.check_and_clamp_taboo(out_lora, out_pag, out_cfg, out_steps, out_denoise)
            
            AutoParameterMutatorNode._GLOBAL_PREV_ACTIVE_CONFIG = {"lora": out_lora, "pag": out_pag, "cfg": out_cfg, "steps": out_steps, "denoise": out_denoise}
            return (out_lora, out_pag, out_cfg, out_steps, out_denoise, out_lora, 1.0, 3.0, "Static pass-through.", "Static pass-through.")

        # ====================================================================================
        # STATE MACHINE: 
        # 1. Check Victory
        # 2. Update History
        # 3. If >= 7: Freeze (Render with same settings)
        # 4. If < 7: Tweak 1 parameter using Qwen feedback, advance round-robin index
        # ====================================================================================

        out_lora = prev_evaluated_config["lora"]
        out_pag = prev_evaluated_config["pag"]
        out_cfg = prev_evaluated_config["cfg"]
        out_steps = prev_evaluated_config["steps"]
        out_denoise = prev_evaluated_config["denoise"]
        
        log_reason = ""
        strategy = ""

        if critic_active and last_critic_score > 0.0:
            AutoParameterMutatorNode._GLOBAL_SCORE_HISTORY.append(last_critic_score)
            if last_critic_score > AutoParameterMutatorNode._GLOBAL_BEST_SCORE:
                AutoParameterMutatorNode._GLOBAL_BEST_SCORE = last_critic_score

            recent_15 = AutoParameterMutatorNode._GLOBAL_SCORE_HISTORY[-15:]
            scores_8_plus = [s for s in recent_15 if s >= 8.0]
            if len(scores_8_plus) >= 10:
                AutoParameterMutatorNode._GLOBAL_VICTORY_ACHIEVED = True

        if AutoParameterMutatorNode._GLOBAL_VICTORY_ACHIEVED:
            strategy = "🏆 [VICTORY ACHIEVED: 10/15 Scores >= 8]"
            log_reason = "Tuning complete. Rendering locked optimal configuration endlessly."
            
        elif critic_active and last_critic_score >= target_lock_score:
            strategy = f"🔒 [FREEZE PHASE: Score {last_critic_score:.1f} >= {target_lock_score}]"
            log_reason = "Score reached target lock threshold. Freezing parameters to test stability."

        else:
            strategy = f"🔧 [TWEAK PHASE: Score {last_critic_score:.1f} < {target_lock_score}]"
            
            if not critic_active:
                log_reason = "No critic score yet. Using base initialization."
                out_lora, out_pag, out_cfg = base_lora_strength, base_pag_scale, base_cfg
            else:
                param_idx = AutoParameterMutatorNode._GLOBAL_CURRENT_TWEAK_PARAM_IDX
                adv_lower = last_critic_advice.lower()
                direction = 0.0
                
                # Qwen text feedback to determine direction
                if param_idx == 0:  # CFG
                    if any(w in adv_lower for w in ["increase cfg", "higher cfg", "raise cfg", "beauty mark", "more prompt", "cupid's bow"]):
                        direction = 0.25
                    elif any(w in adv_lower for w in ["decrease cfg", "lower cfg", "reduce cfg", "less cfg", "fry", "fried", "burned", "too dark", "contrasty", "shadows"]):
                        direction = -0.25
                    else:
                        direction = 0.25
                    out_cfg = round(out_cfg + direction, 2)
                    log_reason = f"Tweaked CFG by {direction} based on critic advice."
                    
                elif param_idx == 1:  # PAG
                    if any(w in adv_lower for w in ["increase pag", "higher pag", "raise pag"]):
                        direction = 0.25
                    elif any(w in adv_lower for w in ["decrease pag", "lower pag", "reduce pag", "cyan", "blob", "halo", "mist", "haze"]):
                        direction = -0.25
                    else:
                        direction = -0.25 # PAG heuristic is better down than up to reduce artifacts
                    out_pag = round(out_pag + direction, 2)
                    log_reason = f"Tweaked PAG by {direction} based on critic advice."
                    
                elif param_idx == 2:  # LoRA
                    if any(w in adv_lower for w in ["increase lora", "boost lora", "raise lora", "higher lora", "more identity", "identity drift"]):
                        direction = 0.25
                    elif any(w in adv_lower for w in ["decrease lora", "lower lora", "reduce lora", "less lora", "tensor burn", "oversaturated", "lumps", "artifacts"]):
                        direction = -0.25
                    else:
                        direction = -0.25
                    out_lora = round(out_lora + direction, 2)
                    log_reason = f"Tweaked LoRA by {direction} based on critic advice."

                # Advance Round-Robin
                AutoParameterMutatorNode._GLOBAL_CURRENT_TWEAK_PARAM_IDX = (param_idx + 1) % 3

        # Enforce Taboo
        taboo_shields = []
        if enable_taboo_defense:
            out_lora, out_pag, out_cfg, out_steps, out_denoise, taboo_shields = self.check_and_clamp_taboo(out_lora, out_pag, out_cfg, out_steps, out_denoise)
            if taboo_shields:
                log_reason += " | 🛡️ " + " | ".join(taboo_shields)

        AutoParameterMutatorNode._GLOBAL_PREV_ACTIVE_CONFIG = {
            "lora": out_lora, "pag": out_pag, "cfg": out_cfg, "steps": out_steps, "denoise": out_denoise
        }
        AutoParameterMutatorNode._save_persisted_state()

        matrix_summary = (
            f"👑 [OPTIMAL PARAMETERS MATRIX]\n"
            f"• Engine State           : {strategy}\n"
            f"• Best Achieved Score    : {AutoParameterMutatorNode._GLOBAL_BEST_SCORE:.1f}/10\n"
            f"• 8+ Score Count (15w)   : {len([s for s in AutoParameterMutatorNode._GLOBAL_SCORE_HISTORY[-15:] if s >= 8.0])}/10\n"
            f"• Active LoRA Scale      : {out_lora:.2f}\n"
            f"• Active CFG Scale       : {out_cfg:.2f}\n"
            f"• Active PAG Scale       : {out_pag:.2f}\n"
            f"• Active Steps           : {out_steps}\n"
            f"• Active Denoise         : {out_denoise:.2f}"
        )

        mutation_log = (
            f"=== {strategy} ===\n"
            f"• Queue Run Index      : #{queue_idx}\n"
            f"• Critic Last Score    : {last_critic_score}\n"
            f"• Output LoRA Strength : {out_lora:.2f}\n"
            f"• Output PAG Scale     : {out_pag:.2f}\n"
            f"• Output CFG           : {out_cfg:.2f}\n"
            f"• Telemetry Rationale  : {log_reason}"
        )

        return (out_lora, out_pag, out_cfg, out_steps, out_denoise, out_lora, 1.0, 3.0, mutation_log, matrix_summary)
