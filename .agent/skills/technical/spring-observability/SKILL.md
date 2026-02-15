---
description: Micrometer metrics (counters, gauges, timers), Distributed tracing with
  Micrometer Tracing + Zipkin/Jaeger, Structured logging (Logback + JSON), Spring
  Boot Actuator endpoints, Prometheus + Grafana setup, Custom health indicators
name: spring-observability
type: skill
---
# Spring Observability

Micrometer metrics (counters, gauges, timers), Distributed tracing with Micrometer Tracing + Zipkin/Jaeger, Structured logging (Logback + JSON), Spring Boot Actuator endpoints, Prometheus + Grafana setup, Custom health indicators

Implement comprehensive observability for Spring Boot applications using Micrometer metrics, distributed tracing, structured logging, and health monitoring.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Micrometer Metrics

Implement custom metrics:

```java
@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final MeterRegistry meterRegistry;
    private final Counter productCreatedCounter;
    private final Timer productQueryTimer;
    private final Gauge productCountGauge;

    public ProductService(ProductRepository productRepository,
                         MeterRegistry meterRegistry) {
        this.productRepository = productRepository;
        this.meterRegistry = meterRegistry;

        // Counter for product creation
        this.productCreatedCounter = Counter.builder("products.created")
            .description("Total number of products created")
            .tag("service", "product-service")
            .register(meterRegistry);

        // Timer for query operations
        this.productQueryTimer = Timer.builder("products.query.duration")
            .description("Time taken to query products")
            .tag("service", "product-service")
            .register(meterRegistry);

        // Gauge for current product count
        this.productCountGauge = Gauge.builder("products.count",
            productRepository, ProductRepository::count)
            .description("Current number of products")
            .register(meterRegistry);
    }

    @Transactional
    public ProductDto create(CreateProductDto dto) {
        Product product = productMapper.toEntity(dto);
        Product saved = productRepository.save(product);

        // Increment counter
        productCreatedCounter.increment(
            Tags.of("category", saved.getCategory().getName()));

        return productMapper.toDto(saved);
    }

    public List<ProductDto> findAll(int page, int size) {
        // Measure query time
        return productQueryTimer.recordCallable(() -> {
            Pageable pageable = PageRequest.of(page, size);
            return productRepository.findAll(pageable)
                .stream()
                .map(productMapper::toDto)
                .toList();
        });
    }
}

// Using @Timed annotation
@RestController
public class ProductController {

    @GetMapping("/products")
    @Timed(value = "products.list", description = "Time to list products")
    public ResponseEntity<List<ProductDto>> getAllProducts() {
        // Implementation
    }

    @PostMapping("/products")
    @Timed(value = "products.create", description = "Time to create product")
    @Counted(value = "products.create.requests", description = "Product creation requests")
    public ResponseEntity<ProductDto> createProduct(@RequestBody CreateProductDto dto) {
        // Implementation
    }
}
```

### Step 2: Distributed Tracing

Configure distributed tracing with Micrometer Tracing:

**Dependencies:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-brave</artifactId>
</dependency>
<dependency>
    <groupId>io.zipkin.reporter2</groupId>
    <artifactId>zipkin-reporter-brave</artifactId>
</dependency>
```

**Configuration:**
```yaml
management:
  tracing:
    sampling:
      probability: 1.0
  zipkin:
    tracing:
      endpoint: http://localhost:9411/api/v2/spans
```

**Using Tracing:**
```java
@Service
public class ProductService {

    private final Tracer tracer;
    private final RestTemplate restTemplate;

    public ProductService(Tracer tracer, RestTemplate restTemplate) {
        this.tracer = tracer;
        this.restTemplate = restTemplate;
    }

