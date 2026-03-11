"""Optional Streamlit helpers (lazy-imported so the core library works without Streamlit)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from .animation import (
    AnimationFrame,
    render_animated_card,
    render_slot_css,
    render_static_card,
)

if TYPE_CHECKING:
    pass


def inject_slot_css() -> None:
    """Inject the slot-machine CSS into the current Streamlit page."""
    import streamlit as st

    st.markdown(render_slot_css(), unsafe_allow_html=True)


def render_prompt_cards(
    prompts: list[str],
    animation_frames: list[AnimationFrame] | None = None,
    key_prefix: str = "prompt",
    on_use: Callable[[str], None] | None = None,
) -> None:
    """Render prompt cards in columns with optional animation and *Use* buttons.

    Parameters
    ----------
    prompts:
        The final prompts to display (one per column).
    animation_frames:
        If provided, renders animated slot-machine reels instead of
        static cards.  Should have the same length as *prompts*.
    key_prefix:
        Streamlit widget key prefix to avoid collisions.
    on_use:
        Callback invoked with the prompt text when a *Use* button is
        clicked.  If ``None``, no buttons are rendered.
    """
    import streamlit as st

    # Auto-increment a counter each time animation_frames are provided so
    # every render gets unique @keyframes names and the browser replays the
    # CSS animation instead of ignoring a duplicate animation-name.
    counter_key = f"_slot_anim_counter_{key_prefix}"
    st.session_state.setdefault(counter_key, 0)
    if animation_frames:
        st.session_state[counter_key] += 1
    anim_id = st.session_state[counter_key]

    columns = st.columns(len(prompts))

    for idx, prompt in enumerate(prompts):
        with columns[idx]:
            if animation_frames and idx < len(animation_frames):
                card_id = f"{anim_id}-{idx}"
                st.markdown(
                    render_animated_card(animation_frames[idx], card_id=card_id),
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    render_static_card(prompt),
                    unsafe_allow_html=True,
                )

            if on_use is not None:
                if st.button(
                    f"Use Prompt {idx + 1}",
                    key=f"{key_prefix}_use_{idx + 1}",
                    use_container_width=True,
                ):
                    on_use(prompt)
