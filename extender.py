"""Extend/enhance a prompt via an LLM."""

from __future__ import annotations

from client import LLMClient
from config import LLMSettings, PromptConfig


def extend_prompt(
    prompt: str,
    config: PromptConfig,
    llm_settings: LLMSettings | None = None,
    client: LLMClient | None = None,
) -> str:
    """Enhance *prompt* using the LLM described by *config*.

    Raises :class:`RuntimeError` on any failure — the caller is
    expected to show the error to the user who is actively waiting.
    """
    settings = llm_settings or LLMSettings()
    llm = client or LLMClient(settings)

    messages = [
        {"role": "system", "content": config.extend_system_prompt},
        {
            "role": "user",
            "content": config.extend_user_template.format(prompt=prompt),
        },
    ]

    return llm.chat(messages, temperature=settings.extend_temperature)
