---
## Overview

description: Ingesting Warehouse Operational Data
---

# Warehouse Data Ingestion Workflow

This workflow guides the ingestion of operational data into the Statistical Dashboard.

**Version:** 1.0.0
**Owner:** DataEngineer
**Skill Set:** `data-ingestion`, `validation`

## Trigger Conditions

This workflow is activated when:
- New operational logs are available for ingestion.
- Systematic ASN data is received via EDI/API.

**Trigger Examples:**
- "Ingest the inbound log from today's morning shift."
- "Load the robotic transaction logs into the Warehouse project."

## 1. Data Source Identification
Identify the source of the data for the specific process:
- **Manual/Legacy**: Excel (.xlsx) or CSV files from warehouse associates.
- **Systemic**: ASN (Advanced Shipping Notice) via EDI or API (JSON/XML).
- **Industrial (IoT)**: Robotic transaction logs, sorter throughput (MQTT/OPC-UA).
- **Vision/Scanner**: Dimensioning data or barcode scan events.

## 2. Ingestion Methods

### A. Manual File Upload (Streamlit UI)
1. Navigate to **Data Management** tab.
2. Select the **Warehouse Project**.
3. Upload the corresponding CSV/Excel template.
    - Template Location: `data/templates/warehouse/`

### B. API / Batch Ingestion (Python)
Use `DataManager.ingest_from_source(source_type, path)` to batch load data.

### C. Industrial Stream Simulation (Future)
Simulate MQTT streams using the `IoTConnector` (to be implemented) for real-time dashboard updates.

## 3. Data Transformation & Validation
- Ensure timestamps are in ISO 8601 format.
- Validate `SKU` existence against the `Inventory` table.
- Calculate `Duration` fields immediately after ingestion to enable cycle-time analysis.

## 4. Verification
- Check the **Dashboard Overview** for updated "Total Units Processed".
- Verify **Warehousing Intel** tab for updated KPI trends (D2S, UPH).


## Trigger Conditions

- User request
- Manual activation


## Phases

1. Initial Analysis
2. Implementation
3. Verification


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
