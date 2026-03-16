---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for warehouse-ingestion. Standardized for IDX Visual
  Editor.
domain: universal
name: warehouse-ingestion
steps:
- actions:
  - '**Manual/Legacy**: Excel (.xlsx) or CSV files from warehouse associates.'
  - '**Systemic**: ASN (Advanced Shipping Notice) via EDI or API (JSON/XML).'
  - '**Industrial (IoT)**: Robotic transaction logs, sorter throughput (MQTT/OPC-UA).'
  - '**Vision/Scanner**: Dimensioning data or barcode scan events.'
  agents:
  - '@Architect'
  goal: ''
  name: Data Source Identification
  skills: []
  tools: []
- actions:
  - 'Template Location: `data/templates/warehouse/`'
  agents:
  - '@Architect'
  goal: ''
  name: Ingestion Methods
  skills: []
  tools: []
- actions:
  - Ensure timestamps are in ISO 8601 format.
  - Validate `SKU` existence against the `Inventory` table.
  - Calculate `Duration` fields immediately after ingestion to enable cycle-time analysis.
  agents:
  - '@Architect'
  goal: ''
  name: Data Transformation & Validation
  skills: []
  tools: []
- actions:
  - Check the **Dashboard Overview** for updated "Total Units Processed".
  - Verify **Warehousing Intel** tab for updated KPI trends (D2S, UPH).
  - User request
  - Manual activation
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - '@Architect'
  goal: ''
  name: Verification
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Warehouse Data Ingestion Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for ingesting warehouse transactional data from various sources (manual, systemic, IoT). Standardized for IDX Visual Editor.

## Trigger Conditions
- Availability of new Excel/CSV logs from associates.
- Triggering an ASN (Advanced Shipping Notice) via API.
- User request: `/warehouse-ingestion`.

**Trigger Examples:**
- "Ingest the robotic transaction logs for 'Robo-Station 4'."
- "Process the incoming JSON payload for order ingestion."

## Phases

### 1. Data Source Identification
- **Agents**: `@Architect`
- **Manual/Legacy**: Excel (.xlsx) or CSV files from warehouse associates.
- **Systemic**: ASN (Advanced Shipping Notice) via EDI or API (JSON/XML).
- **Industrial (IoT)**: Robotic transaction logs, sorter throughput (MQTT/OPC-UA).
- **Vision/Scanner**: Dimensioning data or barcode scan events.

### 2. Ingestion Methods
- **Agents**: `@Architect`
- Template Location: `data/templates/warehouse/`

### 3. Data Transformation & Validation
- **Agents**: `@Architect`
- Ensure timestamps are in ISO 8601 format.
- Validate `SKU` existence against the `Inventory` table.
- Calculate `Duration` fields immediately after ingestion to enable cycle-time analysis.

### 4. Verification
- **Agents**: `@Architect`
- Check the **Dashboard Overview** for updated "Total Units Processed".
- Verify **Warehousing Intel** tab for updated KPI trends (D2S, UPH).
- User request
- Manual activation
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
