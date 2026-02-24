# Plane PMS Native Integration: Technical Guide

This document provides a comprehensive overview of the **Plane Project Management System (PMS)**, its internal architecture, and the native integration patterns utilized by the Antigravity Agent Factory.

---

## 1. What is Plane?

### Platform History & Origin
**Plane** was born out of a desire for a powerful, open-source alternative to proprietary project management tools. Developed primarily by **Makeplane**, it was officially open-sourced in **November 2022**. Since then, it has evolved into a high-performance platform used by thousands of engineering teams to manage complex project lifecycles.

### Core Capabilities
- **Issues & Cycles**: Granular task tracking and sprint planning.
- **Modules**: Grouping issues by logical focus areas.
- **Views & Pages**: Customizable data visualization and collaborative documentation.
- **Extensibility**: A robust Django-based backend that allows for direct ORM access—the core of our native integration.

### Official Documentation & Community
- **Official Website**: [https://plane.so/](https://plane.so/)
- **GitHub Repository**: [makeplane/plane](https://github.com/makeplane/plane)
- **Docs**: [https://docs.plane.so/](https://docs.plane.so/)

---

## 2. Infrastructure: The "Native-Direct" Pattern

The Antigravity Factory utilizes a **Native-Direct** integration pattern. Unlike standard integrations that rely on external API endpoints or restricted MCP servers, this approach interacts directly with the Plane Django application layer via container execution.

### Logic Flow
1.  **Request**: An agent or developer triggers a command via `scripts/pms/manager.py`.
2.  **Safe-Passage**: Payload logic is Base64 encoded to bypass shell-escaping vulnerabilities.
3.  **Execution**: The command is injected into the `plane-api` container via `docker exec`.
4.  **ORM Interaction**: The command executes within the authenticated Django environment, ensuring 100% data integrity and bypassing REST API limitations.

---

## 3. Simplified Local Setup

To get Plane running on your local machine for use with this integration, follow these streamlined steps.

### Prerequisites
- **Docker & Docker Compose** installed. [Official Docker Install Guide](https://docs.docker.com/get-docker/)

### Quick Start (The "One-Command" Setup)
1. **Prepare Environment**:
   ```bash
   mkdir plane-self-host && cd plane-self-host
   curl -fsSL https://raw.githubusercontent.com/makeplane/plane/master/deploy/self-host/install.sh -o setup.sh
   chmod +x setup.sh
   ```
2. **Run Configurator**:
   ```bash
   ./setup.sh --install
   # Set your domain to 'localhost' when prompted.
   ```
3. **Lift Service Stack**:
   ```bash
   ./setup.sh --start
   ```
Access Plane at `http://localhost:8080` (default port).

---

## 4. Service Ecosystem: 12-Component Breakdown

In this environment, the following services work in orchestration to provide the full Plane experience:

| Category | Service | Container Name | Purpose |
| :--- | :--- | :--- | :--- |
| **Core** | **API** | `plane-api` | **The Brain**: Handles ORM operations and API logic. |
| | **Web** | `plane-web` | The primary UI (Next.js/React). |
| | **Admin** | `plane-admin` | Administrative interface for instance settings. |
| **Workers** | **Worker** | `plane-worker` | Executes background tasks (notifications, analytics). |
| | **Beat** | `plane-beat-worker` | Scheduler for recurring background tasks. |
| | **Space** | `plane-space` | Manages project-specific collaborative "Pages". |
| **Data** | **DB** | `plane-db` | Postgres backend (Source of Truth). |
| | **Redis** | `plane-redis` | High-speed caching and task queue management. |
| | **MinIO** | `plane-minio` | S3-compatible storage for attachments. |
| | **MinIO** | `plane-minio` | S3-compatible storage for attachments. |
| **Nervous System** | **Proxy** | `plane-proxy` | Nginx reverse proxy routing traffic. |
| | **Live** | `plane-live` | Realtime event broadcaster for collaborative UI. |

### Note on External Services
In this specific deployment, additional services like **Qdrant** (`antigravity-qdrant`) are utilized by the **Antigravity Agent Factory** for RAG (Retrieval-Augmented Generation), but they are **not** part of the core Plane distribution.

---

## 5. Troubleshooting: Deployment & Known Issues

### Common Problem: "Unregistered Task" (Celery Errors)
**Symptoms**: Tracebacks in `plane-worker` logs containing `KeyError` for specific task types (e.g., `issue_activity` or `recent_visited_task`).

**The Cause**: This occurs when the background worker (Celery) receives a task request from the API but doesn't have the task definition registered in its local registry. This is often due to service version mismatch or the worker needing a "clean" discovery cycle.

**Solution**:
1. **Restart Workers**: Force a fresh registration scan.
   ```bash
   docker restart plane-worker plane-beat-worker
   ```
2. **Total Stack Reset**: If persistent, stop and clear the stack to reset internal registries.
   ```bash
   ./setup.sh --stop
   ./setup.sh --start
   ```
3. **Queue Cleanup**: Flush the Redis cache if "ghost" tasks are stuck in the queue.
   ```bash
   docker exec plane-redis redis-cli FLUSHALL
   ```

### Operational Issues
| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| `Docker command failed` | Container `plane-api` is stopped. | Run `docker start plane-api`. |
| `KeyError: bgtasks...` | Worker task registry mismatch. | Restart `plane-worker` (see above). |
| `State mismatch` | Case/Naming mismatch. | Match exactly with UI (e.g., `In Progress`). |

---

## 6. Implementation Details: Shell-Safe Payloads

The integration utilizes a **Base64-Execution bridge** to handle complex HTML descriptions without risking shell-injection.

### The Bridge Pattern
```python
import base64

# 1. Define the Python logic
cmd_logic = "from plane.db.models import Project; print(Project.objects.all())"

# 2. Encode for shell safe-passage
encoded = base64.b64encode(cmd_logic.encode()).decode()

# 3. Execute via bridge
# docker exec plane-api python manage.py shell -c "import base64; exec(base64.b64decode('...'))"
```

### Advanced Debugging
Access the Plane shell directly for manual ORM inspection:
```bash
docker exec -it plane-api python manage.py shell
```
