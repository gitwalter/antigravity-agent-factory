# PyTorch Deep Learning Fundamentals

> **Stack:** PyTorch | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L14_pytorch_deeplearning`

**Technology:** Python with PyTorch (PyTorch 2.0+)

## Prerequisites

**Required Knowledge:**
- Python programming (functions, classes, OOP)
- Basic linear algebra (tensors, matrix operations)
- Understanding of neural networks (forward pass, backpropagation)
- NumPy basics

**Required Tools:**
- Python 3.8+
- PyTorch 2.0+ installed
- CUDA-capable GPU (optional but recommended)
- Jupyter Notebook or VS Code
- Matplotlib for visualization

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Define models with nn.Module and understand the architecture** (Understand)
2. **Implement training loops with proper gradient management** (Apply)
3. **Use DataLoader for efficient data loading and batching** (Apply)
4. **Apply optimization techniques including learning rate scheduling and mixed precision** (Apply)
5. **Save and load model checkpoints for training resumption** (Apply)

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

### Concept: PyTorch Fundamentals: Tensors, Autograd, and nn.Module

*Understanding PyTorch's core concepts and how neural networks are built*

**Topics Covered:**
- Tensors: creation, operations, device placement (CPU/GPU)
- Autograd: automatic differentiation, requires_grad, backward()
- nn.Module: base class for all neural network modules
- Layer composition: Sequential, ModuleList, ModuleDict
- Forward pass: how data flows through the network
- Gradient computation: computational graph and backpropagation

**Key Points:**
- Tensors are the fundamental data structure (like NumPy arrays with GPU support)
- Autograd tracks operations to compute gradients automatically
- nn.Module provides structure and parameter management
- forward() defines the computation, __call__() handles hooks
- Gradients accumulate - always zero_grad() before backward()
- Model.eval() vs model.train() changes behavior (dropout, batchnorm)

### Demo: Building an Image Classifier

*Live coding a complete CNN image classifier from scratch*

**Topics Covered:**
- Dataset and DataLoader setup with transforms
- Defining CNN architecture with nn.Module
- Loss function and optimizer selection
- Training loop implementation
- Validation loop with metrics
- Model checkpointing

**Key Points:**
- Always normalize images with transforms.Normalize()
- Use DataLoader with num_workers for parallel loading
- Move model and data to same device
- Validate on separate dataset to check overfitting
- Save checkpoints regularly during training

### Exercise: Custom Dataset and DataLoader

*Create a custom dataset class and set up data loading*

**Topics Covered:**
- Implement Dataset class with __len__ and __getitem__
- Apply transforms for preprocessing
- Create DataLoader with appropriate batch size
- Handle different data formats (images, CSV, etc.)

### Exercise: Training Loop Implementation

*Write a complete training loop with gradient management*

**Topics Covered:**
- Forward pass through model
- Loss computation and backward pass
- Optimizer step and gradient zeroing
- Epoch tracking and logging
- Basic metrics calculation

### Challenge: Transfer Learning with Pre-trained Models

*Fine-tune a pre-trained model for a custom task*

**Topics Covered:**
- Load pre-trained weights from torchvision.models
- Modify final layers for new task
- Freeze/unfreeze layers selectively
- Train with different learning rates for different layers
- Evaluate fine-tuned model performance

### Reflection: Key Takeaways and Best Practices

*Consolidate learning and discuss production considerations*

**Topics Covered:**
- Summary of PyTorch fundamentals
- Common pitfalls and debugging strategies
- Performance optimization tips
- Resources for advanced topics

**Key Points:**
- Always check tensor shapes during development
- Use torch.no_grad() for inference to save memory
- Monitor GPU memory usage
- Save checkpoints frequently
- Use torch.compile() for PyTorch 2.0+ performance gains
- Validate your model on unseen data

## Hands-On Exercises

### Exercise: Custom Dataset and DataLoader

Create a custom dataset class for image classification and set up DataLoader

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Use os.walk() or os.listdir() to find all images
- Create a mapping from class names to integer labels
- Use PIL Image.open() to load images
- transforms.ToTensor() converts PIL Image to tensor and scales to [0,1]
- transforms.Normalize() standardizes the data
- Set pin_memory=True for faster GPU transfer

**Common Mistakes to Avoid:**
- Forgetting to convert image to RGB with .convert('RGB')
- Not handling different image formats
- Incorrect normalization values
- Forgetting to set shuffle=True for training
- Not using num_workers for parallel loading

### Exercise: Complete Training Loop

Implement a complete training loop with proper gradient management

**Difficulty:** Medium | **Duration:** 25 minutes

**Hints:**
- Always call optimizer.zero_grad() before backward()
- Move both inputs and targets to the same device as model
- Use model.train() for training, model.eval() for validation
- Use torch.no_grad() during validation to save memory
- Call optimizer.step() after backward() to update weights

**Common Mistakes to Avoid:**
- Forgetting optimizer.zero_grad() - causes gradient accumulation
- Not moving data to device (CPU/GPU mismatch)
- Using model.train() during validation
- Forgetting torch.no_grad() in validation (wastes memory)
- Calling optimizer.step() before backward()
- Not handling batch dimension correctly

### Exercise: Model Checkpointing

Implement save and load functions for model checkpoints

**Difficulty:** Easy | **Duration:** 15 minutes

**Hints:**
- Use model.state_dict() to get model parameters
- Use optimizer.state_dict() to save optimizer state
- Include epoch number to resume training
- Use map_location in torch.load() for device compatibility
- Check if file exists before loading

**Common Mistakes to Avoid:**
- Not saving optimizer state (can't resume training properly)
- Forgetting to create directory before saving
- Not handling device mapping when loading
- Saving full model instead of state_dict (less portable)
- Not checking if checkpoint exists before loading

## Challenges

### Challenge: Transfer Learning with Pre-trained Models

Fine-tune a pre-trained ResNet model for a custom image classification task

**Requirements:**
- Load pre-trained ResNet18 from torchvision.models
- Replace final fully connected layer for your number of classes
- Freeze backbone layers, only train classifier
- Implement learning rate scheduling
- Use mixed precision training with torch.cuda.amp
- Save best model checkpoint based on validation accuracy
- Achieve >85% validation accuracy

**Evaluation Criteria:**
- Model loads pre-trained weights correctly
- Only classifier layers have requires_grad=True
- Training uses mixed precision
- Learning rate decreases according to schedule
- Best model checkpoint is saved
- Validation accuracy meets threshold

**Stretch Goals:**
- Implement fine-tuning with differential learning rates (lower LR for backbone)
- Add data augmentation (random crops, flips, color jitter)
- Visualize training curves with matplotlib
- Implement early stopping based on validation loss
- Export model to ONNX format

## Resources

**Official Documentation:**
- https://pytorch.org/docs/stable/index.html
- https://pytorch.org/tutorials/
- https://pytorch.org/vision/stable/index.html

**Tutorials:**
- https://pytorch.org/tutorials/beginner/basics/intro.html
- https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
- https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html

**Videos:**
- PyTorch Official YouTube Channel
- Deep Learning with PyTorch - Fast.ai

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain how autograd works and when gradients are computed?
- [ ] Do I understand when to use model.train() vs model.eval()?
- [ ] Can I write a complete training loop from scratch?
- [ ] Do I know how to save and load model checkpoints?
- [ ] Can I use DataLoader effectively for my data?

## Next Steps

**Next Workshop:** `L15_llm_finetuning`

**Practice Projects:**
- Image classification on custom dataset
- Object detection with YOLO
- Image segmentation with U-Net
- GAN for image generation

**Deeper Learning:**
- Advanced architectures (ResNet, Transformer, Vision Transformer)
- Distributed training with DDP
- Model optimization (quantization, pruning)
- Deployment with TorchScript and ONNX

## Related Knowledge Files

- `pytorch-patterns.json`
- `deep-learning-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L14_pytorch_deeplearning.json`
