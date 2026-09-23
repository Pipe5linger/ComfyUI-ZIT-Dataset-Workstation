# 🍷 ComfyUI Character Dataset & Master Prompt Workstation (ZIT Engine)

A comprehensive, all-in-one prompt engineering, zero-shot character override, and **automated 4-tier character LoRA dataset generation suite** for ComfyUI (optimized for Flux, Z-Image Turbo, and SDXL).

---

## 🌟 What Sets This Node Apart?
Most prompt generators produce chaotic or repetitive outputs that ruin LoRA training with **facial asymmetry, single-angle overfit, and clothing-to-skin fusion**. 

This suite automates the **mathematically balanced 4-tier character dataset methodology** (50-image gold standard):
1. **🎯 Tier 1: Identity Anchors (15 Images / 30%)** — Extreme face macros, ocular striations, authentic pores, and full 3D head rotation (Frontal, 3/4 Left, 3/4 Right, 90 deg Left Profile, 90 deg Right Profile, Dynamic Up/Down Tilts).
2. **🔥 Tier 2: Raw Anatomy (10 Images / 20%)** — Nudity and micro-lingerie across medium and full-body shots to lock body proportions (e.g. 0.66 waist-to-hip ratio) and eliminate clothing-to-skin fusion.
3. **👗 Tier 3: Wardrobe Agnosticism (15 Images / 30%)** — Cowboy (mid-thigh up) and seated shots across 9 distinct fashion tiers (Haute Couture, Velvet Gowns, Power Suits, Selvedge Denim & Leather, Liquid Latex, Cashmere, Robes) to teach the model that clothing is a temporary wrapper.
4. **🌐 Tier 4: 3D Spatial Awareness (10 Images / 20%)** — Full-body head-to-toe, walking in mid-stride, crouching, and back-of-head shots showing hair volume to eliminate 'Instagram Model' rigidity.
5. **👑 Master 50-Image Matrix** — Runs all 4 tiers in sequential order.

---

## 🚀 Key Features

* **Zero Hardcoded Batch Counts:** Run any batch size in ComfyUI (e.g. 5, 10, 15, 50, 100); the node dynamically cycles through the matrix via seed modulo without repeating patterns.
* **Decoupled Director Camera Rigs & Optics:** Real lens physics (Arri Alexa 65 Anamorphic 50mm, Zeiss Master Prime 32mm, Leica 27mm, Hasselblad 80mm B&W) and masterclass lighting profiles (Roger Deakins, Gordon Willis, Stanley Kubrick, David Fincher, Wong Kar-wai).
* **Smart Context Equalizer:** Enforces semantic harmony so outfits match appropriate environments (e.g. private boudoir vs. rainy Parisian noir street vs. minimal editorial studio).
* **Decoupled Multi-Channel Outputs:** Connect individual channels (character_prompt, scene_prompt, master_fused_prompt, active_wardrobe_text, active_pose_text) to FaceDetailer, Regional Prompting, or Caption Savers.
* **Zero VRAM Overhead:** 100% deterministic pure Python logic.

---

## 🛠️ How to Make It Your Own (Custom Character Integration)

### Method 1: Using the custom_character_override Input Port (Recommended)
1. Add a standard **Primitive (String)** or **Text Multiline** node to your canvas.
2. Enter your character's physical baseline:
   A hyper-realistic 35mm photo of Elena, a 28-year-old Scandinavian woman with high sculpted cheekbones, piercing ice-blue eyes, natural porcelain skin texture with authentic pores, and platinum blonde hair.
3. Connect the string output to the **custom_character_override** input port on 🍷 ZIT Master Prompt Workstation.
4. In the node dropdown, select ✍️ Custom Subject (Input Port).
5. Select any **Tier (1, 2, 3, or 4)** or **👑 Full 50-Image Dataset Curated Matrix** and queue your batch!

### Method 2: Adding Your Character to the Code (zit_nodes.py)
If you want your character baked into the dropdown menu:
1. Open custom_nodes/ComfyUI-Vespera-ZIT/zit_nodes.py.
2. Add your character's name to SUBJECT_MODES.
3. Add your character description into VESPERA_VARIATIONS or define a new dictionary mapping.

---

## 📦 Installation & Setup

1. Clone or copy this repository into your ComfyUI custom nodes directory:
   cd ComfyUI/custom_nodes
   git clone https://github.com/your-username/ComfyUI-Character-Dataset-Workstation.git
2. Restart ComfyUI.
3. Search for **🍷 ZIT Master Prompt Workstation (All-In-One)** or **ZIT Character Override & Synthesizer** in the node menu.

---

## ⚖️ License
MIT License. Free for open-source AI community use and dataset curation pipelines.
