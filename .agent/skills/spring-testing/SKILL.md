---
description: JUnit 5 patterns, Spring Boot Test slices (@WebMvcTest, @DataJpaTest),
  MockMvc for API testing, Testcontainers for integration tests (PostgreSQL, Redis,
  Kafka), Mockito patterns, Test fixtures with @TestConfiguration
name: spring-testing
type: skill
---

# Spring Testing

JUnit 5 patterns, Spring Boot Test slices (@WebMvcTest, @DataJpaTest), MockMvc for API testing, Testcontainers for integration tests (PostgreSQL, Redis, Kafka), Mockito patterns, Test fixtures with @TestConfiguration

## 
# Spring Testing Skill

Write comprehensive tests for Spring Boot applications using JUnit 5, Spring Boot Test slices, MockMvc, Testcontainers, and Mockito.

## 
# Spring Testing Skill

Write comprehensive tests for Spring Boot applications using JUnit 5, Spring Boot Test slices, MockMvc, Testcontainers, and Mockito.

## Process
### Step 1: JUnit 5 Unit Tests

Write unit tests with JUnit 5 and Mockito:

```java
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {
    
    @Mock
    private ProductRepository productRepository;
    
    @Mock
    private ProductMapper productMapper;
    
    @InjectMocks
    private ProductService productService;
    
    @Test
    void shouldFindProductById() {
        // Given
        Long productId = 1L;
        Product product = new Product();
        product.setId(productId);
        product.setName("Test Product");
        
        ProductDto dto = new ProductDto();
        dto.setId(productId);
        dto.setName("Test Product");
        
        when(productRepository.findById(productId)).thenReturn(Optional.of(product));
        when(productMapper.toDto(product)).thenReturn(dto);
        
        // When
        Optional<ProductDto> result = productService.findById(productId);
        
        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getName()).isEqualTo("Test Product");
        verify(productRepository).findById(productId);
        verify(productMapper).toDto(product);
    }
    
    @Test
    void shouldThrowExceptionWhenProductNotFound() {
        // Given
        Long productId = 999L;
        when(productRepository.findById(productId)).thenReturn(Optional.empty());
        
        // When/Then
        assertThatThrownBy(() -> productService.findById(productId)
            .orElseThrow(() -> new ProductNotFoundException(productId)))
            .isInstanceOf(ProductNotFoundException.class)
            .hasMessageContaining("Product not found");
    }
    
    @Test
    void shouldCreateProduct() {
        // Given
        CreateProductDto createDto = new CreateProductDto();
        createDto.setName("New Product");
        createDto.setPrice(BigDecimal.valueOf(99.99));
        
        Product entity = new Product();
        entity.setName("New Product");
        
        Product savedEntity = new Product();
        savedEntity.setId(1L);
        savedEntity.setName("New Product");
        
        ProductDto resultDto = new ProductDto();
        resultDto.setId(1L);
        resultDto.setName("New Product");
        
        when(productMapper.toEntity(createDto)).thenReturn(entity);
        when(productRepository.save(entity)).thenReturn(savedEntity);
        when(productMapper.toDto(savedEntity)).thenReturn(resultDto);
        
        // When
        ProductDto result = productService.create(createDto);
        
        // Then
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("New Product");
        verify(productRepository).save(entity);
    }
    
    @ParameterizedTest
    @ValueSource(strings = {"Product 1", "Product 2", "Product 3"})
    void shouldFindProductsByName(String productName) {
        // Given
        Product product = new Product();
        product.setName(productName);
        when(productRepository.findByNameContainingIgnoreCase(productName))
            .thenReturn(List.of(product));
        
        // When
        List<Product> result = productRepository.findByNameContainingIgnoreCase(productName);
        
        // Then
        assertThat(result).hasSize(1);
        assertThat(result.get(0).getName()).isEqualTo(productName);
    }
}
```

### Step 2: Spring Boot Test Slices

Use test slices for focused testing:

