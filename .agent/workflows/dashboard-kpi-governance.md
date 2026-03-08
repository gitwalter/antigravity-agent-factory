---
description: KPI Definition & Governance Process
dashboard: true
version: 1.0.0
---

# KPI Governance Workflow

**Version:** 1.0.0

Systematic routine for introducing, auditing, and publishing new KPIs.

## Trigger Conditions
- A new KPI is proposed for the dashboard.
- An existing KPI needs recalibration or audit.
- Stakeholders request alignment on metric definitions.

**Trigger Examples:**
- "Define and publish a new UPH metric."
- "Audit the accuracy of the current KPI dictionary."

## Phases

### 1. Definition
- Define the business value of the metric.
- Document the exact formula (e.g., `(Actual / Expected) * 100`).

### 2. Implementation
- Add the new KPI to `GuidanceCenter.get_kpi_dictionary()`.
- Include visualization recommendations and target bands.

### 3. Verification
- Test the logic against a "Golden Dataset".
- Confirm visual clarity in the **KPI Dictionary** tab.

### 4. Stakeholder Sign-off
- Verify alignment with the **Warehouse Analyst** and **Operations Manager** personas.
- Move from "Experimental" to "Standard".


## Trigger Examples
- "Execute this workflow."
