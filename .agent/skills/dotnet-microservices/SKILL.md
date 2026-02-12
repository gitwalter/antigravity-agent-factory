---
description: Service decomposition, API Gateway with YARP, inter-service communication
  (gRPC, REST, message bus), distributed caching, health checks, circuit breakers
name: dotnet-microservices
type: skill
---

# Dotnet Microservices

Service decomposition, API Gateway with YARP, inter-service communication (gRPC, REST, message bus), distributed caching, health checks, circuit breakers

## 
# .NET Microservices Skill

Design and implement microservices architectures with API Gateway, service communication, distributed caching, health checks, and resilience patterns.

## 
# .NET Microservices Skill

Design and implement microservices architectures with API Gateway, service communication, distributed caching, health checks, and resilience patterns.

## Process
### Step 1: Service Decomposition

Identify service boundaries:

```csharp
// Catalog Service - Product management
public class CatalogService
{
    // Product CRUD operations
    // Product search
    // Inventory management
}

// Order Service - Order processing
public class OrderService
{
    // Order creation
    // Order status tracking
    // Order history
}

// Payment Service - Payment processing
public class PaymentService
{
    // Payment processing
    // Refund handling
    // Payment history
}

// User Service - User management
public class UserService
{
    // User registration
    // User profile management
    // Authentication
}
```

### Step 2: API Gateway with YARP

Configure YARP as API Gateway:

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();

app.MapReverseProxy();

app.Run();

// appsettings.json
{
  "ReverseProxy": {
    "Routes": {
      "catalog-route": {
        "ClusterId": "catalog-cluster",
        "Match": {
          "Path": "/api/catalog/{**catch-all}"
        }
      },
      "order-route": {
        "ClusterId": "order-cluster",
        "Match": {
          "Path": "/api/orders/{**catch-all}"
        }
      },
      "payment-route": {
        "ClusterId": "payment-cluster",
        "Match": {
          "Path": "/api/payments/{**catch-all}"
        }
      }
    },
    "Clusters": {
      "catalog-cluster": {
        "Destinations": {
          "catalog-destination": {
            "Address": "http://catalog-service:5001"
          }
        }
      },
      "order-cluster": {
        "Destinations": {
          "order-destination": {
            "Address": "http://order-service:5002"
          }
        }
      },
      "payment-cluster": {
        "Destinations": {
          "payment-destination": {
            "Address": "http://payment-service:5003"
          }
        }
      }
    }
  }
}

// Custom YARP transform
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"))
    .AddTransforms(builderContext =>
    {
        builderContext.AddRequestTransform(async transformContext =>
        {
            // Add correlation ID
            var correlationId = Guid.NewGuid().ToString();
            transformContext.ProxyRequest.Headers.Add("X-Correlation-ID", correlationId);
        });
    });
```

### Step 3: gRPC Service Communication

Implement gRPC for high-performance service communication:

```protobuf
// catalog.proto
syntax = "proto3";

package catalog;

service CatalogService {
  rpc GetProduct (GetProductRequest) returns (ProductResponse);
  rpc GetProducts (GetProductsRequest) returns (ProductsResponse);
  rpc CreateProduct (CreateProductRequest) returns (ProductResponse);
}

message GetProductRequest {
  int32 id = 1;
}

message GetProductsRequest {
  string category = 1;
  int32 page_number = 2;
  int32 page_size = 3;
}

message CreateProductRequest {
  string name = 1;
  string description = 2;
  double price = 3;
  string category = 4;
}

message ProductResponse {
  int32 id = 1;
  string name = 2;
  string description = 3;
  double price = 4;
  string category = 5;
}

message ProductsResponse {
  repeated ProductResponse products = 1;
  int32 total_count = 2;
}
```

```csharp
// Server implementation
public class CatalogGrpcService : CatalogService.CatalogServiceBase
{
    private readonly IProductRepository _repository;
    private readonly ILogger<CatalogGrpcService> _logger;

    public CatalogGrpcService(
        IProductRepository repository,
        ILogger<CatalogGrpcService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public override async Task<ProductResponse> GetProduct(
        GetProductRequest request,
        ServerCallContext context)
    {
        var product = await _repository.GetByIdAsync(request.Id);
        
        if (product == null)
        {
            throw new RpcException(
                new Status(StatusCode.NotFound, "Product not found"));
        }

        return new ProductResponse
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = (double)product.Price,
            Category = product.Category
        };
    }
}

// Register gRPC service
builder.Services.AddGrpc();
app.MapGrpcService<CatalogGrpcService>();

