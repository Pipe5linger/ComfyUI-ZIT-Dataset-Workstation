##### \# ComfyUI-ZIT-Dataset-Workstation

##### 

##### A deterministic, procedural prompt-matrix engine and dataset curation pipeline for ComfyUI. Built specifically to eliminate \*\*angle collapse\*\*, \*\*wardrobe bleed\*\*, and \*\*token competition\*\* when generating character LoRA training datasets.

##### 

##### \---

##### 

##### \## The Problem with Traditional LoRA Datasets

##### 

##### Most character LoRAs suffer from predictable failure modes caused by unstructured dataset curation:

##### \* \*\*Angle \& Pose Collapse:\*\* Standard wildcards and random generation over-sample neutral, front-facing "mugshot" poses, leaving models unable to handle dynamic 3D angles, hard profiles, or vertical pitch.

##### \* \*\*Wardrobe Bleed / Overfitting:\*\* When character tags are bound to clothing descriptions across a dataset, fine-tuning binds the character's physical identity to specific outfits.

##### \* \*\*Asset Desynchronization:\*\* Managing hundreds of generated diffusion images alongside segmentation masks often leads to orphaned files, broken training pairs, and corrupted dataset ratios.

##### 

##### The \*\*ZIT Dataset Workstation\*\* solves this by enforcing a deterministic \*\*4-Tier Training Taxonomy\*\* coupled with automatic post-processing and mask-pairing utilities.

##### 

##### \---

##### 

##### \## 4-Tier Dataset Matrix Architecture

##### 

##### The core engine structures prompt assembly across four balanced operational tiers to ensure complete geometric and semantic coverage:

##### 

##### ```text

##### +-------------------------------------------------------------------------------+

##### |                      ZIT DATASET MATRIX ENGINE PIPELINE                       |

##### +-------------------------------------------------------------------------------+

##### &#x20; \[Subject Trigger]     --> Dynamic User-Defined Physical Anchor

##### &#x20;           +

##### &#x20; \[4-Tier Anchor Matrix] --> Deterministic 3D Camera Rig / Pose / Angle

##### &#x20;           +

##### &#x20; \[Sensory Multipliers] --> Weathering, Optical Halation \& Tactile Physics

##### &#x20;           +

##### &#x20; \[Conflict Scrubber]   --> Automated Regex Filtering of Competing Tokens

##### &#x20;           |

##### &#x20;           v

##### &#x20; \[Master Prompt \& Output Sync] --> KSampler / Automated Dataset Exporter

##### 

##### ```

##### 

##### | Tier | Focus | Target Composition | Key Objectives |

##### | --- | --- | --- | --- |

##### | \*\*Tier 1: Identity Anchors\*\* | 3D Head \& Neck Geometry | 75 Unique Slots | Extreme vertical pitch (looking up/down), 90° hard profiles, over-the-shoulder gaze, macro facial details. |

##### | \*\*Tier 2: Raw Anatomy\*\* | Structural Proportions \& Skin | 50 Unique Slots | Subcutaneous realism, unblemished skin tension, strict anatomical ratios, zero clothing bias. |

##### | \*\*Tier 3: Wardrobe Agnosticism\*\* | Fabric Decoupling | 75 Unique Slots | Diverse rotations across couture, casual, activewear, and lingerie to fully decouple identity from clothing. |

##### | \*\*Tier 4: 3D Spatial Awareness\*\* | Environmental Integration | 50 Unique Slots | Wide focal depths, dynamic volumetric lighting, architectural integration, and atmospheric perspective. |

##### 

##### \---

##### 

##### \## Repository Structure

##### 

##### ```text

##### ComfyUI-ZIT-Dataset-Workstation/

##### ├── \_\_init\_\_.py                  # ComfyUI custom node package loader

##### ├── zit\_nodes.py                 # Core execution engine and node definitions

##### ├── zit\_data.py                  # 4-Tier matrix vault and optical director rigs

##### ├── organize\_lora\_dataset.py     # Pair validation, tier-renaming, and orphan quarantine

##### ├── README.md                    # Documentation

##### └── workflows/

##### &#x20;   └── zit\_dataset\_template.json # Plug-and-play ComfyUI generation workflow

##### 

##### ```

##### 

##### \---

##### 

##### \## Installation

##### 

##### 1\. Navigate to your ComfyUI `custom\\\\\\\_nodes` directory:

##### ```bash

##### cd ComfyUI/custom\_nodes

##### 

##### ```

##### 

##### 

##### 2\. Clone the repository:

##### ```bash

##### git clone \[https://github.com/YourUsername/ComfyUI-ZIT-Dataset-Workstation.git](https://github.com/YourUsername/ComfyUI-ZIT-Dataset-Workstation.git)

##### 

##### ```

##### 

##### 

##### 3\. Restart ComfyUI.

##### 

##### \---

##### 

##### \## Quickstart Workflow

##### 

##### 1\. Open ComfyUI and load `workflows/zit\\\\\\\_dataset\\\\\\\_template.json`.

##### 2\. Locate the \*\*ZIT Dataset Matrix Workstation\*\* node:

##### \* Enter your character's primary \*\*Subject Trigger\*\* (e.g., `my\\\\\\\_character, 1girl`).

##### \* Define your target \*\*Physical/Anatomical Markers\*\* (e.g., `detailed skin texture, athletic build`).

##### \* Select your target generation \*\*Tier\*\* (Tiers 1–4).

##### 

##### 

##### 3\. Queue your batch run. The workflow generates full-resolution renders and automatic black-and-white training masks via BiRefNet.

##### 

##### \---

##### 

##### \## Automated Dataset Pairing \& Curation Utility

##### 

##### After generating your batches, run the included asset management script from your terminal:

##### 

##### ```bash

##### python organize\_lora\_dataset.py

##### 

##### ```

##### 

##### \### What `organize\\\\\\\_lora\\\\\\\_dataset.py` Does:

##### 

##### \* \*\*Active Directory Introspection:\*\* Automatically scans whatever terminal directory or Desktop path you run it from.

##### \* \*\*Strict Pair Enforcement:\*\* Matches every rendered image with its exact companion mask using sequential index tracking.

##### \* \*\*Automatic Orphan Quarantine:\*\* If an image was deleted during visual culling, the script isolates the remaining orphan mask and moves it to `Desktop/orphans/` to prevent training corruption.

##### \* \*\*Canonical Tier Renaming:\*\* Renames paired assets into standardized formats ready for OneTrainer or Kohya:

##### ```text

##### my\_character\_tier1\_anchor\_00001.png

##### my\_character\_tier1\_anchor\_00001\_mask.png

##### 

##### ```

##### 

##### 

##### 

##### \---

##### 

##### \## Roadmap \& Discussion

##### 

##### \* \[ ] External JSON/YAML config support for user-defined custom tier matrices.

##### \* \[ ] Native OneTrainer / Kohya `.toml` metadata export integration.

##### \* \[ ] Multi-subject interactive prompt conditioning.

##### 

##### \### Connect \& Collaborate

##### 

##### This architecture was designed to explore procedural dataset engineering and eliminate sample bias in local diffusion model training.

##### 

##### If you are working on fine-tuning pipelines, dataset optimization, or prompt matrix architectures, feel free to open an issue, submit a PR, or start a discussion on GitHub!

##### 

##### \---

##### 

##### \## License

##### 

##### MIT License. Free for personal and commercial fine-tuning pipelines.

##### 

##### ```

##### 

##### ```

