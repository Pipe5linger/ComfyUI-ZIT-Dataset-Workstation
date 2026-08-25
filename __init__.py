"""
Package : ComfyUI-Vespera-ZIT
Purpose : First-Class Custom Node Pack for Zero-Shot Image Transfer (ZIT) Character Override.
"""

from .zit_nodes import NODE_CLASS_MAPPINGS as ZIT_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ZIT_DISPLAY_MAPPINGS
from .prompt_workstation_refactor import RefactoredPromptWorkstation
from .wardrobe_node_refactor import RefactoredWardrobeNode
from .scene_lighting_node_refactor import RefactoredSceneLightingNode
from .pose_action_node_refactor import RefactoredPoseActionNode
from .ollama_scene_lighting_node import OllamaSceneLightingNode
from .ollama_wardrobe_node import OllamaWardrobeNode

NODE_CLASS_MAPPINGS = {
    **ZIT_CLASS_MAPPINGS,
    "RefactoredPromptWorkstation": RefactoredPromptWorkstation,
    "RefactoredWardrobeNode":      RefactoredWardrobeNode,
    "RefactoredSceneLightingNode": RefactoredSceneLightingNode,
    "RefactoredPoseActionNode":    RefactoredPoseActionNode,
    "OllamaSceneLightingNode":     OllamaSceneLightingNode,
    "OllamaWardrobeNode":          OllamaWardrobeNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **ZIT_DISPLAY_MAPPINGS,
    "RefactoredPromptWorkstation": "Prompt Workstation (Refactored)",
    "RefactoredWardrobeNode":      "Dynamic Wardrobe (Refactored) [Static]",
    "RefactoredSceneLightingNode": "Scene & Lighting (Refactored) [Static]",
    "RefactoredPoseActionNode":    "Pose & Action (Refactored)",
    "OllamaSceneLightingNode":     "Scene & Lighting (Ollama LLM)",
    "OllamaWardrobeNode":          "Dynamic Wardrobe (Ollama LLM)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
