---
description: Export learning workshops to standalone projects with all necessary artifacts
  for maximum AI-assisted learning
name: exporting-workshops
type: skill
---
# Workshop Export

Export learning workshops to standalone projects with all necessary artifacts for maximum AI-assisted learning

# Workshop Export Skill

## Purpose

Export any learning workshop to a standalone project with all necessary artifacts for maximum AI-assisted learning.

## Artifacts Generated

| Artifact | Purpose |
|----------|---------|
| `.cursorrules` | Project-level AI rules and context |
| `{directories.rules}/<lang>.md` | Technology-specific coding rules |
| `.cursor/knowledge/*.json` | Relevant knowledge files |
| `.cursor/WORKSHOP_CONTEXT.md` | AI assistant guidance for workshop phases |
| `README.md` | Workshop overview, exercises, objectives |
| `package.json` / `requirements.txt` | Dependencies |
| `src/exercises/` | Starter code for exercises |
| `.solutions/` | Hidden solutions (gitignored) |
| `.gitignore` | Clean repository patterns |

## Usage

### Via Python Script

```bash
# From factory root
python {directories.scripts}/workshops/export_workshop.py <workshop_id> <target_directory>

# Examples
python {directories.scripts}/workshops/export_workshop.py l01-ethereum-fundamentals {TARGET_DIR}
python {directories.scripts}/workshops/export_workshop.py l07-langchain-fundamentals {TARGET_DIR}
python {directories.scripts}/workshops/export_workshop.py l05-crewai-multiagent {TARGET_DIR}
```

### Via Agent Request

When user asks to start a workshop:

1. **Identify the workshop** from available options:
   - Blockchain: L1 (Ethereum), L2 (Bitcoin), L4 (Solana)
   - AI: L3 (LangGraph), L5 (CrewAI), L6 (HuggingFace), L7 (LangChain), L8 (RAG), L16-L18
   - Web: L9 (React), L10 (Next.js), L11 (FastAPI)
   - Cloud: L12 (Kubernetes), L13 (Docker)
   - ML: L14 (PyTorch), L15 (Fine-tuning)

2. **Ask for target directory** if not specified

3. **Run the export script**:
   ```bash
   python {directories.scripts}/workshops/export_workshop.py {workshop_id} {target_dir}
   ```

4. **Guide user to open the new project** in Cursor

## Available Workshops

| ID | Name | Category |
|----|------|----------|
| l01-ethereum-fundamentals | Ethereum Smart Contracts | Blockchain |
| l02-bitcoin-lightning | Bitcoin & Lightning | Blockchain |
| l03-langgraph-workflows | LangGraph Workflows | AI |
| l04-solana-fundamentals | Solana Development | Blockchain |
| l05-crewai-multiagent | CrewAI Multi-Agent | AI |
| l06-huggingface-transformers | HuggingFace Transformers | AI |
| l07-langchain-fundamentals | LangChain Agents | AI |
| l08-rag-systems | RAG Systems | AI |
| l09-react-modern | Modern React | Web |
| l10-nextjs-fullstack | Next.js Fullstack | Web |
| l11-fastapi-production | FastAPI Production | Web |
| l12-kubernetes-production | Kubernetes | Cloud |
| l13-docker-containerization | Docker | Cloud |
| l14-pytorch-deeplearning | PyTorch Deep Learning | ML |
| l15-llm-finetuning | LLM Fine-Tuning | ML |
| l16-langsmith-observability | LangSmith Observability | AI |
| l17-anthropic-tool-agents | Anthropic Tool Agents | AI |
| l18-deep-research-agents | Deep Research Agents | AI |

## Post-Export Steps

After export, guide the user:

1. **Open the project** in a new Cursor window
2. **Install dependencies**:
   - npm: `npm install`
   - pip: `pip install -r requirements.txt`
3. **Read README.md** for workshop overview
4. **Follow the phases**: Concept → Demo → Exercise → Challenge → Reflection

## Customization

The export script uses stack configurations to customize output:

- **Blockchain projects**: Hardhat config, Solidity rules, contract templates
- **Python AI projects**: pytest config, type hints, async patterns
- **Web projects**: Framework-specific configs and patterns
- **Cloud projects**: YAML configs, deployment templates

## Integration with Workshop Facilitator

The exported project is designed to work with the `@workshop-facilitator` agent:

```
@workshop-facilitator Guide me through the L1 Ethereum workshop
```

The facilitator uses:
- `WORKSHOP_CONTEXT.md` for phase-specific guidance
- Knowledge files for accurate information
- Exercise hints for progressive assistance

## Example Workflow

```
User: I want to learn LangChain

Agent: I'll set up the LangChain workshop for you.

1. Runs: python {directories.scripts}/workshops/export_workshop.py l07-langchain-fundamentals {TARGET_DIR}
2. Project created with:
   - .cursorrules with LangChain context
   - {directories.rules}/python.md with Python best practices
   - Knowledge files for LangChain patterns
   - Exercise starter code
   - Comprehensive README

3. Guide user to open project and begin learning
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Workshop not found | Check workshop ID matches pattern in `{directories.patterns}/workshops/` |
| Permission denied | Run with appropriate permissions or choose different target |
| Dependencies fail | Use `--legacy-peer-deps` for npm or update pip |

## Best Practices

- Validate workshop ID before export - confirm the workshop exists and matches user's learning goals to avoid wasted time
- Ensure target directory is clean or doesn't exist - prevent accidental overwrites by checking directory state first
- Include comprehensive README.md in exports - learners need clear guidance on objectives, phases, and how to use the workshop
- Structure exercises progressively - start with concepts, move to demos, then exercises, building complexity gradually
- Keep solutions hidden but accessible - use `.solutions/` directory with `.gitignore` so learners can check answers without temptation
- Test exported projects before delivery - verify dependencies install correctly and starter code runs on clean environments

---

*Part of the Cursor Agent Factory Learning System*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Process
1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
