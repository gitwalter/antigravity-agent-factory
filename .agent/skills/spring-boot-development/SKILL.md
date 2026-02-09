---
description: Spring Boot 3+ project setup (Initializr), REST controllers, Service layer patterns, Exception handling (@ControllerAdvice), Profiles and configuration, Bean validation, Async operations
---

# Spring Boot Development

Spring Boot 3+ project setup (Initializr), REST controllers, Service layer patterns, Exception handling (@ControllerAdvice), Profiles and configuration, Bean validation, Async operations

## 
# Spring Boot Development Skill

Build production Spring Boot applications using REST controllers, service layer patterns, exception handling, configuration management, and async operations.

## 
# Spring Boot Development Skill

Build production Spring Boot applications using REST controllers, service layer patterns, exception handling, configuration management, and async operations.

## Process
### Step 1: Spring Boot Project Setup

Create a Spring Boot project using Spring Initializr or CLI:

```java
// Main application class
@SpringBootApplication
public class ProductServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProductServiceApplication.class, args);
    }
}
```

**pom.xml dependencies:**
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>
```

### Step 2: REST Controllers

Create REST controllers with proper HTTP methods:

```java
@RestController
@RequestMapping("/api/v1/products")
@Validated
public class ProductController {
    
    private final ProductService productService;
    private static final Logger log = LoggerFactory.getLogger(ProductController.class);
    
    // Constructor injection (preferred)
    public ProductController(ProductService productService) {
        this.productService = productService;
    }
    