// Client implementation
public class CatalogGrpcClient
{
    private readonly CatalogService.CatalogServiceClient _client;

    public CatalogGrpcClient(CatalogService.CatalogServiceClient client)
    {
        _client = client;
    }

    public async Task<ProductDto> GetProductAsync(int id)
    {
        var request = new GetProductRequest { Id = id };
        var response = await _client.GetProductAsync(request);
        
        return new ProductDto
        {
            Id = response.Id,
            Name = response.Name,
            Description = response.Description,
            Price = (decimal)response.Price,
            Category = response.Category
        };
    }
}

// Register gRPC client
builder.Services.AddGrpcClient<CatalogService.CatalogServiceClient>(options =>
{
    options.Address = new Uri("https://catalog-service:5001");
});
```

### Step 4: Message Bus Communication

Implement async messaging with Azure Service Bus or RabbitMQ:

```csharp
// Event publisher
public class OrderEventPublisher
{
    private readonly ServiceBusClient _serviceBusClient;
    private readonly ILogger<OrderEventPublisher> _logger;

    public OrderEventPublisher(
        ServiceBusClient serviceBusClient,
        ILogger<OrderEventPublisher> logger)
    {
        _serviceBusClient = serviceBusClient;
        _logger = logger;
    }

    public async Task PublishOrderCreatedAsync(OrderCreatedEvent orderEvent)
    {
        await using var sender = _serviceBusClient.CreateSender("order-events");

        var message = new ServiceBusMessage(JsonSerializer.Serialize(orderEvent))
        {
            Subject = "OrderCreated",
            MessageId = orderEvent.OrderId.ToString(),
            ApplicationProperties =
            {
                { "EventType", "OrderCreated" },
                { "OrderId", orderEvent.OrderId.ToString() }
            }
        };

        await sender.SendMessageAsync(message);
        _logger.LogInformation("OrderCreated event published: {OrderId}", orderEvent.OrderId);
    }
}

// Event consumer
public class OrderEventHandler : BackgroundService
{
    private readonly ServiceBusClient _serviceBusClient;
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<OrderEventHandler> _logger;

    public OrderEventHandler(
        ServiceBusClient serviceBusClient,
        IServiceProvider serviceProvider,
        ILogger<OrderEventHandler> logger)
    {
        _serviceBusClient = serviceBusClient;
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await using var processor = _serviceBusClient.CreateProcessor(
            "order-events",
            new ServiceBusProcessorOptions
            {
                AutoCompleteMessages = false,
                MaxConcurrentCalls = 1
            });

        processor.ProcessMessageAsync += async args =>
        {
            try
            {
                var eventType = args.Message.ApplicationProperties["EventType"]?.ToString();
                
                if (eventType == "OrderCreated")
                {
                    var orderEvent = JsonSerializer.Deserialize<OrderCreatedEvent>(
                        args.Message.Body);
                    
                    using var scope = _serviceProvider.CreateScope();
                    var inventoryService = scope.ServiceProvider
                        .GetRequiredService<IInventoryService>();
                    
                    await inventoryService.ReserveInventoryAsync(orderEvent!);
                }

                await args.CompleteMessageAsync(args.Message);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing order event");
                await args.AbandonMessageAsync(args.Message);
            }
        };

        await processor.StartProcessingAsync(stoppingToken);

        while (!stoppingToken.IsCancellationRequested)
        {
            await Task.Delay(1000, stoppingToken);
        }
    }
}
```

### Step 5: Distributed Caching with Redis

Implement distributed caching:

```csharp
// Configure Redis
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "MyApp:";
});

// Use distributed cache
public class ProductService
{
    private readonly IDistributedCache _cache;
    private readonly IProductRepository _repository;
    private readonly ILogger<ProductService> _logger;

    public ProductService(
        IDistributedCache cache,
        IProductRepository repository,
        ILogger<ProductService> logger)
    {
        _cache = cache;
        _repository = repository;
        _logger = logger;
    }

    public async Task<ProductDto?> GetProductAsync(int id)
    {
        var cacheKey = $"product:{id}";
        var cachedProduct = await _cache.GetStringAsync(cacheKey);

        if (cachedProduct != null)
        {
            return JsonSerializer.Deserialize<ProductDto>(cachedProduct);
        }

        var product = await _repository.GetByIdAsync(id);
        
        if (product == null)
            return null;

        var productDto = MapToDto(product);
        var options = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(30),
            SlidingExpiration = TimeSpan.FromMinutes(10)
        };

