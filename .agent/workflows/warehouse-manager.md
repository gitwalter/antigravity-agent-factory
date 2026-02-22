---
## Overview

description: Shift Management & SLA Compliance Workflow
---

# Operations Manager Strategic Guide

"Mission Control" perspective for managing shift-level fulfillment health.

**Version:** 1.0.0
**Owner:** OperationsManager
**Skill Set:** `strategic-management`, `labor-optimization`

## Trigger Conditions

This workflow is activated when:
- A new operational shift starts.
- Late Shipment Rate (LSR) exceeds 3.5%.

**Trigger Examples:**
- "Review the shift-level fulfillment health for the night shift."
- "Reassign labor to mitigate the spike in LSR."

## 1. Shift Initialization
- **Volume Review**: Check the **Expected ASN** vs. actual dock arrival.
- **Labor Assignment**: Audit the "Labor Health" metric. Re-assign stowers to picking if the **Late Shipment Rate (LSR)** trend exceeds 3.5%.

## 2. Inbound Performance (Dock-to-Stock)
- **Bottleneck Detection**: If D2S > 2 hours, identify if the delay is at **Unloading** or **Putaway**.
- **Action**: Increase dock-door frequency or assign more associates to stowing.

## 3. Outbound Urgency
- **LSR Monitoring**: Prioritize "Hot Picks" if carrier pickup is within 30 minutes.
- **Click-to-Ship**: Monitor the gap between Order Placement and Pack-out.

## 4. Resolution
- Use the **Warehousing Intel** dashboard to detect "Hidden Inventory" (items received but not stowed).
- Resolve associate station blocks in real-time.


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
