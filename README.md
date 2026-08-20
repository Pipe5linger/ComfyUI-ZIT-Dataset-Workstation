# ComfyUI-ZIT-Dataset-Workstation

A deterministic, procedural prompt-matrix engine and dataset curation pipeline for ComfyUI. Built specifically to eliminate **angle collapse**, **wardrobe bleed**, and **token competition** when generating character LoRA training datasets.

---

## The Problem with Traditional LoRA Datasets

Most character LoRAs suffer from predictable failure modes caused by unstructured dataset curation:
* **Angle & Pose Collapse:** Standard wildcards and random generation over-sample neutral, front-facing "mugshot" poses, leaving models unable to handle dynamic 3D angles, hard profiles, or vertical pitch.
* **Wardrobe Bleed / Overfitting:** When character tags are bound to clothing descriptions across a dataset, fine-tuning binds the character's physical identity to specific outfits.
* **Asset Desynchronization:** Managing hundreds of generated diffusion images alongside segmentation masks often leads to orphaned files, broken training pairs, and corrupted dataset ratios.

The **ZIT Dataset Workstation** solves this by enforcing a deterministic **4-Tier Training Taxonomy** coupled with automatic post-processing and mask-pairing utilities.

---

## 4-Tier Dataset Matrix Architecture

The core engine structures prompt assembly across four balanced operational tiers to ensure complete geometric and semantic coverage:

```text
+-------------------------------------------------------------------------------+
|                      ZIT DATASET MATRIX ENGINE PIPELINE                       |
+-------------------------------------------------------------------------------+
  [Subject Trigger]     --> Dynamic User-Defined Physical Anchor
            +
  [4-Tier Anchor Matrix] --> Deterministic 3D Camera Rig / Pose / Angle
            +
  [Sensory Multipliers] --> Weathering, Optical Halation & Tactile Physics
            +
  [Conflict Scrubber]   --> Automated Regex Filtering of Competing Tokens
            |
            v
  [Master Prompt & Output Sync] --> KSampler / Automated Dataset Exporter