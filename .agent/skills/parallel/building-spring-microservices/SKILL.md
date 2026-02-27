---
agents:
- none
category: parallel
description: Spring Cloud microservices patterns with gateway, discovery, and resilience
knowledge:
- none
name: building-spring-microservices
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Spring Microservices

Spring Cloud microservices patterns with gateway, discovery, and resilience

Build distributed microservices architectures using Spring Cloud Gateway, service discovery, configuration management, and resilience patterns.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Spring Cloud Gateway

Configure API Gateway for routing and cross-cutting concerns:

```java
// GatewayApplication.java
@SpringBootApplication
public class GatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}

// application.yml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=1
            - name: CircuitBreaker
              args:
                name: orderServiceCircuitBreaker
                fallbackUri: forward:/fallback/orders

// GatewayConfig.java
@Configuration
public class GatewayConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r
                .path("/api/users/**")
                .filters(f -> f
                    .addRequestHeader("X-Gateway-Request", "true")
                    .retry(retryConfig -> retryConfig
                        .setRetries(3)
                        .setMethods(HttpMethod.GET)
                        .setBackoff(Duration.ofMillis(100), Duration.ofSeconds(2), 2, false)
                    )
                )
                .uri("lb://user-service"))
            .build();
    }

    @Bean
    public GlobalFilter customGlobalFilter() {
        return (exchange, chain) -> {
            ServerHttpRequest request = exchange.getRequest();
            ServerHttpRequest modifiedRequest = request.mutate()
                .header("X-Gateway-Timestamp", String.valueOf(System.currentTimeMillis()))
                .build();
            return chain.filter(exchange.mutate().request(modifiedRequest).build());
        };
    }
}
```

### Step 2: Service Discovery with Eureka

Set up Eureka server and client registration:

```java
// EurekaServerApplication.java
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}

// eureka-server application.yml
server:
  port: 8761
eureka:
  instance:
    hostname: localhost
  client:
    register-with-eureka: false
    fetch-registry: false

// UserServiceApplication.java (Client)
@SpringBootApplication
@EnableEurekaClient
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}

// user-service application.yml
spring:
  application:
    name: user-service
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
```

### Step 3: Config Server

Centralized configuration management:

```java
// ConfigServerApplication.java
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}

// config-server application.yml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/org/config-repo
          search-paths: '{application}'
          clone-on-start: true

// Client application.yml
spring:
  cloud:
    config:
      uri: http://localhost:8888
      name: user-service
      profile: dev
```

### Step 4: Circuit Breaker with Resilience4j

Implement circuit breaker pattern:

```java
// UserServiceClient.java
@Service
public class UserServiceClient {

    private final RestTemplate restTemplate;
    private final CircuitBreaker circuitBreaker;

    public UserServiceClient(RestTemplate restTemplate, CircuitBreakerRegistry circuitBreakerRegistry) {
        this.restTemplate = restTemplate;
        this.circuitBreaker = circuitBreakerRegistry.circuitBreaker("userService");
    }

    @CircuitBreaker(name = "userService", fallbackMethod = "getUserFallback")
    public User getUser(Long id) {
        return circuitBreaker.executeSupplier(() ->
            restTemplate.getForObject("http://user-service/api/users/{id}", User.class, id)
        );
    }

    public User getUserFallback(Long id, Exception ex) {
        return User.builder()
            .id(id)
            .name("Fallback User")
            .email("fallback@example.com")
            .build();
    }
}

// Resilience4jConfig.java
@Configuration
public class Resilience4jConfig {

    @Bean
    public CircuitBreakerRegistry circuitBreakerRegistry() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            .failureRateThreshold(50)
            .waitDurationInOpenState(Duration.ofMillis(1000))
            .slidingWindowSize(10)
            .build();

        return CircuitBreakerRegistry.of(config);
    }

    @Bean
    public TimeLimiterRegistry timeLimiterRegistry() {
        return TimeLimiterRegistry.of(TimeLimiterConfig.custom()
            .timeoutDuration(Duration.ofSeconds(3))
            .build());
    }
}
```

### Step 5: Distributed Tracing

Set up Micrometer Tracing with Zipkin:

```java
// pom.xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-brave</artifactId>
</dependency>
<dependency>
    <groupId>io.zipkin.reporter2</groupId>
    <artifactId>zipkin-reporter-brave</artifactId>
</dependency>

// application.yml
management:
  tracing:
    sampling:
      probability: 1.0
  zipkin:
    tracing:
      endpoint: http://localhost:9411/api/v2/spans

// TracingConfig.java
@Configuration
public class TracingConfig {

    @Bean
    public Sender sender() {
        return OkHttpSender.create("http://localhost:9411/api/v2/spans");
    }

    @Bean
    public AsyncReporter<Span> spanReporter() {
        return AsyncReporter.create(sender());
    }
}
```

### Step 6: Event-Driven with Spring Cloud Stream

Implement event-driven microservices:

```java
// OrderService.java
@Service
public class OrderService {

    private final StreamBridge streamBridge;

    public OrderService(StreamBridge streamBridge) {
        this.streamBridge = streamBridge;
    }

    public void createOrder(Order order) {
        // Process order
        orderRepository.save(order);

        // Publish event
        streamBridge.send("orderCreated-out-0", OrderCreatedEvent.builder()
            .orderId(order.getId())
            .userId(order.getUserId())
            .totalAmount(order.getTotalAmount())
            .timestamp(Instant.now())
            .build());
    }
}

// NotificationService.java
@SpringBootApplication
@EnableBinding(Sink.class)
public class NotificationService {

    @StreamListener(Sink.INPUT)
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Send notification
        notificationService.sendEmail(event.getUserId(),
            "Order " + event.getOrderId() + " created");
    }
}

// application.yml
spring:
  cloud:
    stream:
      bindings:
        orderCreated-out-0:
          destination: order-created
          binder: kafka
        input:
          destination: order-created
          group: notification-service
      kafka:
        binder:
          brokers: localhost:9092
```

## Output

- Microservices with service discovery integration
- API Gateway with routing and filtering
- Centralized configuration server
- Circuit breaker implementations
- Distributed tracing setup
- Event-driven communication patterns

## Best Practices

- Use API Gateway for single entry point and cross-cutting concerns
- Implement service discovery for dynamic service location
- Use Config Server for centralized configuration management
- Apply circuit breakers to prevent cascading failures
- Implement distributed tracing for observability
- Use event-driven patterns for loose coupling
- Implement retry logic with exponential backoff
- Use rate limiting to protect services
- Monitor service health with health checks
- Implement graceful degradation with fallbacks

## Related

- Knowledge: `{directories.knowledge}/spring-microservices-patterns.json`
- Skill: `developing-spring-boot` for service implementation
- Skill: `observing-spring-apps` for monitoring and metrics

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
