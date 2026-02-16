# Prompt Optimization Patterns (2026)

## Core Principles
1. **Context Engineering**: Prioritize Level 3 progressive disclosure. Never load long documents into Level 1/2 context.
2. **Structured Outputs**: Use XML tags or JSON schemas for every high-stakes LLM call.
3. **Role Anchoring**: Every prompt must begin with a clear Persona/Mission definition.

## Advanced Patterns
- **Few-Shot Calibration**: Provide 3-5 high-fidelity examples for complex logic.
- **Chain-of-Thought (CoT) Gating**: Mandate inner-monologue sections before final output.
- **Token Efficiency**: Use comma-separated lists for metadata; avoid verbose descriptions in system prompts.

## Multi-Model Optimization
- **Claude 3.x/4.x**: Optimized for long-context recall and XML adherence.
- **Gemini 2.x**: Optimized for multi-modal reasoning and high-speed retrieval.