**@WebMvcTest for Controllers:**
```java
@WebMvcTest(ProductController.class)
class ProductControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private ProductService productService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    void shouldGetProductById() throws Exception {
        // Given
        Long productId = 1L;
        ProductDto dto = new ProductDto();
        dto.setId(productId);
        dto.setName("Test Product");
        dto.setPrice(BigDecimal.valueOf(99.99));
        
        when(productService.findById(productId)).thenReturn(Optional.of(dto));
        
        // When/Then
        mockMvc.perform(get("/api/v1/products/{id}", productId)
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(productId))
            .andExpect(jsonPath("$.name").value("Test Product"))
            .andExpect(jsonPath("$.price").value(99.99));
        
        verify(productService).findById(productId);
    }
    
    @Test
    void shouldCreateProduct() throws Exception {
        // Given
        CreateProductDto createDto = new CreateProductDto();
        createDto.setName("New Product");
        createDto.setPrice(BigDecimal.valueOf(99.99));
        
        ProductDto createdDto = new ProductDto();
        createdDto.setId(1L);
        createdDto.setName("New Product");
        createdDto.setPrice(BigDecimal.valueOf(99.99));
        
        when(productService.create(any(CreateProductDto.class))).thenReturn(createdDto);
        
        // When/Then
        mockMvc.perform(post("/api/v1/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(createDto)))
            .andExpect(status().isCreated())
            .andExpect(header().string("Location", "/api/v1/products/1"))
            .andExpect(jsonPath("$.id").value(1L))
            .andExpect(jsonPath("$.name").value("New Product"));
        
        verify(productService).create(any(CreateProductDto.class));
    }
    
    @Test
    void shouldReturnBadRequestWhenValidationFails() throws Exception {
        // Given
        CreateProductDto invalidDto = new CreateProductDto();
        // Missing required fields
        
        // When/Then
        mockMvc.perform(post("/api/v1/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidDto)))
            .andExpect(status().isBadRequest());
    }
}
```

**@DataJpaTest for Repositories:**
```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ProductRepositoryTest {
    
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private CategoryRepository categoryRepository;
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Test
    void shouldSaveAndFindProduct() {
        // Given
        Category category = new Category();
        category.setName("Electronics");
        Category savedCategory = entityManager.persistFlushFind(category);
        
        Product product = new Product();
        product.setName("Laptop");
        product.setPrice(BigDecimal.valueOf(999.99));
        product.setCategory(savedCategory);
        
        // When
        Product saved = productRepository.save(product);
        entityManager.flush();
        entityManager.clear();
        
        // Then
        Optional<Product> found = productRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Laptop");
    }
    
    @Test
    void shouldFindProductsByCategory() {
        // Given
        Category category = entityManager.persistFlushFind(new Category("Electronics"));
        Product product1 = entityManager.persistFlushFind(
            new Product("Laptop", BigDecimal.valueOf(999.99), category));
        Product product2 = entityManager.persistFlushFind(
            new Product("Phone", BigDecimal.valueOf(599.99), category));
        
        // When
        List<Product> products = productRepository.findByCategoryId(category.getId());
        
        // Then
        assertThat(products).hasSize(2);
        assertThat(products).extracting(Product::getName)
            .containsExactlyInAnyOrder("Laptop", "Phone");
    }
}
```

### Step 3: Testcontainers Integration Tests

Use Testcontainers for real database testing:

```java
@SpringBootTest
@Testcontainers
@Transactional
class ProductServiceIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Autowired
    private ProductService productService;
    
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private CategoryRepository categoryRepository;
    
    @Test
    void shouldCreateAndRetrieveProduct() {
        // Given
        Category category = new Category();
        category.setName("Electronics");
        Category savedCategory = categoryRepository.save(category);
        
        CreateProductDto dto = new CreateProductDto();
        dto.setName("Laptop");
        dto.setPrice(BigDecimal.valueOf(999.99));
        dto.setCategoryId(savedCategory.getId());
        
        // When
        ProductDto created = productService.create(dto);
        
        // Then
        assertThat(created.getId()).isNotNull();
        assertThat(created.getName()).isEqualTo("Laptop");
        
        Optional<ProductDto> found = productService.findById(created.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Laptop");
    }
    
    @Test
    void shouldUpdateProduct() {
        // Given
        Category category = categoryRepository.save(new Category("Electronics"));
        ProductDto created = productService.create(createDto("Laptop", category.getId()));
        
        UpdateProductDto updateDto = new UpdateProductDto();
        updateDto.setName("Gaming Laptop");
        updateDto.setPrice(BigDecimal.valueOf(1299.99));
        
        // When
        ProductDto updated = productService.update(created.getId(), updateDto);
        
        // Then
        assertThat(updated.getName()).isEqualTo("Gaming Laptop");
        assertThat(updated.getPrice()).isEqualByComparingTo(BigDecimal.valueOf(1299.99));
    }
}
```

### Step 4: Testcontainers with Redis

Test Redis integration:

```java
@SpringBootTest
@Testcontainers
class CacheServiceIntegrationTest {
    
    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
            .withExposedPorts(6379);
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.redis.host", redis::getHost);
        registry.add("spring.data.redis.port", redis::getFirstMappedPort);
    }
    
    @Autowired
    private CacheService cacheService;
    
    @Test
    void shouldCacheAndRetrieveValue() {
        // Given
        String key = "test-key";
        String value = "test-value";
        
        // When
        cacheService.put(key, value);
        Optional<String> retrieved = cacheService.get(key);
        
        // Then
        assertThat(retrieved).isPresent();
        assertThat(retrieved.get()).isEqualTo(value);
    }
}
```

### Step 5: Testcontainers with Kafka

Test Kafka messaging:

```java
@SpringBootTest
@Testcontainers
class ProductEventPublisherTest {
    
    @Container
    static KafkaContainer kafka = new KafkaContainer(
            DockerImageName.parse("confluentinc/cp-kafka:latest"));
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }
    
    @Autowired
    private ProductEventPublisher eventPublisher;
    
    @Autowired
    private KafkaTemplate<String, ProductEvent> kafkaTemplate;
    
    @Test
    void shouldPublishProductCreatedEvent() throws InterruptedException {
        // Given
        ProductCreatedEvent event = new ProductCreatedEvent(1L, "Laptop");
        
        // When
        eventPublisher.publishProductCreated(event);
        
        // Then
        ConsumerRecord<String, ProductCreatedEvent> record = 
            kafkaTemplate.receive("product-events", 0, 0, Duration.ofSeconds(5));
        assertThat(record).isNotNull();
        assertThat(record.value().getProductId()).isEqualTo(1L);
    }
}
```

### Step 6: Test Configuration with @TestConfiguration

Create test-specific configurations:

```java
@TestConfiguration
public class TestConfig {
    
    @Bean
    @Primary
    public ProductRepository testProductRepository() {
        return mock(ProductRepository.class);
    }
    
    @Bean
    public Clock testClock() {
        return Clock.fixed(Instant.parse("2024-01-01T00:00:00Z"), ZoneOffset.UTC);
    }
}

@SpringBootTest
@Import(TestConfig.class)
class ProductServiceWithTestConfigTest {
    
    @Autowired
    private ProductService productService;
    
    @Autowired
    private Clock clock;
    
    @Test
    void shouldUseTestClock() {
        Instant now = Instant.now(clock);
        assertThat(now).isEqualTo(Instant.parse("2024-01-01T00:00:00Z"));
    }
}
```

### Step 7: Testing Async Operations

Test async methods:

```java
@SpringBootTest
class EmailServiceTest {
    
    @Autowired
    private EmailService emailService;
    
    @Test
    void shouldSendEmailAsync() throws Exception {
        // Given
        String to = "test@example.com";
        String subject = "Test Subject";
        String body = "Test Body";
        
        // When
        CompletableFuture<Void> future = emailService.sendEmailAsync(to, subject, body);
        
        // Then
        future.get(5, TimeUnit.SECONDS);
        assertThat(future.isDone()).isTrue();
    }
}
```