        await _cache.SetStringAsync(
            cacheKey,
            JsonSerializer.Serialize(productDto),
            options);

        return productDto;
    }

    public async Task InvalidateProductCacheAsync(int id)
    {
        var cacheKey = $"product:{id}";
        await _cache.RemoveAsync(cacheKey);
    }
}
```

### Step 6: Circuit Breaker with Polly

Implement resilience patterns:

```csharp
// Configure Polly policies
builder.Services.AddHttpClient<IExternalService, ExternalService>()
    .AddPolicyHandler(GetRetryPolicy())
    .AddPolicyHandler(GetCircuitBreakerPolicy());

private static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(
            retryCount: 3,
            sleepDurationProvider: retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
            onRetry: (outcome, timespan, retryCount, context) =>
            {
                Console.WriteLine($"Retry {retryCount} after {timespan.TotalSeconds} seconds");
            });
}

private static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(
            handledEventsAllowedBeforeBreaking: 5,
            durationOfBreak: TimeSpan.FromSeconds(30),
            onBreak: (exception, duration) =>
            {
                Console.WriteLine($"Circuit breaker opened for {duration.TotalSeconds} seconds");
            },
            onReset: () =>
            {
                Console.WriteLine("Circuit breaker reset");
            });
}

// Use in service
public class ExternalService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ExternalService> _logger;

    public ExternalService(HttpClient httpClient, ILogger<ExternalService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<string> GetDataAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync("/api/data");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
        catch (BrokenCircuitException ex)
        {
            _logger.LogWarning(ex, "Circuit breaker is open");
            throw;
        }
    }
}
```

### Step 7: Health Checks

Implement distributed health checks:

```csharp
// Configure health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy())
    .AddDbContextCheck<ApplicationDbContext>()
    .AddRedis(builder.Configuration.GetConnectionString("Redis"))
    .AddCheck<ExternalServiceHealthCheck>("external-service");

// Custom health check
public class ExternalServiceHealthCheck : IHealthCheck
{
    private readonly HttpClient _httpClient;

    public ExternalServiceHealthCheck(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await _httpClient.GetAsync("/health", cancellationToken);
            return response.IsSuccessStatusCode
                ? HealthCheckResult.Healthy()
                : HealthCheckResult.Unhealthy("External service returned unhealthy status");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("External service is unavailable", ex);
        }
    }
}

// Map health check endpoints
app.MapHealthChecks("/health");
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

```csharp
// Catalog Service - Product management
public class CatalogService
{
    // Product CRUD operations
    // Product search
    // Inventory management
}

// Order Service - Order processing
public class OrderService
{
    // Order creation
    // Order status tracking
    // Order history
}

// Payment Service - Payment processing
public class PaymentService
{
    // Payment processing
    // Refund handling
    // Payment history
}

// User Service - User management
public class UserService
{
    // User registration
    // User profile management
    // Authentication
}
```

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();

app.MapReverseProxy();

app.Run();

// appsettings.json
{
  "ReverseProxy": {
    "Routes": {
      "catalog-route": {
        "ClusterId": "catalog-cluster",
        "Match": {
          "Path": "/api/catalog/{**catch-all}"
        }
      },
      "order-route": {
        "ClusterId": "order-cluster",
        "Match": {
          "Path": "/api/orders/{**catch-all}"
        }
      },
      "payment-route": {
        "ClusterId": "payment-cluster",
        "Match": {
          "Path": "/api/payments/{**catch-all}"
        }
      }
    },
    "Clusters": {
      "catalog-cluster": {
        "Destinations": {
          "catalog-destination": {
            "Address": "http://catalog-service:5001"
          }
        }
      },
      "order-cluster": {
        "Destinations": {
          "order-destination": {
            "Address": "http://order-service:5002"
          }
        }
      },
      "payment-cluster": {
        "Destinations": {
          "payment-destination": {
            "Address": "http://payment-service:5003"
          }
        }
      }
    }
  }
}

// Custom YARP transform
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"))
    .AddTransforms(builderContext =>
    {
        builderContext.AddRequestTransform(async transformContext =>
        {
            // Add correlation ID
            var correlationId = Guid.NewGuid().ToString();
            transformContext.ProxyRequest.Headers.Add("X-Correlation-ID", correlationId);
        });
    });
```

```protobuf
// catalog.proto
syntax = "proto3";

package catalog;

service CatalogService {
  rpc GetProduct (GetProductRequest) returns (ProductResponse);
  rpc GetProducts (GetProductsRequest) returns (ProductsResponse);
  rpc CreateProduct (CreateProductRequest) returns (ProductResponse);
}

