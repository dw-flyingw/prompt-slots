# add-prompt-slots Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a personal Claude Code skill that guides integration of the generate-prompts library (example prompt cards + AI prompt extension) into any existing project.

**Architecture:** Single SKILL.md file in `~/.claude/skills/add-prompt-slots/`. The skill is an integration guide that tells Claude how to vendor the library, write domain-specific config, wire up the UI for any framework, and configure the LLM connection.

**Tech Stack:** Claude Code skills (YAML frontmatter + Markdown), generate-prompts Python library

---

### Task 1: Create the skill directory

**Files:**
- Create: `~/.claude/skills/add-prompt-slots/` (directory)

**Step 1: Create the directory**

```bash
mkdir -p ~/.claude/skills/add-prompt-slots
```

**Step 2: Verify**

```bash
ls ~/.claude/skills/add-prompt-slots/
```

Expected: empty directory exists

---

### Task 2: Write the SKILL.md

**Files:**
- Create: `~/.claude/skills/add-prompt-slots/SKILL.md`

**Step 1: Write the skill file**

Create `~/.claude/skills/add-prompt-slots/SKILL.md` with this exact content:

```markdown
---
name: add-prompt-slots
description: Use when a project needs example prompt suggestions for users to select and an AI-powered prompt extend/enhance feature — integrates the generate-prompts library into any UI framework
---

# Add Prompt Slots

## Overview

Integrate the `generate_prompts` library into an existing project to provide clickable example prompt cards (with slot-machine animation) and an AI-powered "Extend Prompt" feature. Works with any UI framework. The library uses only Python stdlib for HTTP (zero external deps beyond `python-dotenv`).

## When to Use

- Adding example/suggested prompts to a UI
- Users need clickable prompt cards to select from
- Adding a "enhance/extend my prompt" AI feature
- Integrating prompt generation into Streamlit, React, Gradio, Flask, or any other framework

## Execution Loop

**When this skill is invoked, follow this checklist in exact order. Use TodoWrite to create a task for each step, then execute them one by one.**

### Step 1: Analyze the target project

Identify:
- **UI framework** (Streamlit, React, Gradio, Flask, etc.)
- **Domain** (medical, video, coding, legal, etc.) — this drives prompt content
- **Existing LLM usage** — if the project already calls an LLM, note the endpoint/model
- **Project structure** — where source code lives, how deps are managed
- **Where prompt cards should appear** in the UI

### Step 2: Copy the generate-prompts package

Copy from `/data2/opt/generate-prompts/generate_prompts/` into the target project.

**Always copy (core):**
- `__init__.py`
- `config.py` — LLMSettings + PromptConfig dataclasses
- `client.py` — stdlib-only HTTP client
- `generator.py` — generate_example_prompts() with silent fallback
- `extender.py` — extend_prompt() that raises on failure
- `normalizer.py` — ensures exactly N prompts returned

**Copy if Streamlit project:**
- `animation.py` — slot-machine CSS/HTML builders
- `streamlit_component.py` — inject_slot_css(), render_prompt_cards()

**Copy if non-Streamlit but wants animation:**
- `animation.py` — the HTML/CSS it generates is pure HTML, works anywhere

**Never copy:**
- `demo.py`, `main.py` — demos only

Place the package in a sensible location for the project (e.g., `src/generate_prompts/`, `lib/generate_prompts/`, or at the project root as `generate_prompts/`).

After copying, remove any `__pycache__` directories:
```bash
find <target>/generate_prompts -type d -name __pycache__ -exec rm -rf {} +
```

### Step 3: Write a domain-specific PromptConfig

Create a config file (or add to an existing config module) with a `PromptConfig` tailored to the project's domain.

**Rules:**
- `system_prompt` MUST end with `"Return only a JSON array of N strings."` — the generator parses JSON
- `user_prompt` should request diverse, concise prompts (under 120 chars) relevant to the domain
- `extend_system_prompt` should instruct the LLM to preserve user intent while adding domain-relevant detail
- `extend_user_template` MUST contain `{prompt}` as the placeholder
- `fallback_pool` should have at least 2x `count` entries (e.g., 6+ for count=3)
- `count` defaults to 3

**Example for a medical Q&A project:**

```python
from generate_prompts import PromptConfig

medical_config = PromptConfig(
    system_prompt=(
        "Generate exactly 3 example medical questions a patient might ask. "
        "Cover diverse topics. Return only a JSON array of 3 strings."
    ),
    user_prompt="Create three diverse medical questions under 120 characters each.",
    extend_system_prompt=(
        "Enhance this medical question with relevant clinical context, "
        "specificity, and detail. Preserve the original intent. "
        "Return only the enhanced question as plain text."
    ),
    extend_user_template="Enhance this medical question:\n\n{prompt}",
    fallback_pool=[
        "What are common symptoms of type 2 diabetes?",
        "How does blood pressure medication work?",
        "What vaccinations do adults need annually?",
        "What causes chronic lower back pain?",
        "How do I interpret my cholesterol numbers?",
        "What are early warning signs of a stroke?",
    ],
    count=3,
)
```

### Step 4: Wire up the UI

#### Streamlit projects

```python
from generate_prompts import (
    PromptConfig, generate_example_prompts, extend_prompt,
    build_animation_frames, inject_slot_css, render_prompt_cards,
)

# Once at top of page
inject_slot_css()

# Generate prompts (on button click or first load)
if "prompts" not in st.session_state:
    st.session_state["prompts"] = generate_example_prompts(config)

