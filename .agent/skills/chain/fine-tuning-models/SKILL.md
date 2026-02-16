---
description: LoRA/QLoRA/PEFT fine-tuning workflows with Hugging Face transformers
name: fine-tuning-models
type: skill
---
# Model Fine Tuning

LoRA/QLoRA/PEFT fine-tuning workflows with Hugging Face transformers

Fine-tune large language models efficiently using LoRA, QLoRA, and PEFT techniques with Hugging Face transformers and TRL.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Dataset Preparation

Format and tokenize your dataset for fine-tuning:

```python
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer

# Load or create dataset
dataset = load_dataset("json", data_files="training_data.jsonl")

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
tokenizer.pad_token = tokenizer.eos_token

def format_prompt(example):
    """Format instruction-following prompt."""
    return {
        "text": f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['response']}"
    }

def tokenize_function(examples):
    """Tokenize dataset."""
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

# Format and tokenize
dataset = dataset.map(format_prompt)
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset["train"].column_names
)
```

### Step 2: QLoRA Configuration

Set up QLoRA with 4-bit quantization and LoRA adapters:

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# Load model with quantization
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# Prepare model for k-bit training
model = prepare_model_for_kbit_training(model)

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,  # Scaling parameter
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

### Step 3: Training Configuration

Configure TRL SFTTrainer for supervised fine-tuning:

```python
from transformers import TrainingArguments, Trainer
from trl import SFTTrainer
import torch

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
    optim="paged_adamw_8bit",
    lr_scheduler_type="cosine",
    warmup_steps=100,
    report_to="tensorboard"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=tokenized_dataset["train"],
    peft_config=lora_config,
    tokenizer=tokenizer,
    args=training_args,
    packing=False,
    max_seq_length=512,
    dataset_text_field="text"
)
```

### Step 4: Training and Evaluation

Train the model with evaluation during training:

```python
# Train model
trainer.train()

# Evaluate
eval_results = trainer.evaluate()
print(f"Perplexity: {eval_results['eval_loss']:.2f}")

# Save adapter
trainer.save_model("./adapter")
tokenizer.save_pretrained("./adapter")
```

### Step 5: Adapter Merging and Export

Merge LoRA adapter with base model for inference:

```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load adapter
model = PeftModel.from_pretrained(base_model, "./adapter")

# Merge and save
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged_model")
tokenizer.save_pretrained("./merged_model")
```

### Step 6: Quantization Options

Apply different quantization techniques:

```python
# GPTQ quantization
from auto_gptq import AutoGPTQForCausalLM

model_gptq = AutoGPTQForCausalLM.from_quantized(
    "TheBloke/Llama-2-7b-GPTQ",
    device="cuda:0",
    use_triton=True
)

# AWQ quantization
from awq import AutoAWQForCausalLM

model_awq = AutoAWQForCausalLM.from_quantized(
    "TheBloke/Llama-2-7b-AWQ",
    device_map="auto"
)
```

## Output

- Fine-tuned model adapter (LoRA weights)
- Merged model (optional, for standalone inference)
- Training metrics and logs
- Evaluation results
- Tokenizer configuration

## Best Practices

- Use QLoRA for memory-efficient fine-tuning on consumer GPUs
- Start with small rank (r=8-16) and increase if needed
- Monitor training loss to prevent overfitting
- Use gradient checkpointing for very large models
- Save checkpoints regularly during training
- Evaluate on held-out validation set
- Use appropriate learning rates (1e-5 to 5e-4)
- Apply LoRA to attention layers (q_proj, v_proj, k_proj, o_proj)
- Use 4-bit quantization with double quantization for best memory savings
- Merge adapters only when needed for deployment

## Related

- Knowledge: `{directories.knowledge}/llm-fine-tuning-patterns.json`
- Skill: `model-training` for training infrastructure
- Skill: `data-pipeline` for dataset preparation

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
