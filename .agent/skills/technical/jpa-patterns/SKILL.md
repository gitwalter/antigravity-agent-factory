---
description: JPA entity design (relationships, inheritance, embedded), Spring Data
  JPA repositories (derived queries, @Query, Specifications), Transaction management,
  N+1 query prevention (EntityGraph, JOIN FETCH), Auditing, Flyway/Liquibase migrations
name: jpa-patterns
type: skill
---
# Jpa Patterns

JPA entity design (relationships, inheritance, embedded), Spring Data JPA repositories (derived queries, @Query, Specifications), Transaction management, N+1 query prevention (EntityGraph, JOIN FETCH), Auditing, Flyway/Liquibase migrations

Implement production-ready JPA data access layers using Spring Data JPA with proper entity design, repository patterns, transaction management, and query optimization.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: JPA Entity Design

Create entities with proper relationships:

```java
@Entity
@Table(name = "products", indexes = {
    @Index(name = "idx_product_name", columnList = "name"),
    @Index(name = "idx_product_category", columnList = "category_id")
})
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal price;

    @Column(length = 1000)
    private String description;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id", nullable = false)
    private Category category;

    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> orderItems = new ArrayList<>();

    @Embedded
    private AuditInfo auditInfo;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ProductStatus status = ProductStatus.ACTIVE;

    @Version
    private Long version;

    // Constructors, getters, setters

    public void addOrderItem(OrderItem item) {
        orderItems.add(item);
        item.setProduct(this);
    }

    public void removeOrderItem(OrderItem item) {
        orderItems.remove(item);
        item.setProduct(null);
    }
}

@Entity
@Table(name = "categories")
public class Category {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String name;

    @OneToMany(mappedBy = "category", fetch = FetchType.LAZY)
    private List<Product> products = new ArrayList<>();

    // Constructors, getters, setters
}

@Embeddable
public class AuditInfo {

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "created_by", length = 50)
    private String createdBy;

    @Column(name = "updated_by", length = 50)
    private String updatedBy;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    // Getters and setters
}
```

### Step 2: Spring Data JPA Repositories

Create repository interfaces with derived queries:

```java
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    // Derived query methods
    List<Product> findByNameContainingIgnoreCase(String name);

    List<Product> findByPriceBetween(BigDecimal minPrice, BigDecimal maxPrice);

    Optional<Product> findBySku(String sku);

    @Query("SELECT p FROM Product p WHERE p.category.id = :categoryId")
    List<Product> findByCategoryId(@Param("categoryId") Long categoryId);

    @Query("SELECT p FROM Product p WHERE p.status = :status ORDER BY p.name")
    List<Product> findByStatusOrderByName(@Param("status") ProductStatus status);

    @Query(value = "SELECT * FROM products WHERE price > :minPrice", nativeQuery = true)
    List<Product> findExpensiveProducts(@Param("minPrice") BigDecimal minPrice);

    @Modifying
    @Query("UPDATE Product p SET p.status = :status WHERE p.id = :id")
    int updateProductStatus(@Param("id") Long id, @Param("status") ProductStatus status);

    @Modifying
    @Query("DELETE FROM Product p WHERE p.status = :status")
    int deleteByStatus(@Param("status") ProductStatus status);

    // Using Specifications for dynamic queries
    List<Product> findAll(Specification<Product> spec);

    Page<Product> findAll(Specification<Product> spec, Pageable pageable);

    // Using EntityGraph to prevent N+1
    @EntityGraph(attributePaths = {"category"})
    Optional<Product> findById(Long id);

    @EntityGraph(attributePaths = {"category", "orderItems"})
    List<Product> findAll();
}
```

### Step 3: Specifications for Dynamic Queries

Implement dynamic query building:

```java
public class ProductSpecifications {

    public static Specification<Product> hasName(String name) {
        return (root, query, cb) ->
            name == null ? null :
            cb.like(cb.lower(root.get("name")), "%" + name.toLowerCase() + "%");
    }

    public static Specification<Product> hasCategory(Long categoryId) {
        return (root, query, cb) ->
            categoryId == null ? null :
            cb.equal(root.get("category").get("id"), categoryId);
    }

    public static Specification<Product> hasPriceBetween(BigDecimal minPrice, BigDecimal maxPrice) {
        return (root, query, cb) -> {
            if (minPrice == null && maxPrice == null) return null;
            if (minPrice == null) return cb.lessThanOrEqualTo(root.get("price"), maxPrice);
            if (maxPrice == null) return cb.greaterThanOrEqualTo(root.get("price"), minPrice);
            return cb.between(root.get("price"), minPrice, maxPrice);
        };
    }

    public static Specification<Product> hasStatus(ProductStatus status) {
        return (root, query, cb) ->
            status == null ? null :
            cb.equal(root.get("status"), status);
    }
}

// Usage
@Service
public class ProductService {

    private final ProductRepository productRepository;

    public List<ProductDto> searchProducts(ProductSearchCriteria criteria) {
        Specification<Product> spec = Specification.where(null);

        if (criteria.getName() != null) {
            spec = spec.and(ProductSpecifications.hasName(criteria.getName()));
        }
        if (criteria.getCategoryId() != null) {
            spec = spec.and(ProductSpecifications.hasCategory(criteria.getCategoryId()));
        }
        if (criteria.getMinPrice() != null || criteria.getMaxPrice() != null) {
            spec = spec.and(ProductSpecifications.hasPriceBetween(
                criteria.getMinPrice(), criteria.getMaxPrice()));
        }
        if (criteria.getStatus() != null) {
            spec = spec.and(ProductSpecifications.hasStatus(criteria.getStatus()));
        }

        return productRepository.findAll(spec)
            .stream()
            .map(productMapper::toDto)
            .toList();
    }
}
```

