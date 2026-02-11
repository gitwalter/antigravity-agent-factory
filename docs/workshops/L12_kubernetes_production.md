# Kubernetes Production Deployments

> **Stack:** Kubernetes | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L12_kubernetes_production`

**Technology:** YAML with Kubernetes (Kubernetes 1.28+)

## Prerequisites

**Required Knowledge:**
- Container concepts (Docker)
- Basic Linux commands
- YAML syntax
- Networking fundamentals

**Required Tools:**
- kubectl
- minikube or kind (local cluster)
- VS Code with YAML extension
- Docker

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand Kubernetes core concepts: Pods, Deployments, Services** (Understand)
2. **Create and manage Deployments for application scaling** (Apply)
3. **Configure Services for internal and external access** (Apply)
4. **Manage configuration with ConfigMaps and Secrets** (Apply)
5. **Implement observability with logging and monitoring** (Apply)

## Workshop Timeline

| Phase | Duration |
|-------|----------|
| Concept | 30 min |
| Demo | 30 min |
| Exercise | 45 min |
| Challenge | 30 min |
| Reflection | 15 min |
| **Total** | **2.5 hours** |

## Workshop Phases

### Concept: Kubernetes Architecture and Core Concepts

*Understanding Kubernetes architecture and core resources*

**Topics Covered:**
- Kubernetes architecture: control plane and nodes
- Pods: smallest deployable unit
- Deployments: managing Pod replicas
- Services: networking and load balancing
- ConfigMaps and Secrets: configuration management
- Scaling: horizontal and vertical
- Observability: logs, metrics, health checks

**Key Points:**
- Pods are ephemeral; use Deployments for persistence
- Services provide stable networking
- ConfigMaps for non-sensitive config, Secrets for sensitive
- Health checks ensure reliability
- Scaling can be manual or automatic

### Demo: Deploying a Web Application

*Live deployment of a full application stack*

**Topics Covered:**
- Creating Deployment YAML
- Configuring Service for access
- Adding ConfigMap for configuration
- Creating Secret for credentials
- Setting up health checks
- Scaling the deployment
- Viewing logs and metrics

**Key Points:**
- YAML is declarative
- Labels and selectors connect resources
- Health checks prevent bad deployments
- Scaling is simple with Deployments

### Exercise: Basic Deployment and Service

*Create a Deployment and Service for a web app*

**Topics Covered:**
- Write Deployment YAML
- Create Service YAML
- Apply manifests
- Verify deployment
- Access the application

### Exercise: Configuration Management

*Use ConfigMaps and Secrets in deployments*

**Topics Covered:**
- Create ConfigMap
- Create Secret
- Mount in Deployment
- Update deployment
- Verify configuration

### Challenge: Multi-Tier Application Deployment

*Deploy a complete application with frontend, backend, and database*

**Topics Covered:**
- Deploy frontend application
- Deploy backend API
- Deploy database
- Configure Services
- Set up ConfigMaps and Secrets
- Implement health checks
- Scale components

### Reflection: Key Takeaways and Production Considerations

*Consolidate learning and discuss production patterns*

**Topics Covered:**
- Kubernetes best practices
- Resource management
- Security considerations
- Monitoring and observability
- CI/CD integration

**Key Points:**
- Always use Deployments, not Pods directly
- Set resource limits
- Use Secrets for sensitive data
- Implement health checks
- Monitor everything

## Hands-On Exercises

### Exercise: Basic Deployment and Service

Create a Deployment and Service for a web application

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Labels must match between Deployment selector and Pod template
- Service selector must match Pod labels
- Health checks prevent serving traffic to unhealthy pods
- Set resource limits to prevent resource exhaustion

**Common Mistakes to Avoid:**
- Mismatched labels between selector and pods
- Forgetting health checks
- Not setting resource limits
- Wrong service type

### Exercise: Configuration Management

Create and use ConfigMaps and Secrets

**Difficulty:** Medium | **Duration:** 25 minutes

**Common Mistakes to Avoid:**
- Using data instead of stringData for Secrets
- Not base64 encoding Secret values when using data
- Mismatched ConfigMap/Secret names
- Wrong mount paths

## Challenges

### Challenge: Multi-Tier Application Deployment

Deploy a complete application stack with frontend, backend, and database

**Requirements:**
- Deploy frontend application (nginx)
- Deploy backend API (FastAPI)
- Deploy PostgreSQL database
- Configure Services for each tier
- Set up ConfigMaps for configuration
- Create Secrets for database credentials
- Implement health checks for all components
- Scale frontend and backend independently

**Evaluation Criteria:**
- All components deploy successfully
- Services route traffic correctly
- Configuration is externalized
- Secrets are used for sensitive data
- Health checks work
- Scaling works independently
- Components can communicate

**Stretch Goals:**
- Add Ingress for external access
- Implement HorizontalPodAutoscaler
- Add PersistentVolumes for database
- Set up monitoring with Prometheus

## Resources

**Official Documentation:**
- https://kubernetes.io/docs/home/
- https://kubernetes.io/docs/concepts/
- https://kubernetes.io/docs/tutorials/

**Tutorials:**
- Kubernetes Basics - Official Tutorial
- Kubernetes for Beginners - freeCodeCamp

**Videos:**
- Kubernetes Tutorial for Beginners - YouTube
- Kubernetes Deep Dive - CNCF

## Self-Assessment

Ask yourself these questions:

- [ ] Can I create and manage Deployments?
- [ ] Do I understand how Services work?
- [ ] Can I use ConfigMaps and Secrets?
- [ ] Do I know how to scale applications?
- [ ] Can I troubleshoot deployment issues?

## Next Steps

**Next Workshop:** `L13_docker_containerization`

**Practice Projects:**
- Deploy a microservices architecture
- Set up CI/CD with Kubernetes
- Implement monitoring and logging

**Deeper Learning:**
- Advanced Kubernetes patterns
- Helm charts and package management
- Service mesh (Istio, Linkerd)

## Related Knowledge Files

- `kubernetes-patterns.json`
- `docker-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L12_kubernetes_production.json`