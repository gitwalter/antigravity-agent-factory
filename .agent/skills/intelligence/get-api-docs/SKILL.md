---
name: get-api-docs
description: 'Fetch and manage up-to-date API documentation for coding tasks using
  Context Hub (chub). Ensures agents have situation-adequate documentation for modern
  tools and prevents hallucinations.

  '
type: skill
version: 1.0.0
category: intelligence
agents:
- python-ai-specialist
- ai-app-developer
tools:
- run_command
related_skills:
- synthesizing-knowledge
- assessing-risks
knowledge:
- none
templates:
- none
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

# Getting API Documentation (chub)

This skill enables agents to autonomously fetch the latest API documentation for various services and providers, ensuring code accuracy and preventing the use of outdated parameters or methods.

## When to Use
- When you encounter a service or library (e.g., OpenAI, Stripe, Pinecone) where your training data might be outdated.
- When you need to verify the exact parameter structure for an API call.
- When you want to discover the "best practices" or "workarounds" discovered by other agents in the ecosystem.

## Prerequisites
- **Global Installation**: Ensure `@aisuite/chub` is installed via `npm install -g @aisuite/chub`.
- **Network Access**: Requires internet connectivity to search and fetch docs from the hub.
- **Authorized Environment**: Ensure you are running in a compliant shell (PowerShell or Bash) with `node` and `npm` in the path.

## Process
The extraction of up-to-date documentation involves a 3-step cycle: orientation, retrieval, and annotation.

### 1. Orientation
If you are unsure of the available documentation, use `search` to check the database.

```bash
# Search for documentation related to a provider
chub search "openai"

# List all available documentation
chub search
```

### 2. Retrieval
Once you have the ID (e.g., `openai/chat-api`), fetch the documentation. It is often best to output this to a temporary file for better readability.

```bash
# Fetch documentation for a specific API
chub get openai/chat-api

# Fetch and save to a file for reference
chub get openai/chat-api -o tmp/openai_docs.md
```

### 3. Annotation & Feedback
If you discover a workaround or a mistake in the documentation, annotate it to help future sessions. **Always inform the user** before submitting feedback to the community.

```bash
# Save a local note for future use
chub annotate openai/chat-api "Always use GPT-4o for complex reasoning."

# List your saved annotations
chub annotate --list
```

## Best Practices
- **JSON for Large Scales**: Use `--json` if you need to programmatically pick the best match from many results.
- **Language Specificity**: Use `--lang <py|js|ts>` to get examples tailored to your current coding environment.
- **Cache Management**: If the docs seem outdated despite the hub, run `chub update` to refresh the local cache.

## Troubleshooting
- If `chub` is not found, ensure it is installed via `npm install -g @aisuite/chub`.
- If a provider is missing, consider using `web_search` to find documentation and then manually adding it to the project context.
