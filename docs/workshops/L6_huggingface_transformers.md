# Hugging Face Transformers Mastery

> **Stack:** Hugging Face | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L6_huggingface_transformers`

**Technology:** Python with Hugging Face (Transformers 4.40+)

## Prerequisites

**Required Knowledge:**
- Python programming (functions, classes)
- Basic understanding of neural networks
- PyTorch or TensorFlow basics

**Required Tools:**
- Python 3.10+
- PyTorch or TensorFlow installed
- Hugging Face account (for Hub access)
- VS Code or similar IDE

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Load pre-trained models using Auto classes (AutoModel, AutoTokenizer, AutoModelForCausalLM)** (Apply)
2. **Implement inference patterns for text generation and embeddings** (Apply)
3. **Apply quantization techniques (4-bit, 8-bit) for efficient inference** (Apply)
4. **Fine-tune models using PEFT/LoRA techniques** (Apply)
5. **Push models and datasets to Hugging Face Hub** (Apply)

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

### Concept: Transformers Architecture Overview

*Understand the Hugging Face Transformers ecosystem*

**Topics Covered:**
- Hugging Face Hub: Model and dataset repository
- Auto Classes: Dynamic model loading
- Tokenizers: Text preprocessing and encoding
- Model Architectures: Encoder, Decoder, Encoder-Decoder
- Pipelines: High-level inference API
- Quantization: 4-bit and 8-bit model compression
- PEFT: Parameter-Efficient Fine-Tuning (LoRA, QLoRA)

**Key Points:**
- Auto classes automatically select the right model architecture
- Tokenizers handle text preprocessing consistently
- Pipelines provide simple high-level APIs
- Quantization reduces memory without significant accuracy loss
- LoRA enables efficient fine-tuning with minimal parameters
- Hub provides centralized model and dataset storage

### Demo: Loading and Using Models

*Live coding model loading and inference*

**Topics Covered:**
- Loading models from Hub
- Using tokenizers for preprocessing
- Text generation with generate()
- Extracting embeddings
- Using pipelines for quick inference
- Loading quantized models

**Key Points:**
- Always use appropriate Auto class for your task
- Tokenizers must match the model
- Generation parameters affect output quality
- Pipelines simplify common tasks
- Quantization requires compatible libraries

### Exercise: Text Generation Pipeline

*Build a text generation system*

**Topics Covered:**
- Load a causal language model
- Implement text generation
- Add sampling strategies
- Handle long sequences
- Optimize generation parameters

### Challenge: LoRA Fine-Tuning

*Fine-tune a model using LoRA*

**Topics Covered:**
- Prepare training dataset
- Configure LoRA parameters
- Set up training loop
- Monitor training metrics
- Save and load fine-tuned model

### Reflection: Key Takeaways and Production Considerations

*Consolidate learning and discuss production deployment*

**Topics Covered:**
- Summary of Transformers patterns
- Model selection best practices
- Quantization trade-offs
- Fine-tuning strategies
- Production considerations (deployment, optimization)
- Resources for continued learning

**Key Points:**
- Choose models based on task and resource constraints
- Quantization enables efficient deployment
- LoRA is efficient for domain adaptation
- Monitor memory usage and inference speed
- Use pipelines for rapid prototyping

## Hands-On Exercises

### Exercise: Text Generation Pipeline

Build a text generation system with configurable parameters

**Difficulty:** Medium | **Duration:** 45 minutes

**Hints:**
- Use AutoTokenizer.from_pretrained() for tokenizer
- Use AutoModelForCausalLM.from_pretrained() for generation models
- Set pad_token if needed
- Use model.generate() with appropriate parameters
- Temperature controls randomness (lower = more deterministic)
- top_p and top_k control sampling diversity

**Common Mistakes to Avoid:**
- Not setting pad_token
- Forgetting to set model.eval()
- Not handling device placement (CPU vs GPU)
- Wrong model class for generation task
- Not using do_sample=True with temperature

## Challenges

### Challenge: LoRA Fine-Tuning

Fine-tune a language model using LoRA for a specific task

**Requirements:**
- Prepare a training dataset (at least 100 examples)
- Load base model and configure LoRA
- Set up training with Trainer API
- Train for at least 3 epochs
- Evaluate on validation set
- Save fine-tuned model
- Compare performance before and after fine-tuning

**Evaluation Criteria:**
- Dataset is properly formatted
- LoRA configuration is correct
- Training completes without errors
- Model performance improves
- Fine-tuned model can be loaded and used
- Memory usage is significantly lower than full fine-tuning

**Stretch Goals:**
- Use QLoRA (quantized LoRA) for even lower memory
- Push fine-tuned model to Hub
- Create inference script using fine-tuned model
- Compare LoRA vs full fine-tuning performance

## Resources

**Official Documentation:**
- https://huggingface.co/docs/transformers/
- https://huggingface.co/docs/peft/

**Tutorials:**
- https://huggingface.co/learn/nlp-course/
- https://huggingface.co/docs/transformers/training

**Videos:**
- Hugging Face Transformers Course
- Fine-tuning Tutorials

## Self-Assessment

Ask yourself these questions:

- [ ] Can I load models using Auto classes?
- [ ] Do I understand how to configure generation parameters?
- [ ] Can I implement quantization for efficient inference?
- [ ] Do I know how to fine-tune models with LoRA?
- [ ] Can I push models to Hugging Face Hub?

## Next Steps

**Next Workshop:** `L7_langchain_fundamentals`

**Practice Projects:**
- Domain-specific chatbot fine-tuning
- Text classification with transformers
- Multi-modal model exploration

**Deeper Learning:**
- Advanced fine-tuning techniques
- Model optimization and deployment
- Multi-modal transformers

## Related Knowledge Files

- `huggingface-patterns.json`
- `deep-learning-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L6_huggingface_transformers.json`