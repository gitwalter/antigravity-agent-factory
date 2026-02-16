---
description: Tactical Blueprint for ML Training, Deployment, and Monitoring. Focuses
  on production-grade PyTorch loops, distributed training, and MLOps observability.
name: ml-engineering-ops
type: skill
---
# Capability Manifest: ML Engineering Ops

This blueprint provides the **procedural truth** for moving AI models from research "experiments" into production-grade systems.

## When to Use

This skill should be used when completing tasks related to ml engineering ops.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Robust Training Loops (Accelerate/DeepSpeed)
1.  **State Management**: Use `Accelerator` from HuggingFace to handle distributed training, mixed precision (FP16/BF16), and gradient accumulation automatically.
2.  **Checkpoint Truth**: Always implement the `CheckpointManager` pattern. Save the `latest_checkpoint.pt` every epoch and the `best_model.pt` based on validation metrics.
3.  **Distributed Scale**: For large models, use DeepSpeed ZeRO-2/3 to shard parameters and optimizer states across multiple GPUs.

### Procedure 2: Serving & Inference Excellence
1.  **Containerized Serving**: Use `vLLM` or `TGI` for LLM serving to ensure high throughput and low-latency KV-cache management.
2.  **Schema Enforcement**: Wrap every model endpoint in a FastAPI Pydantic layer to validate input/output shapes before they hit the weights.
3.  **Health Gates**: Implement `/health` and `/ready` endpoints that verify GPU availability and model loading status.

### Procedure 3: Observability (Monitoring & Drift)
1.  **Experiment Tracking**: Every training run must be logged to MLflow or Weights & Biases, including hyperparameters, system metrics (GPU util), and loss curves.
2.  **Production Tracing**: Use LangSmith or equivalent to trace every inference request. Monitor for "Hallucination" and "Safety" scores at scale.
3.  **Drift Detection**: Set up automated evaluations to compare the "Inference Truth" against the "Training Distribution" to detect semantic drift.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **CUDA Out of Memory** | Batch size too large or memory leak. | Enable `gradient_accumulation_steps`; reduce micro-batch size; check for untracked tensors in the loop. |
| **NaN Loss** | High learning rate or unstable gradients. | Reduce LR; enable Gradient Clipping; verify input normalization. |
| **Drift Alert** | Model performing poorly on new data. | Trigger the "Fine-Tuning Loop": Collect the failure cases, augment the dataset, and run a versioned fine-tuning job. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Run Training | `accelerate launch train.py` |
| Serving | `python -m vllm.entrypoints.openai.api_server` |
| Log Metrics | `mlflow server --host 0.0.0.0` |
| Security Audit | `pip-audit` |

## Best Practices
Before deploying:
- [ ] Training is reproducible via `pyproject.toml` and pinned seeds.
- [ ] Checkpointing and Resume logic verified.
- [ ] Health checks and Pydantic validation active.
- [ ] Trace analysis active (LangSmith).