message GetProductRequest {
  int32 id = 1;
}

message GetProductsRequest {
  string category = 1;
  int32 page_number = 2;
  int32 page_size = 3;
}

message CreateProductRequest {
  string name = 1;
  string description = 2;
  double price = 3;
  string category = 4;
}

message ProductResponse {
  int32 id = 1;
  string name = 2;
  string description = 3;
  double price = 4;
  string category = 5;
}

message ProductsResponse {
  repeated ProductResponse products = 1;
  int32 total_count = 2;
}
```

```csharp
// Server implementation
public class CatalogGrpcService : CatalogService.CatalogServiceBase
{
    private readonly IProductRepository _repository;
    private readonly ILogger<CatalogGrpcService> _logger;

    public CatalogGrpcService(
        IProductRepository repository,
        ILogger<CatalogGrpcService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public override async Task<ProductResponse> GetProduct(
        GetProductRequest request,
        ServerCallContext context)
    {
        var product = await _repository.GetByIdAsync(request.Id);
        
        if (product == null)
        {
            throw new RpcException(
                new Status(StatusCode.NotFound, "Product not found"));
        }

        return new ProductResponse
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = (double)product.Price,
            Category = product.Category
        };
    }
}

// Register gRPC service
builder.Services.AddGrpc();
app.MapGrpcService<CatalogGrpcService>();

// Client implementation
public class CatalogGrpcClient
{
    private readonly CatalogService.CatalogServiceClient _client;

    public CatalogGrpcClient(CatalogService.CatalogServiceClient client)
    {
        _client = client;
    }

    public async Task<ProductDto> GetProductAsync(int id)
    {
        var request = new GetProductRequest { Id = id };
        var response = await _client.GetProductAsync(request);
        
        return new ProductDto
        {
            Id = response.Id,
            Name = response.Name,
            Description = response.Description,
            Price = (decimal)response.Price,
            Category = response.Category
        };
    }
}

// Register gRPC client
builder.Services.AddGrpcClient<CatalogService.CatalogServiceClient>(options =>
{
    options.Address = new Uri("https://catalog-service:5001");
});
```

```csharp
// Event publisher
public class OrderEventPublisher
{
    private readonly ServiceBusClient _serviceBusClient;
    private readonly ILogger<OrderEventPublisher> _logger;

    public OrderEventPublisher(
        ServiceBusClient serviceBusClient,
        ILogger<OrderEventPublisher> logger)
    {
        _serviceBusClient = serviceBusClient;
        _logger = logger;
    }

    public async Task PublishOrderCreatedAsync(OrderCreatedEvent orderEvent)
    {
        await using var sender = _serviceBusClient.CreateSender("order-events");

        var message = new ServiceBusMessage(JsonSerializer.Serialize(orderEvent))
        {
            Subject = "OrderCreated",
            MessageId = orderEvent.OrderId.ToString(),
            ApplicationProperties =
            {
                { "EventType", "OrderCreated" },
                { "OrderId", orderEvent.OrderId.ToString() }
            }
        };

        await sender.SendMessageAsync(message);
        _logger.LogInformation("OrderCreated event published: {OrderId}", orderEvent.OrderId);
    }
}

// Event consumer
public class OrderEventHandler : BackgroundService
{
    private readonly ServiceBusClient _serviceBusClient;
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<OrderEventHandler> _logger;

    public OrderEventHandler(
        ServiceBusClient serviceBusClient,
        IServiceProvider serviceProvider,
        ILogger<OrderEventHandler> logger)
    {
        _serviceBusClient = serviceBusClient;
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await using var processor = _serviceBusClient.CreateProcessor(
            "order-events",
            new ServiceBusProcessorOptions
            {
                AutoCompleteMessages = false,
                MaxConcurrentCalls = 1
            });

        processor.ProcessMessageAsync += async args =>
        {
            try
            {
                var eventType = args.Message.ApplicationProperties["EventType"]?.ToString();
                
                if (eventType == "OrderCreated")
                {
                    var orderEvent = JsonSerializer.Deserialize<OrderCreatedEvent>(
                        args.Message.Body);
                    
                    using var scope = _serviceProvider.CreateScope();
                    var inventoryService = scope.ServiceProvider
                        .GetRequiredService<IInventoryService>();
                    
                    await inventoryService.ReserveInventoryAsync(orderEvent!);
                }

                await args.CompleteMessageAsync(args.Message);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing order event");
                await args.AbandonMessageAsync(args.Message);
            }
        };

        await processor.StartProcessingAsync(stoppingToken);

        while (!stoppingToken.IsCancellationRequested)
        {
            await Task.Delay(1000, stoppingToken);
        }
    }
}
```

```csharp
// Configure Redis
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "MyApp:";
});