```java
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {
    
    @Mock
    private ProductRepository productRepository;
    
    @Mock
    private ProductMapper productMapper;
    
    @InjectMocks
    private ProductService productService;
    
    @Test
    void shouldFindProductById() {
        // Given
        Long productId = 1L;
        Product product = new Product();
        product.setId(productId);
        product.setName("Test Product");
        
        ProductDto dto = new ProductDto();
        dto.setId(productId);
        dto.setName("Test Product");
        
        when(productRepository.findById(productId)).thenReturn(Optional.of(product));
        when(productMapper.toDto(product)).thenReturn(dto);
        
        // When
        Optional<ProductDto> result = productService.findById(productId);
        
        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getName()).isEqualTo("Test Product");
        verify(productRepository).findById(productId);
        verify(productMapper).toDto(product);
    }
    
    @Test
    void shouldThrowExceptionWhenProductNotFound() {
        // Given
        Long productId = 999L;
        when(productRepository.findById(productId)).thenReturn(Optional.empty());
        
        // When/Then
        assertThatThrownBy(() -> productService.findById(productId)
            .orElseThrow(() -> new ProductNotFoundException(productId)))
            .isInstanceOf(ProductNotFoundException.class)
            .hasMessageContaining("Product not found");
    }
    
    @Test
    void shouldCreateProduct() {
        // Given
        CreateProductDto createDto = new CreateProductDto();
        createDto.setName("New Product");
        createDto.setPrice(BigDecimal.valueOf(99.99));
        
        Product entity = new Product();
        entity.setName("New Product");
        
        Product savedEntity = new Product();
        savedEntity.setId(1L);
        savedEntity.setName("New Product");
        
        ProductDto resultDto = new ProductDto();
        resultDto.setId(1L);
        resultDto.setName("New Product");
        
        when(productMapper.toEntity(createDto)).thenReturn(entity);
        when(productRepository.save(entity)).thenReturn(savedEntity);
        when(productMapper.toDto(savedEntity)).thenReturn(resultDto);
        
        // When
        ProductDto result = productService.create(createDto);
        
        // Then
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("New Product");
        verify(productRepository).save(entity);
    }
    
    @ParameterizedTest
    @ValueSource(strings = {"Product 1", "Product 2", "Product 3"})
    void shouldFindProductsByName(String productName) {
        // Given
        Product product = new Product();
        product.setName(productName);
        when(productRepository.findByNameContainingIgnoreCase(productName))
            .thenReturn(List.of(product));
        
        // When
        List<Product> result = productRepository.findByNameContainingIgnoreCase(productName);
        
        // Then
        assertThat(result).hasSize(1);
        assertThat(result.get(0).getName()).isEqualTo(productName);
    }
}
```