# Render cards with animation
if st.button("Generate New Prompts"):
    old = st.session_state["prompts"]
    new = generate_example_prompts(config)
    st.session_state["prompts"] = new
    st.session_state["frames"] = build_animation_frames(
        from_prompts=old,
        to_prompts=new,
        middle_pool=config.fallback_pool,
    )

render_prompt_cards(
    st.session_state["prompts"],
    animation_frames=st.session_state.get("frames"),
    on_use=lambda p: st.session_state.update({"selected": p}),
)
st.session_state["frames"] = None  # Clear after render

# Extend prompt
user_input = st.text_area("Your prompt", value=st.session_state.get("selected", ""))
if st.button("Extend Prompt"):
    try:
        enhanced = extend_prompt(user_input.strip(), config)
        st.session_state["selected"] = enhanced
        st.rerun()
    except RuntimeError as e:
        st.error(str(e))
```

#### Non-Streamlit projects

Use the core library as a Python backend:

```python
from generate_prompts import generate_example_prompts, extend_prompt

# API endpoint or callback for generating prompts
prompts = generate_example_prompts(config)  # Returns list[str], never raises

# API endpoint or callback for extending a prompt
enhanced = extend_prompt(user_text, config)  # Returns str, raises RuntimeError on failure
```

For the frontend, translate the card pattern:
- Render N prompt cards (buttons, clickable divs, etc.)
- Handle click-to-select (copies prompt text to the main input)
- Add an "Extend" button that calls the backend

For slot-machine animation in non-Streamlit projects, use `animation.py` directly:
```python
from generate_prompts import render_slot_css, render_animated_card, build_animation_frames

css_html = render_slot_css()          # <style> block — inject once
frames = build_animation_frames(old, new, pool)
card_html = render_animated_card(frames[0], card_id="unique-id")  # HTML string
```
The CSS animation is pure HTML — inject `css_html` and `card_html` into any page.

### Step 5: Configure the LLM connection

Add to `.env` (create if it doesn't exist):

```bash
PROMPT_LLM_BASE_URL=https://your-llm-endpoint/v1
PROMPT_LLM_MODEL=your-model-name
PROMPT_LLM_API_KEY=your-api-key
PROMPT_LLM_TIMEOUT=45
PROMPT_LLM_GENERATE_TEMPERATURE=0.9
PROMPT_LLM_EXTEND_TEMPERATURE=0.7
```

- If the project already has an LLM endpoint, reuse those credentials
- If the project uses different env var names, modify `config.py` to read them
- Ensure `python-dotenv` is in the project's dependencies
- Update `.env.example` if one exists

### Step 6: Verify

- Confirm all copied files exist and import correctly
- Test `generate_example_prompts(config)` returns a list of strings (falls back to fallback_pool if no LLM available)
- Test UI renders prompt cards
- Test "Extend" button calls `extend_prompt()` and handles errors

## Quick Reference

| Function | Behavior | Error handling |
|---|---|---|
| `generate_example_prompts(config)` | Returns `list[str]` | Never raises — falls back to `fallback_pool` |
| `extend_prompt(text, config)` | Returns `str` | Raises `RuntimeError` — show error to user |
| `build_animation_frames(old, new, pool)` | Returns `list[AnimationFrame]` | Pure computation, no I/O |
| `render_slot_css()` | Returns `<style>` HTML string | Pure computation |
| `render_animated_card(frame, card_id)` | Returns HTML string | Pure computation |
| `inject_slot_css()` | Streamlit only — injects CSS | Streamlit-specific |
| `render_prompt_cards(prompts, ...)` | Streamlit only — renders cards | Streamlit-specific |

## Common Mistakes

- Forgetting `"Return only a JSON array of N strings."` in `system_prompt` — generation will fail to parse
- Missing `{prompt}` in `extend_user_template` — extend will send the template literally
- Too few fallback_pool entries — users see repeated prompts when LLM is down
- Not clearing animation frames after render — animation replays on every Streamlit rerun
- Wrapping `generate_example_prompts()` in try/except — it already handles all errors internally
- Not wrapping `extend_prompt()` in try/except — it raises RuntimeError on failure
- Hardcoding LLM endpoint instead of using env vars
```

**Step 2: Verify the file was created**

```bash
cat ~/.claude/skills/add-prompt-slots/SKILL.md | head -5
```

Expected: YAML frontmatter with `name: add-prompt-slots`

**Step 3: Commit to generate-prompts repo for tracking**

```bash
cd /data2/opt/generate-prompts
git add docs/plans/2026-02-18-add-prompt-slots-skill.md
git commit -m "Add implementation plan for add-prompt-slots skill"
```

---

### Task 3: Verify skill discovery

**Step 1: Check Claude can discover the skill**

The skill should now appear in Claude Code's skill list. Verify the file exists and has valid frontmatter:

```bash
head -4 ~/.claude/skills/add-prompt-slots/SKILL.md
```

Expected:
```
---
name: add-prompt-slots
description: Use when a project needs example prompt suggestions...
---
```

**Step 2: Verify the skill source files exist**

```bash
ls /data2/opt/generate-prompts/generate_prompts/*.py
```

Expected: `__init__.py`, `animation.py`, `client.py`, `config.py`, `extender.py`, `generator.py`, `normalizer.py`, `streamlit_component.py`

---

### Task 4: Commit everything

**Step 1: Commit the plan**

```bash
cd /data2/opt/generate-prompts
git add docs/plans/2026-02-18-add-prompt-slots-skill.md
git commit -m "Add implementation plan for add-prompt-slots skill"
```
