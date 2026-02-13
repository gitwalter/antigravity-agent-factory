---
description: Production model serving with vLLM, TGI, Ollama, Triton, FastAPI endpoints,
  batching, and GPU optimization
name: model-serving
type: skill
---
# Model Serving

Production model serving with vLLM, TGI, Ollama, Triton, FastAPI endpoints, batching, and GPU optimization

Deploy and serve ML models in production with optimized inference engines, GPU memory management, and scalable API endpoints.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: vLLM Server Setup

vLLM provides PagedAttention and continuous batching for efficient LLM serving.

```python
# vllm_server.py
from vllm import LLM, SamplingParams
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="vLLM Inference Server")

# Initialize vLLM engine
llm = LLM(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    tensor_parallel_size=1,  # Increase for multi-GPU
    gpu_memory_utilization=0.9,  # Use 90% of GPU memory
    max_model_len=4096,  # Context length
    trust_remote_code=True,
    enable_prefix_caching=True,  # Cache common prefixes
)

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    stop: Optional[List[str]] = None

class CompletionResponse(BaseModel):
    text: str
    finish_reason: str
    tokens: int

@app.post("/v1/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest):
    """Generate completion with vLLM."""
    try:
        sampling_params = SamplingParams(
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens,
            stop=request.stop,
        )
        
        outputs = llm.generate([request.prompt], sampling_params)
        output = outputs[0]
        
        return CompletionResponse(
            text=output.outputs[0].text,
            finish_reason=output.outputs[0].finish_reason,
            tokens=len(output.outputs[0].token_ids),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/completions/batch")
async def create_completion_batch(requests: List[CompletionRequest]):
    """Batch completion endpoint for multiple prompts."""
    sampling_params = SamplingParams(
        temperature=requests[0].temperature,
        top_p=requests[0].top_p,
        max_tokens=requests[0].max_tokens,
    )
    
    prompts = [req.prompt for req in requests]
    outputs = llm.generate(prompts, sampling_params)
    
    return [
        {
            "text": output.outputs[0].text,
            "finish_reason": output.outputs[0].finish_reason,
        }
        for output in outputs
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 2: Text Generation Inference (TGI) Deployment

TGI provides optimized serving with token streaming and Flash Attention.

```python
# tgi_client.py
import requests
import json
from typing import Iterator

