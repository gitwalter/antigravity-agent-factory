---
agents:
- none
category: chain
description: Azure App Service deployment, Azure Functions, Service Bus messaging,
  Key Vault integration, Container Apps, Application Insights
knowledge:
- none
name: integrations-with-azure
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Azure Integration

Azure App Service deployment, Azure Functions, Service Bus messaging, Key Vault integration, Container Apps, Application Insights

Integrate .NET applications with Azure services including App Service, Functions, Service Bus, Key Vault, Container Apps, and Application Insights.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Azure App Service Deployment

Deploy ASP.NET Core app to App Service:

```csharp
// Configure for App Service
var builder = WebApplication.CreateBuilder(args);

// App Service automatically provides these environment variables:
// - WEBSITE_SITE_NAME
// - WEBSITE_INSTANCE_ID
// - WEBSITE_HOSTNAME

// Use managed identity for Azure resources
builder.Services.AddAzureClients(clientBuilder =>
{
    clientBuilder.UseCredential(new DefaultAzureCredential());
});

var app = builder.Build();
app.Run();
```

```bash
# Create App Service plan
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --name myAppName \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --runtime "DOTNET|8.0"

# Deploy from local Git
az webapp deployment source config-local-git \
  --name myAppName \
  --resource-group myResourceGroup

# Deploy using ZIP
az webapp deployment source config-zip \
  --resource-group myResourceGroup \
  --name myAppName \
  --src myapp.zip
```

### Step 2: Azure Functions (Isolated Worker Model)

Create Azure Functions with .NET 8 isolated worker:

```csharp
// Program.cs
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWebApplication()
    .ConfigureServices(services =>
    {
        services.AddApplicationInsightsTelemetryWorkerService();
        services.AddApplicationInsightsKubernetesEnricher();
    })
    .Build();

host.Run();

// Function
public class HttpFunction
{
    private readonly ILogger<HttpFunction> _logger;

    public HttpFunction(ILogger<HttpFunction> logger)
    {
        _logger = logger;
    }

    [Function("HttpFunction")]
    public HttpResponseData Run(
        [HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequestData req)
    {
        _logger.LogInformation("C# HTTP trigger function processed a request.");

        var response = req.CreateResponse(HttpStatusCode.OK);
        response.Headers.Add("Content-Type", "text/plain; charset=utf-8");
        response.WriteString("Welcome to Azure Functions!");

        return response;
    }
}

// Service Bus trigger
public class ServiceBusFunction
{
    [Function("ProcessMessage")]
    public void ProcessMessage(
        [ServiceBusTrigger("myqueue", Connection = "ServiceBusConnection")] string message,
        FunctionContext context)
    {
        var logger = context.GetLogger("ProcessMessage");
        logger.LogInformation($"Message received: {message}");
    }
}

// Timer trigger
public class TimerFunction
{
    [Function("TimerFunction")]
    public void Run([TimerTrigger("0 */5 * * * *")] TimerInfo timer)
    {
        // Runs every 5 minutes
    }
}
```

### Step 3: Azure Service Bus Messaging

Implement message queuing with Service Bus:

```csharp
// Register Service Bus client
builder.Services.AddAzureClients(clientBuilder =>
{
    clientBuilder.AddServiceBusClient(
        builder.Configuration.GetConnectionString("ServiceBus"));
});

// Send messages
public class OrderService
{
    private readonly ServiceBusClient _serviceBusClient;
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        ServiceBusClient serviceBusClient,
        ILogger<OrderService> logger)
    {
        _serviceBusClient = serviceBusClient;
        _logger = logger;
    }

    public async Task SendOrderMessageAsync(Order order)
    {
        await using var sender = _serviceBusClient.CreateSender("orders");

        var message = new ServiceBusMessage(JsonSerializer.Serialize(order))
        {
            MessageId = order.Id.ToString(),
            Subject = "NewOrder",
            ApplicationProperties =
            {
                { "OrderType", order.Type },
                { "Priority", order.Priority }
            }
        };

        await sender.SendMessageAsync(message);
        _logger.LogInformation("Order message sent: {OrderId}", order.Id);
    }

    public async Task SendBatchMessagesAsync(IEnumerable<Order> orders)
    {
        await using var sender = _serviceBusClient.CreateSender("orders");
        using var batch = await sender.CreateMessageBatchAsync();

        foreach (var order in orders)
        {
            var message = new ServiceBusMessage(JsonSerializer.Serialize(order));
            if (!batch.TryAddMessage(message))
            {
                await sender.SendMessagesAsync(batch);
                batch.Dispose();
                using var newBatch = await sender.CreateMessageBatchAsync();
                newBatch.TryAddMessage(message);
            }
        }

        if (batch.Count > 0)
        {
            await sender.SendMessagesAsync(batch);
        }
    }
}

// Receive messages
public class OrderProcessor : BackgroundService
{
    private readonly ServiceBusClient _serviceBusClient;
    private readonly ILogger<OrderProcessor> _logger;

    public OrderProcessor(
        ServiceBusClient serviceBusClient,
        ILogger<OrderProcessor> logger)
    {
        _serviceBusClient = serviceBusClient;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await using var processor = _serviceBusClient.CreateProcessor(
            "orders",
            new ServiceBusProcessorOptions
            {
                AutoCompleteMessages = false,
                MaxConcurrentCalls = 1
            });

        processor.ProcessMessageAsync += MessageHandler;
        processor.ProcessErrorAsync += ErrorHandler;

        await processor.StartProcessingAsync(stoppingToken);

        while (!stoppingToken.IsCancellationRequested)
        {
            await Task.Delay(1000, stoppingToken);
        }

        await processor.StopProcessingAsync();
    }

    private async Task MessageHandler(ProcessMessageEventArgs args)
    {
        try
        {
            var order = JsonSerializer.Deserialize<Order>(args.Message.Body);
            _logger.LogInformation("Processing order: {OrderId}", order?.Id);

            // Process order
            await ProcessOrderAsync(order!);

            await args.CompleteMessageAsync(args.Message);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing message");
            await args.AbandonMessageAsync(args.Message);
        }
    }

    private Task ErrorHandler(ProcessErrorEventArgs args)
    {
        _logger.LogError(args.Exception, "Service Bus error");
        return Task.CompletedTask;
    }

    private Task ProcessOrderAsync(Order order)
    {
        // Order processing logic
        return Task.CompletedTask;
    }
}
```

