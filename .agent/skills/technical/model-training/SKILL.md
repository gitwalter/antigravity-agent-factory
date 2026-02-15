---
description: PyTorch training loops, distributed training with DeepSpeed/FSDP, hyperparameter
  tuning with Optuna, experiment tracking, mixed precision training, checkpointing
name: model-training
type: skill
---
# Model Training

PyTorch training loops, distributed training with DeepSpeed/FSDP, hyperparameter tuning with Optuna, experiment tracking, mixed precision training, checkpointing

Implement production-ready PyTorch training loops with modern patterns including Accelerate, distributed training (DeepSpeed/FSDP), hyperparameter optimization with Optuna, experiment tracking, mixed precision training, and robust checkpointing strategies.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Modern PyTorch Training Loop with Accelerate

Use Accelerate for simplified distributed training:

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from accelerate import Accelerator
from accelerate.utils import set_seed
import os

class SimpleDataset(Dataset):
    """Example dataset."""
    def __init__(self, size=1000):
        self.data = torch.randn(size, 10)
        self.labels = torch.randint(0, 2, (size,))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

class SimpleModel(nn.Module):
    """Example model."""
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def train_with_accelerate(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    num_epochs: int = 10,
    learning_rate: float = 1e-3,
    checkpoint_dir: str = "./checkpoints"
):
    """Training loop with Accelerate."""
    # Initialize accelerator
    accelerator = Accelerator(
        gradient_accumulation_steps=4,
        mixed_precision="fp16",  # or "bf16" or None
        log_with="tensorboard",  # or "wandb", "mlflow"
        project_dir="./logs"
    )

    # Set seed for reproducibility
    set_seed(42)

    # Prepare model, optimizer, and dataloader
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    model, optimizer, train_loader, val_loader = accelerator.prepare(
        model, optimizer, train_loader, val_loader
    )

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch_idx, (data, target) in enumerate(train_loader):
            # Forward pass
            outputs = model(data)
            loss = criterion(outputs, target)

            # Backward pass with gradient accumulation
            accelerator.backward(loss)

            # Optimizer step (only after accumulation)
            if (batch_idx + 1) % accelerator.gradient_accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()

            total_loss += loss.item()

            # Logging
            if batch_idx % 100 == 0:
                accelerator.log(
                    {"train_loss": loss.item()},
                    step=epoch * len(train_loader) + batch_idx
                )

        # Validation
        model.eval()
        val_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for data, target in val_loader:
                outputs = model(data)
                loss = criterion(outputs, target)
                val_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()

        avg_train_loss = total_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        accuracy = 100 * correct / total

        accelerator.log({
            "epoch": epoch,
            "train_loss": avg_train_loss,
            "val_loss": avg_val_loss,
            "val_accuracy": accuracy
        }, step=epoch)

        # Save checkpoint
        if accelerator.is_main_process:
            checkpoint_path = os.path.join(checkpoint_dir, f"checkpoint_epoch_{epoch}.pt")
            accelerator.save_state(checkpoint_path)

            # Save best model
            if epoch == 0 or accuracy > best_accuracy:
                best_accuracy = accuracy
                accelerator.save_model(model, os.path.join(checkpoint_dir, "best_model.pt"))

        accelerator.print(f"Epoch {epoch}: Train Loss={avg_train_loss:.4f}, "
                         f"Val Loss={avg_val_loss:.4f}, Accuracy={accuracy:.2f}%")

    accelerator.end_training()

# Usage
model = SimpleModel()
train_dataset = SimpleDataset(size=1000)
val_dataset = SimpleDataset(size=200)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

train_with_accelerate(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    num_epochs=10,
    learning_rate=1e-3
)
```

### Step 2: Distributed Training with DeepSpeed

Implement DeepSpeed ZeRO for large model training:

```python
import deepspeed
from deepspeed.ops.adam import FusedAdam
import json

