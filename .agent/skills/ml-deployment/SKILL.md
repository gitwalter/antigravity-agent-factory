---
description: Deploy ML models to production with Docker, Kubernetes, cloud platforms,
  and edge devices
name: ml-deployment
type: skill
---

# Ml Deployment

Deploy ML models to production with Docker, Kubernetes, cloud platforms, and edge devices

## 
# ML Deployment Skill

Deploy machine learning models to production environments using containerization, orchestration, and cloud platforms with GPU support.

## 
# ML Deployment Skill

Deploy machine learning models to production environments using containerization, orchestration, and cloud platforms with GPU support.

## Process
### Step 1: Dockerfile for ML with GPU Support

```dockerfile
# Dockerfile.ml
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files (use .dockerignore to exclude large files)
COPY models/ ./models/

# Copy application code
COPY app/ ./app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile.ml.multistage (optimized)
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy model cache (pre-downloaded models)
COPY --from=builder /root/.cache/huggingface ./models/cache

# Copy application
COPY app/ ./app/
COPY models/ ./models/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Kubernetes GPU Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-serving
  labels:
    app: ml-inference
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml-inference
  template:
    metadata:
      labels:
        app: ml-inference
    spec:
      containers:
      - name: model-server
        image: your-registry/ml-model:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            nvidia.com/gpu: 1
            memory: "8Gi"
            cpu: "4"
          limits:
            nvidia.com/gpu: 1
            memory: "16Gi"
            cpu: "8"
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        - name: MODEL_PATH
          value: "/app/models/model.pth"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-inference
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Step 3: Kubernetes GPU Scheduling with Kueue

```yaml
# kueue-config.yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: gpu-flavor
spec:
  nodeLabels:
    nvidia.com/gpu.product: "A100"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: gpu-queue
spec:
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    - name: gpu-flavor
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 4
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: ml-queue
  namespace: default
spec:
  clusterQueue: gpu-queue
---
apiVersion: batch/v1
kind: Job
metadata:
  name: ml-training-job
  namespace: default
spec:
  parallelism: 1
  completions: 1
  template:
    metadata:
      labels:
        kueue.x-k8s.io/queue-name: ml-queue
    spec:
      containers:
      - name: training
        image: ml-training:latest
        resources:
          requests:
            nvidia.com/gpu: 1
          limits:
            nvidia.com/gpu: 1
      restartPolicy: Never
```

### Step 4: AWS SageMaker Deployment

```python
# sagemaker_deploy.py
import boto3
import sagemaker
from sagemaker.huggingface import HuggingFaceModel, HuggingFacePredictor
from sagemaker.serverless import ServerlessInferenceConfig

def deploy_to_sagemaker(
    model_id: str,
    instance_type: str = "ml.g5.xlarge",
    serverless: bool = False,
):
    """Deploy model to SageMaker."""
    
    role = sagemaker.get_execution_role()
    sess = sagemaker.Session()
    
    # Create HuggingFace model
    huggingface_model = HuggingFaceModel(
        model_data=f"s3://your-bucket/models/{model_id}/",
        role=role,
        transformers_version="4.37",
        pytorch_version="2.1",
        py_version="py310",
        entry_point="inference.py",
        source_dir="code/",
        env={
            "HF_MODEL_ID": model_id,
            "HF_TASK": "text-generation",
        },
    )
    
    if serverless:
        # Serverless deployment
        predictor = huggingface_model.deploy(
            serverless_inference_config=ServerlessInferenceConfig(
                memory_size_in_mb=4096,
                max_concurrency=10,
            ),
        )
    else:
        # Real-time endpoint
        predictor = huggingface_model.deploy(
            initial_instance_count=1,
            instance_type=instance_type,
            endpoint_name=f"{model_id}-endpoint",
        )
    
    return predictor

# Invoke endpoint
def invoke_sagemaker(predictor, prompt: str):
    """Invoke SageMaker endpoint."""
    response = predictor.predict({
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
        },
    })
    return response

# Cleanup
def delete_endpoint(predictor):
    """Delete SageMaker endpoint."""
    predictor.delete_model()
    predictor.delete_endpoint()
```

### Step 5: GCP Vertex AI Deployment

```python
# vertex_ai_deploy.py
from google.cloud import aiplatform
from google.cloud.aiplatform import models, endpoints

def deploy_to_vertex_ai(
    model_path: str,
    project_id: str,
    region: str = "us-central1",
):
    """Deploy model to Vertex AI."""
    
    aiplatform.init(project=project_id, location=region)
    
    # Upload model
    model = models.Model.upload(
        display_name="llm-model",
        artifact_uri=model_path,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/pytorch-gpu.1-13:latest",
    )
    
    # Create endpoint
    endpoint = endpoints.Endpoint.create(
        display_name="llm-endpoint",
    )
    
    # Deploy model to endpoint
    endpoint.deploy(
        model=model,
        deployed_model_display_name="llm-deployment",
        machine_type="n1-standard-4",
        accelerator_type="NVIDIA_TESLA_T4",
        accelerator_count=1,
        min_replica_count=1,
        max_replica_count=3,
        traffic_percentage=100,
    )
    
    return endpoint

