---
description: Tactical Blueprint for Production-Grade Docker. Focuses on security hardening,
  image optimization, and multi-stage builds.
name: docker-deployment
type: skill
---
# Capability Manifest: Docker Production Mastery

This blueprint provides the **procedural truth** for building, securing, and deploying production-grade containers.

## When to Use

This skill should be used when completing tasks related to docker deployment.

## Process

Follow these procedures to implement the capability:

### Procedure 1: The "Clean Core" Dockerfile (Multi-Stage)
1.  **Stage 1: Build**: Use a heavy image (e.g., `python:3.11-bookworm`) to compile dependencies.
2.  **Stage 2: Final**: Use a minimal 'distroless' or 'slim' image (e.g., `python:3.11-slim-bookworm` or `gcr.io/distroless/python3`).
3.  **Strict Selection**: Only copy the resulting artifacts (e.g., `/usr/local/lib/python3.11/site-packages`) to the final stage.

### Procedure 2: Security Hardening (The Guardian Gate)
1.  **Non-Root Execution**: Always create a dedicated user (`USER appuser`) and give it ownership of only the required directories.
2.  **Secret Redaction**: Never use `ENV` for secrets. Use `docker secrets` or mount environment variables at runtime.
3.  **Read-Only Filesystem**: Mount the application volume as read-only wherever possible using `:ro`.

### Procedure 3: Observability & Health
1.  **Prescriptive Healthchecks**: Implement a `HEALTHCHECK` that probes the specific application port or a dedicated `/health` endpoint.
2.  **Signal Handling**: Ensure the application (or a light init like `tini`) correctly handles `SIGTERM` for graceful container shutdown.
3.  **Structured Logging**: Configure the container to output JSON logs to `stdout/stderr` for driver-level capture.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Image Size > 1GB** | Missing `.dockerignore` or failing to use multi-stage builds. | Add `.dockerignore` for `venv`, `.git`, and `__pycache__`; implement Stage 2 prune. |
| **Permission Denied** | Application trying to write to a directory owned by root. | Check `USER` directive and `chown` permissions in the Dockerfile. |
| **Container Restart Loop** | Entrypoint script failing or Healthcheck timing out during startup. | Review `docker logs`; increase `start_period` in the healthcheck. |

## Idiomatic Code Patterns (The Gold Standard)

### The "Secure & Slim" Python Template
```dockerfile
# BUILDER
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# RUNTIME
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd -m appuser && chown -R appuser /app
USER appuser
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

## Prerequisites

| Action | Command / Tool |
| :--- | :--- |
| Vulnerability Scan | `docker scout quickview` or `trivy image <name>` |
| Inspect Layers | `dive <image_id>` |
| Prune Everything | `docker system prune -a --volumes` |

## Best Practices
Before building a production image:
- [ ] Multi-stage build is implemented.
- [ ] User is non-root (`USER appuser`).
- [ ] `.dockerignore` is present and comprehensive.
- [ ] Healthcheck is specific to the application state.
- [ ] Image base is a pinned version (e.g., `:3.11.5-slim`, not `:latest`).
