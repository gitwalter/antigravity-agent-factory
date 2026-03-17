---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for warehouse-manager. Standardized for IDX Visual
  Editor.
domain: universal
name: warehouse-manager
steps:
- actions:
  - '**Volume Review**: Check the **Expected ASN** vs. actual dock arrival.'
  - '**Labor Assignment**: Audit the "Labor Health" metric. Re-assign stowers to picking
    if the **Late Shipment Rate (LSR)** trend exceeds 3.5%.'
  agents:
  - '@Architect'
  goal: ''
  name: Shift Initialization
  skills: []
  tools: []
- actions:
  - '**Bottleneck Detection**: If D2S > 2 hours, identify if the delay is at **Unloading**
    or **Putaway**.'
  - Increase dock-door frequency or assign more associates to stowing.
  agents:
  - '@Architect'
  goal: ''
  name: Inbound Performance (Dock-to-Stock)
  skills: []
  tools: []
- actions:
  - '**LSR Monitoring**: Prioritize "Hot Picks" if carrier pickup is within 30 minutes.'
  - '**Click-to-Ship**: Monitor the gap between Order Placement and Pack-out.'
  agents:
  - '@Architect'
  goal: ''
  name: Outbound Urgency
  skills: []
  tools: []
- actions:
  - Use the **Warehousing Intel** dashboard to detect "Hidden Inventory" (items received
    but not stowed).
  - Resolve associate station blocks in real-time.
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
  name: Resolution
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Operations Manager Strategic Guide

**Version:** 1.0.0

## Overview
Antigravity workflow for warehouse managers to oversee shift initializing, inbound/outbound performance, and issue resolution. Standardized for IDX Visual Editor.

## Trigger Conditions
- Manager reviewing shift KPIs and labor health.
- Detecting bottlenecks in dock-to-stock or outbound shipments.
- User request: `/warehouse-manager`.

**Trigger Examples:**
- "Initialize the 'Night Shift' strategy for the operations team."
- "Optimize the dock-to-stock flow to reduce delays in unloading."

## Phases

### 1. Shift Initialization
- **Agents**: `@Architect`
- **Volume Review**: Check the **Expected ASN** vs. actual dock arrival.
- **Labor Assignment**: Audit the "Labor Health" metric. Re-assign stowers to picking if the **Late Shipment Rate (LSR)** trend exceeds 3.5%.

### 2. Inbound Performance (Dock-to-Stock)
- **Agents**: `@Architect`
- **Bottleneck Detection**: If D2S > 2 hours, identify if the delay is at **Unloading** or **Putaway**.
- Increase dock-door frequency or assign more associates to stowing.

### 3. Outbound Urgency
- **Agents**: `@Architect`
- **LSR Monitoring**: Prioritize "Hot Picks" if carrier pickup is within 30 minutes.
- **Click-to-Ship**: Monitor the gap between Order Placement and Pack-out.

### 4. Resolution
- **Agents**: `@Architect`
- Use the **Warehousing Intel** dashboard to detect "Hidden Inventory" (items received but not stowed).
- Resolve associate station blocks in real-time.
- User request
- Manual activation
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