    @GetMapping
    public ResponseEntity<List<ProductDto>> getAllProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        log.info("Fetching all products - page: {}, size: {}", page, size);
        List<ProductDto> products = productService.findAll(page, size);
        return ResponseEntity.ok(products);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<ProductDto> getProduct(@PathVariable Long id) {
        log.info("Fetching product with id: {}", id);
        ProductDto product = productService.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));
        return ResponseEntity.ok(product);
    }
    
    @PostMapping
    public ResponseEntity<ProductDto> createProduct(
            @Valid @RequestBody CreateProductDto dto) {
        log.info("Creating new product: {}", dto);
        ProductDto created = productService.create(dto);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .header("Location", "/api/v1/products/" + created.getId())
            .body(created);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<ProductDto> updateProduct(
            @PathVariable Long id,
            @Valid @RequestBody UpdateProductDto dto) {
        log.info("Updating product {} with data: {}", id, dto);
        ProductDto updated = productService.update(id, dto);
        return ResponseEntity.ok(updated);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        log.info("Deleting product with id: {}", id);
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Step 3: Service Layer Patterns

Implement service layer with business logic:

```java
@Service
@Transactional(readOnly = true)
public class ProductService {
    
    private final ProductRepository productRepository;
    private final ProductMapper productMapper;
    
    public ProductService(ProductRepository productRepository, 
                         ProductMapper productMapper) {
        this.productRepository = productRepository;
        this.productMapper = productMapper;
    }
    
    public List<ProductDto> findAll(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return productRepository.findAll(pageable)
            .stream()
            .map(productMapper::toDto)
            .toList();
    }
    
    public Optional<ProductDto> findById(Long id) {
        return productRepository.findById(id)
            .map(productMapper::toDto);
    }
    
    @Transactional
    public ProductDto create(CreateProductDto dto) {
        Product product = productMapper.toEntity(dto);
        Product saved = productRepository.save(product);
        return productMapper.toDto(saved);
    }
    
    @Transactional
    public ProductDto update(Long id, UpdateProductDto dto) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));
        
        productMapper.updateEntity(dto, product);
        Product updated = productRepository.save(product);
        return productMapper.toDto(updated);
    }
    
    @Transactional
    public void delete(Long id) {
        if (!productRepository.existsById(id)) {
            throw new ProductNotFoundException(id);
        }
        productRepository.deleteById(id);
    }
}
```

### Step 4: Exception Handling with @ControllerAdvice

Global exception handling:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    
    @ExceptionHandler(ProductNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleProductNotFound(
            ProductNotFoundException ex) {
        log.warn("Product not found: {}", ex.getMessage());
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.NOT_FOUND.value())
            .error("Product Not Found")
            .message(ex.getMessage())
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationErrors(
            MethodArgumentNotValidException ex) {
        log.warn("Validation errors: {}", ex.getMessage());
        Map<String, String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                FieldError::getDefaultMessage,
                (existing, replacement) -> existing));
        
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .error("Validation Failed")
            .message("Invalid input data")
            .errors(errors)
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolation(
            ConstraintViolationException ex) {
        log.warn("Constraint violation: {}", ex.getMessage());
        Map<String, String> errors = ex.getConstraintViolations()
            .stream()
            .collect(Collectors.toMap(
                v -> v.getPropertyPath().toString(),
                ConstraintViolation::getMessage));
        
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .error("Validation Failed")
            .message("Invalid input data")
            .errors(errors)
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        log.error("Unexpected error", ex);
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .error("Internal Server Error")
            .message("An unexpected error occurred")
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### Step 5: Profiles and Configuration

Configure application properties with profiles:

**application.yml:**
```yaml
spring:
  application:
    name: product-service
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

---
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:postgresql://localhost:5432/products_dev
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:postgres}
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true

logging:
  level:
    root: INFO
    com.example.productservice: DEBUG

---
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: ${DATABASE_URL}
    username: ${DATABASE_USERNAME}
    password: ${DATABASE_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false

logging:
  level:
    root: WARN
    com.example.productservice: INFO
```

**Configuration Properties:**
```java
@ConfigurationProperties(prefix = "app")
@Validated
public class ApplicationProperties {
    
    @NotBlank
    private String name;
    
    @Min(1)
    @Max(100)
    private int maxPageSize = 20;
    
    private Cache cache = new Cache();
    
    // Getters and setters
    
    public static class Cache {
        private int ttlSeconds = 300;
        private int maxSize = 1000;
        
        // Getters and setters
    }
}

// Register in configuration
@Configuration
@EnableConfigurationProperties(ApplicationProperties.class)
public class AppConfig {
}
```

### Step 6: Bean Validation

Use Bean Validation for input validation:

```java
public class CreateProductDto {
    
    @NotBlank(message = "Product name is required")
    @Size(min = 3, max = 100, message = "Name must be between 3 and 100 characters")
    private String name;
    
    @NotNull(message = "Price is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Price must be greater than 0")
    @Digits(integer = 10, fraction = 2, message = "Invalid price format")
    private BigDecimal price;
    
    @NotBlank(message = "Description is required")
    @Size(max = 1000, message = "Description must not exceed 1000 characters")
    private String description;
    
    @NotNull(message = "Category ID is required")
    @Positive(message = "Category ID must be positive")
    private Long categoryId;
    
    @Email(message = "Contact email must be valid")
    private String contactEmail;
    
    @Pattern(regexp = "^[A-Z]{2}\\d{4}$", message = "SKU must match pattern XX####")
    private String sku;
    
    // Getters and setters
}
```

### Step 7: Async Operations

Implement async operations with `@Async`:

```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
    
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> {
            LoggerFactory.getLogger(AsyncConfig.class)
                .error("Async method {} failed", method.getName(), ex);
        };
    }
}

@Service
public class EmailService {
    
    private static final Logger log = LoggerFactory.getLogger(EmailService.class);
    
    @Async
    public CompletableFuture<Void> sendEmailAsync(String to, String subject, String body) {
        log.info("Sending email to {} asynchronously", to);
        try {
            // Simulate email sending
            Thread.sleep(1000);
            log.info("Email sent successfully to {}", to);
            return CompletableFuture.completedFuture(null);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return CompletableFuture.failedFuture(e);
        }
    }
    
    @Async("taskExecutor")
    public CompletableFuture<String> processLargeFileAsync(String filePath) {
        log.info("Processing file {} asynchronously", filePath);
        // Process file
        return CompletableFuture.completedFuture("Processed: " + filePath);
    }
}

// Usage in controller
@PostMapping("/{id}/notify")
public ResponseEntity<Void> notifyProductCreated(@PathVariable Long id) {
    ProductDto product = productService.findById(id)
        .orElseThrow(() -> new ProductNotFoundException(id));
    
    emailService.sendEmailAsync(
        product.getContactEmail(),
        "Product Created",
        "Your product has been created: " + product.getName()
    );
    
    return ResponseEntity.accepted().build();
}
```

```java
// Main application class
@SpringBootApplication
public class ProductServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProductServiceApplication.class, args);
    }
}
```

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>
```

```java
@RestController
@RequestMapping("/api/v1/products")
@Validated
public class ProductController {
    
    private final ProductService productService;
    private static final Logger log = LoggerFactory.getLogger(ProductController.class);
    
    // Constructor injection (preferred)
    public ProductController(ProductService productService) {
        this.productService = productService;
    }
    
    @GetMapping
    public ResponseEntity<List<ProductDto>> getAllProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        log.info("Fetching all products - page: {}, size: {}", page, size);
        List<ProductDto> products = productService.findAll(page, size);
        return ResponseEntity.ok(products);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<ProductDto> getProduct(@PathVariable Long id) {
        log.info("Fetching product with id: {}", id);
        ProductDto product = productService.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));
        return ResponseEntity.ok(product);
    }
    
    @PostMapping
    public ResponseEntity<ProductDto> createProduct(
            @Valid @RequestBody CreateProductDto dto) {
        log.info("Creating new product: {}", dto);
        ProductDto created = productService.create(dto);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .header("Location", "/api/v1/products/" + created.getId())
            .body(created);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<ProductDto> updateProduct(
            @PathVariable Long id,
            @Valid @RequestBody UpdateProductDto dto) {
        log.info("Updating product {} with data: {}", id, dto);
        ProductDto updated = productService.update(id, dto);
        return ResponseEntity.ok(updated);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        log.info("Deleting product with id: {}", id);
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

```java
@Service
@Transactional(readOnly = true)
public class ProductService {
    
    private final ProductRepository productRepository;
    private final ProductMapper productMapper;
    
    public ProductService(ProductRepository productRepository, 
                         ProductMapper productMapper) {
        this.productRepository = productRepository;
        this.productMapper = productMapper;
    }
    
    public List<ProductDto> findAll(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return productRepository.findAll(pageable)
            .stream()
            .map(productMapper::toDto)
            .toList();
    }
    
    public Optional<ProductDto> findById(Long id) {
        return productRepository.findById(id)
            .map(productMapper::toDto);
    }
    
    @Transactional
    public ProductDto create(CreateProductDto dto) {
        Product product = productMapper.toEntity(dto);
        Product saved = productRepository.save(product);
        return productMapper.toDto(saved);
    }
    
    @Transactional
    public ProductDto update(Long id, UpdateProductDto dto) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));
        
        productMapper.updateEntity(dto, product);
        Product updated = productRepository.save(product);
        return productMapper.toDto(updated);
    }
    
    @Transactional
    public void delete(Long id) {
        if (!productRepository.existsById(id)) {
            throw new ProductNotFoundException(id);
        }
        productRepository.deleteById(id);
    }
}
```

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    
    @ExceptionHandler(ProductNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleProductNotFound(
            ProductNotFoundException ex) {
        log.warn("Product not found: {}", ex.getMessage());
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.NOT_FOUND.value())
            .error("Product Not Found")
            .message(ex.getMessage())
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationErrors(
            MethodArgumentNotValidException ex) {
        log.warn("Validation errors: {}", ex.getMessage());
        Map<String, String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                FieldError::getDefaultMessage,
                (existing, replacement) -> existing));
        
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .error("Validation Failed")
            .message("Invalid input data")
            .errors(errors)
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolation(
            ConstraintViolationException ex) {
        log.warn("Constraint violation: {}", ex.getMessage());
        Map<String, String> errors = ex.getConstraintViolations()
            .stream()
            .collect(Collectors.toMap(
                v -> v.getPropertyPath().toString(),
                ConstraintViolation::getMessage));
        
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .error("Validation Failed")
            .message("Invalid input data")
            .errors(errors)
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        log.error("Unexpected error", ex);
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .error("Internal Server Error")
            .message("An unexpected error occurred")
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

```yaml
spring:
  application:
    name: product-service
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

---
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:postgresql://localhost:5432/products_dev
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:postgres}
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true

logging:
  level:
    root: INFO
    com.example.productservice: DEBUG

---
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: ${DATABASE_URL}
    username: ${DATABASE_USERNAME}
    password: ${DATABASE_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false

logging:
  level:
    root: WARN
    com.example.productservice: INFO
```

```java
@ConfigurationProperties(prefix = "app")
@Validated
public class ApplicationProperties {
    
    @NotBlank
    private String name;
    
    @Min(1)
    @Max(100)
    private int maxPageSize = 20;
    
    private Cache cache = new Cache();
    
    // Getters and setters
    
    public static class Cache {
        private int ttlSeconds = 300;
        private int maxSize = 1000;
        
        // Getters and setters
    }
}

// Register in configuration
@Configuration
@EnableConfigurationProperties(ApplicationProperties.class)
public class AppConfig {
}
```

```java
public class CreateProductDto {
    
    @NotBlank(message = "Product name is required")
    @Size(min = 3, max = 100, message = "Name must be between 3 and 100 characters")
    private String name;
    
    @NotNull(message = "Price is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Price must be greater than 0")
    @Digits(integer = 10, fraction = 2, message = "Invalid price format")
    private BigDecimal price;
    
    @NotBlank(message = "Description is required")
    @Size(max = 1000, message = "Description must not exceed 1000 characters")
    private String description;
    
    @NotNull(message = "Category ID is required")
    @Positive(message = "Category ID must be positive")
    private Long categoryId;
    
    @Email(message = "Contact email must be valid")
    private String contactEmail;
    
    @Pattern(regexp = "^[A-Z]{2}\\d{4}$", message = "SKU must match pattern XX####")
    private String sku;
    
    // Getters and setters
}
```

```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
    
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> {
            LoggerFactory.getLogger(AsyncConfig.class)
                .error("Async method {} failed", method.getName(), ex);
        };
    }
}

@Service
public class EmailService {
    
    private static final Logger log = LoggerFactory.getLogger(EmailService.class);
    
    @Async
    public CompletableFuture<Void> sendEmailAsync(String to, String subject, String body) {
        log.info("Sending email to {} asynchronously", to);
        try {
            // Simulate email sending
            Thread.sleep(1000);
            log.info("Email sent successfully to {}", to);
            return CompletableFuture.completedFuture(null);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return CompletableFuture.failedFuture(e);
        }
    }
    
    @Async("taskExecutor")
    public CompletableFuture<String> processLargeFileAsync(String filePath) {
        log.info("Processing file {} asynchronously", filePath);
        // Process file
        return CompletableFuture.completedFuture("Processed: " + filePath);
    }
}

// Usage in controller
@PostMapping("/{id}/notify")
public ResponseEntity<Void> notifyProductCreated(@PathVariable Long id) {
    ProductDto product = productService.findById(id)
        .orElseThrow(() -> new ProductNotFoundException(id));
    
    emailService.sendEmailAsync(
        product.getContactEmail(),
        "Product Created",
        "Your product has been created: " + product.getName()
    );
    
    return ResponseEntity.accepted().build();
}
```

## Best Practices
- Use constructor injection instead of field injection
- Always use `@Transactional(readOnly = true)` for read operations
- Use DTOs for API requests/responses (never expose entities)
- Implement proper exception handling with `@ControllerAdvice`
- Use Bean Validation for input validation
- Configure profiles for different environments
- Use `@Async` for long-running operations
- Implement proper logging with SLF4J
- Use `@ConfigurationProperties` for type-safe configuration
- Follow RESTful conventions for API endpoints
- Use `ResponseEntity` for proper HTTP status codes
- Implement health checks with Actuator
- Use `@Valid` on request bodies
- Handle `Optional` properly with `orElseThrow()`

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
| Not using `readOnly = true` | Add to read methods |

## Related
- Knowledge: `knowledge/spring-patterns.json`
- Skill: `jpa-patterns` for data access
- Skill: `spring-testing` for testing

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: spring-patterns.json
