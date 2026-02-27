---
agents:
- none
category: parallel
description: Docker multi-stage builds for Java (JDK vs JRE), GraalVM native images,
  Jib for containerization, Kubernetes deployment (Deployment, Service, ConfigMap,
  Secrets), Helm charts, Health probes (liveness, readiness, startup), Resource limits
knowledge:
- none
name: containerizing-java-apps
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Java Containerization

Docker multi-stage builds for Java (JDK vs JRE), GraalVM native images, Jib for containerization, Kubernetes deployment (Deployment, Service, ConfigMap, Secrets), Helm charts, Health probes (liveness, readiness, startup), Resource limits

Containerize Java applications with Docker, build native images with GraalVM, deploy to Kubernetes with Helm charts, and configure health probes and resource management.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Docker Multi-Stage Builds

Create optimized Docker images:

**Dockerfile (Multi-stage):**
```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Copy JAR from build stage
COPY --from=build /app/target/*.jar app.jar

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Run application
ENTRYPOINT ["java", "-XX:+UseContainerSupport", \
            "-XX:MaxRAMPercentage=75.0", \
            "-Djava.security.egd=file:/dev/./urandom", \
            "-jar", "app.jar"]
```

**Dockerfile with Gradle:**
```dockerfile
# Stage 1: Build
FROM gradle:8-jdk17-alpine AS build
WORKDIR /app

COPY build.gradle settings.gradle ./
COPY gradle ./gradle
RUN gradle dependencies --no-daemon

COPY src ./src
RUN gradle build --no-daemon -x test

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

COPY --from=build /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-XX:+UseContainerSupport", \
            "-XX:MaxRAMPercentage=75.0", \
            "-jar", "app.jar"]
```

### Step 2: Jib for Containerization

Use Jib for faster builds without Docker daemon:

**Maven Plugin:**
```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <version>3.4.0</version>
    <configuration>
        <from>
            <image>eclipse-temurin:17-jre-alpine</image>
        </from>
        <to>
            <image>myregistry/product-service:${project.version}</image>
        </to>
        <container>
            <ports>
                <port>8080</port>
            </ports>
            <environment>
                <SPRING_PROFILES_ACTIVE>prod</SPRING_PROFILES_ACTIVE>
            </environment>
            <jvmFlags>
                <jvmFlag>-XX:+UseContainerSupport</jvmFlag>
                <jvmFlag>-XX:MaxRAMPercentage=75.0</jvmFlag>
            </jvmFlags>
            <creationTime>USE_CURRENT_TIMESTAMP</creationTime>
        </container>
    </configuration>
</plugin>
```

**Build commands:**
```bash
# Build image
mvn compile jib:build

# Build to Docker daemon
mvn compile jib:dockerBuild

# Build to tar file
mvn compile jib:buildTar
```

### Step 3: GraalVM Native Images

Build native executables:

**Dependencies:**
```xml
<dependency>
    <groupId>org.springframework.experimental</groupId>
    <artifactId>spring-native</artifactId>
    <version>0.12.1</version>
</dependency>
```

**Native Build Configuration:**
```xml
<plugin>
    <groupId>org.graalvm.buildtools</groupId>
    <artifactId>native-maven-plugin</artifactId>
    <version>0.9.28</version>
    <executions>
        <execution>
            <id>test-native</id>
            <phase>test</phase>
            <goals>
                <goal>test</goal>
            </goals>
        </execution>
        <execution>
            <id>build-native</id>
            <phase>package</phase>
            <goals>
                <goal>build</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**Dockerfile for Native Image:**
```dockerfile
FROM ghcr.io/graalvm/native-image:ol8-java17-22.3.0 AS build
WORKDIR /app

COPY . .
RUN ./mvnw native:compile -Pnative

FROM gcr.io/distroless/base-debian11
WORKDIR /app

COPY --from=build /app/target/product-service app

EXPOSE 8080

ENTRYPOINT ["./app"]
```

### Step 4: Kubernetes Deployment

Create Kubernetes manifests:

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  labels:
    app: product-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
    spec:
      containers:
      - name: product-service
        image: myregistry/product-service:1.0.0
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: product-service-secrets
              key: database-url
        - name: DATABASE_USERNAME
          valueFrom:
            secretKeyRef:
              name: product-service-secrets
              key: database-username
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: product-service-secrets
              key: database-password
        envFrom:
        - configMapRef:
            name: product-service-config
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /actuator/health/startup
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30
```

