# LLM Fine-Tuning Techniques

> **Stack:** Hugging Face + PEFT | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L15_llm_finetuning`

**Technology:** Python with Hugging Face + PEFT (Transformers 4.40+)

## Prerequisites

**Required Knowledge:**
- Python programming (classes, decorators, context managers)
- Understanding of transformer architecture basics
- Familiarity with PyTorch (tensors, models, training loops)
- Basic NLP concepts (tokenization, embeddings, attention)

**Required Tools:**
- Python 3.8+
- transformers library (4.40+)
- peft library
- datasets library
- CUDA-capable GPU (required for training)
- Hugging Face account and token

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand when to fine-tune vs prompt engineering and the trade-offs** (Understand)
2. **Prepare datasets for instruction tuning with proper formatting** (Apply)
3. **Implement LoRA and QLoRA fine-tuning for parameter-efficient training** (Apply)
4. **Use SFTTrainer for supervised fine-tuning workflows** (Apply)
5. **Evaluate fine-tuned models using appropriate metrics and benchmarks** (Analyze)

## Workshop Timeline

| Phase | Duration |
|-------|----------|
| Concept | 30 min |
| Demo | 30 min |
| Exercise | 45 min |
| Challenge | 30 min |
| Reflection | 15 min |
| **Total** | **2.5 hours** |

## Workshop Phases

### Concept: Fine-Tuning Landscape and LoRA Theory

*Understanding when and how to fine-tune LLMs efficiently*

**Topics Covered:**
- Fine-tuning vs prompt engineering: when to use each
- Full fine-tuning vs parameter-efficient methods
- LoRA (Low-Rank Adaptation): theory and benefits
- QLoRA: quantized LoRA for memory efficiency
- Instruction tuning: dataset format and best practices
- Evaluation metrics: perplexity, BLEU, ROUGE, human evaluation

**Key Points:**
- Fine-tuning is expensive but provides task-specific adaptation
- LoRA trains only small adapter matrices, reducing parameters by 100-1000x
- QLoRA uses 4-bit quantization + LoRA for even more memory savings
- Instruction tuning requires prompt-response pairs in specific format
- Always evaluate on held-out test set
- Fine-tuning can cause catastrophic forgetting - use LoRA to mitigate

### Demo: QLoRA Setup and Fine-Tuning

*Live coding a complete QLoRA fine-tuning setup*

**Topics Covered:**
- Loading base model with BitsAndBytes quantization
- Setting up LoRA config with PEFT
- Preparing instruction dataset
- Configuring SFTTrainer
- Training with gradient checkpointing
- Saving and loading adapters

**Key Points:**
- Use 4-bit quantization for memory efficiency
- LoRA rank (r) controls adapter size vs expressiveness trade-off
- Format data as chat templates
- Use gradient checkpointing to save memory
- Save only adapters, not full model

### Exercise: Dataset Preparation for Instruction Tuning

*Format a dataset for instruction fine-tuning*

**Topics Covered:**
- Load dataset from Hugging Face or local files
- Format as instruction-response pairs
- Apply chat template formatting
- Tokenize and prepare for training

### Exercise: LoRA Fine-Tuning Setup

*Set up and run LoRA fine-tuning on a small model*

**Topics Covered:**
- Load base model
- Configure LoRA adapters
- Set up training arguments
- Run training loop
- Save adapters

### Challenge: Custom Instruction Dataset Fine-Tuning

*Fine-tune a model on a custom domain-specific dataset*

**Topics Covered:**
- Create custom instruction dataset
- Implement QLoRA fine-tuning
- Evaluate model performance
- Compare before/after fine-tuning
- Deploy fine-tuned model for inference

### Reflection: Key Takeaways and Production Considerations

*Consolidate learning and discuss deployment strategies*

**Topics Covered:**
- Summary of fine-tuning approaches
- Memory and compute requirements
- Evaluation strategies
- Deployment considerations
- Resources for advanced techniques

**Key Points:**
- LoRA/QLoRA make fine-tuning accessible on consumer hardware
- Instruction tuning requires high-quality, diverse datasets
- Always evaluate on held-out test set
- Monitor training loss to detect overfitting
- Save adapters separately for easy model switching
- Consider inference speed when choosing quantization

## Hands-On Exercises

### Exercise: Dataset Preparation for Instruction Tuning

Format a dataset for instruction fine-tuning with proper chat template

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Use tokenizer.apply_chat_template() for proper formatting
- Chat format: list of dicts with "role" and "content"
- Set add_generation_prompt=False for training data
- Use padding="max_length" for consistent batch shapes
- Remove original columns after formatting

**Common Mistakes to Avoid:**
- Not using chat template (model-specific format)
- Including generation prompt in training data
- Forgetting to set pad_token
- Not truncating long sequences
- Wrong message format (not list of dicts)

### Exercise: LoRA Fine-Tuning Setup

Set up and run LoRA fine-tuning using PEFT and SFTTrainer

**Difficulty:** Medium | **Duration:** 25 minutes

**Hints:**
- Use BitsAndBytesConfig for 4-bit quantization
- prepare_model_for_kbit_training() enables gradient checkpointing
- LoRA rank (r) typically 8-64, alpha usually 2*r
- target_modules should match model architecture
- Use gradient_checkpointing=True to save memory
- optim="paged_adamw_32bit" is memory-efficient

**Common Mistakes to Avoid:**
- Not preparing model for k-bit training
- Wrong target_modules for model architecture
- Forgetting gradient_checkpointing (runs out of memory)
- Not using gradient_accumulation_steps
- Saving full model instead of just adapter
- Wrong task_type in LoraConfig

## Challenges

### Challenge: Custom Instruction Dataset Fine-Tuning

Fine-tune a model on a custom domain-specific instruction dataset

**Requirements:**
- Create or collect domain-specific instruction dataset (100+ examples)
- Format dataset with proper chat template
- Implement QLoRA fine-tuning with optimal hyperparameters
- Evaluate model on test set with appropriate metrics
- Compare model outputs before and after fine-tuning
- Save and load adapter for inference
- Demonstrate improvement on domain-specific tasks

**Evaluation Criteria:**
- Dataset is properly formatted and diverse
- QLoRA training completes without errors
- Model shows improvement on domain tasks
- Evaluation metrics show positive change
- Adapter can be loaded and used for inference
- Before/after comparison demonstrates value

**Stretch Goals:**
- Implement evaluation with multiple metrics (BLEU, ROUGE, human eval)
- Fine-tune with different LoRA ranks and compare
- Create a simple web interface for model inference
- Implement continuous learning with additional data
- Optimize inference speed with quantization

## Resources

**Official Documentation:**
- https://huggingface.co/docs/transformers/
- https://huggingface.co/docs/peft/
- https://huggingface.co/docs/trl/
- https://huggingface.co/docs/datasets/

**Tutorials:**
- https://huggingface.co/docs/peft/tutorial/peft_lora
- https://huggingface.co/docs/trl/tutorials/sft_trainer
- https://huggingface.co/blog/4bit-transformers-bitsandbytes
- https://huggingface.co/blog/llama2

**Videos:**
- Hugging Face Course on Fine-tuning
- QLoRA: Efficient Finetuning of Quantized LLMs

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain when fine-tuning is preferable to prompt engineering?
- [ ] Do I understand how LoRA reduces parameters while maintaining performance?
- [ ] Can I format datasets correctly for instruction tuning?
- [ ] Can I set up and run QLoRA fine-tuning?
- [ ] Do I know how to evaluate fine-tuned models effectively?

## Next Steps

**Next Workshop:** `L16_advanced_llm_techniques`

**Practice Projects:**
- Fine-tune model for code generation
- Create domain-specific chatbot (legal, medical, etc.)
- Fine-tune for structured output generation
- Multi-task fine-tuning with different adapters

**Deeper Learning:**
- RLHF (Reinforcement Learning from Human Feedback)
- Advanced PEFT methods (AdaLoRA, DoRA)
- Model merging and ensemble techniques
- Efficient inference optimization

## Related Knowledge Files

- `llm-fine-tuning-patterns.json`
- `huggingface-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L15_llm_finetuning.json`