    public ProductDto getProduct(Long id) {
        Span span = tracer.nextSpan()
            .name("get-product")
            .tag("product.id", String.valueOf(id))
            .start();

        try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
            span.event("Fetching product");
            ProductDto product = restTemplate.getForObject(
                "http://product-service/api/v1/products/{id}",
                ProductDto.class,
                id);
            span.event("Product fetched");
            return product;
        } catch (Exception e) {
            span.tag("error", true);
            span.tag("error.message", e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}

// Automatic tracing with @NewSpan
@Service
public class OrderService {

    @NewSpan("process-order")
    public OrderDto processOrder(CreateOrderDto dto) {
        // Method automatically traced
    }

    @ContinueSpan(log = "validate-order")
    public void validateOrder(@SpanTag("order.id") Long orderId) {
        // Continue existing span
    }
}
```

### Step 3: Structured Logging

Configure JSON logging with Logback:

**logback-spring.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>

    <springProfile name="prod">
        <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
            <encoder class="net.logstash.logback.encoder.LogstashEncoder">
                <includeCallerData>true</includeCallerData>
                <customFields>{"service":"product-service","environment":"prod"}</customFields>
            </encoder>
        </appender>

        <root level="INFO">
            <appender-ref ref="JSON"/>
        </root>
    </springProfile>

    <springProfile name="dev">
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{yyyy-MM-dd HH:mm:ss} - %msg%n</pattern>
            </encoder>
        </appender>

        <root level="DEBUG">
            <appender-ref ref="CONSOLE"/>
        </root>
    </springProfile>
</configuration>
```

**Using Structured Logging:**
```java
@RestController
@Slf4j
public class ProductController {

    @GetMapping("/products/{id}")
    public ResponseEntity<ProductDto> getProduct(@PathVariable Long id) {
        MDC.put("productId", String.valueOf(id));
        MDC.put("operation", "getProduct");

        log.info("Fetching product",
            kv("productId", id),
            kv("timestamp", Instant.now()));

        try {
            ProductDto product = productService.findById(id)
                .orElseThrow(() -> new ProductNotFoundException(id));

            log.info("Product fetched successfully",
                kv("productId", id),
                kv("productName", product.getName()));

            return ResponseEntity.ok(product);
        } catch (ProductNotFoundException e) {
            log.warn("Product not found",
                kv("productId", id),
                kv("error", e.getMessage()));
            throw e;
        } finally {
            MDC.clear();
        }
    }
}
```

### Step 4: Spring Boot Actuator

Configure Actuator endpoints:

**application.yml:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env,loggers
      base-path: /actuator
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
    metrics:
      enabled: true
    prometheus:
      enabled: true
  health:
    probes:
      enabled: true
    livenessState:
      enabled: true
    readinessState:
      enabled: true
  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: ${spring.application.name}
      environment: ${spring.profiles.active}
```

**Custom Info Endpoint:**
```java
@Component
public class CustomInfoContributor implements InfoContributor {

    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("app", Map.of(
            "name", "Product Service",
            "version", "1.0.0",
            "buildTime", Instant.now().toString()
        ));
    }
}
```

### Step 5: Custom Health Indicators

Create custom health checks:

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    private final DataSource dataSource;

    public DatabaseHealthIndicator(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Health health() {
        try (Connection connection = dataSource.getConnection()) {
            if (connection.isValid(1)) {
                return Health.up()
                    .withDetail("database", "PostgreSQL")
                    .withDetail("status", "Available")
                    .build();
            }
        } catch (SQLException e) {
            return Health.down()
                .withDetail("database", "PostgreSQL")
                .withDetail("error", e.getMessage())
                .withException(e)
                .build();
        }
        return Health.down().build();
    }
}

@Component
public class ExternalServiceHealthIndicator implements HealthIndicator {

    private final RestTemplate restTemplate;

    public ExternalServiceHealthIndicator(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Override
    public Health health() {
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(
                "http://external-service/health",
                String.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                return Health.up()
                    .withDetail("external-service", "Available")
                    .build();
            }
        } catch (Exception e) {
            return Health.down()
                .withDetail("external-service", "Unavailable")
                .withException(e)
                .build();
        }
        return Health.down().build();
    }
}
```

### Step 6: Prometheus + Grafana Setup

Configure Prometheus scraping:

**prometheus.yml:**
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'product-service'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['localhost:8080']
        labels:
          service: 'product-service'
          environment: 'prod'
```

**Grafana Dashboard JSON:**
```json
{
  "dashboard": {
    "title": "Product Service Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_server_requests_seconds_count[5m])",
            "legendFormat": "{{uri}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_server_requests_seconds_count{status=~'5..'}[5m])",
            "legendFormat": "5xx Errors"
          }
        ]
      },
      {
        "title": "Response Time",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_server_requests_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

- Use Micrometer for metrics (not direct Prometheus)
- Implement distributed tracing for request tracking
- Use structured logging (JSON format)
- Configure health probes for Kubernetes
- Export metrics to Prometheus
- Use correlation IDs in logs
- Create custom health indicators
- Monitor business metrics, not just technical metrics
- Set up alerting rules
- Use tags/labels consistently
- Implement SLIs and SLOs
- Use sampling for high-volume traces
- Configure log levels per environment

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No metrics | Add Micrometer metrics |
| Unstructured logs | Use JSON logging |
| Missing health checks | Configure Actuator |
| No distributed tracing | Set up Micrometer Tracing |
| Hardcoded log messages | Use structured logging |
| Missing correlation IDs | Add MDC context |

## Related

- Knowledge: `{directories.knowledge}/spring-observability-patterns.json`
- Skill: `spring-microservices` for distributed systems
- Skill: `java-containerization` for health probes

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