### Step 4: Transaction Management

Proper transaction boundaries:

```java
@Service
@Transactional(readOnly = true)
public class ProductService {

    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;

    // Read-only transaction (default)
    public Optional<ProductDto> findById(Long id) {
        return productRepository.findById(id)
            .map(productMapper::toDto);
    }

    // Write transaction (overrides class-level)
    @Transactional
    public ProductDto create(CreateProductDto dto) {
        Category category = categoryRepository.findById(dto.getCategoryId())
            .orElseThrow(() -> new CategoryNotFoundException(dto.getCategoryId()));

        Product product = productMapper.toEntity(dto);
        product.setCategory(category);

        return productMapper.toDto(productRepository.save(product));
    }

    // Transaction with isolation level
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public ProductDto updatePrice(Long id, BigDecimal newPrice) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));

        product.setPrice(newPrice);
        return productMapper.toDto(productRepository.save(product));
    }

    // Transaction with propagation
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logProductAccess(Long productId) {
        // This runs in a separate transaction
        auditLogRepository.save(new AuditLog("PRODUCT_ACCESS", productId));
    }
}
```

### Step 5: Preventing N+1 Query Problems

Use EntityGraph and JOIN FETCH:

```java
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    // Using @EntityGraph
    @EntityGraph(attributePaths = {"category"})
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithCategory(@Param("id") Long id);

    @EntityGraph(attributePaths = {"category", "orderItems"})
    List<Product> findAll();

    // Using JOIN FETCH in @Query
    @Query("SELECT p FROM Product p JOIN FETCH p.category WHERE p.status = :status")
    List<Product> findByStatusWithCategory(@Param("status") ProductStatus status);

    @Query("SELECT DISTINCT p FROM Product p " +
           "LEFT JOIN FETCH p.category " +
           "LEFT JOIN FETCH p.orderItems " +
           "WHERE p.id IN :ids")
    List<Product> findByIdsWithRelations(@Param("ids") List<Long> ids);
}

// Custom repository implementation
@Repository
public class ProductRepositoryImpl implements ProductRepositoryCustom {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public List<Product> findAllWithRelations() {
        return entityManager.createQuery(
            "SELECT DISTINCT p FROM Product p " +
            "LEFT JOIN FETCH p.category " +
            "LEFT JOIN FETCH p.orderItems o " +
            "LEFT JOIN FETCH o.order",
            Product.class)
            .getResultList();
    }
}
```

### Step 6: JPA Auditing

Enable auditing with `@CreatedDate` and `@LastModifiedDate`:

```java
@Configuration
@EnableJpaAuditing
public class JpaAuditingConfig {

    @Bean
    public AuditorAware<String> auditorProvider() {
        return new SpringSecurityAuditorAware();
    }
}

@Entity
@EntityListeners(AuditingEntityListener.class)
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @CreatedBy
    @Column(length = 50, updatable = false)
    private String createdBy;

    @LastModifiedBy
    @Column(length = 50)
    private String lastModifiedBy;

    // Other fields...
}

public class SpringSecurityAuditorAware implements AuditorAware<String> {

    @Override
    public Optional<String> getCurrentAuditor() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated()) {
            return Optional.of("system");
        }
        return Optional.of(authentication.getName());
    }
}
```

### Step 7: Database Migrations with Flyway

Configure Flyway for database migrations:

**pom.xml:**
```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-database-postgresql</artifactId>
</dependency>
```

**application.yml:**
```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
    validate-on-migrate: true
```

**Migration files:**

`db/migration/V1__Create_products_table.sql`:
```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description VARCHAR(1000),
    category_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    version BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    CONSTRAINT fk_product_category FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE INDEX idx_product_name ON products(name);
CREATE INDEX idx_product_category ON products(category_id);
```

`db/migration/V2__Add_sku_to_products.sql`:
```sql
ALTER TABLE products ADD COLUMN sku VARCHAR(20);
CREATE UNIQUE INDEX idx_product_sku ON products(sku);
```

## Best Practices

- Use `FetchType.LAZY` for `@ManyToOne` and `@OneToMany` relationships
- Use `@EntityGraph` or `JOIN FETCH` to prevent N+1 queries
- Always use `@Transactional(readOnly = true)` for read operations
- Use `@Version` for optimistic locking
- Implement proper equals/hashCode for entities (use business key)
- Use `@Embedded` for value objects
- Use Specifications for dynamic queries
- Configure proper cascade types (`CascadeType.ALL`, `orphanRemoval`)
- Use database migrations (Flyway/Liquibase) instead of `ddl-auto`
- Implement auditing with `@CreatedDate` and `@LastModifiedDate`
- Use `@Modifying` with `@Query` for bulk operations
- Avoid `SELECT *` - specify needed fields
- Use pagination for large result sets

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| N+1 queries | Use `@EntityGraph` or `JOIN FETCH` |
| Missing `@Transactional` | Add transaction boundaries |
| Eager fetching everywhere | Use lazy loading with fetch joins |
| Exposing entities directly | Use DTOs |
| No pagination | Use `Pageable` |
| `ddl-auto=update` in production | Use Flyway/Liquibase |
| Missing `@Version` | Add optimistic locking |
| Fetching all data | Use projections or DTOs |

## Related

- Knowledge: `{directories.knowledge}/spring-patterns.json`
- Skill: `spring-boot-development` for service layer
- Skill: `spring-testing` for testing repositories

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