# Predict
def predict_vertex_ai(endpoint, instances):
    """Make prediction with Vertex AI endpoint."""
    predictions = endpoint.predict(instances=instances)
    return predictions
```

### Step 6: Serverless GPU with Modal

```python
# modal_deploy.py
import modal

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "torch",
        "transformers",
        "accelerate",
    )
    .env({"HF_HOME": "/cache"})
)

stub = modal.Stub("ml-inference")

@stub.cls(
    image=image,
    gpu="A10G",
    container_idle_timeout=300,
    timeout=600,
)
class ModelInference:
    def __enter__(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2",
            cache_dir="/cache",
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2",
            cache_dir="/cache",
            device_map="auto",
        )
    
    @modal.method
    def generate(self, prompt: str, max_tokens: int = 512):
        """Generate text."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Deploy: modal deploy modal_deploy.py
# Call: ModelInference().generate.remote("Hello, world!")
```

### Step 7: ONNX Export for Edge Deployment

```python
# onnx_export.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import onnx
import onnxruntime as ort

def export_to_onnx(
    model_name: str,
    output_path: str = "model.onnx",
    max_seq_length: int = 512,
):
    """Export HuggingFace model to ONNX."""
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    
    # Create dummy input
    dummy_input = tokenizer(
        "Hello, world!",
        return_tensors="pt",
        max_length=max_seq_length,
        padding="max_length",
    )
    
    # Export
    torch.onnx.export(
        model,
        (dummy_input["input_ids"],),
        output_path,
        input_names=["input_ids"],
        output_names=["logits"],
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence_length"},
            "logits": {0: "batch_size", 1: "sequence_length"},
        },
        opset_version=14,
    )
    
    # Verify
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)
    
    return output_path

def run_onnx_inference(model_path: str, input_text: str):
    """Run inference with ONNX Runtime."""
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    
    # Prepare input
    inputs = tokenizer(input_text, return_tensors="np")
    
    # Create ONNX Runtime session
    session = ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"],  # or CUDAExecutionProvider
    )
    
    # Run inference
    outputs = session.run(
        None,
        {"input_ids": inputs["input_ids"].astype("int64")},
    )
    
    # Decode
    logits = outputs[0]
    predicted_ids = logits.argmax(axis=-1)
    return tokenizer.decode(predicted_ids[0], skip_special_tokens=True)
```

```dockerfile
# Dockerfile.ml
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files (use .dockerignore to exclude large files)
COPY models/ ./models/

# Copy application code
COPY app/ ./app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile.ml.multistage (optimized)
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy model cache (pre-downloaded models)
COPY --from=builder /root/.cache/huggingface ./models/cache

# Copy application
COPY app/ ./app/
COPY models/ ./models/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-serving
  labels:
    app: ml-inference
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml-inference
  template:
    metadata:
      labels:
        app: ml-inference
    spec:
      containers:
      - name: model-server
        image: your-registry/ml-model:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            nvidia.com/gpu: 1
            memory: "8Gi"
            cpu: "4"
          limits:
            nvidia.com/gpu: 1
            memory: "16Gi"
            cpu: "8"
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        - name: MODEL_PATH
          value: "/app/models/model.pth"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-inference
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

```yaml
# kueue-config.yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: gpu-flavor
spec:
  nodeLabels:
    nvidia.com/gpu.product: "A100"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: gpu-queue
spec:
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    - name: gpu-flavor
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 4
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: ml-queue
  namespace: default
spec:
  clusterQueue: gpu-queue
---
apiVersion: batch/v1
kind: Job
metadata:
  name: ml-training-job
  namespace: default
spec:
  parallelism: 1
  completions: 1
  template:
    metadata:
      labels:
        kueue.x-k8s.io/queue-name: ml-queue
    spec:
      containers:
      - name: training
        image: ml-training:latest
        resources:
          requests:
            nvidia.com/gpu: 1
          limits:
            nvidia.com/gpu: 1
      restartPolicy: Never
```

```python
# sagemaker_deploy.py
import boto3
import sagemaker
from sagemaker.huggingface import HuggingFaceModel, HuggingFacePredictor
from sagemaker.serverless import ServerlessInferenceConfig

def deploy_to_sagemaker(
    model_id: str,
    instance_type: str = "ml.g5.xlarge",
    serverless: bool = False,
):
    """Deploy model to SageMaker."""
    
    role = sagemaker.get_execution_role()
    sess = sagemaker.Session()
    
    # Create HuggingFace model
    huggingface_model = HuggingFaceModel(
        model_data=f"s3://your-bucket/models/{model_id}/",
        role=role,
        transformers_version="4.37",
        pytorch_version="2.1",
        py_version="py310",
        entry_point="inference.py",
        source_dir="code/",
        env={
            "HF_MODEL_ID": model_id,
            "HF_TASK": "text-generation",
        },
    )
    
    if serverless:
        # Serverless deployment
        predictor = huggingface_model.deploy(
            serverless_inference_config=ServerlessInferenceConfig(
                memory_size_in_mb=4096,
                max_concurrency=10,
            ),
        )
    else:
        # Real-time endpoint
        predictor = huggingface_model.deploy(
            initial_instance_count=1,
            instance_type=instance_type,
            endpoint_name=f"{model_id}-endpoint",
        )
    
    return predictor

# Invoke endpoint
def invoke_sagemaker(predictor, prompt: str):
    """Invoke SageMaker endpoint."""
    response = predictor.predict({
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
        },
    })
    return response

# Cleanup
def delete_endpoint(predictor):
    """Delete SageMaker endpoint."""
    predictor.delete_model()
    predictor.delete_endpoint()
```

```python
# vertex_ai_deploy.py
from google.cloud import aiplatform
from google.cloud.aiplatform import models, endpoints

def deploy_to_vertex_ai(
    model_path: str,
    project_id: str,
    region: str = "us-central1",
):
    """Deploy model to Vertex AI."""
    
    aiplatform.init(project=project_id, location=region)
    
    # Upload model
    model = models.Model.upload(
        display_name="llm-model",
        artifact_uri=model_path,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/pytorch-gpu.1-13:latest",
    )
    
    # Create endpoint
    endpoint = endpoints.Endpoint.create(
        display_name="llm-endpoint",
    )
    
    # Deploy model to endpoint
    endpoint.deploy(
        model=model,
        deployed_model_display_name="llm-deployment",
        machine_type="n1-standard-4",
        accelerator_type="NVIDIA_TESLA_T4",
        accelerator_count=1,
        min_replica_count=1,
        max_replica_count=3,
        traffic_percentage=100,
    )
    
    return endpoint

# Predict
def predict_vertex_ai(endpoint, instances):
    """Make prediction with Vertex AI endpoint."""
    predictions = endpoint.predict(instances=instances)
    return predictions
```

```python
# modal_deploy.py
import modal

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "torch",
        "transformers",
        "accelerate",
    )
    .env({"HF_HOME": "/cache"})
)

stub = modal.Stub("ml-inference")

@stub.cls(
    image=image,
    gpu="A10G",
    container_idle_timeout=300,
    timeout=600,
)
class ModelInference:
    def __enter__(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2",
            cache_dir="/cache",
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2",
            cache_dir="/cache",
            device_map="auto",
        )
    
    @modal.method
    def generate(self, prompt: str, max_tokens: int = 512):
        """Generate text."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Deploy: modal deploy modal_deploy.py