```java
@WebMvcTest(ProductController.class)
class ProductControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private ProductService productService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    void shouldGetProductById() throws Exception {
        // Given
        Long productId = 1L;
        ProductDto dto = new ProductDto();
        dto.setId(productId);
        dto.setName("Test Product");
        dto.setPrice(BigDecimal.valueOf(99.99));
        
        when(productService.findById(productId)).thenReturn(Optional.of(dto));
        
        // When/Then
        mockMvc.perform(get("/api/v1/products/{id}", productId)
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(productId))
            .andExpect(jsonPath("$.name").value("Test Product"))
            .andExpect(jsonPath("$.price").value(99.99));
        
        verify(productService).findById(productId);
    }
    
    @Test
    void shouldCreateProduct() throws Exception {
        // Given
        CreateProductDto createDto = new CreateProductDto();
        createDto.setName("New Product");
        createDto.setPrice(BigDecimal.valueOf(99.99));
        
        ProductDto createdDto = new ProductDto();
        createdDto.setId(1L);
        createdDto.setName("New Product");
        createdDto.setPrice(BigDecimal.valueOf(99.99));
        
        when(productService.create(any(CreateProductDto.class))).thenReturn(createdDto);
        
        // When/Then
        mockMvc.perform(post("/api/v1/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(createDto)))
            .andExpect(status().isCreated())
            .andExpect(header().string("Location", "/api/v1/products/1"))
            .andExpect(jsonPath("$.id").value(1L))
            .andExpect(jsonPath("$.name").value("New Product"));
        
        verify(productService).create(any(CreateProductDto.class));
    }
    
    @Test
    void shouldReturnBadRequestWhenValidationFails() throws Exception {
        // Given
        CreateProductDto invalidDto = new CreateProductDto();
        // Missing required fields
        
        // When/Then
        mockMvc.perform(post("/api/v1/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidDto)))
            .andExpect(status().isBadRequest());
    }
}
```

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ProductRepositoryTest {
    
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private CategoryRepository categoryRepository;
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Test
    void shouldSaveAndFindProduct() {
        // Given
        Category category = new Category();
        category.setName("Electronics");
        Category savedCategory = entityManager.persistFlushFind(category);
        
        Product product = new Product();
        product.setName("Laptop");
        product.setPrice(BigDecimal.valueOf(999.99));
        product.setCategory(savedCategory);
        
        // When
        Product saved = productRepository.save(product);
        entityManager.flush();
        entityManager.clear();
        
        // Then
        Optional<Product> found = productRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Laptop");
    }
    
    @Test
    void shouldFindProductsByCategory() {
        // Given
        Category category = entityManager.persistFlushFind(new Category("Electronics"));
        Product product1 = entityManager.persistFlushFind(
            new Product("Laptop", BigDecimal.valueOf(999.99), category));
        Product product2 = entityManager.persistFlushFind(
            new Product("Phone", BigDecimal.valueOf(599.99), category));
        
        // When
        List<Product> products = productRepository.findByCategoryId(category.getId());
        
        // Then
        assertThat(products).hasSize(2);
        assertThat(products).extracting(Product::getName)
            .containsExactlyInAnyOrder("Laptop", "Phone");
    }
}
```

```java
@SpringBootTest
@Testcontainers
@Transactional
class ProductServiceIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Autowired
    private ProductService productService;
    
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private CategoryRepository categoryRepository;
    
    @Test
    void shouldCreateAndRetrieveProduct() {
        // Given
        Category category = new Category();
        category.setName("Electronics");
        Category savedCategory = categoryRepository.save(category);
        
        CreateProductDto dto = new CreateProductDto();
        dto.setName("Laptop");
        dto.setPrice(BigDecimal.valueOf(999.99));
        dto.setCategoryId(savedCategory.getId());
        
        // When
        ProductDto created = productService.create(dto);
        
        // Then
        assertThat(created.getId()).isNotNull();
        assertThat(created.getName()).isEqualTo("Laptop");
        
        Optional<ProductDto> found = productService.findById(created.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Laptop");
    }
    
    @Test
    void shouldUpdateProduct() {
        // Given
        Category category = categoryRepository.save(new Category("Electronics"));
        ProductDto created = productService.create(createDto("Laptop", category.getId()));
        
        UpdateProductDto updateDto = new UpdateProductDto();
        updateDto.setName("Gaming Laptop");
        updateDto.setPrice(BigDecimal.valueOf(1299.99));
        
        // When
        ProductDto updated = productService.update(created.getId(), updateDto);
        
        // Then
        assertThat(updated.getName()).isEqualTo("Gaming Laptop");
        assertThat(updated.getPrice()).isEqualByComparingTo(BigDecimal.valueOf(1299.99));
    }
}
```

```java
@SpringBootTest
@Testcontainers
class CacheServiceIntegrationTest {
    
    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
            .withExposedPorts(6379);
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.redis.host", redis::getHost);
        registry.add("spring.data.redis.port", redis::getFirstMappedPort);
    }
    
    @Autowired
    private CacheService cacheService;
    
    @Test
    void shouldCacheAndRetrieveValue() {
        // Given
        String key = "test-key";
        String value = "test-value";
        
        // When
        cacheService.put(key, value);
        Optional<String> retrieved = cacheService.get(key);
        
        // Then
        assertThat(retrieved).isPresent();
        assertThat(retrieved.get()).isEqualTo(value);
    }
}
```

```java
@SpringBootTest
@Testcontainers
class ProductEventPublisherTest {
    
