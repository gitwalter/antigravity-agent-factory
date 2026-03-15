---
agents:
- java-systems-specialist
category: parallel
description: 'Spring Boot 3+ project setup (Initializr), REST controllers, Service
  layer patterns, Exception handling (@ControllerAdvice), Profiles and configuration,
  Bean validation, Async operations

  '
knowledge:
- none
name: developing-spring-boot
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---
# Spring Boot Development

Spring Boot 3+ project setup (Initializr), REST controllers, Service layer patterns, Exception handling (@ControllerAdvice), Profiles and configuration, Bean validation, Async operations

Build production Spring Boot applications using REST controllers, service layer patterns, exception handling, configuration management, and async operations.

## Process

1. **Project Setup** – Use Spring Initializr or `scripts/scaffold.py --name myapp --group-id com.example`.
2. **REST Controllers** – Create `@RestController` with HTTP methods, constructor injection, DTOs.
3. **Service Layer** – Implement `@Service` with `@Transactional(readOnly = true)` for reads, `@Transactional` for writes.
4. **Exception Handling** – Add `@RestControllerAdvice` with handlers for domain exceptions, `MethodArgumentNotValidException`, `ConstraintViolationException`, and generic `Exception`.
5. **Configuration** – Use `application.yml` with profiles (`dev`, `prod`), `@ConfigurationProperties` for type-safe config.
6. **Bean Validation** – Add `@Valid` on request bodies, use `@NotBlank`, `@NotNull`, `@Size`, etc. on DTOs.
7. **Async** – Use `@EnableAsync` and `@Async` for long-running operations.

## Best Practices

- Use constructor injection instead of field injection
- Use `@Transactional(readOnly = true)` for read operations
- Use DTOs for API requests/responses (never expose entities)
- Implement `@ControllerAdvice` for global exception handling
- Use Bean Validation for input validation
- Configure profiles for different environments
- Use `@Async` for long-running operations
- Follow RESTful conventions, use `ResponseEntity` for proper HTTP status codes

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Field injection with `@Autowired` | Use constructor injection |
| Exposing entities directly | Use DTOs |
| Missing `@Transactional` on writes | Add `@Transactional` |
| Synchronous blocking operations | Use `@Async` |
| Hardcoded configuration | Use `@ConfigurationProperties` |
| No exception handling | Implement `@ControllerAdvice` |
| Missing validation | Add Bean Validation |
| Not using `readOnly = true` on reads | Add to read methods |

## Bundled Resources

| Resource | Purpose |
|----------|---------|
| [Installation Guide](../../../docs/setup/installation.md) | 5-minute guide: Setup and run |
| [scripts/utils.py](scripts/utils.py) | Project utilities |
| [scripts/validate.py](scripts/validate.py) | Verify project follows skill patterns |
| [examples/rest_api/](examples/rest_api/) | REST API example and run instructions |

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
