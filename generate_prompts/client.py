"""Stdlib-only HTTP client for OpenAI-compatible chat endpoints."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import LLMSettings


class LLMClient:
    """Minimal OpenAI-compatible chat client using only :mod:`urllib`."""

    def __init__(self, settings: LLMSettings) -> None:
        self._settings = settings
        self._endpoint = f"{settings.base_url.rstrip('/')}/chat/completions"

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
    ) -> str:
        """Send a chat completion request and return the assistant text."""
        payload = {
            "model": self._settings.model,
            "temperature": temperature if temperature is not None else 0.7,
            "messages": messages,
        }
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._settings.api_key:
            headers["Authorization"] = f"Bearer {self._settings.api_key}"

        req = urllib.request.Request(
            self._endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                req, timeout=self._settings.timeout
            ) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(
                f"LLM request failed ({exc.code}): {detail[:400]}"
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc

        choices = body.get("choices", [])
        if not choices:
            raise RuntimeError("LLM response did not include choices")

        content = choices[0].get("message", {}).get("content", "")
        if isinstance(content, list):
            parts = [
                part.get("text", "")
                for part in content
                if isinstance(part, dict)
            ]
            content = "\n".join(p for p in parts if p.strip())

        text = content.strip()
        if not text:
            raise RuntimeError("LLM returned an empty response")
        return text
