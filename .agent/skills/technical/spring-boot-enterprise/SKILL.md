---
description: Tactical Blueprint for production-grade Spring Boot 3+ applications.
  Focuses on procedural execution, tool-calling sequences, and idiomatic excellence.
name: spring-boot-enterprise
type: skill
---
# Capability Manifest: Spring Boot Enterprise

This blueprint provides the **procedural truth** for engineering, testing, and deploying high-fidelity Spring Boot 3+ services in the Antigravity Agent Factory.

## Operational Environment

- **JDK**: 21 (LTS) - Mandatory usage of `records`, `sealed classes`, and `switch expressions`.
- **Build**: Maven 3.9+ (Wrapped).
- **Primary Stack**: Boot 3.4, Spring Data JPA (PostgreSQL), Spring Security (OIDC), Micrometer (OTEL).

## Process

Follow these procedures to build enterprise-grade Spring Boot applications:

### Procedure 1: Scaffolding a Service
Execute these steps in sequence to ensure standard factory hygiene:
1.  **Generate**: `mvn archetype:generate -Dfilter=antigravity-service-pattern` (or use internal `scaffold.py`).
2.  **Verify Structure**: Ensure `src/main/java` follows `com.antigravity.[domain].[service]` pattern.
3.  **Truth Check**: Validate that `pom.xml` contains the `spring-boot-starter-validation` and `spring-boot-starter-actuator`.

### Procedure 2: Implementing a Domain Feature (Red-Green-Refactor)
1.  **Red**: Create a Slice Test (e.g., `@WebMvcTest` for API or `@DataJpaTest` for Persistence). 
    - *Tool*: `mvn test -Dtest=MyFeatureTest`
2.  **Green**: Implement the service logic.
    - *Axiom Check*: Use a `record` for DTOs. Never leak Entities through the Controller.
3.  **Refactor**: Run Static Analysis.
    - *Tool*: `mvn checkstyle:check` and `mvn pmd:check`.

### Procedure 3: Resilience & Observability Setup
1.  **Add Actuator**: Ensure `/actuator/health` and `/actuator/metrics` are exposed but secured.
2.  **Configure Logging**: Use `logback-spring.xml` with JSON output for ELK/Loki.
3.  **Circuit Breakers**: Use Resilience4j for all external API calls.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| `BeanDefinitionOverrideException` | Duplicate bean names in context. | Check for `@Component` vs `@Bean` duplication in `@Configuration` classes. Use `@Primary` only as a last resort. |
| `LazyInitializationException` | Accessing proxy outside transaction. | **Never** use `spring.jpa.open-in-view=true`. Use DTO mapping within the `@Service` layer or `EntityGraph`. |
| `ConnectionTimeout` | DB Pool saturation. | Check `hikari.maximum-pool-size`. Verify all DB streams/connections are within `try-with-resources`. |

## Idiomatic Code Patterns (The Gold Standard)

### The "Truthful" Record DTO
```java
public record UserResponse(
    UUID id,
    @NotBlank String username,
    @Email String email,
    LocalDateTime createdAt
) {}
```

### The "Observable" Service
```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderService {
    private final ObservationRegistry observationRegistry;

    @Transactional
    public OrderResponse placeOrder(OrderRequest request) {
        return Observation.createNotStarted("order.place", observationRegistry)
            .observe(() -> {
                // Business logic here
                return new OrderResponse(...);
            });
    }
}
```

## Prerequisites

| Action | Command |
| :--- | :--- |
| Build & Check | `mvn clean verify` |
| Fast Test Loop | `mvn test -DskipITs` |
| Check Vulnerabilities | `mvn ossindex:audit` |
| Format Code | `mvn spotless:apply` |

## When to Use
Use this blueprint whenever building, refactoring, or debugging a Java/Spring service. It is the authoritative source for "How we build" vs "What Spring is."


## Best Practices

- Follow the system axioms (A1-A5)
- Ensure all changes are verifiable
- Document complex logic for future maintenance
