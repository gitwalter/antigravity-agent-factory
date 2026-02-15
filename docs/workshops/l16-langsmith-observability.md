# LangSmith Observability and Evaluation

> **Stack:** LangSmith | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L16_langsmith_observability`

**Technology:** Python with LangSmith (LangSmith 0.1+)

## Prerequisites

**Required Workshops:**
- L7_langchain_fundamentals

**Required Knowledge:**
- LangChain basics (chains, agents, tools)
- Python environment variables and configuration
- Basic understanding of observability and monitoring
- Evaluation concepts (metrics, datasets, test cases)

**Required Tools:**
- Python 3.10+
- LangSmith account (free tier available)
- LangSmith API key
- LangChain 0.3+ installed

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand LangSmith's role in LLM app lifecycle (tracing, debugging, evaluation)** (Understand)
2. **Set up tracing for LangChain and LangGraph applications** (Apply)
3. **Create and manage datasets for testing and evaluation** (Apply)
4. **Build evaluation pipelines with custom evaluators** (Apply)
5. **Use LangSmith for prompt iteration and A/B testing** (Create)

## Workshop Timeline

| Phase | Duration |
|-------|----------|
| Concept | 30 min |
| Demo | 30 min |
| Exercise | 45 min |
| Challenge | 30 min |
| Reflection | 15 min |
| **Total** | **2.5 hours** |

## Workshop Phases

### Concept: LangSmith Architecture and Observability Concepts

*Understanding LangSmith's role in the LLM application lifecycle*

**Topics Covered:**
- LangSmith overview: tracing, debugging, evaluation, monitoring
- Run trees: hierarchical execution traces
- Tracing concepts: automatic vs manual instrumentation
- Evaluation frameworks: datasets, evaluators, test cases
- Feedback loops: human feedback and model improvement
- Prompt iteration: versioning and A/B testing
- Production monitoring: alerts, dashboards, metrics

**Key Points:**
- LangSmith automatically traces LangChain/LangGraph calls when configured
- Run trees show the complete execution flow with timing and costs
- Datasets enable systematic testing across multiple examples
- Evaluators measure quality metrics (correctness, relevance, etc.)
- Feedback helps improve models through human-in-the-loop learning
- Prompt experiments enable data-driven prompt optimization

### Demo: Instrumenting a LangChain App and Viewing Traces

*Live coding: Add tracing to a LangChain app and explore the LangSmith UI*

**Topics Covered:**
- Setting up LangSmith API key and environment variables
- Enabling automatic tracing for LangChain
- Running a chain and viewing traces in LangSmith UI
- Exploring run tree: inputs, outputs, timing, costs
- Adding metadata and tags to traces
- Creating a dataset from existing runs
- Adding feedback to runs

**Key Points:**
- LANGCHAIN_TRACING_V2=true enables tracing
- LANGCHAIN_PROJECT organizes runs by project
- Run trees show complete execution hierarchy
- Metadata enables filtering and searching
- Datasets can be created from successful runs

### Exercise: Add Tracing to Existing App and Analyze Traces

*Instrument an existing LangChain application and analyze the execution traces*

**Topics Covered:**
- Configure environment variables for tracing
- Add metadata and tags to runs
- View and analyze traces in LangSmith UI
- Identify performance bottlenecks
- Extract insights from run trees

### Exercise: Create Evaluation Dataset and Run Evaluations

*Build a dataset and run evaluations with custom evaluators*

**Topics Covered:**
- Create dataset with examples
- Implement custom evaluators
- Run evaluations on dataset
- Analyze evaluation results
- Compare model performance across examples

### Challenge: Build Prompt Iteration Workflow with Automated Evaluation

*Create a workflow that tests multiple prompt versions and selects the best*

**Topics Covered:**
- Define multiple prompt variations
- Run each prompt on evaluation dataset
- Compare results using evaluators
- Select best performing prompt
- Document prompt evolution

### Reflection: Production Monitoring, Alerts, and Collaboration

*Consolidate learning and explore production patterns*

**Topics Covered:**
- Setting up production monitoring
- Configuring alerts for anomalies
- Team collaboration features
- Best practices for observability
- Integrating LangSmith into CI/CD pipelines

**Key Points:**
- Enable tracing in all environments (dev, staging, prod)
- Use projects to organize runs by environment
- Set up alerts for errors and performance degradation
- Use datasets for regression testing
- Share insights with team through LangSmith UI

## Hands-On Exercises

### Exercise: Add Tracing to Existing App and Analyze Traces

Instrument a LangChain application with tracing and analyze the execution flow

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Environment variables must be set before importing LangChain modules
- Use config parameter to add metadata and tags
- Metadata is useful for filtering runs later
- Tags help organize runs by category

**Common Mistakes to Avoid:**
- Setting environment variables after imports
- Forgetting to set LANGCHAIN_PROJECT
- Not using config parameter for metadata
- Using wrong API key format

### Exercise: Create Evaluation Dataset and Run Evaluations

Build a dataset and evaluate a chain using custom evaluators

**Difficulty:** Hard | **Duration:** 25 minutes

**Hints:**
- create_dataset is idempotent - safe to call multiple times
- Use create_examples to add examples to a dataset
- evaluation parameter accepts a list of evaluators
- Custom evaluators receive run and example parameters
- Results are viewable in LangSmith UI

**Common Mistakes to Avoid:**
- Not handling dataset already exists error
- Wrong format for examples (must have inputs/outputs)
- Evaluator functions not returning correct format
- Forgetting to set LANGCHAIN_PROJECT

## Challenges

### Challenge: Build Prompt Iteration Workflow with Automated Evaluation

Create a system that tests multiple prompt versions and selects the best performing one

**Requirements:**
- Define at least 3 different prompt variations
- Create or use an existing evaluation dataset
- Run each prompt version on the dataset
- Compare results using multiple evaluators
- Select the best performing prompt based on aggregate scores
- Document the prompt evolution and results

**Evaluation Criteria:**
- All prompt versions are tested systematically
- Evaluation metrics are calculated correctly
- Best prompt is selected based on data
- Results are clearly documented
- Code is reusable for future prompt iterations

**Stretch Goals:**
- Implement A/B testing framework
- Add statistical significance testing
- Create visualization of prompt performance
- Automate prompt selection based on thresholds
- Integrate with version control for prompt history

## Resources

**Official Documentation:**
- https://docs.smith.langchain.com/
- https://docs.smith.langchain.com/tracing
- https://docs.smith.langchain.com/evaluation
- https://docs.smith.langchain.com/datasets

**Tutorials:**
- LangSmith Quick Start Guide
- Building Evaluation Pipelines
- Prompt Engineering with LangSmith
- Production Monitoring Best Practices

**Videos:**
- LangSmith Overview - LangChain YouTube
- Evaluation Tutorial - LangSmith Docs
- Production Observability - AI Engineer Summit

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain LangSmith's role in the LLM app lifecycle?
- [ ] Can I set up tracing for my applications?
- [ ] Can I create and manage evaluation datasets?
- [ ] Can I build custom evaluators?
- [ ] Can I use LangSmith for prompt iteration?

## Next Steps

**Next Workshop:** `L17_production_deployment`

**Practice Projects:**
- Add LangSmith tracing to an existing LangChain app
- Create evaluation dataset for a RAG system
- Build prompt A/B testing framework
- Set up production monitoring with alerts

**Deeper Learning:**
- Advanced LangSmith features (experiments, annotations)
- Custom evaluator development
- Integrating LangSmith into CI/CD pipelines
- Team collaboration and sharing in LangSmith

## Related Knowledge Files

- `langsmith-patterns.json`
- `langchain-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L16_langsmith_observability.json`
