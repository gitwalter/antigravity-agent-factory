---
## Overview

description: Personal Productivity & Station Execution Workflow
---

# Warehouse Associate Operational Guide

This guide ensures maximum throughput and accuracy at individual workstations (Stow/Pick/Pack).

**Version:** 1.0.0
**Owner:** StationAssociate
**Skill Set:** `station-performance`, `accuracy-metrics`

## Trigger Conditions

This workflow is activated when:
- A new shift begins at a dedicated workstation.
- Station throughput (UPH) falls below baseline.

**Trigger Examples:**
- "Start the shift verification for Stow station 42."
- "Review personal UPH metrics for the current picking session."

## 1. Station Verification
- **Log In**: Authenticate at the station terminal.
- **Supply Check**: Ensure adequate boxes, tape, and dunnage are available.
- **Safety First**: Check ergonomics and clear tripping hazards.

## 2. Execution (UPH Focus)
- **Pick/Stow Sequence**: Follow the system-suggested route to minimize travel time.
- **Scan-First Policy**: Always scan the bin followed by the item to ensure 99.9% accuracy.
- **Random Stow Logic**: Place items in the first available, safe location; don't "organize" unless the system instructs.

## 3. Real-Time Tracking
- Monitor your **Current UPH** on the dashboard.
- If UPH drops < 80% of personal baseline, check for conveyor bottlenecks or supply shortages.
- Report any **Damaged SKU** immediately via the "Damaged" flag to keep inventory counts accurate.

## 4. Shift Handoff
- Clean station for the next associate.
- Log out to finalize your "Shift Units" count.


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
