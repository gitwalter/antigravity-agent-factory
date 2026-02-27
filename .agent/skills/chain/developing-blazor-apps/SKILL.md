---
agents:
- none
category: chain
description: Blazor Server, WebAssembly, and Auto render modes, component lifecycle,
  state management, JavaScript interop, authentication
knowledge:
- none
name: developing-blazor-apps
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Blazor Development

Blazor Server, WebAssembly, and Auto render modes, component lifecycle, state management, JavaScript interop, authentication

Build interactive web UIs with Blazor Server, WebAssembly, or Auto render modes. Create reusable components, manage state, and integrate with JavaScript.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Render Modes (.NET 8+)

Choose appropriate render mode for your scenario:

```csharp
// Blazor Server - Server-side rendering with SignalR
@rendermode InteractiveServer

// Blazor WebAssembly - Client-side rendering
@rendermode InteractiveWebAssembly

// Blazor Auto - Server first, then WebAssembly
@rendermode InteractiveAuto

// Static Server-Side Rendering (SSR)
@rendermode RenderMode.Server
```

```csharp
// Configure in Program.cs
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()    // Server
    .AddInteractiveWebAssemblyComponents(); // WebAssembly

// In App.razor
<Routes @rendermode="InteractiveAuto" />
```

### Step 2: Component Basics

Create reusable Blazor components:

```razor
@* ProductCard.razor *@
@using MyApp.Models

<div class="card">
    <div class="card-body">
        <h5 class="card-title">@Product.Name</h5>
        <p class="card-text">@Product.Description</p>
        <p class="card-text">
            <strong>Price: $@Product.Price.ToString("F2")</strong>
        </p>
        <button class="btn btn-primary" @onclick="AddToCart">
            Add to Cart
        </button>
    </div>
</div>

@code {
    [Parameter]
    public Product Product { get; set; } = default!;

    [Parameter]
    public EventCallback<Product> OnAddToCart { get; set; }

    private async Task AddToCart()
    {
        await OnAddToCart.InvokeAsync(Product);
    }
}

@* Usage *@
<ProductCard Product="@product" OnAddToCart="HandleAddToCart" />
```

### Step 3: Component Lifecycle

Use lifecycle methods appropriately:

```razor
@code {
    protected override void OnInitialized()
    {
        // Called once when component is first created
        // Good for: Setting up initial state
    }

    protected override async Task OnInitializedAsync()
    {
        // Async version - preferred for data loading
        Products = await ProductService.GetAllAsync();
    }

    protected override void OnParametersSet()
    {
        // Called when parameters change
        // Good for: Reacting to parameter changes
    }

    protected override async Task OnParametersSetAsync()
    {
        // Async version
        if (ProductId.HasValue)
        {
            Product = await ProductService.GetByIdAsync(ProductId.Value);
        }
    }

    protected override void OnAfterRender(bool firstRender)
    {
        // Called after each render
        // Good for: JavaScript interop, DOM manipulation
        if (firstRender)
        {
            // First render only
        }
    }

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        // Async version
        await base.OnAfterRenderAsync(firstRender);
    }

    public override async Task SetParametersAsync(ParameterView parameters)
    {
        // Override to customize parameter setting
        await base.SetParametersAsync(parameters);
    }
}
```

### Step 4: State Management

Manage component state:

```razor
@* Using Cascading Values *@
<CascadingValue Value="@theme">
    <ChildComponent />
</CascadingValue>

@code {
    private string theme = "light";
}

@* Child component receives cascading value *@
@code {
    [CascadingParameter]
    public string Theme { get; set; } = default!;
}

@* Using Fluxor for complex state (install Fluxor.Blazor.Web) *@
@inject IState<CartState> CartState
@inject IDispatcher Dispatcher

<div>
    Cart Items: @CartState.Value.Items.Count
</div>

<button @onclick="AddItem">Add Item</button>

@code {
    private void AddItem()
    {
        Dispatcher.Dispatch(new AddItemToCartAction { Item = new CartItem() });
    }
}
```

### Step 5: JavaScript Interop

Call JavaScript from C# and vice versa:

```razor
@inject IJSRuntime JSRuntime
@implements IAsyncDisposable

<button @onclick="ShowAlert">Show Alert</button>
<button @onclick="GetWindowSize">Get Window Size</button>

@code {
    private IJSObjectReference? jsModule;

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            jsModule = await JSRuntime.InvokeAsync<IJSObjectReference>(
                "import", "./js/component.js");
        }
    }

    private async Task ShowAlert()
    {
        await JSRuntime.InvokeVoidAsync("alert", "Hello from Blazor!");
    }

    private async Task GetWindowSize()
    {
        var size = await JSRuntime.InvokeAsync<WindowSize>("getWindowSize");
        Console.WriteLine($"Width: {size.Width}, Height: {size.Height}");
    }

    private async Task CallModuleMethod()
    {
        if (jsModule != null)
        {
            await jsModule.InvokeVoidAsync("doSomething");
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (jsModule != null)
        {
            await jsModule.DisposeAsync();
        }
    }
}

@* JavaScript file (wwwroot/js/component.js) *@
export function getWindowSize() {
    return {
        width: window.innerWidth,
        height: window.innerHeight
    };
}

export function doSomething() {
    console.log('Called from Blazor');
}

@* Call C# from JavaScript *@
window.blazorInterop = {
    showMessage: (message) => {
        DotNet.invokeMethodAsync('MyApp', 'ShowMessage', message);
    }
};
```

