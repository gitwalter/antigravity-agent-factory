---
name: data-pipeline-orchestration
description: Workflow for managing Data Pipelines using ELT patterns, dbt modeling,
  and orchestration.
version: 1.0.0
type: pipeline
domain: python
agents:
- data-architect-specialist
blueprints:
- modern-data-stack
steps:
- name: Ingestion
  description: Ingest raw data into a landing zone or staging schema in the data warehouse.
- name: Modeling Setup
  description: Initialize dbt project or create new models for transformation.
- name: Staging
  description: Implement staging models to stabilize schemas and perform basic casting.
- name: Business Logic
  description: Develop core business logic in intermediate and mart models.
- name: Validation
  description: Run dbt tests (dbt test) to verify data quality and uniqueness.
- name: Documentation
  description: Generate and review dbt documentation to maintain lineage.
- name: Orchestration
  description: Configure orchestration tasks in Airflow (DAGs) or Dagster (Assets).
- name: Monitoring
  description: Implement data drift detection using specialized validation tools.
- name: Deployment
  description: Deploy models to production environment using a blue-green strategy.
- name: Maintenance
  description: Monitor pipeline performance and data freshness SLAs.
tags:
- data
- pipeline
- orchestration
- standardized
---


# Data Pipeline Orchestration Workflow

**Version:** 1.0.0

**Goal:** Standardized process for ELT and data pipeline management ensuring data quality and lineage.

## Trigger Conditions
- New data source ingestion requested.
- Data quality issues identified in existing pipelines.
- Requirement for new business metrics or transformations.

**Trigger Examples:**
- "Ingest the new marketing data into Snowflake."
- "Create a new dbt model for customer churn analysis."
- "Fix the data quality test failure in the sales pipeline."
- "Orchestrate the nightly ETL run using Airflow."

## Phases

### 1. Ingestion & Setup
Identify raw data sources and initialize the modeling environment.
- **Agent**: `data-architect-specialist`
- **Action**: Ingest raw data into staging; run `dbt init` if starting fresh.

### 2. Modeling & Transformation
Implement the core business logic through layered modeling.
- **Action**: Create staging, intermediate, and mart models in dbt.

### 3. Validation & Documentation
Ensure data integrity and observability.
- **Action**: Run `dbt test` and `dbt docs generate`.

### 4. Orchestration & Deployment
Automate the pipeline and promote to production.
- **Action**: Create Airflow DAGs; deploy using blue-green strategy.

## Best Practices
- **Idempotency**: Ensure ingestion and transformations can be re-run without side effects.
- **Testing**: Implement freshness, uniqueness, and nullity tests on all mart models.
- **Lineage**: Maintain a complete lineage graph using dbt documentation.

## Related Workflows
- `ml-training-pipeline.md` - Consumes modeled data.
- `cicd-pipeline.md` - Infrastructure for deployment.


## Trigger Examples
- "Execute data-pipeline-orchestration.md"
