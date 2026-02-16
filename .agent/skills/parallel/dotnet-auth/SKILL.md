---
description: ASP.NET Core authentication and authorization patterns
name: dotnet-auth
type: skill
---
# Dotnet Auth

ASP.NET Core authentication and authorization patterns

Implement secure authentication and authorization in ASP.NET Core applications using Identity, JWT, OAuth 2.0, and Azure AD.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Configure JWT Authentication

```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

builder.Services.AddAuthorization();
```

### Step 2: Generate JWT Tokens

```csharp
public class TokenService(IConfiguration config)
{
    public string GenerateToken(ApplicationUser user, IList<string> roles)
    {
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id),
            new(ClaimTypes.Email, user.Email!),
        };
        claims.AddRange(roles.Select(r => new Claim(ClaimTypes.Role, r)));

        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(config["Jwt:Key"]!));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: config["Jwt:Issuer"],
            audience: config["Jwt:Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddHours(1),
            signingCredentials: creds);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

### Step 3: Policy-Based Authorization

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"))
    .AddPolicy("PremiumUser", policy =>
        policy.RequireClaim("subscription", "premium"))
    .AddPolicy("MinAge", policy =>
        policy.AddRequirements(new MinimumAgeRequirement(18)));

// Usage on endpoints
app.MapGet("/admin", [Authorize(Policy = "AdminOnly")] () => "Admin area");
```

### Step 4: ASP.NET Core Identity Setup

```csharp
builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options =>
{
    options.Password.RequireDigit = true;
    options.Password.RequiredLength = 8;
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.User.RequireUniqueEmail = true;
})
.AddEntityFrameworkStores<ApplicationDbContext>()
.AddDefaultTokenProviders();
```

### Step 5: Azure AD / Entra ID Integration

```csharp
builder.Services.AddMicrosoftIdentityWebApiAuthentication(
    builder.Configuration, "AzureAd");

// appsettings.json
// "AzureAd": {
//   "Instance": "https://login.microsoftonline.com/",
//   "TenantId": "your-tenant-id",
//   "ClientId": "your-client-id"
// }
```

## Output

- Secured API endpoints with JWT or Azure AD authentication
- Role-based and policy-based authorization rules
- Token generation and validation services
- Identity setup with Entity Framework stores

## Best Practices

- **Use ASP.NET Core Identity**: Leverage Identity framework for user management, password hashing, and two-factor authentication
- **JWT Validation**: Always validate JWT tokens including issuer, audience, lifetime, and signing key to prevent token tampering
- **HTTPS Enforcement**: Require HTTPS in production and use HSTS headers to prevent man-in-the-middle attacks
- **CORS Configuration**: Configure CORS policies explicitly with allowed origins, methods, and headers instead of allowing all
- **Secret Management**: Store secrets (JWT keys, client secrets) in secure configuration stores (Azure Key Vault, User Secrets) never in code
- **Password Policies**: Enforce strong password requirements (length, complexity) and implement account lockout after failed attempts
- **Token Expiration**: Use short-lived access tokens (15-60 minutes) with refresh tokens for better security
- **Role-Based Authorization**: Implement role-based and policy-based authorization for fine-grained access control

## Related Skills

- `dotnet-backend` - ASP.NET Core API patterns
- `azure-integration` - Azure service integration

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
