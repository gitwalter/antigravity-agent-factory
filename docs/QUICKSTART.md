# Quick Start Guide

Welcome to Antigravity Agent Factory! This guide will have you up and running in just a few minutes.

> **Looking for more options?** See [GETTING_STARTED.md](GETTING_STARTED.md) for all onboarding paths:
> - **Express Lane** (10-15 min) - Guided individual setup
> - **Team Huddle** (1-2 hours) - Small team alignment
> - **Workshop Series** (11-15 hours) - Full team transformation

---

## The Fastest Way to Start

Run this single command to see the factory in action:

```powershell
python cli/factory_cli.py --quickstart
```

That's it! In about 30 seconds, you'll have a complete demo project showing everything the factory can create.

---

## What Just Happened?

The `--quickstart` command created a demo project called **TaskMaster Demo** - an AI-powered task management API. Here's what you got:

```
quickstart-demo/
├── .agent/
│   ├── agents/               # 3 AI agents ready to help you
│   │   ├── code-reviewer.md  # Reviews your code
│   │   ├── test-generator.md # Creates tests
│   │   └── explorer.md       # Explores codebases
│   └── skills/               # Reusable procedures
│       ├── bugfix-workflow/
│       ├── feature-workflow/
│       ├── tdd/
│       └── grounding/
├── knowledge/                # Domain knowledge in JSON
├── templates/                # Code and doc templates
├── workflows/                # How your team works
├── .agentrules              # The brain - AI guidance
├── PURPOSE.md                # The heart - mission & goals
└── README.md                 # Project documentation
```

---

## Understanding What You Got

### The Brain: `.agentrules`

This file configures how AI agents behave in your project. It includes:

- **Layer 0**: Axiom Zero (love, truth, beauty, flourishing) + Core Axioms (A1-A5)
- **Layer 1**: Your project's purpose and success criteria
- **Layer 2**: Ethical boundaries and quality standards
- **Layer 3**: Development methodology
- **Layer 4**: Technical configuration

Open it to see how the 5-layer architecture works! The Guardian Protocol ensures all agents act with love, move with truth, and illuminate with beauty.

### The Heart: `PURPOSE.md`

This document captures:

- **Mission**: What your project aims to achieve
- **Stakeholders**: Who you're building for
- **Success Criteria**: How you'll know you succeeded

### Your AI Team: `.agent/agents/`

Each agent is a specialized AI assistant:

| Agent | What It Does |
|-------|--------------|
| **code-reviewer** | Reviews code against best practices and style guides |
| **test-generator** | Creates unit tests, integration tests, and test plans |
| **explorer** | Helps you understand and navigate codebases |

### Reusable Skills: `.agent/skills/`

Skills are step-by-step procedures your agents can follow:

| Skill | What It Does |
|-------|--------------|
| **bugfix-workflow** | Fix bugs using ticket information |
| **feature-workflow** | Implement features from specifications |
| **tdd** | Test-driven development process |
| **grounding** | Verify data before implementation |

---

## Value Propagation Features

The Factory includes powerful features that make your system more autonomous and reliable:

### Development Autonomy (Layer 1)
Self-healing CI/CD pipeline monitoring that detects and fixes errors automatically.

**Try it:** Say "Monitor CI pipeline" or "Fix pipeline errors"

### Knowledge Independence (Layer 2)
Extend your knowledge base without waiting for Factory updates. Add domain expertise, patterns, and best practices on your own.

**Try it:** Say "Extend knowledge for [topic]"

### Grounding Verification (Layer 0)
Two-pass verification system that detects AI hallucinations and ensures factual accuracy before implementation.

**Try it:** Say "Verify this claim" when you need to check if something is accurate

### PM Integration (Layer 3 - Opt-In)
Project management integration with Jira, GitHub Issues, or other backends. Enable during onboarding or add later.

**Setup:** See [ONBOARDING_GUIDE.md](ONBOARDING_GUIDE.md) for configuration details

---

## Try It Out

### Step 1: Open in Antigravity IDE

Open the `quickstart-demo` folder in Antigravity IDE.

### Step 2: Explore with Your AI Team

Try these prompts to see your agents in action:

**Ask the Explorer:**
> "Help me understand the structure of this project"

**Ask the Code Reviewer:**
> "Review the .agentrules file and explain its sections"

**Ask for Test Generation:**
> "Create a test plan for a new task endpoint"