class TGIClient:
    """Client for HuggingFace Text Generation Inference server."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
    
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False,
    ) -> str | Iterator[str]:
        """Generate text with TGI server."""
        url = f"{self.base_url}/generate"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": True,
            },
        }
        
        if stream:
            payload["parameters"]["details"] = True
            response = requests.post(
                url,
                json=payload,
                stream=True,
                headers={"Content-Type": "application/json"},
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "token" in data:
                        yield data["token"]["text"]
        else:
            response = requests.post(url, json=payload)
            return response.json()["generated_text"]

# TGI server startup (run in terminal):
# docker run --gpus all -p 8080:80 \
#   -v $PWD/models:/data \
#   ghcr.io/huggingface/text-generation-inference:latest \
#   --model-id mistralai/Mistral-7B-Instruct-v0.2 \
#   --num-shard 1 \
#   --max-batch-total-tokens 4096
```

### Step 3: Ollama for Local Development

Ollama provides lightweight local model serving.

```python
# ollama_client.py
import requests
from typing import Iterator, Optional

class OllamaClient:
    """Client for Ollama local model server."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        system: Optional[str] = None,
    ) -> str | Iterator[str]:
        """Generate with Ollama."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
        }
        if system:
            payload["system"] = system
        
        response = requests.post(url, json=payload, stream=stream)
        
        if stream:
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
                    if data.get("done"):
                        break
        else:
            return response.json()["response"]
    
    def pull_model(self, model: str):
        """Pull model from Ollama registry."""
        url = f"{self.base_url}/api/pull"
        response = requests.post(url, json={"name": model}, stream=True)
        for line in response.iter_lines():
            if line:
                print(json.loads(line))

# Usage:
# client = OllamaClient()
# client.pull_model("llama2:7b")
# response = client.generate("llama2:7b", "Explain quantum computing")
```

### Step 4: FastAPI Model Endpoint with Batching

```python
# fastapi_batch_server.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from collections import deque
import asyncio
import time

app = FastAPI()

class BatchQueue:
    """Batching queue for efficient inference."""
    
    def __init__(self, batch_size: int = 8, timeout: float = 0.1):
        self.batch_size = batch_size
        self.timeout = timeout
        self.queue = deque()
        self.lock = asyncio.Lock()
    
    async def add_request(self, request: dict) -> asyncio.Future:
        """Add request to batch queue."""
        future = asyncio.Future()
        async with self.lock:
            self.queue.append((request, future))
        return future
    
    async def get_batch(self) -> List[tuple]:
        """Get batch of requests."""
        await asyncio.sleep(self.timeout)
        async with self.lock:
            batch = []
            for _ in range(min(self.batch_size, len(self.queue))):
                if self.queue:
                    batch.append(self.queue.popleft())
            return batch

batch_queue = BatchQueue(batch_size=8, timeout=0.1)

class InferenceRequest(BaseModel):
    prompt: str
    max_tokens: int = 512

class InferenceResponse(BaseModel):
    text: str
    latency_ms: float

async def process_batch(batch: List[tuple], model):
    """Process batch of requests."""
    requests = [req for req, _ in batch]
    futures = [future for _, future in batch]
    
    # Batch inference
    prompts = [req["prompt"] for req in requests]
    start_time = time.time()
    
    # Simulate batch inference
    results = await asyncio.gather(*[
        model.generate(prompt) for prompt in prompts
    ])
    
    latency = (time.time() - start_time) * 1000
    
    # Set results
    for future, result in zip(futures, results):
        future.set_result({
            "text": result,
            "latency_ms": latency / len(batch),
        })

@app.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    """Inference endpoint with automatic batching."""
    future = await batch_queue.add_request(request.dict())
    result = await future
    return InferenceResponse(**result)
```

### Step 5: GPU Memory Tuning

```python
# gpu_memory_tuning.py
import torch
from vllm import LLM

def optimize_gpu_memory(
    model_name: str,
    available_memory_gb: float,
    context_length: int = 4096,
):
    """Configure vLLM for optimal GPU memory usage."""
    
    # Calculate optimal settings
    if available_memory_gb < 16:
        # Small GPU: Use quantization
        quantization = "awq"  # or "gptq"
        gpu_memory_utilization = 0.85
        max_model_len = 2048
    elif available_memory_gb < 24:
        # Medium GPU
        quantization = None
        gpu_memory_utilization = 0.9
        max_model_len = 4096
    else:
        # Large GPU
        quantization = None
        gpu_memory_utilization = 0.95
        max_model_len = 8192
    
    llm = LLM(
        model=model_name,
        quantization=quantization,
        gpu_memory_utilization=gpu_memory_utilization,
        max_model_len=max_model_len,
        enable_prefix_caching=True,
        enable_chunked_prefill=True,  # For long contexts
    )
    
    return llm

# Monitor GPU usage
def monitor_gpu():
    """Monitor GPU memory usage."""
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            allocated = torch.cuda.memory_allocated(i) / 1e9
            reserved = torch.cuda.memory_reserved(i) / 1e9
            total = props.total_memory / 1e9
            
            print(f"GPU {i}: {allocated:.2f}GB allocated, "
                  f"{reserved:.2f}GB reserved, {total:.2f}GB total")
```

### Step 6: Load Balancing Pattern

```python
# load_balancer.py
from fastapi import FastAPI, HTTPException
import httpx
from typing import List
import random

class ModelLoadBalancer:
    """Load balancer for multiple model instances."""
    
    def __init__(self, endpoints: List[str]):
        self.endpoints = endpoints
        self.client = httpx.AsyncClient(timeout=30.0)
        self.health_status = {endpoint: True for endpoint in endpoints}
    
    async def health_check(self, endpoint: str) -> bool:
        """Check if endpoint is healthy."""
        try:
            response = await self.client.get(f"{endpoint}/health")
            return response.status_code == 200
        except:
            return False
    
    async def select_endpoint(self) -> str:
        """Select healthy endpoint using round-robin."""
        healthy = [
            ep for ep in self.endpoints
            if self.health_status.get(ep, False)
        ]
        
        if not healthy:
            raise HTTPException(status_code=503, detail="No healthy endpoints")
        
        return random.choice(healthy)  # Simple random, can use weighted
    
    async def forward_request(self, path: str, payload: dict):
        """Forward request to selected endpoint."""
        endpoint = await self.select_endpoint()
        url = f"{endpoint}{path}"
        
        try:
            response = await self.client.post(url, json=payload)
            return response.json()
        except Exception as e:
            self.health_status[endpoint] = False
            raise HTTPException(status_code=502, detail=str(e))

# Usage in FastAPI
app = FastAPI()
balancer = ModelLoadBalancer([
    "http://model-1:8000",
    "http://model-2:8000",
    "http://model-3:8000",
])

@app.post("/generate")
async def generate(prompt: str):
    """Generate with load balancing."""
    return await balancer.forward_request(
        "/v1/completions",
        {"prompt": prompt}
    )
```

## Output

- Production-ready model serving endpoints
- Optimized GPU memory configuration
- Batching strategies for throughput
- Load balancing across instances
- Health monitoring and failover

## Best Practices

- Use vLLM for production LLM serving (PagedAttention)
- Enable prefix caching for repeated prompts
- Batch requests to maximize GPU utilization
- Monitor GPU memory and adjust `gpu_memory_utilization`
- Use quantization (AWQ/GPTQ) for smaller GPUs
- Implement health checks and load balancing
- Set appropriate timeouts for batch processing

## Related

- Skill: `ml-deployment`
- Skill: `ml-monitoring`
- Skill: `ai-cost-optimization`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
