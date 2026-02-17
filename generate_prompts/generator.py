"""Generate example prompts via an LLM."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .client import LLMClient
from .config import LLMSettings, PromptConfig
from .normalizer import normalize_prompts, random_sample_prompts

if TYPE_CHECKING:
    pass


def generate_example_prompts(
    config: PromptConfig,
    llm_settings: LLMSettings | None = None,
    client: LLMClient | None = None,
) -> list[str]:
    """Generate example prompts for a domain described by *config*.

    On any LLM failure the function falls back silently to
    ``config.fallback_pool`` so callers never see an exception.
    """
    settings = llm_settings or LLMSettings()
    llm = client or LLMClient(settings)
    fallback = random_sample_prompts(config.fallback_pool, config.count)

    messages = [
        {"role": "system", "content": config.system_prompt},
        {"role": "user", "content": config.user_prompt},
    ]

    try:
        raw = llm.chat(messages, temperature=settings.generate_temperature)
        cleaned = raw.strip().strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
        parsed = json.loads(cleaned)
        if isinstance(parsed, list):
            prompts = [str(item).strip() for item in parsed if str(item).strip()]
            return normalize_prompts(
                prompts, count=config.count, fallback_pool=config.fallback_pool
            )
    except Exception:
        return fallback

    return fallback