### Step 3: Try a Workflow

Say something like:
> "I need to add a new endpoint to create tasks. Walk me through the feature workflow."

Your agent will guide you through the feature-workflow skill step by step!

---

## Customizing Your Demo

### Use a Different Blueprint

The quickstart uses `python-fastapi` by default. Try other blueprints:

```powershell
# TypeScript/React
python cli/factory_cli.py --quickstart --quickstart-blueprint typescript-react

# Next.js Full-Stack
python cli/factory_cli.py --quickstart --quickstart-blueprint nextjs-fullstack

# AI Agent Development
python cli/factory_cli.py --quickstart --quickstart-blueprint ai-agent-development

# SAP ABAP
python cli/factory_cli.py --quickstart --quickstart-blueprint sap-abap
```

### Choose a Different Output Location

```powershell
python cli/factory_cli.py --quickstart --quickstart-output C:\Projects\my-demo
```

---

## Ready for More?

Now that you've seen what the factory creates, you're ready to build your own project!

### Option A: Interactive Mode (Recommended)

Answer questions to customize everything:

```powershell
python cli/factory_cli.py --interactive --output C:\Projects\my-project
```

You'll be guided through:
1. **Project Context** - Name, description, domain
2. **Technology Stack** - Language, frameworks
3. **Workflow Methodology** - Agile, Kanban, etc.
4. **Agent Capabilities** - Which agents you need
5. **Integrations** - Jira, Confluence, GitHub

### Option B: Blueprint-Based

Start from a pre-configured blueprint and customize later:

```powershell
python cli/factory_cli.py --blueprint python-fastapi --output C:\Projects\my-api
```

### Option C: Chat-Based (In Antigravity IDE)

Open the factory project in Cursor and say:
> "Create a new agent system for my e-commerce platform"

The AI will guide you through the full requirements process.

---

## Available Blueprints

| Blueprint | Best For |
|-----------|----------|
| `python-fastapi` | REST APIs, microservices |
| `ai-agent-development` | AI/ML applications, chatbots |
| `multi-agent-systems` | Complex multi-agent orchestration |
| `typescript-react` | Web applications, SPAs |
| `nextjs-fullstack` | Full-stack React with SSR |
| `java-spring` | Enterprise Java applications |
| `kotlin-spring` | Kotlin microservices |
| `csharp-dotnet` | .NET enterprise APIs |
| `sap-abap` | SAP ABAP/RAP development |
| `sap-cap` | SAP Cloud Application Programming |
| `sap-rap` | SAP RESTful ABAP Programming |
| `sap-cpi-pi` | SAP integration development |
| `python-ml-experimentation` | ML research with PyTorch/sklearn |
| `python-deep-learning` | Deep learning with Transformers |
| `python-rag-system` | Production RAG applications |
| `python-fine-tuning` | LLM fine-tuning with LoRA |
| `starter-ml-classification` | Beginner ML (great for learning!) |
| `starter-chatbot` | Beginner chatbot (great for learning!) |
| `starter-rag` | Beginner RAG (great for learning!) |

See all blueprints with:
```powershell
python cli/factory_cli.py --list-blueprints
```

---

## For Teams

If you're working with a team, consider the **Team Workshop** approach:

1. Say: **"We want to run team workshops for our project"**
2. Complete 5 collaborative workshops (11-15 hours total)
3. Align your team on vision, values, and technology
4. Generate a system everyone believes in

See the [Team Workshop Guide](TEAM_WORKSHOP_GUIDE.md) for details.

---

## Getting Help

- **Prerequisites**: [PREREQUISITES.md](PREREQUISITES.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Full Documentation**: [FACTORY_REFERENCE.md](FACTORY_REFERENCE.md)
- **Examples**: [docs/examples/](examples/)

---

## What's Next?

You've taken the first step! Here are some paths forward:

1. **Your first week** - Follow the [First Week Guide](FIRST_WEEK_GUIDE.md) to get the most out of your system
2. **Explore the examples** - See complete walkthroughs in [docs/examples/](examples/)
3. **Read the architecture** - Understand the 5-layer system in [LAYERED_ARCHITECTURE.md](LAYERED_ARCHITECTURE.md)
4. **Customize patterns** - Learn to extend the factory in [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md)
5. **Join the community** - Contribute blueprints, patterns, and skills!

---

We can't wait to see what you create!

---

*[Back to README](../README.md)*