# Call: ModelInference().generate.remote("Hello, world!")
```

```python
# onnx_export.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import onnx
import onnxruntime as ort

def export_to_onnx(
    model_name: str,
    output_path: str = "model.onnx",
    max_seq_length: int = 512,
):
    """Export HuggingFace model to ONNX."""
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    
    # Create dummy input
    dummy_input = tokenizer(
        "Hello, world!",
        return_tensors="pt",
        max_length=max_seq_length,
        padding="max_length",
    )
    
    # Export
    torch.onnx.export(
        model,
        (dummy_input["input_ids"],),
        output_path,
        input_names=["input_ids"],
        output_names=["logits"],
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence_length"},
            "logits": {0: "batch_size", 1: "sequence_length"},
        },
        opset_version=14,
    )
    
    # Verify
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)
    
    return output_path

def run_onnx_inference(model_path: str, input_text: str):
    """Run inference with ONNX Runtime."""
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    
    # Prepare input
    inputs = tokenizer(input_text, return_tensors="np")
    
    # Create ONNX Runtime session
    session = ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"],  # or CUDAExecutionProvider
    )
    
    # Run inference
    outputs = session.run(
        None,
        {"input_ids": inputs["input_ids"].astype("int64")},
    )
    
    # Decode
    logits = outputs[0]
    predicted_ids = logits.argmax(axis=-1)
    return tokenizer.decode(predicted_ids[0], skip_special_tokens=True)
```

## Output
- Containerized ML models with GPU support
- Kubernetes deployments with resource management
- Cloud platform integrations
- Serverless GPU inference setup
- Edge-optimized ONNX models

## Best Practices
- Use multi-stage Docker builds to reduce image size
- Cache model downloads in Docker layers
- Set appropriate resource requests/limits in K8s
- Use Kueue for GPU resource scheduling
- Enable health checks and auto-scaling
- Export to ONNX for edge deployment
- Use serverless GPU for cost optimization
- Monitor GPU utilization and costs

## Related
- Skill: `model-serving`
- Skill: `ml-monitoring`
- Skill: `ai-cost-optimization`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: boto3, google-cloud-aiplatform, azure-ai-ml, onnx, onnxruntime
> - Knowledge: cloud-ml-deployment.json, kubernetes-ml-patterns.json
