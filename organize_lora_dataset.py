import os
import re
import shutil
from pathlib import Path

# ==============================================================================
# USER CONFIGURATION (Edit these before running)
# ==============================================================================
CHARACTER_NAME = "my_character" # Change this to your character's name
DATASET_OUTPUT_DIR = r"./curated_lora_dataset" # Defaults to a local subfolder
REQUIRE_STRICT_PAIRS = True
# ==============================================================================
# ... (Keep the rest of your robust orphan-quarantine logic exactly the same) ...