def create_deepspeed_config(
    zero_stage: int = 2,
    offload_optimizer: bool = False,
    offload_param: bool = False,
    gradient_accumulation_steps: int = 1,
    train_batch_size: int = 32,
    learning_rate: float = 1e-3
) -> dict:
    """Create DeepSpeed configuration."""
    config = {
        "train_batch_size": train_batch_size,
        "train_micro_batch_size_per_gpu": train_batch_size,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "optimizer": {
            "type": "AdamW",
            "params": {
                "lr": learning_rate,
                "betas": [0.9, 0.999],
                "eps": 1e-8,
                "weight_decay": 0.01
            }
        },
        "scheduler": {
            "type": "WarmupLR",
            "params": {
                "warmup_min_lr": 0,
                "warmup_max_lr": learning_rate,
                "warmup_num_steps": 1000
            }
        },
        "zero_optimization": {
            "stage": zero_stage,
            "offload_optimizer": {
                "device": "cpu" if offload_optimizer else "none"
            },
            "offload_param": {
                "device": "cpu" if offload_param else "none"
            },
            "overlap_comm": True,
            "contiguous_gradients": True,
            "sub_group_size": 1e9,
            "reduce_bucket_size": "auto",
            "stage3_prefetch_bucket_size": "auto",
            "stage3_param_persistence_threshold": "auto",
            "stage3_max_live_parameters": 1e9,
            "stage3_max_reuse_distance": 1e9,
            "stage3_gather_16bit_weights_on_model_save": True
        },
        "gradient_clipping": 1.0,
        "fp16": {
            "enabled": True,
            "loss_scale": 0,
            "loss_scale_window": 1000,
            "initial_scale_power": 16,
            "hysteresis": 2,
            "min_loss_scale": 1
        },
        "wall_clock_breakdown": False
    }
    return config

def train_with_deepspeed(
    model: nn.Module,
    train_loader: DataLoader,
    config_path: str = "deepspeed_config.json"
):
    """Training with DeepSpeed."""
    # Save config
    config = create_deepspeed_config(zero_stage=2, offload_optimizer=False)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # Initialize DeepSpeed
    model_engine, optimizer, train_loader, _ = deepspeed.initialize(
        model=model,
        model_parameters=model.parameters(),
        training_data=train_dataset,
        config=config_path
    )

    # Training loop
    for epoch in range(num_epochs):
        model_engine.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            # Forward pass
            outputs = model_engine(data)
            loss = criterion(outputs, target)

            # Backward pass
            model_engine.backward(loss)

            # Optimizer step
            model_engine.step()

            # Logging
            if batch_idx % 100 == 0:
                print(f"Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item()}")

        # Save checkpoint
        model_engine.save_checkpoint(
            save_dir=f"./checkpoints/epoch_{epoch}",
            tag=f"epoch_{epoch}"
        )
```

### Step 3: Distributed Training with FSDP (Fully Sharded Data Parallel)

Use PyTorch FSDP for efficient distributed training:

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
import torch.distributed as dist

def train_with_fsdp(
    model: nn.Module,
    train_loader: DataLoader,
    num_epochs: int = 10
):
    """Training with FSDP."""
    # Initialize distributed
    dist.init_process_group(backend="nccl")

    # Auto-wrap policy for transformer layers
    auto_wrap_policy = transformer_auto_wrap_policy

    # Create FSDP model
    model = FSDP(
        model,
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        auto_wrap_policy=auto_wrap_policy,
        mixed_precision=torch.distributed.fsdp.MixedPrecision(
            param_dtype=torch.float16,
            reduce_dtype=torch.float16,
            buffer_dtype=torch.float16
        ),
        device_id=torch.cuda.current_device()
    )

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data = data.cuda()
            target = target.cuda()

            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, target)
            loss.backward()
            optimizer.step()

            if batch_idx % 100 == 0:
                print(f"Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item()}")

        # Save checkpoint
        if dist.get_rank() == 0:
            save_policy = torch.distributed.fsdp.FullStateDictConfig(offload_to_cpu=True)
            with FSDP.state_dict_type(model, StateDictType.FULL_STATE_DICT, save_policy):
                state_dict = model.state_dict()
                torch.save(state_dict, f"./checkpoints/epoch_{epoch}.pt")

    dist.destroy_process_group()
```

### Step 4: Hyperparameter Tuning with Optuna

Systematic hyperparameter optimization:

```python
import optuna
from optuna.trial import TrialState
import joblib

def objective(trial: optuna.Trial, train_loader: DataLoader, val_loader: DataLoader):
    """Optuna objective function."""
    # Suggest hyperparameters
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-2)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64, 128])
    weight_decay = trial.suggest_loguniform("weight_decay", 1e-6, 1e-3)
    dropout_rate = trial.suggest_uniform("dropout_rate", 0.0, 0.5)

    # Create model with suggested dropout
    model = SimpleModel()
    # Add dropout layers based on dropout_rate

    # Create optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay
    )

    # Training loop (simplified)
    num_epochs = 5  # Fewer epochs for hyperparameter search
    best_val_loss = float("inf")

    for epoch in range(num_epochs):
        model.train()
        for data, target in train_loader:
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, target)
            loss.backward()
            optimizer.step()

        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for data, target in val_loader:
                outputs = model(data)
                loss = criterion(outputs, target)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)

        # Report intermediate value
        trial.report(avg_val_loss, epoch)

        # Pruning
        if trial.should_prune():
            raise optuna.TrialPruned()

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss

    return best_val_loss

def run_hyperparameter_search(
    train_loader: DataLoader,
    val_loader: DataLoader,
    n_trials: int = 50,
    study_name: str = "hyperparameter_study"
):
    """Run hyperparameter optimization."""
    # Create study
    study = optuna.create_study(
        direction="minimize",
        study_name=study_name,
        pruner=optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=3)
    )

    # Optimize
    study.optimize(
        lambda trial: objective(trial, train_loader, val_loader),
        n_trials=n_trials,
        timeout=3600  # 1 hour timeout
    )

    # Print results
    print("Number of finished trials: ", len(study.trials))
    print("Number of pruned trials: ", len([t for t in study.trials if t.state == TrialState.PRUNED]))
    print("Number of complete trials: ", len([t for t in study.trials if t.state == TrialState.COMPLETE]))

    print("\nBest trial:")
    trial = study.best_trial
    print(f"  Value: {trial.value}")
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")

    # Save study
    joblib.dump(study, f"{study_name}.pkl")

    # Visualize
    try:
        import optuna.visualization as vis
        fig = vis.plot_optimization_history(study)
        fig.show()
    except:
        pass

    return study

# Usage
study = run_hyperparameter_search(train_loader, val_loader, n_trials=50)
best_params = study.best_params
```

### Step 5: Experiment Tracking with MLflow

Track experiments and metrics:

```python
import mlflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient

def train_with_mlflow(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    experiment_name: str = "model_training",
    run_name: str = None
):
    """Training with MLflow tracking."""
    # Set experiment
    mlflow.set_experiment(experiment_name)

    # Start run
    with mlflow.start_run(run_name=run_name):
        # Log hyperparameters
        mlflow.log_params({
            "learning_rate": 1e-3,
            "batch_size": 32,
            "num_epochs": 10,
            "optimizer": "AdamW"
        })

        # Training loop
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
        criterion = nn.CrossEntropyLoss()

        for epoch in range(10):
            model.train()
            train_loss = 0

            for data, target in train_loader:
                optimizer.zero_grad()
                outputs = model(data)
                loss = criterion(outputs, target)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()

            # Validation
            model.eval()
            val_loss = 0
            correct = 0
            total = 0

            with torch.no_grad():
                for data, target in val_loader:
                    outputs = model(data)
                    loss = criterion(outputs, target)
                    val_loss += loss.item()

                    _, predicted = torch.max(outputs.data, 1)
                    total += target.size(0)
                    correct += (predicted == target).sum().item()

            # Log metrics
            mlflow.log_metrics({
                "train_loss": train_loss / len(train_loader),
                "val_loss": val_loss / len(val_loader),
                "val_accuracy": 100 * correct / total
            }, step=epoch)

        # Log model
        mlflow.pytorch.log_model(model, "model")

        # Log artifacts
        mlflow.log_artifact("./checkpoints/best_model.pt")

        # Register model (optional)
        mlflow.pytorch.log_model(
            model,
            "model",
            registered_model_name="SimpleModel"
        )

    print(f"MLflow run completed. View at: {mlflow.get_tracking_uri()}")

# Usage
train_with_mlflow(model, train_loader, val_loader, experiment_name="my_experiment")
```

### Step 6: Mixed Precision Training

Implement automatic mixed precision (AMP):

