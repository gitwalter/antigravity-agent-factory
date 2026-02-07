# Google Agent System

The **Google Agent System** blueprint enables you to build intelligent AI agents using Google's generative AI models (Gemini) via the `google-generativeai` SDK.

## Features

- **Native Tool Use**: Leverages Gemini's automatic function calling capabilities.
- **Structured Output**: Uses Pydantic models to ensure strictly formatted JSON responses.
- **Safety Settings**: Configurable safety filters to align with A4 (Non-Harm) axioms.
- **System Instructions**: Deep integration of system prompts for character and rule maintenance.

## Prerequisites

1. **Google API Key**: Get one from [Google AI Studio](https://aistudio.google.com/).
2. **Python 3.9+**: Required for the SDK.

## Usage

Generate a new project using this blueprint:

```bash
python cli/factory_cli.py --blueprint google-agent-system --output my-google-agent
```

## Configuration

Set your API key in the generated `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Customization

- **Agent Logic**: Modify `agents/core/google_agent.py` (or similar) to change behavior.
- **Tools**: Add Python functions to `tools/` and register them in the agent's `tools` list.
- **Patterns**: Refer to `knowledge/google-generative-ai-patterns.json` for coding patterns.
