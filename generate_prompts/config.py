"""Configuration dataclasses for the generate-prompts library."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


@dataclass
class LLMSettings:
    """LLM endpoint settings, loaded from ``PROMPT_LLM_*`` env vars."""

    base_url: str = field(
        default_factory=lambda: os.environ.get(
            "PROMPT_LLM_BASE_URL", "http://localhost:8000/v1"
        )
    )
    model: str = field(
        default_factory=lambda: os.environ.get(
            "PROMPT_LLM_MODEL", "openai/gpt-oss-120b"
        )
    )
    api_key: str = field(
        default_factory=lambda: os.environ.get("PROMPT_LLM_API_KEY", "")
    )
    timeout: int = field(
        default_factory=lambda: int(os.environ.get("PROMPT_LLM_TIMEOUT", "45"))
    )
    generate_temperature: float = field(
        default_factory=lambda: float(
            os.environ.get("PROMPT_LLM_GENERATE_TEMPERATURE", "0.9")
        )
    )
    extend_temperature: float = field(
        default_factory=lambda: float(
            os.environ.get("PROMPT_LLM_EXTEND_TEMPERATURE", "0.7")
        )
    )


@dataclass
class PromptConfig:
    """Domain-specific prompt configuration.

    Defines what kind of prompts the library generates and how it
    enhances them.  Completely independent of deployment settings.
    """

    system_prompt: str = (
        "Generate exactly 3 simple, minimal prompts. "
        "Return only a JSON array of 3 strings."
    )
    user_prompt: str = (
        "Create three diverse prompts. "
        "Each should be under 140 characters and leave room for expansion."
    )
    extend_system_prompt: str = (
        "You improve prompts by adding vivid detail while preserving intent. "
        "Return only the final enhanced prompt as plain text."
    )
    extend_user_template: str = (
        "Enhance this prompt while preserving meaning:\n\n{prompt}"
    )
    fallback_pool: list[str] = field(default_factory=list)
    count: int = 3
