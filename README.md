# generate-prompts

A lightweight Python library for generating and enhancing LLM prompts with built-in fallbacks and optional slot-machine animations. Works with any OpenAI-compatible API endpoint.

## What it does

- **Generate** domain-specific example prompts via an LLM, with automatic fallback to a static pool if the LLM is unavailable
- **Extend** prompts by enriching them with detail through an LLM call
- **Animate** prompt transitions with a slot-machine CSS/HTML effect (for web UIs)
- **Normalize** prompt lists to a guaranteed count, padding from a fallback pool when needed

## Project structure

```
generate-prompts/
  animation.py            # Slot-machine CSS/HTML builders
  client.py               # Stdlib HTTP client for OpenAI-compatible APIs
  config.py               # PromptConfig and LLMSettings dataclasses
  extender.py             # extend_prompt() — enhance a prompt via LLM
  generator.py            # generate_example_prompts() — generate via LLM with fallback
  normalizer.py           # normalize_prompts(), random_sample_prompts()
  streamlit_component.py  # Optional Streamlit helpers (cards, CSS injection)
  demo.py                 # Interactive Streamlit demo
  main.py                 # CLI demo across three domains
  pyproject.toml
  .env.example
```

## Adding to an existing project

### 1. Copy the source files

Clone or copy the modules you need into your project. The minimum set for prompt generation and extension is:

```bash
# From the generate-prompts repo
cp config.py client.py generator.py extender.py normalizer.py /path/to/your/project/
```

If you want the slot-machine animation UI:

```bash
cp animation.py streamlit_component.py /path/to/your/project/
```

### 2. Install the dependency

The only runtime dependency is `python-dotenv` (for loading `.env` files). If you don't use `.env` files it's optional — the library falls back gracefully.

```bash
pip install python-dotenv
```

For the Streamlit UI components:

```bash
pip install streamlit
```

### 3. Configure your LLM endpoint

Create a `.env` file (or set environment variables) with your OpenAI-compatible endpoint:

```bash
PROMPT_LLM_BASE_URL=http://localhost:8000/v1
PROMPT_LLM_MODEL=openai/gpt-oss-120b
PROMPT_LLM_API_KEY=
PROMPT_LLM_TIMEOUT=45
PROMPT_LLM_GENERATE_TEMPERATURE=0.9
PROMPT_LLM_EXTEND_TEMPERATURE=0.7
```

Or pass settings directly in code:

```python
from config import LLMSettings

settings = LLMSettings(
    base_url="https://api.openai.com/v1",
    model="gpt-4o",
    api_key="sk-...",
)
```

### 4. Define your domain config

Create a `PromptConfig` that describes what kind of prompts you need:

```python
from config import PromptConfig

my_config = PromptConfig(
    system_prompt=(
        "Generate exactly 3 short prompts for a recipe suggestion app. "
        "Return only a JSON array of 3 strings."
    ),
    user_prompt="Create three diverse recipe prompts under 100 characters each.",
    extend_system_prompt=(
        "Enhance this recipe prompt with specific ingredients, techniques, "
        "and cuisine details. Return only the enhanced prompt as plain text."
    ),
    extend_user_template="Enhance this recipe prompt:\n\n{prompt}",
    fallback_pool=[
        "Quick weeknight pasta with fresh vegetables",
        "Slow-braised lamb shoulder with root vegetables",
        "Light summer salad with citrus dressing",
    ],
    count=3,
)
```

The `fallback_pool` is critical — these are returned when the LLM is unreachable, so your UI always has prompts to display.

### 5. Generate and extend prompts

```python
from generator import generate_example_prompts
from extender import extend_prompt

# Generate — returns fallback_pool on LLM failure, never raises
prompts = generate_example_prompts(my_config)
# >>> ["Quick weeknight pasta with fresh vegetables", ...]

# Extend — raises RuntimeError on failure
enhanced = extend_prompt(prompts[0], my_config)
# >>> "Quick weeknight pasta with seasonal roasted vegetables, tossed in ..."
```

`generate_example_prompts` never raises — on any LLM error it silently returns prompts from the fallback pool. `extend_prompt` raises `RuntimeError` so you can show the error to the user.

### 6. Add the animation UI (optional)

For Streamlit apps, use the built-in components:

```python
from animation import build_animation_frames
from streamlit_component import inject_slot_css, render_prompt_cards

# Once per page
inject_slot_css()

# Build frames for the slot-machine transition
frames = build_animation_frames(
    from_prompts=my_config.fallback_pool,
    to_prompts=prompts,
    middle_pool=my_config.fallback_pool,
)

# Render cards with animation and "Use" buttons
render_prompt_cards(
    prompts,
    animation_frames=frames,
    on_use=lambda p: st.session_state.update(selected=p),
)
```

For non-Streamlit apps, use the HTML builders directly:

```python
from animation import render_animated_card, render_slot_css, build_animation_frames

css = render_slot_css()       # <style>...</style> block
html = render_animated_card(frames[0])  # <div> with animation
```

## Running the demos

**Streamlit demo** (interactive UI):

```bash
streamlit run demo.py
```

**CLI demo** (three domains, prints to terminal):

```bash
python main.py
```

## API reference

### `PromptConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `system_prompt` | `str` | Generic generation prompt | System message for generating prompts |
| `user_prompt` | `str` | Generic user prompt | User message for generating prompts |
| `extend_system_prompt` | `str` | Generic enhance prompt | System message for extending prompts |
| `extend_user_template` | `str` | `"...{prompt}"` | User message template — must contain `{prompt}` |
| `fallback_pool` | `list[str]` | `[]` | Static prompts used when the LLM is unavailable |
| `count` | `int` | `3` | Number of prompts to generate |

### `LLMSettings`

| Field | Env var | Default |
|-------|---------|---------|
| `base_url` | `PROMPT_LLM_BASE_URL` | `http://localhost:8000/v1` |
| `model` | `PROMPT_LLM_MODEL` | `openai/gpt-oss-120b` |
| `api_key` | `PROMPT_LLM_API_KEY` | `""` |
| `timeout` | `PROMPT_LLM_TIMEOUT` | `45` |
| `generate_temperature` | `PROMPT_LLM_GENERATE_TEMPERATURE` | `0.9` |
| `extend_temperature` | `PROMPT_LLM_EXTEND_TEMPERATURE` | `0.7` |

### Functions

| Function | Module | Returns | Raises |
|----------|--------|---------|--------|
| `generate_example_prompts(config, llm_settings?, client?)` | `generator` | `list[str]` | Never |
| `extend_prompt(prompt, config, llm_settings?, client?)` | `extender` | `str` | `RuntimeError` |
| `normalize_prompts(prompts, count?, fallback_pool?)` | `normalizer` | `list[str]` | Never |
| `random_sample_prompts(pool, count?)` | `normalizer` | `list[str]` | Never |
| `build_animation_frames(from_prompts, to_prompts, middle_pool, durations?)` | `animation` | `list[AnimationFrame]` | Never |
| `render_slot_css()` | `animation` | `str` (HTML) | Never |
| `render_static_card(prompt)` | `animation` | `str` (HTML) | Never |
| `render_animated_card(frame)` | `animation` | `str` (HTML) | Never |
| `inject_slot_css()` | `streamlit_component` | `None` | Never |
| `render_prompt_cards(prompts, animation_frames?, key_prefix?, on_use?)` | `streamlit_component` | `None` | Never |

## Requirements

- Python >= 3.11
- `python-dotenv` (optional, for `.env` loading)
- `streamlit` (optional, for UI components)
