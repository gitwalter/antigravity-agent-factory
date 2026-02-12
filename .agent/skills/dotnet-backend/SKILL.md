---
description: ASP.NET Core Minimal APIs, Controllers, dependency injection, middleware,
  background services, options pattern, health checks
name: dotnet-backend
type: skill
---

# Dotnet Backend

ASP.NET Core Minimal APIs, Controllers, dependency injection, middleware, background services, options pattern, health checks

## 
# .NET Backend Development Skill

Build production ASP.NET Core applications using Minimal APIs, Controllers, dependency injection, middleware, and background services.

## 
# .NET Backend Development Skill

Build production ASP.NET Core applications using Minimal APIs, Controllers, dependency injection, middleware, and background services.

## Process
### Step 1: Minimal APIs Setup

Minimal APIs provide a lightweight way to build HTTP APIs:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Simple GET endpoint
app.MapGet("/", () => "Hello World!");

// GET with route parameter
app.MapGet("/users/{id:int}", (int id) => 
    Results.Ok(new { UserId = id, Name = "John Doe" }));

// POST with request body
app.MapPost("/users", (User user) =>
{
    // Process user
    return Results.Created($"/users/{user.Id}", user);
});

// PUT endpoint
app.MapPut("/users/{id:int}", (int id, User user) =>
{
    // Update user
    return Results.Ok(user);
});

// DELETE endpoint
app.MapDelete("/users/{id:int}", (int id) =>
{
    // Delete user
    return Results.NoContent();
});

app.Run();
```

### Step 2: Controllers Pattern

Traditional MVC controllers for complex scenarios:

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(
        IProductService productService,
        ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetProducts(
        CancellationToken cancellationToken)
    {
        var products = await _productService.GetAllAsync(cancellationToken);
        return Ok(products);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<ProductDto>> GetProduct(
        int id,
        CancellationToken cancellationToken)
    {
        var product = await _productService.GetByIdAsync(id, cancellationToken);
        
        if (product == null)
            return NotFound();

        return Ok(product);
    }

    [HttpPost]
    public async Task<ActionResult<ProductDto>> CreateProduct(
        CreateProductDto dto,
        CancellationToken cancellationToken)
    {
        var product = await _productService.CreateAsync(dto, cancellationToken);
        return CreatedAtAction(
            nameof(GetProduct),
            new { id = product.Id },
            product);
    }

    [HttpPut("{id:int}")]
    public async Task<IActionResult> UpdateProduct(
        int id,
        UpdateProductDto dto,
        CancellationToken cancellationToken)
    {
        await _productService.UpdateAsync(id, dto, cancellationToken);
        return NoContent();
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> DeleteProduct(
        int id,
        CancellationToken cancellationToken)
    {
        await _productService.DeleteAsync(id, cancellationToken);
        return NoContent();
    }
}
```

### Step 3: Dependency Injection Configuration

Configure services with appropriate lifetimes:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Singleton - Single instance for application lifetime
builder.Services.AddSingleton<ICacheService, CacheService>();

// Scoped - One instance per HTTP request (most common)
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IProductRepository, ProductRepository>();

// Transient - New instance every time
builder.Services.AddTransient<IValidator<CreateProductDto>, CreateProductDtoValidator>();

// Register DbContext (scoped)
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Register HttpClient (use IHttpClientFactory)
builder.Services.AddHttpClient<IExternalApiService, ExternalApiService>(client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.Timeout = TimeSpan.FromSeconds(30);
});

var app = builder.Build();
```

### Step 4: Middleware Pipeline

Configure middleware in order:

```csharp
var app = builder.Build();

// Exception handling (early in pipeline)
app.UseExceptionHandler("/error");

// HTTPS redirection
app.UseHttpsRedirection();

// CORS
app.UseCors(policy => policy
    .WithOrigins("https://example.com")
    .AllowAnyMethod()
    .AllowAnyHeader()
    .AllowCredentials());

// Authentication & Authorization
app.UseAuthentication();
app.UseAuthorization();

// Custom middleware
app.Use(async (context, next) =>
{
    // Before request
    var stopwatch = Stopwatch.StartNew();
    
    await next();
    
    // After request
    stopwatch.Stop();
    context.Response.Headers.Add("X-Response-Time", stopwatch.ElapsedMilliseconds.ToString());
});

// Static files
app.UseStaticFiles();

// Routing
app.MapControllers();
app.MapMinimalApiEndpoints();