```python
from torch.cuda.amp import autocast, GradScaler

def train_with_amp(
    model: nn.Module,
    train_loader: DataLoader,
    num_epochs: int = 10
):
    """Training with automatic mixed precision."""
    model = model.cuda()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()
    scaler = GradScaler()  # For gradient scaling

    for epoch in range(num_epochs):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.cuda(), target.cuda()

            optimizer.zero_grad()

            # Forward pass with autocast
            with autocast():
                outputs = model(data)
                loss = criterion(outputs, target)

            # Backward pass with scaler
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            if batch_idx % 100 == 0:
                print(f"Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item()}")
```

### Step 7: Checkpointing and Resume Strategies

Robust checkpointing with resume capability:

```python
import os
from pathlib import Path

class CheckpointManager:
    """Manage model checkpoints and resume training."""

    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.best_loss = float("inf")

    def save_checkpoint(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        epoch: int,
        loss: float,
        is_best: bool = False,
        metadata: dict = None
    ):
        """Save checkpoint."""
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": loss,
            "best_loss": self.best_loss,
            "metadata": metadata or {}
        }

        # Save regular checkpoint
        checkpoint_path = self.checkpoint_dir / f"checkpoint_epoch_{epoch}.pt"
        torch.save(checkpoint, checkpoint_path)

        # Save best model
        if is_best or loss < self.best_loss:
            self.best_loss = loss
            best_path = self.checkpoint_dir / "best_model.pt"
            torch.save(checkpoint, best_path)
            print(f"Saved best model with loss: {loss:.4f}")

        # Save latest checkpoint
        latest_path = self.checkpoint_dir / "latest_checkpoint.pt"
        torch.save(checkpoint, latest_path)

    def load_checkpoint(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer = None,
        checkpoint_path: str = None,
        resume: bool = True
    ):
        """Load checkpoint."""
        if checkpoint_path is None:
            checkpoint_path = self.checkpoint_dir / "latest_checkpoint.pt"

        if not os.path.exists(checkpoint_path):
            print(f"No checkpoint found at {checkpoint_path}")
            return 0

        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint["model_state_dict"])

        if optimizer and resume:
            optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        start_epoch = checkpoint["epoch"] + 1 if resume else 0
        self.best_loss = checkpoint.get("best_loss", float("inf"))

        print(f"Loaded checkpoint from epoch {checkpoint['epoch']}")
        print(f"Resume training from epoch {start_epoch}")

        return start_epoch

# Usage in training loop
checkpoint_manager = CheckpointManager()

# Resume training
start_epoch = checkpoint_manager.load_checkpoint(model, optimizer, resume=True)

for epoch in range(start_epoch, num_epochs):
    # Training...
    val_loss = validate(model, val_loader)

    # Save checkpoint
    is_best = val_loss < checkpoint_manager.best_loss
    checkpoint_manager.save_checkpoint(
        model=model,
        optimizer=optimizer,
        epoch=epoch,
        loss=val_loss,
        is_best=is_best,
        metadata={"learning_rate": optimizer.param_groups[0]["lr"]}
    )
```

## Output

After training, you'll have:

1. **Trained Model** - Optimized model weights
2. **Checkpoints** - Regular and best model checkpoints
3. **Training Logs** - Metrics, losses, and training history
4. **Hyperparameter Results** - Optimal hyperparameters from tuning
5. **Experiment Tracking** - MLflow/W&B runs with all metrics
6. **Resume Capability** - Ability to resume training from checkpoints

## Best Practices

- Always use Accelerate for simplified distributed training
- Implement proper checkpointing and resume logic
- Track experiments with MLflow or W&B
- Use mixed precision (AMP) for faster training
- Optimize hyperparameters systematically with Optuna
- Validate data before training
- Monitor for overfitting with validation metrics
- Use gradient accumulation for effective larger batch sizes

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No checkpointing | Save checkpoints regularly |
| No experiment tracking | Use MLflow/W&B |
| Hardcoded hyperparameters | Use Optuna for optimization |
| No validation | Always validate during training |
| Sync operations in training loop | Use async/overlap operations |
| No gradient scaling with AMP | Always use GradScaler |

## Related

- Knowledge: `{directories.knowledge}/pytorch-patterns.json`, `{directories.knowledge}/model-training-patterns.json`
- Skill: `model-fine-tuning`
- Skill: `llm-evaluation`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
