---
agents:
- '@Architect'
- data-architect-specialist
blueprints:
- universal
description: Antigravity workflow for data-pipeline-orchestration. Standardized for
  IDX Visual Editor.
domain: universal
name: data-pipeline-orchestration
steps:
- actions:
  - Ingest raw data into staging; run `dbt init` if starting fresh.
  agents:
  - data-architect-specialist
  goal: ''
  name: Ingestion & Setup
  skills: []
  tools: []
- actions:
  - Create staging, intermediate, and mart models in dbt.
  agents:
  - '@Architect'
  goal: ''
  name: Modeling & Transformation
  skills: []
  tools: []
- actions:
  - Run `dbt test` and `dbt docs generate`.
  agents:
  - '@Architect'
  goal: ''
  name: Validation & Documentation
  skills: []
  tools: []
- actions:
  - '**Idempotency**: Ensure ingestion and transformations can be re-run without side
    effects.'
  - '**Testing**: Implement freshness, uniqueness, and nullity tests on all mart models.'
  - '**Lineage**: Maintain a complete lineage graph using dbt documentation.'
  - '`ml-training-pipeline.md` - Consumes modeled data.'
  - '`cicd-pipeline.md` - Infrastructure for deployment.'
  - '"Execute data-pipeline-orchestration.md"'
  - Create Airflow DAGs; deploy using blue-green strategy.
  agents:
  - '@Architect'
  goal: ''
  name: Orchestration & Deployment
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Data Pipeline Orchestration Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for data-pipeline-orchestration using dbt and Airflow. Standardized for IDX Visual Editor.

## Trigger Conditions
- Fresh raw data available for ingestion.
- Need to transform and model datasets for analytical purposes.
- User request: `/data-pipeline-orchestration`.

**Trigger Examples:**
- "Orchestrate the ingestion of the last 24h logs."
- "Run the dbt transformations for the sales mart."

## Phases

### 1. Ingestion & Setup
- **Agents**: `data-architect-specialist`
- Ingest raw data into staging; run `dbt init` if starting fresh.

### 2. Modeling & Transformation
- **Agents**: `@Architect`
- Create staging, intermediate, and mart models in dbt.

### 3. Validation & Documentation
- **Agents**: `@Architect`
- Run `dbt test` and `dbt docs generate`.

### 4. Orchestration & Deployment
- **Agents**: `@Architect`
- **Idempotency**: Ensure ingestion and transformations can be re-run without side effects.
- **Testing**: Implement freshness, uniqueness, and nullity tests on all mart models.
- **Lineage**: Maintain a complete lineage graph using dbt documentation.
- `ml-training-pipeline.md` - Consumes modeled data.
- `cicd-pipeline.md` - Infrastructure for deployment.
- "Execute data-pipeline-orchestration.md"
- Create Airflow DAGs; deploy using blue-green strategy.
