# How to Use the add-prompt-slots Skill in Claude Code

## Invocation

Describe what you want in natural language. Claude will automatically detect and invoke the skill. Examples:

```
"Add example prompt suggestions to my Streamlit app"
"Integrate the generate-prompts library into my project"
"I need clickable prompt cards with an extend feature"
```

Or invoke it explicitly:

```
/add-prompt-slots
```

## What It Does

The skill guides Claude through a 6-step process:

1. **Analyze** your target project (framework, domain, structure)
2. **Copy** the `generate_prompts` package into your project
3. **Write** a domain-specific `PromptConfig` (system prompts, fallbacks, etc.)
4. **Wire up the UI** — Streamlit gets full card rendering + slot-machine animation; other frameworks get the Python backend + HTML/CSS you can embed
5. **Configure** the LLM connection via `.env` variables
6. **Verify** everything works

## Prerequisites

- A target project to integrate into
- An LLM endpoint (set via `PROMPT_LLM_BASE_URL`, `PROMPT_LLM_MODEL`, `PROMPT_LLM_API_KEY` in `.env`)
- `python-dotenv` in your project's dependencies

## Example

If you have a Streamlit medical Q&A app and want prompt suggestions:

```
"Add example prompt cards to my medical Q&A Streamlit app at /path/to/my-medical-app"
```

Claude will copy the library, create medical-domain prompts, wire up the Streamlit components, and configure the LLM connection.