### Step 6: Forms and Validation

Create forms with validation:

```razor
@using System.ComponentModel.DataAnnotations

<EditForm Model="@product" OnValidSubmit="HandleValidSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary />

    <InputText @bind-Value="product.Name" placeholder="Product Name" />
    <ValidationMessage For="@(() => product.Name)" />

    <InputNumber @bind-Value="product.Price" placeholder="Price" />
    <ValidationMessage For="@(() => product.Price)" />

    <InputTextArea @bind-Value="product.Description" placeholder="Description" />
    <ValidationMessage For="@(() => product.Description)" />

    <button type="submit" class="btn btn-primary">Submit</button>
</EditForm>

@code {
    private Product product = new();

    private async Task HandleValidSubmit()
    {
        await ProductService.CreateAsync(product);
        // Handle success
    }
}

@* Model with validation *@
public class Product
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(200, ErrorMessage = "Name cannot exceed 200 characters")]
    public string Name { get; set; } = string.Empty;

    [Required]
    [Range(0.01, 10000, ErrorMessage = "Price must be between 0.01 and 10000")]
    public decimal Price { get; set; }

    [StringLength(1000)]
    public string Description { get; set; } = string.Empty;
}
```

### Step 7: Authentication with Blazor

Implement authentication:

```razor
@* AuthorizeView component *@
<AuthorizeView>
    <Authorized>
        <p>Hello, @context.User.Identity?.Name!</p>
        <button @onclick="Logout">Logout</button>
    </Authorized>
    <NotAuthorized>
        <p>You're not authorized.</p>
        <a href="/login">Login</a>
    </NotAuthorized>
</AuthorizeView>

@* Authorize attribute *@
@page "/admin"
@attribute [Authorize(Roles = "Admin")]

<h1>Admin Panel</h1>

@* Check authorization in code *@
@inject AuthenticationStateProvider AuthenticationStateProvider

@code {
    protected override async Task OnInitializedAsync()
    {
        var authState = await AuthenticationStateProvider.GetAuthenticationStateAsync();
        var user = authState.User;

        if (user.Identity?.IsAuthenticated == true)
        {
            // User is authenticated
        }

        if (user.IsInRole("Admin"))
        {
            // User is admin
        }
    }
}
```

### Step 8: SignalR Integration (Blazor Server)

Real-time updates with SignalR:

```csharp
// Hub
public class NotificationHub : Hub
{
    public async Task SendNotification(string message)
    {
        await Clients.All.SendAsync("ReceiveNotification", message);
    }
}

// Register in Program.cs
builder.Services.AddSignalR();
app.MapHub<NotificationHub>("/notificationHub");

// In Blazor component
@inject HubConnection HubConnection
@implements IAsyncDisposable

@code {
    private List<string> notifications = new();

    protected override async Task OnInitializedAsync()
    {
        HubConnection = new HubConnectionBuilder()
            .WithUrl("/notificationHub")
            .Build();

        HubConnection.On<string>("ReceiveNotification", (message) =>
        {
            notifications.Add(message);
            StateHasChanged();
        });

        await HubConnection.StartAsync();
    }

    public async ValueTask DisposeAsync()
    {
        if (HubConnection is not null)
        {
            await HubConnection.DisposeAsync();
        }
    }
}
```

## Best Practices

- Use `OnInitializedAsync` for data loading
- Implement `IAsyncDisposable` for cleanup
- Use `StateHasChanged()` to trigger re-render
- Prefer async lifecycle methods
- Use cascading values for theme/context sharing
- Implement proper error boundaries
- Use `@key` directive for list rendering performance
- Minimize JavaScript interop calls
- Use `RenderFragment` for component composition
- Implement proper loading states
- Use `@bind` for two-way data binding
- Validate user input with DataAnnotations

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Loading data in OnInitialized | Use OnInitializedAsync |
| Not disposing resources | Implement IAsyncDisposable |
| Too many re-renders | Use ShouldRender() override |
| Blocking async calls | Use async/await properly |
| Missing error handling | Add ErrorBoundary component |
| Not using @key in loops | Add @key for list items |

## Related

- Knowledge: `{directories.knowledge}/blazor-patterns.json`
- Skill: `building-dotnet-backend` for API setup
- Skill: `authenticating-dotnet` for authentication

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
