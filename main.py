"""Demo showing generate-prompts across three domains."""

from generate_prompts import (
    PromptConfig,
    build_animation_frames,
    extend_prompt,
    generate_example_prompts,
    render_animated_card,
)

# ---------------------------------------------------------------------------
# Domain 1: Video Generation
# ---------------------------------------------------------------------------
VIDEO_CONFIG = PromptConfig(
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
)

# ---------------------------------------------------------------------------
# Domain 2: Medical QA
# ---------------------------------------------------------------------------
MEDICAL_CONFIG = PromptConfig(
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
)

# ---------------------------------------------------------------------------
# Domain 3: Image Generation
# ---------------------------------------------------------------------------
IMAGE_CONFIG = PromptConfig(
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
)


def main() -> None:
    configs = {
        "Video Generation": VIDEO_CONFIG,
        "Medical QA": MEDICAL_CONFIG,
        "Image Generation": IMAGE_CONFIG,
    }

    for name, config in configs.items():
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")

        # --- Generate examples ---
        prompts = generate_example_prompts(config)
        print("\nGenerated examples:")
        for i, p in enumerate(prompts, 1):
            print(f"  {i}. {p}")

        # --- Extend the first prompt ---
        print(f"\nExtending: {prompts[0]!r}")
        try:
            enhanced = extend_prompt(prompts[0], config)
            print(f"  Enhanced: {enhanced}")
        except RuntimeError as exc:
            print(f"  [Error] {exc}")

        # --- Animation HTML (just show it renders) ---
        frames = build_animation_frames(
            from_prompts=config.fallback_pool[:3],
            to_prompts=prompts,
            middle_pool=config.fallback_pool,
        )
        html_snippet = render_animated_card(frames[0])
        print(f"\nAnimation HTML ({len(html_snippet)} chars): {html_snippet[:120]}...")


if __name__ == "__main__":
    main()
