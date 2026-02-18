# Design: add-prompt-slots Skill

## Overview

A Claude Code skill that guides Claude through integrating the `generate_prompts` library into any existing project. The skill covers both features: example prompt cards (with slot-machine animation) and AI-powered prompt extension.

## Skill Identity

- **Name:** `add-prompt-slots`
- **Description:** `Use when a project needs example prompt suggestions for users to select and an AI-powered prompt extend/enhance feature — integrates the generate-prompts library into any UI framework`
- **Type:** Integration guide (Approach 1 — flexible, framework-agnostic)

## Core Workflow

1. **Analyze the target project** — Identify the UI framework, existing LLM usage, project structure, and the domain (medical, video, coding, etc.)
2. **Copy the generate-prompts package** — Vendor `generate_prompts/` into the target project. Only copy the core files needed (skip `streamlit_component.py` if not a Streamlit project).
3. **Write a domain-specific PromptConfig** — Claude crafts tailored system prompts, user prompts, extend prompts, and fallback pools for the project's domain.
4. **Wire up the UI** — Integrate prompt cards and the extend button into the project's existing UI, adapting to whatever framework it uses.
5. **Configure the LLM connection** — Set up `.env` with `PROMPT_LLM_*` variables pointing to an OpenAI-compatible endpoint.

## File Selection Logic

**Always copy (core):**
- `__init__.py`, `config.py`, `client.py`, `generator.py`, `extender.py`, `normalizer.py`

**Copy if Streamlit:**
- `animation.py`, `streamlit_component.py`

**Copy if non-Streamlit but wants animation:**
- `animation.py` (HTML/CSS is framework-agnostic)

**Never copy:**
- `demo.py`, `main.py` (demos only)

## PromptConfig Authoring Rules

- `system_prompt` must end with `"Return only a JSON array of N strings."`
- `user_prompt` should request diverse prompts under 120 chars
- `extend_system_prompt` must instruct LLM to preserve original intent
- `extend_user_template` must contain `{prompt}` placeholder
- `fallback_pool` should have at least 2x `count` entries
- `count` defaults to 3

## UI Integration Patterns

**Streamlit:** Use built-in `streamlit_component.py` directly.

**Non-Streamlit:** Use core library as Python backend behind API endpoints or callbacks. Translate the card pattern to the project's frontend. Use `animation.py` HTML/CSS output if animation is wanted.

**UX rules:**
- Generation never blocks/crashes (silent fallback)
- Extension can fail — always show errors to user
- Clear animation state after render

## LLM Configuration

- `PROMPT_LLM_BASE_URL`, `PROMPT_LLM_MODEL`, `PROMPT_LLM_API_KEY`, `PROMPT_LLM_TIMEOUT`, `PROMPT_LLM_GENERATE_TEMPERATURE`, `PROMPT_LLM_EXTEND_TEMPERATURE`
- Reuse project's existing LLM credentials when possible
- Only runtime dependency: `python-dotenv`
