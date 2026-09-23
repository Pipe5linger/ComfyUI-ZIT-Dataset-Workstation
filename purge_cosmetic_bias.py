import os
import re

target_files = [
    r"D:\AI\Projects\ComfyUI\custom_nodes\ComfyUI-Vespera-ZIT\zit_data.py",
    r"D:\AI\Projects\ComfyUI\custom_nodes\ComfyUI-Vespera-ZIT\prompt_workstation_refactor.py",
    r"D:\AI\Projects\ComfyUI\custom_nodes\ComfyUI-Vespera-ZIT\ollama_coherent_prompt_node.py"
]

replacements = [
    (re.compile(r"soft black satin-sheen lips", re.IGNORECASE), "soft naturally contoured satin-sheen lips"),
    (re.compile(r"soft black satin lips", re.IGNORECASE), "soft naturally contoured satin lips"),
    (re.compile(r"soft black lips", re.IGNORECASE), "soft naturally contoured lips"),
    (re.compile(r"black satin lips", re.IGNORECASE), "naturally contoured satin lips"),
    (re.compile(r"black lips", re.IGNORECASE), "naturally contoured lips"),
    (re.compile(r"smoky black kohl eyeliner", re.IGNORECASE), "smoky eyeliner shadow"),
    (re.compile(r"smoky black kohl", re.IGNORECASE), "smoky eyeliner shadow"),
    (re.compile(r"midnight blackberry lips", re.IGNORECASE), "naturally contoured lips"),
    (re.compile(r"dark berry lips", re.IGNORECASE), "naturally contoured lips")
]

for filepath in target_files:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content
    for pattern, replacement in replacements:
        content = pattern.sub(replacement, content)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes needed: {filepath}")
