---
description: Tactical Blueprint for production-grade FastAPI applications. Focuses
  on procedural execution, tool-calling sequences, and idiomatic excellence.
name: fastapi-enterprise
type: skill
---
# Capability Manifest: FastAPI Enterprise

This blueprint provides the **procedural truth** for engineering, testing, and deploying high-fidelity Python backends in the Antigravity Agent Factory.

## Operational Environment

- **Runtime**: Python 3.11/3.12 (Mandatory Type Hinting).
- **Core Stack**: FastAPI 0.110+, Pydantic v2, SQLAlchemy 2.0 (Async), Alembic.
- **Observability**: Prometheus/OpenTelemetry, Structured Logging (JSON).

## Process

Follow these procedures to implement the capability:

### Procedure 1: Scaffolding a Feature Domain
FastAPI applications in this factory follow a **Domain-Driven Design (DDD)** structure.
Execute these steps to add a new domain:
1.  **Create Directory**: `mkdir -p src/domains/[domain_name]/{models,schemas,routers,services}`.
2.  **Initialize Models**: Create `models.py` using SQLAlchemy 2.0 `Mapped` syntax.
3.  **Create Schemas**: Define Pydantic v2 models for `In`, `Out`, and `Update`.
4.  **Register Router**: Import and include the new router in `src/main.py` with versioned prefix (e.g., `/api/v1/[domain]`).

### Procedure 2: Implementing Async Data Access
1.  **Session Injection**: Use the `get_async_session` dependency.
2.  **Query Pattern**: Use `select()` and `scalar_one_or_none()` for single items; `scalars().all()` for lists.
3.  **Eager Loading**: Mandatory use of `selectinload()` for relationships to prevent "Truth" violations (Async N+1 errors).

### Procedure 3: Production Validation & Guards
1.  **Security**: Use `HTTPBearer` or `OAuth2PasswordBearer` for all protected routes.
2.  **Graceful Failures**: Implement a global `Exception` handler that returns standard JSON error responses.
3.  **Middle-Layer Guards**: Use Pydantic `@field_validator` for complex business logic validation.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| `MissingGreenlet` | Synchronous operation in async session. | Ensure all DB calls are awaited and use `AsyncSession`; check for `run_sync()` usage for legacy sync operations. |
| `ValidationError` | Pydantic model mismatch. | Audit the `response_model` in the route decorator; verify all fields match the DB model or DTO. |
| `422 Unprocessable Entity` | Data type mismatch or missing field. | Check the OpenAPI docs (`/docs`) for specific field errors; ensure `Optional` fields have defaults. |

## Idiomatic Code Patterns (The Gold Standard)

### The "Truthful" Pydantic Model
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def password_complexity(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v
```

### The "Observable" Router
```python
@router.post("/", response_model=UserOut, status_code=status.HTTP_211_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Observable creation flow with structured logging and audit trailing.
    """
    logger.info("creating_user", user_email=user_in.email, triggered_by=current_user.id)
    return await UserService(db).create(user_in)
```

## Prerequisites

| Action | Command |
| :--- | :--- |
| Run Dev Server | `fastapi dev src/main.py` |
| Fast Test Loop | `pytest -v -k "not integration"` |
| Run Migrations | `alembic upgrade head` |
| Format Code | `ruff format .` |

## When to Use
Use this blueprint whenever building, refactoring, or debugging a Python/FastAPI service. It is the authoritative source for "How we build" vs "What FastAPI is."


## Best Practices

- Follow the system axioms (A1-A5)
- Ensure all changes are verifiable
- Document complex logic for future maintenance
