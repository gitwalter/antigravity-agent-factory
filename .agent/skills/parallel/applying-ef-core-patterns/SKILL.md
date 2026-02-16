---
description: Entity Framework Core patterns for data access, migrations, and query
  optimization
name: applying-ef-core-patterns
type: skill
---
# Ef Core Patterns

Entity Framework Core patterns for data access, migrations, and query optimization

# Entity Framework Core Patterns

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### 1. DbContext Configuration and Lifetime

```csharp
// DbContext with proper configuration
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
        // Disable change tracking for read-only scenarios
        // ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
    }

    public DbSet<Product> Products { get; set; }
    public DbSet<Category> Categories { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure entities
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(200);
            entity.HasIndex(e => e.Name);

            // Configure relationships
            entity.HasOne(e => e.Category)
                  .WithMany(c => c.Products)
                  .HasForeignKey(e => e.CategoryId)
                  .OnDelete(DeleteBehavior.Restrict);
        });

        // Seed data
        modelBuilder.Entity<Category>().HasData(
            new Category { Id = 1, Name = "Electronics" },
            new Category { Id = 2, Name = "Clothing" }
        );
    }
}

// Register in DI container (Program.cs or Startup.cs)
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        connectionString,
        sqlOptions => sqlOptions.MigrationsAssembly("YourProject.Migrations")
    ),
    ServiceLifetime.Scoped // Default: one context per request
);
```

### 2. Migrations Workflow

```csharp
// Create initial migration
// dotnet ef migrations add InitialCreate --project YourProject

// Update database
// dotnet ef database update --project YourProject

// Generate SQL script
// dotnet ef migrations script --project YourProject --output migration.sql

// Add migration programmatically
public class MigrationService
{
    private readonly ApplicationDbContext _context;

    public MigrationService(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task ApplyMigrationsAsync()
    {
        var pendingMigrations = await _context.Database.GetPendingMigrationsAsync();
        if (pendingMigrations.Any())
        {
            await _context.Database.MigrateAsync();
        }
    }

    public string GenerateMigrationScript(string fromMigration, string toMigration)
    {
        return _context.Database.GenerateCreateScript();
    }
}
```

### 3. Repository Pattern with EF Core

```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
    Task<bool> ExistsAsync(int id);
}

public class Repository<T> : IRepository<T> where T : class
{
    protected readonly ApplicationDbContext _context;
    protected readonly DbSet<T> _dbSet;

    public Repository(ApplicationDbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }

    public virtual async Task<T?> GetByIdAsync(int id)
    {
        return await _dbSet.FindAsync(id);
    }

    public virtual async Task<IEnumerable<T>> GetAllAsync()
    {
        return await _dbSet.ToListAsync();
    }

    public virtual async Task<T> AddAsync(T entity)
    {
        await _dbSet.AddAsync(entity);
        await _context.SaveChangesAsync();
        return entity;
    }

    public virtual async Task UpdateAsync(T entity)
    {
        _dbSet.Update(entity);
        await _context.SaveChangesAsync();
    }

    public virtual async Task DeleteAsync(int id)
    {
        var entity = await GetByIdAsync(id);
        if (entity != null)
        {
            _dbSet.Remove(entity);
            await _context.SaveChangesAsync();
        }
    }

    public virtual async Task<bool> ExistsAsync(int id)
    {
        return await _dbSet.FindAsync(id) != null;
    }
}

// Specific repository with custom queries
public interface IProductRepository : IRepository<Product>
{
    Task<IEnumerable<Product>> GetByCategoryAsync(int categoryId);
    Task<Product?> GetByNameAsync(string name);
}

public class ProductRepository : Repository<Product>, IProductRepository
{
    public ProductRepository(ApplicationDbContext context) : base(context) { }

    public async Task<IEnumerable<Product>> GetByCategoryAsync(int categoryId)
    {
        return await _dbSet
            .Where(p => p.CategoryId == categoryId)
            .ToListAsync();
    }

    public async Task<Product?> GetByNameAsync(string name)
    {
        return await _dbSet
            .FirstOrDefaultAsync(p => p.Name == name);
    }
}
```

### 4. Query Optimization

**Compiled Queries**:

```csharp
public static class CompiledQueries
{
    private static readonly Func<ApplicationDbContext, int, Task<Product?>> GetProductById =
        EF.CompileAsyncQuery((ApplicationDbContext context, int id) =>
            context.Products.FirstOrDefault(p => p.Id == id));

    public static async Task<Product?> GetProductAsync(ApplicationDbContext context, int id)
    {
        return await GetProductById(context, id);
    }
}
```

