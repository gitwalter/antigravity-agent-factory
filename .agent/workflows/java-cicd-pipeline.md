---
## Overview

description: Comprehensive CI/CD pipeline workflow for Java/Spring Boot applications using Maven/Gradle, Testcontainers, Docker/Ji...
---

# Java Cicd Pipeline

Comprehensive CI/CD pipeline workflow for Java/Spring Boot applications using Maven/Gradle, Testcontainers, Docker/Jib, and Kubernetes/Helm deployment. This workflow covers build, test, package, and deployment phases with quality gates and security scanning.

**Version:** 1.0.0
**Created:** 2026-02-09
**Agent:** spring-developer, java-architect

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`.

## Trigger Conditions

This workflow is activated when:

- User requests "set up CI/CD pipeline", "create build pipeline", "configure deployment"
- User mentions "GitHub Actions", "GitLab CI", "Jenkins", "CI/CD"
- User asks to "automate build and deployment" or "set up continuous integration"
- User requests "Docker build", "Kubernetes deployment automation"

**Trigger Examples:**
- "Set up CI/CD pipeline for Spring Boot application"
- "Create GitHub Actions workflow for Java project"
- "Configure automated testing an

## Steps

### Checkout Code

### Cache Dependencies

### Set Up Java Environment

### Build Application

### Quality Checks

### Unit Tests

### Integration Tests with Testcontainers

### API Tests

### Test Coverage

### Build Docker Image

### Scan Image for Vulnerabilities

### Push to Registry

### Prepare Kubernetes Manifests

### Deploy with Helm

### Verify Deployment

### Rollback on Failure


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
