"""Reusable LLM prompt generator & extender library."""

from .animation import AnimationFrame, build_animation_frames, render_animated_card, render_slot_css, render_static_card
from .config import LLMSettings, PromptConfig
from .client import LLMClient
from .extender import extend_prompt
from .generator import generate_example_prompts
from .normalizer import normalize_prompts, random_sample_prompts

__all__ = [
    "AnimationFrame",
    "LLMClient",
    "LLMSettings",
    "PromptConfig",
    "build_animation_frames",
    "extend_prompt",
    "generate_example_prompts",
    "normalize_prompts",
    "random_sample_prompts",
    "render_animated_card",
    "render_slot_css",
    "render_static_card",
]