**service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: product-service
spec:
  selector:
    app: product-service
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  type: ClusterIP
```

**configmap.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: product-service-config
data:
  application.yml: |
    spring:
      application:
        name: product-service
      datasource:
        url: ${DATABASE_URL}
        username: ${DATABASE_USERNAME}
        password: ${DATABASE_PASSWORD}
    management:
      endpoints:
        web:
          exposure:
            include: health,info,metrics,prometheus
      health:
        probes:
          enabled: true
```

**secret.yaml:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: product-service-secrets
type: Opaque
stringData:
  database-url: jdbc:postgresql://postgres:5432/products
  database-username: postgres
  database-password: changeme
```

### Step 5: Helm Charts

Create Helm chart structure:

**Chart.yaml:**
```yaml
apiVersion: v2
name: product-service
description: Product Service Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"
```

**values.yaml:**
```yaml
replicaCount: 3

image:
  repository: myregistry/product-service
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: "nginx"
  annotations: {}
  hosts:
    - host: product-service.example.com
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: http
  initialDelaySeconds: 60
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: http
  initialDelaySeconds: 30
  periodSeconds: 5

startupProbe:
  httpGet:
    path: /actuator/health/startup
    port: http
  initialDelaySeconds: 0
  periodSeconds: 10
  failureThreshold: 30

config:
  springProfilesActive: prod

secrets:
  databaseUrl: ""
  databaseUsername: ""
  databasePassword: ""
```

**{directories.templates}/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "product-service.fullname" . }}
  labels:
    {{- include "product-service.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "product-service.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "product-service.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: {{ .Values.config.springProfilesActive | quote }}
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "product-service.fullname" . }}-secrets
              key: database-url
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        livenessProbe:
          {{- toYaml .Values.livenessProbe | nindent 10 }}
        readinessProbe:
          {{- toYaml .Values.readinessProbe | nindent 10 }}
        startupProbe:
          {{- toYaml .Values.startupProbe | nindent 10 }}
```

**{directories.templates}/_helpers.tpl:**
```yaml
{{- define "product-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "product-service.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "product-service.labels" -}}
helm.sh/chart: {{ include "product-service.chart" . }}
{{ include "product-service.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "product-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "product-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### Step 6: Health Probes Configuration

Configure Spring Boot Actuator for health probes:

**application.yml:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  health:
    probes:
      enabled: true
    livenessState:
      enabled: true
    readinessState:
      enabled: true
```

**Custom Health Indicators:**
```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    private final DataSource dataSource;

    public DatabaseHealthIndicator(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Health health() {
        try (Connection connection = dataSource.getConnection()) {
            if (connection.isValid(1)) {
                return Health.up()
                    .withDetail("database", "Available")
                    .build();
            }
        } catch (SQLException e) {
            return Health.down()
                .withDetail("database", "Unavailable")
                .withException(e)
                .build();
        }
        return Health.down().build();
    }
}
```

## Best Practices

- Use multi-stage builds for smaller images
- Use JRE instead of JDK in runtime stage
- Create non-root users in containers
- Set proper resource limits
- Configure health probes (liveness, readiness, startup)
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Use Helm for deployment management
- Set proper JVM flags for containers (`-XX:+UseContainerSupport`)
- Use `MaxRAMPercentage` instead of fixed heap size
- Enable health probes in Spring Boot Actuator
- Use image pull policies appropriately
- Implement graceful shutdown
- Use init containers for setup tasks

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Using JDK in production | Use JRE or distroless images |
| Running as root | Create non-root user |
| No resource limits | Set requests and limits |
| Missing health probes | Configure liveness/readiness |
| Hardcoded secrets | Use Kubernetes Secrets |
| Large image sizes | Use multi-stage builds |
| Fixed JVM heap size | Use MaxRAMPercentage |

## Related

- Knowledge: `{directories.knowledge}/java-containerization-patterns.json`
- Skill: `building-spring-microservices` for service architecture
- Skill: `observing-spring-apps` for health checks

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
