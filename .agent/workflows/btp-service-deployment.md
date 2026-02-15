---
## Overview

description: End-to-end workflow for deploying SAP applications to SAP Business Technology Platform (BTP). Covers build configurat...
---

# Btp Service Deployment

End-to-end workflow for deploying SAP applications to SAP Business Technology Platform (BTP). Covers build configuration, service bindings, Cloud Foundry/Kyma deployment, and monitoring setup.

**Version:** 1.0.0  
**Created:** 2026-02-09  
**Applies To:** sap-developer, btp-deployment

## Trigger Conditions

This workflow is activated when:

- Deploying CAP application to BTP
- Deploying RAP extension to BTP ABAP
- Setting up BTP services and bindings
- Configuring CI/CD for BTP

**Trigger Examples:**
- "Deploy my CAP application to BTP Cloud Foundry"
- "Set up XSUAA for my application"
- "Configure destination service for on-premise connectivity"
- "Deploy to BTP Kyma runtime"

## Steps

### Create MTA Descriptor (mta.yaml)

### Configure XSUAA (xs-security.json)

### Create Manifest.yml (Optional)

### Configure XSUAA Service

### Configure Destination Service (if needed)

### Configure Connectivity Service (if needed)

### Configure SAP HANA Cloud (if needed)

### Build MTA Archive

### Deploy to Cloud Foundry

### Deploy to Kyma (Alternative)

### Verify Service Bindings

### Configure Routes

### Assign Roles (if needed)

### Set Up Monitoring


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