app.Run();
```

### Step 5: Background Services

Long-running background tasks:

```csharp
public class EmailBackgroundService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<EmailBackgroundService> _logger;

    public EmailBackgroundService(
        IServiceProvider serviceProvider,
        ILogger<EmailBackgroundService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // Create scope for scoped services
                using var scope = _serviceProvider.CreateScope();
                var emailService = scope.ServiceProvider
                    .GetRequiredService<IEmailService>();

                await emailService.ProcessPendingEmailsAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing emails");
            }

            // Wait 5 minutes before next run
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}

// Register in Program.cs
builder.Services.AddHostedService<EmailBackgroundService>();
```

### Step 6: Options Pattern

Strongly-typed configuration:

```csharp
// appsettings.json
{
  "EmailSettings": {
    "SmtpServer": "smtp.example.com",
    "Port": 587,
    "FromEmail": "noreply@example.com",
    "ApiKey": "your-api-key"
  }
}

// Options class
public class EmailSettings
{
    public const string SectionName = "EmailSettings";
    
    public string SmtpServer { get; set; } = string.Empty;
    public int Port { get; set; }
    public string FromEmail { get; set; } = string.Empty;
    public string ApiKey { get; set; } = string.Empty;
}

// Register options
builder.Services.Configure<EmailSettings>(
    builder.Configuration.GetSection(EmailSettings.SectionName));

// Validate options
builder.Services.AddOptions<EmailSettings>()
    .Bind(builder.Configuration.GetSection(EmailSettings.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart();

// Use in service
public class EmailService
{
    private readonly EmailSettings _settings;

    public EmailService(IOptions<EmailSettings> options)
    {
        _settings = options.Value;
    }
}
```

### Step 7: Health Checks

Monitor application health:

```csharp
// Register health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy())
    .AddDbContextCheck<ApplicationDbContext>()
    .AddCheck<DatabaseHealthCheck>("database")
    .AddCheck<ExternalApiHealthCheck>("external-api");

// Custom health check
public class DatabaseHealthCheck : IHealthCheck
{
    private readonly ApplicationDbContext _context;

    public DatabaseHealthCheck(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            await _context.Database.CanConnectAsync(cancellationToken);
            return HealthCheckResult.Healthy("Database is available");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Database is unavailable", ex);
        }
    }
}

// Map health check endpoints
app.MapHealthChecks("/health");
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false
});
```

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Simple GET endpoint
app.MapGet("/", () => "Hello World!");

// GET with route parameter
app.MapGet("/users/{id:int}", (int id) => 
    Results.Ok(new { UserId = id, Name = "John Doe" }));

// POST with request body
app.MapPost("/users", (User user) =>
{
    // Process user
    return Results.Created($"/users/{user.Id}", user);
});

// PUT endpoint
app.MapPut("/users/{id:int}", (int id, User user) =>
{
    // Update user
    return Results.Ok(user);
});

// DELETE endpoint
app.MapDelete("/users/{id:int}", (int id) =>
{
    // Delete user
    return Results.NoContent();
});

app.Run();
```

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(
        IProductService productService,
        ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetProducts(
        CancellationToken cancellationToken)
    {
        var products = await _productService.GetAllAsync(cancellationToken);
        return Ok(products);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<ProductDto>> GetProduct(
        int id,
        CancellationToken cancellationToken)
    {
        var product = await _productService.GetByIdAsync(id, cancellationToken);
        
        if (product == null)
            return NotFound();

        return Ok(product);
    }

    [HttpPost]
    public async Task<ActionResult<ProductDto>> CreateProduct(
        CreateProductDto dto,
        CancellationToken cancellationToken)
    {
        var product = await _productService.CreateAsync(dto, cancellationToken);
        return CreatedAtAction(
            nameof(GetProduct),
            new { id = product.Id },
            product);
    }

    [HttpPut("{id:int}")]
    public async Task<IActionResult> UpdateProduct(
        int id,
        UpdateProductDto dto,
        CancellationToken cancellationToken)
    {
        await _productService.UpdateAsync(id, dto, cancellationToken);
        return NoContent();
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> DeleteProduct(
        int id,
        CancellationToken cancellationToken)
    {
        await _productService.DeleteAsync(id, cancellationToken);
        return NoContent();
    }
}
```

```csharp
var builder = WebApplication.CreateBuilder(args);

// Singleton - Single instance for application lifetime
builder.Services.AddSingleton<ICacheService, CacheService>();

// Scoped - One instance per HTTP request (most common)
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IProductRepository, ProductRepository>();

// Transient - New instance every time
builder.Services.AddTransient<IValidator<CreateProductDto>, CreateProductDtoValidator>();

// Register DbContext (scoped)
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Register HttpClient (use IHttpClientFactory)
builder.Services.AddHttpClient<IExternalApiService, ExternalApiService>(client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.Timeout = TimeSpan.FromSeconds(30);
});

var app = builder.Build();
```

```csharp
var app = builder.Build();

// Exception handling (early in pipeline)
app.UseExceptionHandler("/error");

// HTTPS redirection
app.UseHttpsRedirection();

// CORS
app.UseCors(policy => policy
    .WithOrigins("https://example.com")
    .AllowAnyMethod()
    .AllowAnyHeader()
    .AllowCredentials());

// Authentication & Authorization
app.UseAuthentication();
app.UseAuthorization();

// Custom middleware
app.Use(async (context, next) =>
{
    // Before request
    var stopwatch = Stopwatch.StartNew();
    
    await next();
    
    // After request
    stopwatch.Stop();
    context.Response.Headers.Add("X-Response-Time", stopwatch.ElapsedMilliseconds.ToString());
});

// Static files
app.UseStaticFiles();

// Routing
app.MapControllers();
app.MapMinimalApiEndpoints();

app.Run();
```

```csharp
public class EmailBackgroundService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<EmailBackgroundService> _logger;

    public EmailBackgroundService(
        IServiceProvider serviceProvider,
        ILogger<EmailBackgroundService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // Create scope for scoped services
                using var scope = _serviceProvider.CreateScope();
                var emailService = scope.ServiceProvider
                    .GetRequiredService<IEmailService>();

                await emailService.ProcessPendingEmailsAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing emails");
            }

            // Wait 5 minutes before next run
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}

