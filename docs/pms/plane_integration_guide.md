# Plane PMS Integration Guide

This document provides a comprehensive overview of the **Plane Project Management System (PMS)** and how the Antigravity Agent Factory integrates with it.

---

## 1. What is Plane?

### Platform History & Origin
**Plane** was born out of a desire for a powerful, open-source alternative to proprietary project management tools. Developed primarily by **Makeplane**, it was officially open-sourced in **November 2022**. Since then, it has evolved into a high-performance platform used by thousands of engineering teams to manage complex project lifecycles.

### Core Capabilities
- **Issues & Cycles**: Granular task tracking and sprint planning.
- **Modules**: Grouping issues by logical focus areas.
- **Views & Pages**: Customizable data visualization and collaborative documentation.
- **REST API & MCP**: Programmatic access for agentic automation.

### Official Resources
- **Official Website**: [https://plane.so/](https://plane.so/)
- **GitHub Repository**: [makeplane/plane](https://github.com/makeplane/plane)
- **Docs**: [https://docs.plane.so/](https://docs.plane.so/)

---

## 2. Current Architecture: Cloud Plane + MCP

The Antigravity Agent Factory now uses a **cloud-hosted Plane instance** accessed entirely through the **Plane MCP (Model Context Protocol) server**. This replaces the legacy local Docker-based approach and provides a cleaner, more reliable integration.

### How It Works

```
Agent Request  →  MCP Tool Call (mcp_plane_*)  →  Cloud Plane API  →  Response
```

1. **Request**: An agent needs to create, update, or query work items.
2. **MCP Tool Call**: The agent invokes a `mcp_plane_*` tool (e.g., `mcp_plane_create_work_item`).
3. **Cloud API**: The Plane MCP server routes the request to the cloud-hosted Plane instance via its REST API.
4. **Response**: Structured JSON data is returned directly to the agent.

### Advantages Over the Legacy Approach
| Aspect | Legacy (Docker/Local) | Current (Cloud/MCP) |
| :--- | :--- | :--- |
| **Infrastructure** | Self-hosted, 12 Docker containers | Zero infrastructure; managed cloud |
| **Interface** | Python script → `docker exec` → Django ORM | Direct `mcp_plane_*` tool calls |
| **Reliability** | Dependent on local Docker health | Cloud-managed uptime |
| **Agent Access** | Subprocess calls via `manager.py` | Native MCP tool integration |
| **Shell Safety** | Required Base64 encoding for payloads | Not applicable; structured JSON |
| **Maintenance** | Manual upgrades, container restarts | Automatic cloud updates |

### Project Context

| Property | Value |
| :--- | :--- |
| **Project Identifier** | `AGENT` |
| **Project ID** | `e71eb003-87d4-4b0c-a765-a044ac5affbe` |
| **Workspace** | `agent-factory` |

---

## 3. MCP Tool Reference

All project management operations use the `mcp_plane_*` tools. Below is a quick-reference mapping.

### Core Operations

| Operation | MCP Tool |
| :--- | :--- |
| List work items | `mcp_plane_list_work_items` |
| Create work item | `mcp_plane_create_work_item` |
| Retrieve work item | `mcp_plane_retrieve_work_item` |
| Update work item | `mcp_plane_update_work_item` |
| Search work items | `mcp_plane_search_work_items` |
| Delete work item | `mcp_plane_delete_work_item` |

### Metadata & Context

| Operation | MCP Tool |
| :--- | :--- |
| List labels | `mcp_plane_list_labels` |
| List states | `mcp_plane_list_states` |
| List cycles | `mcp_plane_list_cycles` |
| List modules | `mcp_plane_list_modules` |
| Get current user | `mcp_plane_get_me` |
| List projects | `mcp_plane_list_projects` |

### Associations

| Operation | MCP Tool |
| :--- | :--- |
| Add to cycle | `mcp_plane_add_work_items_to_cycle` |
| Add to module | `mcp_plane_add_work_items_to_module` |
| Create comment | `mcp_plane_create_work_item_comment` |
| Create link | `mcp_plane_create_work_item_link` |
| Create relation | `mcp_plane_create_work_item_relation` |

### Operational Skill

For the full end-to-end workflow (pre-flight checklist, mandatory module/cycle association, label governance), see the [managing-plane-tasks](../../.agent/skills/routing/managing-plane-tasks/SKILL.md) skill.

---

## 4. Legacy Architecture (Historical Reference)

> [!NOTE]
> This section is preserved for historical context. The legacy architecture is **deprecated** and should not be used for new work. All operations should use the MCP tools described in §2–§3.

### The "Native-Direct" Pattern (Deprecated)

The original integration used a **Native-Direct** pattern, interacting directly with the Plane Django application layer via Docker container execution.

**Logic Flow:**
1. **Request**: An agent or developer triggered a command via `scripts/pms/manager.py`.
2. **Safe-Passage**: Payload logic was Base64 encoded to bypass shell-escaping vulnerabilities.
3. **Execution**: The command was injected into the `plane-api` container via `docker exec`.
4. **ORM Interaction**: The command executed within the authenticated Django environment.

### Legacy Service Ecosystem (12 Components)

| Category | Service | Container Name | Purpose |
| :--- | :--- | :--- | :--- |
| **Core** | **API** | `plane-api` | Handled ORM operations and API logic. |
| | **Web** | `plane-web` | Primary UI (Next.js/React). |
| | **Admin** | `plane-admin` | Administrative interface. |
| **Workers** | **Worker** | `plane-worker` | Background tasks (notifications, analytics). |
| | **Beat** | `plane-beat-worker` | Scheduler for recurring tasks. |
| | **Space** | `plane-space` | Collaborative "Pages". |
| **Data** | **DB** | `plane-db` | Postgres backend. |
| | **Redis** | `plane-redis` | Caching and task queue. |
| | **MinIO** | `plane-minio` | S3-compatible attachment storage. |
| **Network** | **Proxy** | `plane-proxy` | Nginx reverse proxy. |
| | **Live** | `plane-live` | Realtime event broadcaster. |

### Legacy Troubleshooting

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| `Docker command failed` | Container `plane-api` stopped. | `docker start plane-api`. |
| `KeyError: bgtasks...` | Worker task registry mismatch. | Restart `plane-worker`. |
| `State mismatch` | Case/naming mismatch. | Match exactly with UI values. |
| Celery "Unregistered Task" | Worker needs fresh registration. | `docker restart plane-worker plane-beat-worker`. |

### Legacy Scripts (Deleted)

| Script | Purpose | Status |
| :--- | :--- | :--- |
| `scripts/pms/manager.py` | CLI for issue CRUD via Django ORM | **DELETED** |
| `scripts/pms/test_plane_conn.py` | API connection test | **DELETED** |
| `scripts/pms/dump_settings.py` | Dump Django settings | **DELETED** |
| `scripts/pms/migrate_legacy_data.py` | SQLite→Plane migration | **DELETED** |

---

## 5. Migration Notes

The migration from local to cloud Plane occurred as part of the v1.5.x release cycle. Key changes:

1. **Infrastructure**: The 12-container Docker Compose stack was replaced by a managed cloud Plane instance at `plane.so`.
2. **Interface**: The `manager.py` script (subprocess → `docker exec` → Django ORM) was replaced by the Plane MCP server providing native `mcp_plane_*` tool calls.
3. **Authentication**: Moved from implicit container-level Django auth to API token-based auth configured in the MCP server config.
4. **Skill Updates**: The `managing-plane-tasks` skill (v2.0.0) was rewritten to use MCP tools exclusively. The `mastering-project-management` skill was updated to reference MCP operations.
5. **Final Cleanup**: As of v1.5.0, the `scripts/pms/` directory and all legacy property-based verification scripts have been **removed** from the repository to prevent architectural drift.

---

*Operational maturity is the foundation of high-velocity agency.*
