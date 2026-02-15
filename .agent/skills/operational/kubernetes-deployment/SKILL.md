---
description: Deployment/Service/ConfigMap/Secret patterns, Horizontal Pod Autoscaler,
  Ingress configuration, Health probes (liveness/readiness/startup), Resource requests
  and limits, Helm chart basics, Kustomize overlays, Rolling updates
name: kubernetes-deployment
type: skill
---
# Kubernetes Deployment

Deployment/Service/ConfigMap/Secret patterns, Horizontal Pod Autoscaler, Ingress configuration, Health probes (liveness/readiness/startup), Resource requests and limits, Helm chart basics, Kustomize overlays, Rolling updates

Deploy applications to Kubernetes with production-ready configurations including autoscaling, health checks, and resource management.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Deployment Pattern

Create a Deployment with proper configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: my-app:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: log-level
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /health/startup
            port: 8000
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30
```

### Step 2: Service Pattern

Expose Deployment with a Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  type: ClusterIP  # Or LoadBalancer, NodePort
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### Step 3: ConfigMap Pattern

Store configuration in ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  log-level: "INFO"
  api-timeout: "30"
  max-connections: "100"
  app.properties: |
    feature.flag.enabled=true
    cache.ttl=3600
```

```yaml
# Use in Deployment
env:
- name: LOG_LEVEL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: log-level
# Or mount as file
volumeMounts:
- name: config
  mountPath: /app/config
volumes:
- name: config
  configMap:
    name: app-config
```

### Step 4: Secret Pattern

Store secrets securely:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
stringData:
  url: "postgresql://user:pass@db:5432/mydb"
  password: "secret-password"
```

```bash
# Create from file
kubectl create secret generic db-secret \
  --from-file=password=./secrets/password.txt

# Create from literal
kubectl create secret generic db-secret \
  --from-literal=password=secret-password
```

```yaml
# Use in Deployment
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: password
```

### Step 5: Horizontal Pod Autoscaler

Configure autoscaling:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

### Step 6: Ingress Configuration

Set up Ingress for external access:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - api.example.com
    secretName: my-app-tls
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app-service
            port:
              number: 80
```

### Step 7: Health Probes

Configure comprehensive health checks:

```yaml
# Liveness probe - container is running
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

# Readiness probe - container is ready to serve
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3

# Startup probe - container is starting
startupProbe:
  httpGet:
    path: /health/startup
    port: 8000
  initialDelaySeconds: 0
  periodSeconds: 10
  failureThreshold: 30
```

### Step 8: Resource Requests and Limits

Set appropriate resource constraints:

```yaml
resources:
  requests:
    memory: "256Mi"  # Guaranteed
    cpu: "250m"      # Guaranteed
  limits:
    memory: "512Mi"  # Maximum
    cpu: "500m"      # Maximum
```

### Step 9: Helm Chart Basics

Create a Helm chart:

```bash
helm create my-app
```

```yaml
# values.yaml
replicaCount: 3
image:
  repository: my-app
  tag: "1.0.0"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

```yaml
# {directories.templates}/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: app
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
```

```bash
# Install
helm install my-app ./my-app

# Upgrade
helm upgrade my-app ./my-app

# Uninstall
helm uninstall my-app
```

### Step 10: Kustomize Overlays

Use Kustomize for environment-specific configs:

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
commonLabels:
  app: my-app
```

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases:
- ../../base
replicas:
- name: my-app
  count: 5
patchesStrategicMerge:
- deployment-patch.yaml
```

```bash
# Apply
kubectl apply -k overlays/production
```

### Step 11: Rolling Updates

Configure rolling update strategy:

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Can create 1 extra pod
      maxUnavailable: 0  # Must have all pods available
```

## Best Practices

- Always set resource requests and limits
- Use health probes (liveness, readiness, startup)
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Set up HPA for autoscaling
- Use RollingUpdate strategy
- Label resources consistently
- Use namespaces for isolation
- Monitor resource usage
- Use Ingress for external access
- Enable TLS/SSL
- Use Helm or Kustomize for management
- Set appropriate replica counts
- Use anti-affinity for high availability

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No resource limits | Set requests and limits |
| Missing health probes | Add liveness/readiness probes |
| Secrets in ConfigMap | Use Secret resource |
| No autoscaling | Configure HPA |
| Single replica | Use multiple replicas |
| No rolling update | Configure RollingUpdate strategy |

## Related

- Knowledge: `{directories.knowledge}/kubernetes-deployment-patterns.json`
- Skill: `docker-deployment` for container images

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
