"""Interactive Streamlit demo for the generate-prompts library."""

from __future__ import annotations

import streamlit as st

from generate_prompts import PromptConfig, build_animation_frames, extend_prompt, generate_example_prompts
from generate_prompts.streamlit_component import inject_slot_css, render_prompt_cards

# ---------------------------------------------------------------------------
# Domain configs
# ---------------------------------------------------------------------------
DOMAINS: dict[str, PromptConfig] = {
    "Video Generation": PromptConfig(
        system_prompt=(
            "Generate exactly 3 simple, minimal text-to-video prompts that are easy to extend. "
            "Keep them high-quality but intentionally sparse so a user can add details later. "
            "Return only a JSON array of 3 strings."
        ),
        user_prompt=(
            "Create three diverse prompts across different styles/scenes. "
            "Each prompt should be under 120 characters, avoid long adjective chains, "
            "and leave room for expansion."
        ),
        extend_system_prompt=(
            "You improve prompts for human-centric cinematic video generation. "
            "Keep the original intent, add vivid visual details, subject motion, "
            "camera movement, lighting, style, and setting continuity. "
            "Return only the final enhanced prompt as plain text."
        ),
        extend_user_template=(
            "Enhance this prompt for high-quality video generation while preserving meaning:\n\n{prompt}"
        ),
        fallback_pool=[
            "A cat exploring a sunlit garden in slow motion",
            "Timelapse of a city skyline from sunset to night",
            "A dancer performing on a rooftop at golden hour",
        ],
    ),
    "Medical QA": PromptConfig(
        system_prompt=(
            "Generate exactly 3 clinical questions for a medical AI model. "
            "Return a JSON array of 3 strings."
        ),
        user_prompt=(
            "Create diverse questions across different specialties. "
            "Each should be concise and clinically relevant."
        ),
        extend_system_prompt=(
            "Enhance clinical questions with precise medical context, "
            "relevant lab values, and differential considerations. "
            "Return only the enhanced question as plain text."
        ),
        extend_user_template="Enhance this clinical question:\n\n{prompt}",
        fallback_pool=[
            "What are first-line treatments for type 2 diabetes with CKD?",
            "Describe the differential diagnosis for acute chest pain in a 55-year-old.",
            "What imaging is indicated for suspected pulmonary embolism?",
        ],
    ),
    "Image Generation": PromptConfig(
        system_prompt=(
            "Generate exactly 3 creative image generation prompts. "
            "Return only a JSON array of 3 strings."
        ),
        user_prompt=(
            "Create three diverse prompts for different visual styles. "
            "Each should be vivid but under 100 characters."
        ),
        extend_system_prompt=(
            "Enhance image prompts with composition, lighting, color palette, "
            "and artistic style details. Return only the enhanced prompt as plain text."
        ),
        extend_user_template="Enhance this image prompt with rich visual details:\n\n{prompt}",
        fallback_pool=[
            "A misty forest with bioluminescent mushrooms at dusk",
            "Cyberpunk street market in the rain, neon reflections",
            "Watercolor painting of a coastal village at sunrise",
        ],
    ),
}

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Prompt Generator Demo", layout="wide")
st.title("Prompt Generator & Extender")
st.caption("Generate example prompts, see slot-machine animations, and extend prompts via LLM.")
inject_slot_css()

# ---------------------------------------------------------------------------
# Domain selector
# ---------------------------------------------------------------------------
domain = st.selectbox("Domain", list(DOMAINS.keys()))
config = DOMAINS[domain]

# ---------------------------------------------------------------------------
# Generate prompts
# ---------------------------------------------------------------------------
if st.button("Generate Prompts", type="primary"):
    with st.spinner("Generating..."):
        prompts = generate_example_prompts(config)
    st.session_state["prompts"] = prompts
    st.session_state["domain"] = domain
    # Build animation frames from fallback -> generated
    st.session_state["frames"] = build_animation_frames(
        from_prompts=config.fallback_pool[:3],
        to_prompts=prompts,
        middle_pool=config.fallback_pool,
    )

# ---------------------------------------------------------------------------
# Display prompt cards
# ---------------------------------------------------------------------------
prompts: list[str] = st.session_state.get("prompts", config.fallback_pool)
frames = st.session_state.get("frames")

# Only show animations if they were just generated for the current domain
show_frames = frames if st.session_state.get("domain") == domain else None

st.subheader("Example Prompts")

def on_use(prompt: str) -> None:
    st.session_state["selected_prompt"] = prompt

render_prompt_cards(
    prompts,
    animation_frames=show_frames,
    key_prefix=f"card_{domain}",
    on_use=on_use,
)

# Clear animation frames after rendering so subsequent reruns
# (e.g. clicking "Use Prompt") show static cards, not repeat animations.
if show_frames:
    st.session_state["frames"] = None

# ---------------------------------------------------------------------------
# Extend a selected prompt
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Extend a Prompt")

selected = st.session_state.get("selected_prompt", "")
user_input = st.text_area(
    "Prompt to extend",
    value=selected,
    height=100,
    placeholder="Click 'Use Prompt' above or type your own...",
)

if st.button("Extend", disabled=not user_input.strip()):
    with st.spinner("Extending..."):
        try:
            enhanced = extend_prompt(user_input.strip(), config)
            st.session_state["selected_prompt"] = enhanced
            st.rerun()
        except RuntimeError as exc:
            st.error(f"LLM error: {exc}")
