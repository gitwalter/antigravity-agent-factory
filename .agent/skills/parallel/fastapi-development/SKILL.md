---
description: FastAPI project structure, Router organization, Dependency injection,
  Pydantic v2 models, Background tasks, WebSocket endpoints, Middleware, CORS, OpenAPI
  customization
name: fastapi-development
type: skill
---
# Fastapi Development

FastAPI project structure, Router organization, Dependency injection, Pydantic v2 models, Background tasks, WebSocket endpoints, Middleware, CORS, OpenAPI customization

Build production FastAPI applications with proper structure, dependency injection, Pydantic validation, and async patterns.

## Process

1. **Scaffold** – Run `python scripts/scaffold.py --name myapp --output-dir .` or create structure manually. See REFERENCE.md § Project Structure.
2. **App Entry** – FastAPI instance with CORS middleware, routers, health endpoint at `/health`. See REFERENCE.md § Main Application.
3. **Routers** – APIRouter per domain with prefix (e.g. `/api/v1/users`), thin handlers delegating to services. See REFERENCE.md § Router Organization.
4. **Dependencies** – `get_db`, `get_current_user` in `core/dependencies.py`; inject via `Depends()`. See REFERENCE.md § Dependency Injection.
5. **Schemas** – Pydantic v2 models in `domains/*/schemas.py`; separate Create/Update/Response; use `ConfigDict(from_attributes=True)` for ORM. See REFERENCE.md § Pydantic v2 Models.
6. **Background Tasks** – Use `BackgroundTasks.add_task()` for non-blocking work (emails, cleanup). See REFERENCE.md § Background Tasks.
7. **WebSockets** – ConnectionManager pattern; `accept()`, `receive_text()`, `send_text()`, handle `WebSocketDisconnect`. See REFERENCE.md § WebSocket Endpoints.
8. **Middleware** – Add logging, timing, rate limiting via `BaseHTTPMiddleware`. See REFERENCE.md § Middleware.
9. **OpenAPI** – Customize via `app.openapi` override or `get_openapi()`. See REFERENCE.md § OpenAPI Customization.

## Best Practices

- Domain-driven structure (organize by feature, not layer)
- Keep routers thin; delegate to service layer
- Use dependency injection for all external resources
- Separate Pydantic schemas from SQLAlchemy models
- Use async for all I/O
- Implement exception handlers; use `response_model` to limit exposed data
- Add type hints throughout; use Pydantic validators for complex validation
- Add health check at `/health`; configure CORS from settings
- Use structured logging; HTTPS in production

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Business logic in routers | Move to service layer |
| Synchronous database calls | Use async database drivers |
| Missing validation | Use Pydantic models |
| Global state | Use dependency injection |
| Missing error handling | Add exception handlers |
| No response models | Use `response_model` parameter |

## Bundled Resources

- **QUICKSTART.md** – 5-minute getting started guide
- **REFERENCE.md** – Detailed code examples (project structure, routers, dependencies, Pydantic, background tasks, WebSocket, middleware, CORS, OpenAPI)
- **scripts/scaffold.py** – Generate FastAPI project structure (`--name`, `--output-dir`)
- **scripts/verify.py** – Check project follows skill patterns (`--project-dir`)
- **examples/basic_app/** – Minimal working FastAPI app (health endpoint, CRUD resource, Pydantic models)

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
