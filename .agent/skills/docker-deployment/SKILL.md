---
description: Dockerfile best practices (multi-stage builds, layer caching), Docker Compose for development, GPU support (NVIDIA Container Toolkit), Image optimization (slim/distroless), Health checks, Secrets management, Volume patterns
---

# Docker Deployment

Dockerfile best practices (multi-stage builds, layer caching), Docker Compose for development, GPU support (NVIDIA Container Toolkit), Image optimization (slim/distroless), Health checks, Secrets management, Volume patterns

## 
# Docker Deployment Skill

Build production-ready Docker images and containers with best practices for security, performance, and maintainability.

## 
# Docker Deployment Skill

Build production-ready Docker images and containers with best practices for security, performance, and maintainability.

## Process
### Step 1: Multi-Stage Dockerfile

Use multi-stage builds to reduce image size:

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
```

### Step 2: Layer Caching Optimization

Order Dockerfile instructions to maximize cache hits:

```dockerfile
# Bad: Changes to code invalidate dependency cache
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt

# Good: Dependencies cached separately
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### Step 3: Docker Compose for Development

Create docker-compose.yml for local development:

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - DEBUG=true
    volumes:
      - .:/app
      - /app/venv  # Exclude venv from volume
    depends_on:
      - db
      - redis
    command: uvicorn main:app --reload --host 0.0.0.0

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  redis_data:
```

### Step 4: GPU Support (NVIDIA Container Toolkit)

Enable GPU support for ML workloads:

```dockerfile
# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Copy application
COPY . /app
WORKDIR /app

CMD ["python3", "main.py"]
```

```yaml
# docker-compose.yml with GPU
services:
  ml-service:
    image: my-ml-app:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

### Step 5: Image Optimization

Use slim/distroless images for smaller, more secure containers:

```dockerfile
# Using distroless (most secure)
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["main.py"]

# Using slim (smaller, still has shell)
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["python", "main.py"]

# Using alpine (smallest, but compatibility issues)
FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["python", "main.py"]
```

### Step 6: Health Checks

Implement health checks for container orchestration:

```dockerfile
# Dockerfile health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Or use Python script
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1
```

```yaml
# docker-compose.yml health check
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s
```

### Step 7: Secrets Management

Manage secrets securely in Docker:

```yaml
# docker-compose.yml with secrets
services:
  api:
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
```

```bash
# Create secret
echo "my-secret-password" | docker secret create db_password -

# Use in service
docker service create \
  --secret db_password \
  --env DB_PASSWORD_FILE=/run/secrets/db_password \
  my-app
```

### Step 8: Volume Patterns

Use volumes for persistent data:

```yaml
# Named volumes (recommended)
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    driver: local

# Bind mounts (development only)
services:
  api:
    volumes:
      - ./src:/app/src  # Development
      - ./config:/app/config:ro  # Read-only

# tmpfs for temporary data
services:
  cache:
    tmpfs:
      - /tmp:size=100m,noexec,nosuid
```

### Step 9: .NET Dockerfile Example

```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["MyApp.csproj", "./"]
RUN dotnet restore "MyApp.csproj"
COPY . .
RUN dotnet build "MyApp.csproj" -c Release -o /app/build

# Publish stage
FROM build AS publish
RUN dotnet publish "MyApp.csproj" -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

### Step 10: Java Dockerfile Example

```dockerfile
# Build stage
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
```

```dockerfile
# Bad: Changes to code invalidate dependency cache
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt

# Good: Dependencies cached separately
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - DEBUG=true
    volumes:
      - .:/app
      - /app/venv  # Exclude venv from volume
    depends_on:
      - db
      - redis
    command: uvicorn main:app --reload --host 0.0.0.0

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  redis_data:
```

```dockerfile
# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Copy application
COPY . /app
WORKDIR /app

CMD ["python3", "main.py"]
```

```yaml
# docker-compose.yml with GPU
services:
  ml-service:
    image: my-ml-app:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

```dockerfile
# Using distroless (most secure)
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["main.py"]

# Using slim (smaller, still has shell)
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["python", "main.py"]

# Using alpine (smallest, but compatibility issues)
FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /app/dist /app
CMD ["python", "main.py"]
```

```dockerfile
# Dockerfile health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Or use Python script
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1
```

```yaml
# docker-compose.yml health check
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s
```

```yaml
# docker-compose.yml with secrets
services:
  api:
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
```

```bash
# Create secret
echo "my-secret-password" | docker secret create db_password -

# Use in service
docker service create \
  --secret db_password \
  --env DB_PASSWORD_FILE=/run/secrets/db_password \
  my-app
```

```yaml
# Named volumes (recommended)
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    driver: local

# Bind mounts (development only)
services:
  api:
    volumes:
      - ./src:/app/src  # Development
      - ./config:/app/config:ro  # Read-only

# tmpfs for temporary data
services:
  cache:
    tmpfs:
      - /tmp:size=100m,noexec,nosuid
```

```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["MyApp.csproj", "./"]
RUN dotnet restore "MyApp.csproj"
COPY . .
RUN dotnet build "MyApp.csproj" -c Release -o /app/build

# Publish stage
FROM build AS publish
RUN dotnet publish "MyApp.csproj" -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

```dockerfile
# Build stage
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Best Practices
- Use multi-stage builds to reduce image size
- Order Dockerfile instructions to maximize cache hits
- Use .dockerignore to exclude unnecessary files
- Run containers as non-root user
- Use specific image tags (not `latest`)
- Add health checks for all services
- Use secrets management for sensitive data
- Use named volumes for persistent data
- Keep images minimal (slim/distroless)
- Scan images for vulnerabilities
- Use build arguments for build-time configuration
- Set appropriate resource limits
- Use labels for metadata

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Running as root | Use non-root user |
| Copying everything | Use .dockerignore |
| Installing unnecessary packages | Use minimal base images |
| No health checks | Add HEALTHCHECK directive |
| Secrets in image | Use secrets management |
| Large images | Use multi-stage builds |
| No layer caching | Order instructions properly |

## Related
- Knowledge: `knowledge/docker-patterns.json`
- Skill: `kubernetes-deployment` for orchestration

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: docker-patterns.json
