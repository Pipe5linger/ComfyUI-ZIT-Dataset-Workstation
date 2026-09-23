"""
Package : ComfyUI-Vespera-ZIT
Purpose : Resilient Custom Node Pack for Zero-Shot Image Transfer (ZIT) Character Override,
          Dynamic Backbone Matrix, Auto-Tuning & Watchdog.
          Features Fault-Isolated Modular Loading to prevent cascading import failures.
"""

import sys
import traceback

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 1. Base ZIT Multi-Nodes
try:
    from .zit_nodes import (
        NODE_CLASS_MAPPINGS as ZIT_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS as ZIT_DISPLAY_MAPPINGS
    )
    NODE_CLASS_MAPPINGS.update(ZIT_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(ZIT_DISPLAY_MAPPINGS)
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading zit_nodes.py: {e}")
    traceback.print_exc()

# 2. Refactored Prompt Workstation
try:
    from .prompt_workstation_refactor import RefactoredPromptWorkstation
    NODE_CLASS_MAPPINGS["RefactoredPromptWorkstation"] = RefactoredPromptWorkstation
    NODE_DISPLAY_NAME_MAPPINGS["RefactoredPromptWorkstation"] = "Prompt Workstation (Refactored)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading prompt_workstation_refactor.py: {e}")

# 3. Refactored Wardrobe Node
try:
    from .wardrobe_node_refactor import RefactoredWardrobeNode
    NODE_CLASS_MAPPINGS["RefactoredWardrobeNode"] = RefactoredWardrobeNode
    NODE_DISPLAY_NAME_MAPPINGS["RefactoredWardrobeNode"] = "Dynamic Wardrobe (Refactored) [Static]"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading wardrobe_node_refactor.py: {e}")

# 4. Refactored Scene & Lighting Node
try:
    from .scene_lighting_node_refactor import RefactoredSceneLightingNode
    NODE_CLASS_MAPPINGS["RefactoredSceneLightingNode"] = RefactoredSceneLightingNode
    NODE_DISPLAY_NAME_MAPPINGS["RefactoredSceneLightingNode"] = "Scene & Lighting (Refactored) [Static]"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading scene_lighting_node_refactor.py: {e}")

# 5. Refactored Pose & Action Node
try:
    from .pose_action_node_refactor import RefactoredPoseActionNode
    NODE_CLASS_MAPPINGS["RefactoredPoseActionNode"] = RefactoredPoseActionNode
    NODE_DISPLAY_NAME_MAPPINGS["RefactoredPoseActionNode"] = "Pose & Action (Refactored)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading pose_action_node_refactor.py: {e}")

# 6. Ollama Dynamic Scene & Lighting
try:
    from .ollama_scene_lighting_node import OllamaSceneLightingNode
    NODE_CLASS_MAPPINGS["OllamaSceneLightingNode"] = OllamaSceneLightingNode
    NODE_DISPLAY_NAME_MAPPINGS["OllamaSceneLightingNode"] = "Scene & Lighting (Ollama LLM)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading ollama_scene_lighting_node.py: {e}")

# 7. Ollama Dynamic Wardrobe
try:
    from .ollama_wardrobe_node import OllamaWardrobeNode
    NODE_CLASS_MAPPINGS["OllamaWardrobeNode"] = OllamaWardrobeNode
    NODE_DISPLAY_NAME_MAPPINGS["OllamaWardrobeNode"] = "Dynamic Wardrobe (Ollama LLM)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading ollama_wardrobe_node.py: {e}")

# 7.5 Ollama Coherent Prompt Node
try:
    from .ollama_coherent_prompt_node import OllamaCoherentPromptNode
    NODE_CLASS_MAPPINGS["OllamaCoherentPromptNode"] = OllamaCoherentPromptNode
    NODE_DISPLAY_NAME_MAPPINGS["OllamaCoherentPromptNode"] = "👑 Coherent Prompt Matrix (Ollama LLM)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading ollama_coherent_prompt_node.py: {e}")

# 7.6 Ollama LoRA Critic Node
try:
    from .ollama_lora_critic_node import OllamaLoRACriticNode
    NODE_CLASS_MAPPINGS["OllamaLoRACriticNode"] = OllamaLoRACriticNode
    NODE_DISPLAY_NAME_MAPPINGS["OllamaLoRACriticNode"] = "👑 Ollama LoRA Critic (Advisory)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading ollama_lora_critic_node.py: {e}")

# 7.7 Auto LoRA Mutator Node
try:
    from .auto_lora_mutator_node import AutoLoRAMutatorNode
    NODE_CLASS_MAPPINGS["AutoLoRAMutatorNode"] = AutoLoRAMutatorNode
    NODE_DISPLAY_NAME_MAPPINGS["AutoLoRAMutatorNode"] = "👑 Auto LoRA Stack Mutator (Vespera-ZIT)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading auto_lora_mutator_node.py: {e}")


# 8. Qwen Vision Critic
try:
    from .qwen_vision_critic_node import QwenVisionCriticNode
    NODE_CLASS_MAPPINGS["QwenVisionCriticNode"] = QwenVisionCriticNode
    NODE_DISPLAY_NAME_MAPPINGS["QwenVisionCriticNode"] = "👑 Qwen Vision Critic (Vespera-ZIT)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading qwen_vision_critic_node.py: {e}")

# 9. Auto Parameter Mutator
try:
    from .auto_parameter_mutator_node import AutoParameterMutatorNode
    NODE_CLASS_MAPPINGS["AutoParameterMutatorNode"] = AutoParameterMutatorNode
    NODE_DISPLAY_NAME_MAPPINGS["AutoParameterMutatorNode"] = "👑 Auto Parameter Mutator & Wildcard (Vespera-ZIT)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading auto_parameter_mutator_node.py: {e}")

# 10. Execution Watchdog
try:
    from .execution_watchdog_node import ExecutionWatchdogNode
    NODE_CLASS_MAPPINGS["ExecutionWatchdogNode"] = ExecutionWatchdogNode
    NODE_DISPLAY_NAME_MAPPINGS["ExecutionWatchdogNode"] = "👑 Execution Watchdog & Kill Order (Vespera-ZIT)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading execution_watchdog_node.py: {e}")

# 11. Dynamic Backbone Loader
try:
    from .dynamic_backbone_loader_node import DynamicBackboneLoaderNode
    NODE_CLASS_MAPPINGS["DynamicBackboneLoaderNode"] = DynamicBackboneLoaderNode
    NODE_DISPLAY_NAME_MAPPINGS["DynamicBackboneLoaderNode"] = "🔄 Dynamic Backbone Matrix Loader (FP8/BF16/CLIP)"
except Exception as e:
    print(f"\n❌ [ComfyUI-Vespera-ZIT] Failed loading dynamic_backbone_loader_node.py: {e}")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
