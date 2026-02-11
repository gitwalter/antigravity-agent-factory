# Docker Containerization Best Practices

> **Stack:** Docker | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L13_docker_containerization`

**Technology:** Dockerfile with Docker (Docker 24+)

## Prerequisites

**Required Knowledge:**
- Basic Linux commands
- Understanding of application deployment
- Command line basics

**Required Tools:**
- Docker Desktop or Docker Engine
- VS Code with Docker extension
- Git

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Write efficient Dockerfiles using multi-stage builds** (Apply)
2. **Optimize Docker layer caching for faster builds** (Analyze)
3. **Implement security best practices (non-root user, minimal base images)** (Apply)
4. **Use Docker Compose for multi-container applications** (Apply)
5. **Configure Docker networking and volumes** (Apply)

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

### Concept: Docker Fundamentals and Best Practices

*Understanding Docker architecture and production best practices*

**Topics Covered:**
- Docker architecture: images, containers, layers
- Dockerfile best practices
- Multi-stage builds for optimization
- Layer caching and build optimization
- Security: non-root users, minimal images, secrets
- Docker Compose for orchestration
- Networking: bridge, host, overlay networks
- Volumes: bind mounts and named volumes

**Key Points:**
- Multi-stage builds reduce final image size
- Layer order affects cache efficiency
- Always use non-root users in production
- Minimal base images improve security
- Compose simplifies multi-container apps

### Demo: Building Production-Ready Containers

*Live coding a secure, optimized Dockerfile*

**Topics Covered:**
- Writing multi-stage Dockerfile
- Optimizing layer caching
- Adding non-root user
- Creating docker-compose.yml
- Setting up networks and volumes
- Building and testing the image

**Key Points:**
- Separate build and runtime stages
- Copy only what's needed
- Use specific base image tags
- Set proper file permissions

### Exercise: Multi-Stage Dockerfile

*Create an optimized multi-stage Dockerfile*

**Topics Covered:**
- Write build stage
- Create runtime stage
- Copy artifacts efficiently
- Add non-root user
- Optimize layer order

### Exercise: Docker Compose Setup

*Create docker-compose.yml for multi-service app*

**Topics Covered:**
- Define services
- Configure networks
- Set up volumes
- Add environment variables
- Configure dependencies

### Challenge: Full Stack Application Containerization

*Containerize a complete application with frontend, backend, and database*

**Topics Covered:**
- Containerize frontend application
- Containerize backend API
- Set up database container
- Create docker-compose.yml
- Configure networking
- Set up volumes for persistence
- Add health checks

### Reflection: Key Takeaways and Production Considerations

*Consolidate learning and discuss deployment*

**Topics Covered:**
- Docker best practices summary
- Security considerations
- Performance optimization
- CI/CD integration
- Monitoring and logging

**Key Points:**
- Always use multi-stage builds
- Security is non-negotiable
- Optimize for cache efficiency
- Use Compose for development
- Monitor container health

## Hands-On Exercises

### Exercise: Multi-Stage Dockerfile

Create an optimized multi-stage Dockerfile for a Python application

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Separate build dependencies from runtime
- Use --from flag to copy from builder stage
- Create non-root user before copying files
- Set proper file ownership with --chown
- Use HEALTHCHECK for container health

**Common Mistakes to Avoid:**
- Not separating build and runtime stages
- Forgetting to switch to non-root user
- Copying unnecessary files
- Not optimizing layer order
- Missing health checks

### Exercise: Docker Compose Setup

Create docker-compose.yml for a web application with database

**Difficulty:** Medium | **Duration:** 25 minutes

**Common Mistakes to Avoid:**
- Not setting up health checks
- Missing depends_on conditions
- Not configuring networks
- Forgetting volume definitions
- Not using restart policies

## Challenges

### Challenge: Full Stack Application Containerization

Containerize a complete application with frontend, backend, and database

**Requirements:**
- Create multi-stage Dockerfile for frontend
- Create multi-stage Dockerfile for backend
- Set up PostgreSQL database container
- Create docker-compose.yml orchestrating all services
- Configure custom networks
- Set up volumes for database persistence
- Add health checks for all services
- Implement non-root users in all containers
- Optimize image sizes

**Evaluation Criteria:**
- All Dockerfiles use multi-stage builds
- Images are optimized and secure
- Compose file orchestrates all services
- Networking allows service communication
- Volumes persist data correctly
- Health checks work
- All containers run as non-root
- Build times are optimized

**Stretch Goals:**
- Add Redis cache container
- Implement Docker secrets
- Set up reverse proxy with Nginx
- Add monitoring with Prometheus
- Create production and development Compose files

## Resources

**Official Documentation:**
- https://docs.docker.com/
- https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- https://docs.docker.com/compose/

**Tutorials:**
- Docker Getting Started - Official
- Docker Deep Dive - Pluralsight

**Videos:**
- Docker Tutorial for Beginners - freeCodeCamp
- Docker Best Practices - DockerCon

## Self-Assessment

Ask yourself these questions:

- [ ] Can I write efficient multi-stage Dockerfiles?
- [ ] Do I understand layer caching optimization?
- [ ] Can I implement security best practices?
- [ ] Do I know how to use Docker Compose?
- [ ] Can I configure networking and volumes?

## Next Steps

**Next Workshop:** `L12_kubernetes_production`

**Practice Projects:**
- Containerize a microservices architecture
- Set up CI/CD with Docker
- Create development and production environments

**Deeper Learning:**
- Advanced Docker networking
- Docker security scanning
- Container orchestration with Kubernetes

## Related Knowledge Files

- `docker-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L13_docker_containerization.json`