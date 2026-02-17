"""generate-prompts — reusable LLM prompt generator & extender library."""

from .animation import (
    SLOT_CSS,
    AnimationFrame,
    build_animation_frames,
    render_animated_card,
    render_slot_css,
    render_static_card,
)
from .client import LLMClient
from .config import LLMSettings, PromptConfig
from .extender import extend_prompt
from .generator import generate_example_prompts
from .normalizer import normalize_prompts, random_sample_prompts

__all__ = [
    "AnimationFrame",
    "LLMClient",
    "LLMSettings",
    "PromptConfig",
    "SLOT_CSS",
    "build_animation_frames",
    "extend_prompt",
    "generate_example_prompts",
    "normalize_prompts",
    "random_sample_prompts",
    "render_animated_card",
    "render_slot_css",
    "render_static_card",
]