### Step 4: Azure Key Vault Integration

Secure secrets with Key Vault:

```csharp
// Configure Key Vault
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{builder.Configuration["KeyVaultName"]}.vault.azure.net/"),
    new DefaultAzureCredential());

// Use secrets in configuration
var connectionString = builder.Configuration["DatabaseConnectionString"];

// Access Key Vault directly
builder.Services.AddAzureClients(clientBuilder =>
{
    clientBuilder.AddSecretClient(
        new Uri($"https://{builder.Configuration["KeyVaultName"]}.vault.azure.net/"));
});

// Use SecretClient
public class ApiService
{
    private readonly SecretClient _secretClient;

    public ApiService(SecretClient secretClient)
    {
        _secretClient = secretClient;
    }

    public async Task<string> GetApiKeyAsync()
    {
        var secret = await _secretClient.GetSecretAsync("ApiKey");
        return secret.Value.Value;
    }

    public async Task SetSecretAsync(string name, string value)
    {
        await _secretClient.SetSecretAsync(name, value);
    }
}

// Use managed identity
var credential = new DefaultAzureCredential();
var client = new SecretClient(
    new Uri("https://myvault.vault.azure.net/"),
    credential);
```

### Step 5: Azure Container Apps

Deploy containerized applications:

```csharp
// Dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["MyApp.csproj", "./"]
RUN dotnet restore "MyApp.csproj"
COPY . .
RUN dotnet build "MyApp.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "MyApp.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

```bash
# Create Container Apps environment
az containerapp env create \
  --name myContainerEnv \
  --resource-group myResourceGroup \
  --location eastus

# Create Container App
az containerapp create \
  --name myApp \
  --resource-group myResourceGroup \
  --environment myContainerEnv \
  --image myregistry.azurecr.io/myapp:latest \
  --target-port 8080 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10
```

### Step 6: Application Insights Monitoring

Monitor applications with Application Insights:

```csharp
// Configure Application Insights
builder.Services.AddApplicationInsightsTelemetry(options =>
{
    options.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"];
});

// Custom telemetry
public class OrderService
{
    private readonly TelemetryClient _telemetryClient;
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        TelemetryClient telemetryClient,
        ILogger<OrderService> logger)
    {
        _telemetryClient = telemetryClient;
        _logger = logger;
    }

    public async Task ProcessOrderAsync(Order order)
    {
        using var operation = _telemetryClient.StartOperation<DependencyTelemetry>("ProcessOrder");
        operation.Telemetry.Type = "OrderProcessing";

        try
        {
            _telemetryClient.TrackEvent("OrderProcessingStarted", new Dictionary<string, string>
            {
                { "OrderId", order.Id.ToString() },
                { "OrderType", order.Type }
            });

            // Process order
            await ProcessOrderInternalAsync(order);

            _telemetryClient.TrackEvent("OrderProcessingCompleted");
            operation.Telemetry.Success = true;
        }
        catch (Exception ex)
        {
            _telemetryClient.TrackException(ex);
            operation.Telemetry.Success = false;
            throw;
        }
    }

    public void TrackCustomMetric(string metricName, double value)
    {
        _telemetryClient.TrackMetric(metricName, value);
    }

    public void TrackCustomTrace(string message)
    {
        _telemetryClient.TrackTrace(message, SeverityLevel.Information);
    }
}
```

## Best Practices

- Use managed identity for Azure resource access
- Store secrets in Key Vault, not in code
- Use Application Insights for monitoring
- Implement retry policies for Azure services
- Use connection pooling for Service Bus
- Configure health checks for App Service
- Use staging slots for zero-downtime deployments
- Implement proper error handling and logging
- Use environment-specific configuration
- Monitor costs and optimize resource usage

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Hardcoded connection strings | Use Key Vault or managed identity |
| Not using managed identity | Use DefaultAzureCredential |
| Missing error handling | Add try-catch and retry policies |
| No monitoring | Add Application Insights |
| Hardcoded secrets | Store in Key Vault |

## Related

- Knowledge: `{directories.knowledge}/azure-patterns.json`
- Skill: `building-dotnet-microservices` for distributed systems
- Agent: `dotnet-architect` for architecture decisions

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
