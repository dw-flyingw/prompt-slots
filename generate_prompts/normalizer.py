"""Utilities for normalising and padding prompt lists."""

from __future__ import annotations

import random


def normalize_prompts(
    prompts: list[str],
    count: int = 3,
    fallback_pool: list[str] | None = None,
) -> list[str]:
    """Return exactly *count* non-empty prompt strings.

    Strips whitespace, drops blanks, then pads from *fallback_pool* if
    there are fewer than *count* valid prompts.
    """
    pool = fallback_pool or []
    cleaned = [s.strip() for s in prompts if s and s.strip()]

    if len(cleaned) < count:
        for candidate in pool:
            if len(cleaned) >= count:
                break
            if candidate not in cleaned:
                cleaned.append(candidate)

    # Last-resort padding with placeholder text
    while len(cleaned) < count:
        cleaned.append("Sample prompt unavailable.")

    return cleaned[:count]


def random_sample_prompts(
    pool: list[str],
    count: int = 3,
) -> list[str]:
    """Return *count* random prompts from *pool*, with replacement if needed."""
    if not pool:
        return ["Sample prompt unavailable."] * count
    if len(pool) >= count:
        return random.sample(pool, count)
    return [random.choice(pool) for _ in range(count)]
