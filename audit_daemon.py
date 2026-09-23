"""
Module  : Audit Daemon & Sweep Synthesis Engine
Package : ComfyUI-Vespera-ZIT
Purpose : Comprehensive Comparative Batch Audit, Model Extraction, Pareto Multi-Objective Optimization,
          ComfyUI Lifecycle Tying (Auto-Start on Broadcast, Silent Auto-Kill on Teardown),
          and Golden Recipe Persistence for ZIT Dataset Harvesting.
"""

import os
import sys
import re
import json
import time
import socket
import datetime
import urllib.request
from pathlib import Path
from typing import Dict, List, Any, Optional
from PIL import Image

DEFAULT_OUTPUT_DIR = Path(r"D:\AI\Projects\ComfyUI\output")
DEFAULT_LOG_DIR = Path(r"D:\AI\Outputs\ZIT_Benchmark_Logs")
DEFAULT_STREAM_FILE = DEFAULT_LOG_DIR / "zit_telemetry_stream.jsonl"
DEFAULT_RECIPE_FILE = DEFAULT_LOG_DIR / "golden_vespera_recipe.json"
DEFAULT_COMFY_URL = "http://127.0.0.1:8188"


def is_comfyui_alive(comfy_url: str = DEFAULT_COMFY_URL, timeout_sec: float = 1.5) -> bool:
    """Checks if ComfyUI server is actively broadcasting/online."""
    try:
        url = f"{comfy_url.rstrip('/')}/system_stats"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            return resp.status == 200
    except Exception:
        # Fallback to direct raw socket ping on port
        try:
            parsed = urllib.request.urlparse(comfy_url)
            host = parsed.hostname or "127.0.0.1"
            port = parsed.port or 8188
            with socket.create_connection((host, port), timeout=timeout_sec):
                return True
        except Exception:
            return False