**Projections** (select only needed fields):

```csharp
// Instead of loading full entities
public async Task<IEnumerable<ProductDto>> GetProductSummariesAsync()
{
    return await _context.Products
        .Select(p => new ProductDto
        {
            Id = p.Id,
            Name = p.Name,
            Price = p.Price,
            CategoryName = p.Category.Name // Include related data efficiently
        })
        .ToListAsync();
}
```

**Split Queries** (avoid cartesian explosion):

```csharp
// Configure split query for one-to-many relationships
public async Task<Category?> GetCategoryWithProductsAsync(int categoryId)
{
    return await _context.Categories
        .Include(c => c.Products)
        .AsSplitQuery() // Prevents cartesian explosion
        .FirstOrDefaultAsync(c => c.Id == categoryId);
}
```

### 5. Bulk Operations

```csharp
using Microsoft.EntityFrameworkCore;

public class BulkOperationsService
{
    private readonly ApplicationDbContext _context;

    public BulkOperationsService(ApplicationDbContext context)
    {
        _context = context;
    }

    // Bulk insert
    public async Task BulkInsertAsync(IEnumerable<Product> products)
    {
        await _context.Products.AddRangeAsync(products);
        await _context.SaveChangesAsync();
    }

    // Bulk update using ExecuteUpdate (EF Core 7+)
    public async Task BulkUpdatePriceAsync(int categoryId, decimal newPrice)
    {
        await _context.Products
            .Where(p => p.CategoryId == categoryId)
            .ExecuteUpdateAsync(p => p.SetProperty(x => x.Price, newPrice));
    }

    // Bulk delete using ExecuteDelete (EF Core 7+)
    public async Task BulkDeleteAsync(int categoryId)
    {
        await _context.Products
            .Where(p => p.CategoryId == categoryId)
            .ExecuteDeleteAsync();
    }
}
```

### 6. Change Tracking Optimization

```csharp
public class OptimizedQueryService
{
    private readonly ApplicationDbContext _context;

    public OptimizedQueryService(ApplicationDbContext context)
    {
        _context = context;
    }

    // Disable change tracking for read-only queries
    public async Task<IEnumerable<Product>> GetReadOnlyProductsAsync()
    {
        return await _context.Products
            .AsNoTracking() // Disable change tracking
            .ToListAsync();
    }

    // Use AsNoTrackingWithIdentityResolution for read-only queries with includes
    public async Task<Category?> GetCategoryReadOnlyAsync(int id)
    {
        return await _context.Categories
            .AsNoTrackingWithIdentityResolution() // Better than AsNoTracking for includes
            .Include(c => c.Products)
            .FirstOrDefaultAsync(c => c.Id == id);
    }

    // Attach entity without tracking changes
    public void AttachWithoutTracking(Product product)
    {
        _context.Entry(product).State = EntityState.Detached;
    }

    // Update only specific properties
    public async Task UpdateProductPriceAsync(int id, decimal newPrice)
    {
        var product = new Product { Id = id, Price = newPrice };
        _context.Entry(product).Property(p => p.Price).IsModified = true;
        await _context.SaveChangesAsync();
    }
}
```

## Best Practices

- **Use AsNoTracking for Reads**: Disable change tracking for read-only queries to improve performance and reduce memory usage
- **Batch Operations**: Use AddRange, ExecuteUpdate, and ExecuteDelete for bulk operations instead of individual calls
- **Avoid N+1 Queries**: Use Include, ThenInclude, or projections to eagerly load related data instead of querying in loops
- **Use Migrations**: Always use EF Core migrations for schema changes, never modify database directly
- **Connection Pooling**: Configure connection pooling appropriately for your workload to manage database connections efficiently
- **Compiled Queries**: Use EF.CompileAsyncQuery for frequently executed queries to improve performance
- **Select Specific Fields**: Use Select projections to fetch only needed fields instead of loading entire entities
- **Indexes**: Add database indexes for frequently queried fields and foreign keys to improve query performance

## Output

- Properly configured DbContext with entity relationships
- Migration scripts and database update strategy
- Repository pattern implementation with custom queries
- Optimized queries using compiled queries, projections, and split queries
- Bulk operation methods for efficient data manipulation
- Change tracking optimization for read-only scenarios
- Performance benchmarks and optimization recommendations

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
