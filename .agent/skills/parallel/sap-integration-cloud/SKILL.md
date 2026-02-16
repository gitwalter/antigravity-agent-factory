---
description: Tactical Blueprint for SAP Cloud Integration (CPI), Event Mesh, and API
  Management. Focuses on secure, observable, and resilient enterprise integration
  patterns.
name: sap-integration-cloud
type: skill
---
# Capability Manifest: SAP Integration Cloud

This blueprint provides the **procedural truth** for engineering resilient integration solutions across the SAP BTP and S/4HANA ecosystem.

## When to Use

This skill should be used when completing tasks related to sap integration cloud.

## Process

Follow these procedures to integrate SAP systems via Cloud Integration:

### Procedure 1: Resilient iFlow Design (CPI)
1.  **Modular Transformation**: Use Groovy scripts for complex logic, but keep them focused and unit-testable. Use `XmlSlurper` and `JsonBuilder` for efficient parsing and building.
2.  **Explicit Routing**: Use Content-Based Routers to handle different message types. Document the routing logic in the `MessageLog` for observability.
3.  **Error Subprocess Truth**: Every iFlow must have an `Exception Subprocess`. Use a custom script to log the `CamelExceptionCaught` and trigger retries or DLQ (Dead Letter Queue) placement.

### Procedure 2: Event-Driven Orchestration (Event Mesh)
1.  **Topic Hierarchy**: Use a standard semantic hierarchy (e.g., `s4/salesorder/created`).
2.  **Idempotency Gate**: Consumer logic must implement an idempotency check (e.g., checking a local table or cache for the `EventID`) to avoid duplicate processing.
3.  **CloudEvents Standard**: Ensure all events comply with the CloudEvents specification for cross-system compatibility.

### Procedure 3: Secure API Exposure (API Management)
1.  **Policy Enforcement**:
    - **Spike Arrest**: Prevent traffic surges.
    - **Verify OAuth**: Mandatory for all external-facing APIs.
    - **Response Cache**: Use for read-heavy, low-changing data to protect S/4HANA resources.
2.  **Transformation Gating**: Use the API proxy to handle minor protocol translations (e.g., XML to JSON) before the message reaches the backend.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **HTTP 500 (Integration)** | Transformation script error or backend timeout. | Inspect CPI Message Monitor for the `exchangeId`; check the `Exception Subprocess` log for script stack traces. |
| **Event Loss** | No queue subscription or TTL expired. | Check Event Mesh Management UI for "Dropped Messages"; verify queue capacity and client connectivity. |
| **OAuth 401** | Token expired or Principal Propagation failure. | Check BTP Destination configuration; verify trust setup between S/4HANA and BTP. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Test Script | `Local Groovy REPL / CPI Simulation` |
| Monitor Traffic | `CPI Message Monitoring` |
| Inspect Queue | `SAP Event Mesh Cockpit` |
| Manage Policy | `SAP API Business Hub (API Management)` |

## Best Practices
Before finalizing any integration:
- [ ] Exception subprocess implemented with logging.
- [ ] OAuth/Security policy active.
- [ ] Idempotency strategy defined for Event consumers.
- [ ] Rate limiting (Spike Arrest) active for Public APIs.