def query_ollama_synthesis(
    prompt: str,
    ollama_url: str = "http://127.0.0.1:11434",
    model: str = "qwen2.5:7b-instruct",
    timeout_sec: float = 60.0
) -> str:
    """Queries local Ollama instance for text synthesis of benchmark audit."""
    try:
        url = f"{ollama_url.rstrip('/')}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": 0,
            "options": {
                "temperature": 0.3,
                "num_predict": 768
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as e:
        return f"[Ollama Synthesis Fallback]: Statistical summary generated without LLM commentary ({e})."


def sync_to_ulm_daemon(fact_text: str, ulm_url: str = "http://127.0.0.1:8890") -> bool:
    """Dispatches the discovered golden matrix fact to ULM Daemon memory."""
    try:
        url = f"{ulm_url.rstrip('/')}/api/facts"
        payload = {
            "fact": fact_text,
            "category": "technical",
            "confidence": 0.98,
            "project_tag": "ComfyUI-Vespera-ZIT"
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            return resp.status == 200
    except Exception:
        return False


def extract_metadata_from_pngs(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    prefix: str = "Ves_V4_Dynamic_Sweep_Renders",
    max_count: int = 30
) -> List[Dict[str, Any]]:
    """
    Extracts every single hardware and model detail directly from rendered PNG metadata.
    """
    if not output_dir.exists():
        return []

    matching_files = sorted(
        [p for p in output_dir.glob(f"{prefix}_*.png")],
        key=lambda p: p.stat().st_mtime
    )

    if not matching_files:
        matching_files = sorted(
            [p for p in output_dir.glob("*.png")],
            key=lambda p: p.stat().st_mtime
        )

    target_files = matching_files[-max_count:]
    extracted_records: List[Dict[str, Any]] = []

    prev_mtime = None
    for f in target_files:
        try:
            mtime = f.stat().st_mtime
            render_delta = round(mtime - prev_mtime, 1) if prev_mtime else 0.0
            prev_mtime = mtime
            file_size_kb = round(f.stat().st_size / 1024, 1)

            with Image.open(f) as img:
                raw_prompt = img.info.get("prompt", "{}")
                prompt_data = json.loads(raw_prompt)

                unet_name = "N/A"
                clip_name = "N/A"
                vae_name = "N/A"
                lora_name = "N/A"
                lora_strength = 1.0
                lora_details = {}
                seed = "N/A"
                steps = 14
                cfg = 3.0
                pag = 1.15
                sampler_name = "euler"
                scheduler = "FlowMatchEulerDiscreteScheduler"

                for node_id, node_info in prompt_data.items():
                    class_type = node_info.get("class_type", "")
                    inputs = node_info.get("inputs", {})

                    if "UNETLoader" in class_type:
                        unet_name = inputs.get("unet_name", unet_name)
                    elif "CLIPLoader" in class_type:
                        clip_name = inputs.get("clip_name", clip_name)
                    elif "VAELoader" in class_type:
                        vae_name = inputs.get("vae_name", vae_name)
                    elif "Power LoRA Loader" in class_type or "DoRA" in class_type:
                        lora_1 = inputs.get("LORA_1", {})
                        if isinstance(lora_1, dict):
                            lora_name = lora_1.get("lora", lora_name)
                            lora_strength = lora_1.get("strength", lora_strength)
                        lora_details = inputs
                    elif "KSampler" in class_type:
                        seed = inputs.get("seed", seed)
                        sampler_name = inputs.get("sampler_name", sampler_name)
                        scheduler = inputs.get("scheduler", scheduler)
                    elif "AutoParameterMutatorNode" in class_type:
                        steps = inputs.get("base_steps", steps)
                        cfg = inputs.get("base_cfg", cfg)
                        pag = inputs.get("base_pag_scale", pag)

                record = {
                    "filename": f.name,
                    "timestamp": datetime.datetime.fromtimestamp(mtime).isoformat(),
                    "file_size_kb": file_size_kb,
                    "render_seconds": render_delta,
                    "unet_model": unet_name,
                    "text_encoder": clip_name,
                    "vae": vae_name,
                    "lora_name": lora_name,
                    "lora_strength": lora_strength,
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "pag": pag,
                    "sampler": sampler_name,
                    "scheduler": scheduler,
                    "full_lora_stack": lora_details
                }
                extracted_records.append(record)
        except Exception as err:
            pass

    return extracted_records


def run_batch_audit(
    stream_file: Path = DEFAULT_STREAM_FILE,
    recipe_output_file: Path = DEFAULT_RECIPE_FILE,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    ollama_url: str = "http://127.0.0.1:11434",
    ollama_model: str = "qwen2.5:7b-instruct",
    ulm_url: str = "http://127.0.0.1:8890",
    lookback_frames: int = 30
) -> Dict[str, Any]:
    """
    Parses telemetry stream and extracts PNG metadata directly to produce
    a comprehensive comparative audit comparing models, render times, and parameters.
    """
    png_records = extract_metadata_from_pngs(output_dir=output_dir, max_count=lookback_frames)

    stream_records: List[Dict[str, Any]] = []
    if stream_file.exists():
        try:
            with open(stream_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            stream_records.append(json.loads(line))
                        except Exception:
                            pass
        except Exception:
            pass

    combined_data = []
    for p_rec in png_records:
        matched_stream = next((s for s in stream_records if s.get("iteration") == p_rec.get("filename")), None)
        score = float(matched_stream.get("score", 9.0)) if matched_stream else 9.0
        advice = matched_stream.get("advice", "Optimal biometric balance") if matched_stream else "Optimal biometric balance"
        
        render_sec = max(float(p_rec.get("render_seconds", 60.0)), 1.0)
        if render_sec <= 1.0 and len(combined_data) > 0:
            render_sec = combined_data[-1]["render_seconds"]
            p_rec["render_seconds"] = render_sec
        elif render_sec <= 1.0:
            render_sec = 95.0
            p_rec["render_seconds"] = 95.0

        efficiency = round((score * 10.0) / (render_sec ** 0.40), 2)
        p_rec["score"] = score
        p_rec["advice"] = advice
        p_rec["harvest_efficiency"] = efficiency
        combined_data.append(p_rec)

    if not combined_data:
        return {"status": "error", "message": "No render files found to audit."}

    model_groups: Dict[str, List[Dict[str, Any]]] = {}
    for r in combined_data:
        model_name = r.get("unet_model", "Unknown")
        if model_name not in model_groups:
            model_groups[model_name] = []
        model_groups[model_name].append(r)

    model_summary = {}
    for m_name, items in model_groups.items():
        avg_time = sum(i["render_seconds"] for i in items) / len(items)
        avg_eff = sum(i["harvest_efficiency"] for i in items) / len(items)
        avg_size = sum(i["file_size_kb"] for i in items) / len(items)
        model_summary[m_name] = {
            "sample_count": len(items),
            "average_render_seconds": round(avg_time, 1),
            "average_efficiency": round(avg_eff, 2),
            "average_file_size_kb": round(avg_size, 1)
        }

    sorted_by_efficiency = sorted(combined_data, key=lambda x: x["harvest_efficiency"], reverse=True)
    pareto_winner = sorted_by_efficiency[0]

    prompt_breakdown = "\n".join([
        f"- {m_name}: Avg Time = {stats['average_render_seconds']}s | Efficiency Index = {stats['average_efficiency']} | Samples = {stats['sample_count']}"
        for m_name, stats in model_summary.items()
    ])

    audit_prompt = (
        "You are an AI Diffusion Architect auditing a multi-model comparative sweep for Vespera-ZIT.\n"
        "Here is the hardware & model benchmark breakdown:\n"
        f"{prompt_breakdown}\n\n"
        f"Top Performing Run: {pareto_winner.get('filename')} with UNet '{pareto_winner.get('unet_model')}', "
        f"Text Encoder '{pareto_winner.get('text_encoder')}', LoRA '{pareto_winner.get('lora_name')}' @ {pareto_winner.get('lora_strength')}, "
        f"Render Time = {pareto_winner.get('render_seconds')}s, Efficiency = {pareto_winner.get('harvest_efficiency')}.\n\n"
        "Provide an autopsy covering:\n"
        "1. Model Speed vs Stability Comparison (which UNet architecture won and why)\n"
        "2. VRAM & Pipeline Efficiency Assessment for RTX 4070 12GB\n"
        "3. Final Locked Recommendation for the Character LoRA Dataset Harvesting."
    )

    llm_analysis = query_ollama_synthesis(
        prompt=audit_prompt,
        ollama_url=ollama_url,
        model=ollama_model
    )

    golden_recipe = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_audited_frames": len(combined_data),
        "model_architecture_comparison": model_summary,
        "pareto_winner": pareto_winner,
        "llm_synthesis": llm_analysis
    }

    try:
        recipe_output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(recipe_output_file, "w", encoding="utf-8") as f:
            json.dump(golden_recipe, f, indent=2)
    except Exception as e:
        pass

    fact_text = (
        f"ZIT Multi-Model Audit: {pareto_winner.get('unet_model')} won with {pareto_winner.get('render_seconds')}s render time. "
        f"LoRA: {pareto_winner.get('lora_name')} @ {pareto_winner.get('lora_strength')}. Comparison: {json.dumps(model_summary)}"
    )
    sync_to_ulm_daemon(fact_text, ulm_url=ulm_url)

    return golden_recipe


def run_continuous_daemon(
    comfy_url: str = DEFAULT_COMFY_URL,
    poll_interval_sec: float = 10.0,
    consecutive_offline_limit: int = 3
) -> None:
    """
    Continuous background daemon lifecycle:
    1. Waits until ComfyUI starts broadcasting online.
    2. Once active, monitors outputs and telemetry.
    3. If ComfyUI is terminated/killed, silently terminates itself.
    """
    # Phase 1: Wait for ComfyUI to start broadcasting
    while not is_comfyui_alive(comfy_url):
        time.sleep(2.0)

    # Phase 2: Active monitoring loop tied to ComfyUI heartbeat
    last_processed_count = 0
    offline_strikes = 0

    while True:
        time.sleep(poll_interval_sec)

        # Heartbeat check: If ComfyUI stopped broadcasting, die silently
        if not is_comfyui_alive(comfy_url):
            offline_strikes += 1
            if offline_strikes >= consecutive_offline_limit:
                # ComfyUI is dead -> silent suicide
                sys.exit(0)
        else:
            offline_strikes = 0

        # Check for new outputs in output dir
        try:
            png_files = list(DEFAULT_OUTPUT_DIR.glob("Ves_V4_Dynamic_Sweep_Renders_*.png"))
            current_count = len(png_files)
            if current_count > last_processed_count and current_count % 5 == 0:
                last_processed_count = current_count
                run_batch_audit()
        except Exception:
            pass


if __name__ == "__main__":
    if "--daemon" in sys.argv or "-d" in sys.argv:
        run_continuous_daemon()
    else:
        # Default single-shot execution
        result = run_batch_audit()
        print(json.dumps(result, indent=2))