// Register in Program.cs
builder.Services.AddHostedService<EmailBackgroundService>();
```

```csharp
// appsettings.json
{
  "EmailSettings": {
    "SmtpServer": "smtp.example.com",
    "Port": 587,
    "FromEmail": "noreply@example.com",
    "ApiKey": "your-api-key"
  }
}

// Options class
public class EmailSettings
{
    public const string SectionName = "EmailSettings";
    
    public string SmtpServer { get; set; } = string.Empty;
    public int Port { get; set; }
    public string FromEmail { get; set; } = string.Empty;
    public string ApiKey { get; set; } = string.Empty;
}

// Register options
builder.Services.Configure<EmailSettings>(
    builder.Configuration.GetSection(EmailSettings.SectionName));

// Validate options
builder.Services.AddOptions<EmailSettings>()
    .Bind(builder.Configuration.GetSection(EmailSettings.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart();

// Use in service
public class EmailService
{
    private readonly EmailSettings _settings;

    public EmailService(IOptions<EmailSettings> options)
    {
        _settings = options.Value;
    }
}
```

```csharp
// Register health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy())
    .AddDbContextCheck<ApplicationDbContext>()
    .AddCheck<DatabaseHealthCheck>("database")
    .AddCheck<ExternalApiHealthCheck>("external-api");

// Custom health check
public class DatabaseHealthCheck : IHealthCheck
{
    private readonly ApplicationDbContext _context;

    public DatabaseHealthCheck(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            await _context.Database.CanConnectAsync(cancellationToken);
            return HealthCheckResult.Healthy("Database is available");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Database is unavailable", ex);
        }
    }
}

// Map health check endpoints
app.MapHealthChecks("/health");
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false
});
```

## Best Practices
- Use `async Task` for all I/O operations
- Register services with appropriate lifetimes (Scoped for DbContext, Singleton for caches)
- Use `IHttpClientFactory` instead of `HttpClient` directly
- Implement proper error handling with exception middleware
- Use cancellation tokens for async operations
- Configure CORS properly for production
- Use Options pattern for configuration
- Implement health checks for monitoring
- Use structured logging with `ILogger<T>`
- Add request/response logging middleware
- Implement rate limiting for public APIs
- Use `Results` class for Minimal API responses

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| `HttpClient` as singleton | Use `IHttpClientFactory` |
| Synchronous I/O in async methods | Use `async/await` throughout |
| DbContext as singleton | Use scoped lifetime |
| Missing cancellation tokens | Pass `CancellationToken` to async methods |
| Hardcoded configuration | Use Options pattern |
| No error handling | Add exception middleware |

## Related
- Knowledge: `knowledge/dotnet-patterns.json`
- Skill: `ef-core-patterns` for data access
- Skill: `dotnet-auth` for authentication

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: dotnet-patterns.json