    @Container
    static KafkaContainer kafka = new KafkaContainer(
            DockerImageName.parse("confluentinc/cp-kafka:latest"));
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }
    
    @Autowired
    private ProductEventPublisher eventPublisher;
    
    @Autowired
    private KafkaTemplate<String, ProductEvent> kafkaTemplate;
    
    @Test
    void shouldPublishProductCreatedEvent() throws InterruptedException {
        // Given
        ProductCreatedEvent event = new ProductCreatedEvent(1L, "Laptop");
        
        // When
        eventPublisher.publishProductCreated(event);
        
        // Then
        ConsumerRecord<String, ProductCreatedEvent> record = 
            kafkaTemplate.receive("product-events", 0, 0, Duration.ofSeconds(5));
        assertThat(record).isNotNull();
        assertThat(record.value().getProductId()).isEqualTo(1L);
    }
}
```

```java
@TestConfiguration
public class TestConfig {
    
    @Bean
    @Primary
    public ProductRepository testProductRepository() {
        return mock(ProductRepository.class);
    }
    
    @Bean
    public Clock testClock() {
        return Clock.fixed(Instant.parse("2024-01-01T00:00:00Z"), ZoneOffset.UTC);
    }
}

@SpringBootTest
@Import(TestConfig.class)
class ProductServiceWithTestConfigTest {
    
    @Autowired
    private ProductService productService;
    
    @Autowired
    private Clock clock;
    
    @Test
    void shouldUseTestClock() {
        Instant now = Instant.now(clock);
        assertThat(now).isEqualTo(Instant.parse("2024-01-01T00:00:00Z"));
    }
}
```

```java
@SpringBootTest
class EmailServiceTest {
    
    @Autowired
    private EmailService emailService;
    
    @Test
    void shouldSendEmailAsync() throws Exception {
        // Given
        String to = "test@example.com";
        String subject = "Test Subject";
        String body = "Test Body";
        
        // When
        CompletableFuture<Void> future = emailService.sendEmailAsync(to, subject, body);
        
        // Then
        future.get(5, TimeUnit.SECONDS);
        assertThat(future.isDone()).isTrue();
    }
}
```

## Best Practices
- Use `@WebMvcTest` for controller tests (faster, focused)
- Use `@DataJpaTest` for repository tests
- Use `@SpringBootTest` with Testcontainers for integration tests
- Use `@MockBean` for Spring beans in slice tests
- Use `@Mock` and `@InjectMocks` for unit tests
- Use Testcontainers for real database testing
- Use `@Transactional` in integration tests for cleanup
- Use `@DynamicPropertySource` for Testcontainers configuration
- Use `@ParameterizedTest` for testing multiple inputs
- Use AssertJ for fluent assertions
- Use `@TestConfiguration` for test-specific beans
- Mock external dependencies
- Test both success and failure scenarios
- Use descriptive test method names

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Using `@SpringBootTest` for unit tests | Use `@ExtendWith(MockitoExtension.class)` |
| Not using Testcontainers | Use Testcontainers for integration tests |
| Testing implementation details | Test behavior, not implementation |
| Shared test data | Use `@BeforeEach` or test fixtures |
| Not cleaning up | Use `@Transactional` or `@DirtiesContext` |
| Hardcoded test data | Use builders or factories |

## Related
- Knowledge: `knowledge/testcontainers-patterns.json`
- Skill: `spring-boot-development` for application code
- Skill: `jpa-patterns` for repository testing

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: testcontainers-patterns.json
