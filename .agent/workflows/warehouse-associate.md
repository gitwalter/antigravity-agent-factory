---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for warehouse-associate. Standardized for IDX Visual
  Editor.
domain: universal
name: warehouse-associate
steps:
- actions:
  - '**Log In**: Authenticate at the station terminal.'
  - '**Supply Check**: Ensure adequate boxes, tape, and dunnage are available.'
  - '**Safety First**: Check ergonomics and clear tripping hazards.'
  agents:
  - '@Architect'
  goal: ''
  name: Station Verification
  skills: []
  tools: []
- actions:
  - '**Pick/Stow Sequence**: Follow the system-suggested route to minimize travel
    time.'
  - '**Scan-First Policy**: Always scan the bin followed by the item to ensure 99.9%
    accuracy.'
  - '**Random Stow Logic**: Place items in the first available, safe location; don''t
    "organize" unless the system instructs.'
  agents:
  - '@Architect'
  goal: ''
  name: Execution (UPH Focus)
  skills: []
  tools: []
- actions:
  - Monitor your **Current UPH** on the dashboard.
  - If UPH drops < 80% of personal baseline, check for conveyor bottlenecks or supply
    shortages.
  - Report any **Damaged SKU** immediately via the "Damaged" flag to keep inventory
    counts accurate.
  agents:
  - '@Architect'
  goal: ''
  name: Real-Time Tracking
  skills: []
  tools: []
- actions:
  - Clean station for the next associate.
  - Log out to finalize your "Shift Units" count.
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
  name: Shift Handoff
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Warehouse Associate Operational Guide

**Version:** 1.0.0

## Overview
Antigravity workflow for warehouse associates covering daily operations, safety, and productivity (UPH) standards. Standardized for IDX Visual Editor.

## Trigger Conditions
- Associate starting or ending a shift.
- Requirement for stowing or picking items in the warehouse.
- User request: `/warehouse-associate`.

**Trigger Examples:**
- "Execute the operational guide for the start of the 'Morning Shift'."
- "Provide the pick/stow sequence instructions for a new associate."

## Phases

### 1. Station Verification
- **Agents**: `@Architect`
- **Log In**: Authenticate at the station terminal.
- **Supply Check**: Ensure adequate boxes, tape, and dunnage are available.
- **Safety First**: Check ergonomics and clear tripping hazards.

### 2. Execution (UPH Focus)
- **Agents**: `@Architect`
- **Pick/Stow Sequence**: Follow the system-suggested route to minimize travel time.
- **Scan-First Policy**: Always scan the bin followed by the item to ensure 99.9% accuracy.
- **Random Stow Logic**: Place items in the first available, safe location; don't "organize" unless the system instructs.

### 3. Real-Time Tracking
- **Agents**: `@Architect`
- Monitor your **Current UPH** on the dashboard.
- If UPH drops < 80% of personal baseline, check for conveyor bottlenecks or supply shortages.
- Report any **Damaged SKU** immediately via the "Damaged" flag to keep inventory counts accurate.

### 4. Shift Handoff
- **Agents**: `@Architect`
- Clean station for the next associate.
- Log out to finalize your "Shift Units" count.
- User request
- Manual activation
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
