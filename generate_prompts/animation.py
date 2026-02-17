"""Slot-machine animation CSS and HTML builders."""

from __future__ import annotations

import html
from dataclasses import dataclass, field

SLOT_CSS = """\
.example-slot-card {
    border: 1px solid rgba(0, 179, 136, 0.35);
    border-radius: 12px;
    min-height: 150px;
    max-height: 150px;
    padding: 12px;
    overflow: hidden;
    color: #e9f5ee;
    background: linear-gradient(180deg, rgba(11, 17, 14, 0.95), rgba(14, 24, 19, 0.95));
    font-size: 0.92rem;
    line-height: 1.35;
}
.example-slot-shell {
    border: 1px solid rgba(0, 179, 136, 0.35);
    border-radius: 12px;
    min-height: 150px;
    max-height: 150px;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(11, 17, 14, 0.95), rgba(14, 24, 19, 0.95));
}
.example-slot-reel {
    --slot-item-height: 150px;
    display: flex;
    flex-direction: column;
    transform: translateY(0);
    animation-name: slot-reel-stop;
    animation-timing-function: cubic-bezier(0.18, 0.9, 0.24, 1.06);
    animation-fill-mode: forwards;
}
.example-slot-item {
    min-height: 150px;
    max-height: 150px;
    padding: 12px;
    color: #e9f5ee;
    font-size: 0.92rem;
    line-height: 1.35;
    overflow: hidden;
}
@keyframes slot-reel-stop {
    0% {
        transform: translateY(0);
        filter: blur(0.6px);
    }
    82% {
        transform: translateY(calc(-3 * var(--slot-item-height)));
        filter: blur(0);
    }
    92% {
        transform: translateY(calc(-3 * var(--slot-item-height) + 8px));
    }
    100% {
        transform: translateY(calc(-3 * var(--slot-item-height)));
    }
}
"""

DEFAULT_DURATIONS_MS = [900, 1200, 1500]


@dataclass
class AnimationFrame:
    """One card's worth of slot-machine animation data."""

    from_prompt: str
    middle_1: str
    middle_2: str
    to_prompt: str
    duration_ms: int = 1200


def build_animation_frames(
    from_prompts: list[str],
    to_prompts: list[str],
    middle_pool: list[str],
    durations: list[int] | None = None,
) -> list[AnimationFrame]:
    """Build one :class:`AnimationFrame` per card with staggered timing.

    *middle_pool* is used to pick two intermediate reel items per card.
    *durations* defaults to ``[900, 1200, 1500]``.
    """
    import random

    durations = durations or DEFAULT_DURATIONS_MS
    count = min(len(from_prompts), len(to_prompts))
    frames: list[AnimationFrame] = []

    for i in range(count):
        m1 = random.choice(middle_pool) if middle_pool else ""
        m2 = random.choice(middle_pool) if middle_pool else ""
        frames.append(
            AnimationFrame(
                from_prompt=from_prompts[i],
                middle_1=m1,
                middle_2=m2,
                to_prompt=to_prompts[i],
                duration_ms=durations[i % len(durations)],
            )
        )

    return frames


def render_slot_css() -> str:
    """Return a ``<style>`` block containing the slot-machine CSS."""
    return f"<style>\n{SLOT_CSS}</style>"


def render_static_card(prompt: str) -> str:
    """Return an HTML ``<div>`` for a non-animated prompt card."""
    return f"<div class='example-slot-card'>{html.escape(prompt)}</div>"


def render_animated_card(frame: AnimationFrame) -> str:
    """Return an HTML block for one animated slot-machine reel."""
    return (
        "<div class='example-slot-shell'>"
        f"<div class='example-slot-reel' style='animation-duration:{frame.duration_ms}ms;'>"
        f"<div class='example-slot-item'>{html.escape(frame.from_prompt)}</div>"
        f"<div class='example-slot-item'>{html.escape(frame.middle_1)}</div>"
        f"<div class='example-slot-item'>{html.escape(frame.middle_2)}</div>"
        f"<div class='example-slot-item'>{html.escape(frame.to_prompt)}</div>"
        "</div>"
        "</div>"
    )