// Use distributed cache
public class ProductService
{
    private readonly IDistributedCache _cache;
    private readonly IProductRepository _repository;
    private readonly ILogger<ProductService> _logger;

    public ProductService(
        IDistributedCache cache,
        IProductRepository repository,
        ILogger<ProductService> logger)
    {
        _cache = cache;
        _repository = repository;
        _logger = logger;
    }

    public async Task<ProductDto?> GetProductAsync(int id)
    {
        var cacheKey = $"product:{id}";
        var cachedProduct = await _cache.GetStringAsync(cacheKey);

        if (cachedProduct != null)
        {
            return JsonSerializer.Deserialize<ProductDto>(cachedProduct);
        }

        var product = await _repository.GetByIdAsync(id);
        
        if (product == null)
            return null;

        var productDto = MapToDto(product);
        var options = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(30),
            SlidingExpiration = TimeSpan.FromMinutes(10)
        };

        await _cache.SetStringAsync(
            cacheKey,
            JsonSerializer.Serialize(productDto),
            options);

        return productDto;
    }

    public async Task InvalidateProductCacheAsync(int id)
    {
        var cacheKey = $"product:{id}";
        await _cache.RemoveAsync(cacheKey);
    }
}
```

```csharp
// Configure Polly policies
builder.Services.AddHttpClient<IExternalService, ExternalService>()
    .AddPolicyHandler(GetRetryPolicy())
    .AddPolicyHandler(GetCircuitBreakerPolicy());

private static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(
            retryCount: 3,
            sleepDurationProvider: retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
            onRetry: (outcome, timespan, retryCount, context) =>
            {
                Console.WriteLine($"Retry {retryCount} after {timespan.TotalSeconds} seconds");
            });
}

private static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(
            handledEventsAllowedBeforeBreaking: 5,
            durationOfBreak: TimeSpan.FromSeconds(30),
            onBreak: (exception, duration) =>
            {
                Console.WriteLine($"Circuit breaker opened for {duration.TotalSeconds} seconds");
            },
            onReset: () =>
            {
                Console.WriteLine("Circuit breaker reset");
            });
}

// Use in service
public class ExternalService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ExternalService> _logger;

    public ExternalService(HttpClient httpClient, ILogger<ExternalService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<string> GetDataAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync("/api/data");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
        catch (BrokenCircuitException ex)
        {
            _logger.LogWarning(ex, "Circuit breaker is open");
            throw;
        }
    }
}
```

```csharp
// Configure health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy())
    .AddDbContextCheck<ApplicationDbContext>()
    .AddRedis(builder.Configuration.GetConnectionString("Redis"))
    .AddCheck<ExternalServiceHealthCheck>("external-service");

// Custom health check
public class ExternalServiceHealthCheck : IHealthCheck
{
    private readonly HttpClient _httpClient;

    public ExternalServiceHealthCheck(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await _httpClient.GetAsync("/health", cancellationToken);
            return response.IsSuccessStatusCode
                ? HealthCheckResult.Healthy()
                : HealthCheckResult.Unhealthy("External service returned unhealthy status");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("External service is unavailable", ex);
        }
    }
}

// Map health check endpoints
app.MapHealthChecks("/health");
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

## Best Practices
- Keep services small and focused on single business capability
- Use API Gateway for routing and cross-cutting concerns
- Prefer async messaging for loose coupling
- Use gRPC for high-performance synchronous communication
- Implement circuit breakers to prevent cascading failures
- Use distributed caching to reduce database load
- Implement health checks for all services
- Use correlation IDs for request tracing
- Implement idempotency for message processing
- Use service discovery or configuration for service addresses
- Implement proper error handling and retry policies
- Monitor service dependencies and health

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Shared database across services | Each service has its own database |
| Synchronous communication everywhere | Use async messaging where appropriate |
| No circuit breaker | Implement circuit breaker pattern |
| Missing health checks | Add health checks for all services |
| No distributed tracing | Implement correlation IDs and tracing |
| Tight coupling between services | Use events and message bus |

## Related
- Knowledge: `knowledge/dotnet-microservices-patterns.json`
- Skill: `azure-integration` for Azure services
- Agent: `dotnet-architect` for architecture decisions

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: dotnet-microservices-patterns.json
