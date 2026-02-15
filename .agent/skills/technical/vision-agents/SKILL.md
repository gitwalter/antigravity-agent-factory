---
description: Image analysis with multi-modal LLMs (GPT-4V, Gemini Vision), object
  detection integration, image generation pipelines, and visual question answering
name: vision-agents
type: skill
---
# Vision Agents

Image analysis with multi-modal LLMs (GPT-4V, Gemini Vision), object detection integration, image generation pipelines, and visual question answering

Build agents that understand and generate images using multi-modal LLMs, object detection, and visual question answering.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Image Analysis with GPT-4V

```python
from openai import OpenAI
from PIL import Image
import base64
import io

def analyze_image_gpt4v(image_path: str, prompt: str, api_key: str) -> str:
    """Analyze image using GPT-4 Vision.
    
    Args:
        image_path: Path to image file
        prompt: Question or instruction about the image
        api_key: OpenAI API key
    """
    client = OpenAI(api_key=api_key)
    
    # Read and encode image
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content

# With LangChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def analyze_image_langchain(image_path: str, prompt: str) -> str:
    """Analyze image using LangChain with GPT-4V."""
    llm = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=500)
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": image_path}
        ]
    )
    
    response = llm.invoke([message])
    return response.content
```

### Step 2: Image Analysis with Gemini Vision

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from PIL import Image

def analyze_image_gemini(image_path: str, prompt: str) -> str:
    """Analyze image using Google Gemini Vision."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    
    # Load image
    image = Image.open(image_path)
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": image}
        ]
    )
    
    response = llm.invoke([message])
    return response.content

# Multi-image analysis
def compare_images(image_paths: list[str], prompt: str) -> str:
    """Compare multiple images."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    
    images = [Image.open(path) for path in image_paths]
    
    content = [{"type": "text", "text": prompt}]
    for img in images:
        content.append({"type": "image_url", "image_url": img})
    
    message = HumanMessage(content=content)
    response = llm.invoke([message])
    return response.content
```

### Step 3: Object Detection Integration

```python
from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np

class VisionAgent:
    """Agent that combines object detection with LLM reasoning."""
    
    def __init__(self, yolo_model_path: str = "yolov8n.pt", llm_model: str = "gemini-1.5-pro"):
        self.detector = YOLO(yolo_model_path)
        self.llm = ChatGoogleGenerativeAI(model=llm_model)
    
    def detect_objects(self, image_path: str, confidence: float = 0.5) -> list:
        """Detect objects in image."""
        results = self.detector(image_path, conf=confidence)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detections.append({
                    "class": self.detector.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "bbox": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                })
        
        return detections
    
    def analyze_with_context(self, image_path: str, question: str) -> str:
        """Analyze image with object detection context."""
        # Detect objects
        detections = self.detect_objects(image_path)
        
        # Build context
        objects_str = ", ".join([d["class"] for d in detections])
        context = f"Detected objects: {objects_str}"
        
        # Analyze with LLM
        image = Image.open(image_path)
        message = HumanMessage(
            content=[
                {"type": "text", "text": f"{context}\n\nQuestion: {question}"},
                {"type": "image_url", "image_url": image}
            ]
        )
        
        response = self.llm.invoke([message])
        return response.content
    
    def draw_detections(self, image_path: str, output_path: str):
        """Draw detected objects on image."""
        results = self.detector(image_path)
        
        # Load image
        img = cv2.imread(image_path)
        
        # Draw boxes
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = f"{self.detector.names[class_id]} {confidence:.2f}"
                
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imwrite(output_path, img)

# Usage
agent = VisionAgent()
detections = agent.detect_objects("photo.jpg")
answer = agent.analyze_with_context("photo.jpg", "What is the main subject?")
```

### Step 4: Visual Question Answering

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from PIL import Image

class VisualQA:
    """Visual Question Answering system."""
    
    def __init__(self, model: str = "gemini-1.5-pro"):
        self.llm = ChatGoogleGenerativeAI(model=model)
    
    def answer_question(self, image_path: str, question: str, context: str = None) -> dict:
        """Answer a question about an image."""
        image = Image.open(image_path)
        
        prompt = question
        if context:
            prompt = f"Context: {context}\n\nQuestion: {question}"
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": image}
            ]
        )
        
        response = self.llm.invoke([message])
        
        return {
            "question": question,
            "answer": response.content,
            "image": image_path
        }
    
    def multi_question(self, image_path: str, questions: list[str]) -> list:
        """Answer multiple questions about an image."""
        results = []
        for question in questions:
            result = self.answer_question(image_path, question)
            results.append(result)
        return results
    
    def compare_scenarios(self, image_path: str, scenarios: list[str]) -> dict:
        """Compare different scenarios or interpretations."""
        image = Image.open(image_path)
        
        prompt = "Analyze this image considering these scenarios:\n"
        for i, scenario in enumerate(scenarios, 1):
            prompt += f"{i}. {scenario}\n"
        prompt += "\nProvide insights for each scenario."
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": image}
            ]
        )
        
        response = self.llm.invoke([message])
        return {"analysis": response.content, "scenarios": scenarios}

# Usage
vqa = VisualQA()
result = vqa.answer_question("photo.jpg", "What objects are in this image?")
```

### Step 5: Image Generation Pipelines

```python
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

class ImageGenerator:
    """Generate images from text descriptions."""
    
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        if torch.cuda.is_available():
            self.pipe = self.pipe.to("cuda")
    
    def generate(self, prompt: str, negative_prompt: str = "", num_images: int = 1) -> list[Image.Image]:
        """Generate images from prompt."""
        images = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_images_per_prompt=num_images,
            num_inference_steps=50
        ).images
        
        return images
    
    def generate_with_style(self, prompt: str, style: str) -> Image.Image:
        """Generate image with specific style."""
        style_prompts = {
            "photorealistic": "photorealistic, high quality, detailed",
            "anime": "anime style, vibrant colors, detailed",
            "oil painting": "oil painting, artistic, detailed brushstrokes",
            "sketch": "pencil sketch, black and white, detailed"
        }
        
        enhanced_prompt = f"{prompt}, {style_prompts.get(style, '')}"
        images = self.generate(enhanced_prompt)
        return images[0]
    
    def img2img(self, image_path: str, prompt: str, strength: float = 0.75) -> Image.Image:
        """Modify existing image based on prompt."""
        from diffusers import StableDiffusionImg2ImgPipeline
        
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        
        init_image = Image.open(image_path).convert("RGB")
        
        image = pipe(
            prompt=prompt,
            image=init_image,
            strength=strength,
            num_inference_steps=50
        ).images[0]
        
        return image

# Using OpenAI DALL-E
def generate_dalle(prompt: str, api_key: str, size: str = "1024x1024") -> str:
    """Generate image using DALL-E."""
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1
    )
    
    return response.data[0].url
```

### Step 6: Multi-Modal RAG Integration

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage
from PIL import Image

class MultiModalRAG:
    """RAG system that handles both text and images."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
        self.embeddings = HuggingFaceEmbeddings()
        self.vectorstore = None
    
    def add_image_document(self, image_path: str, description: str, metadata: dict = None):
        """Add image with description to vector store."""
        # Generate description if not provided
        if not description:
            image = Image.open(image_path)
            message = HumanMessage(
                content=[
                    {"type": "text", "text": "Describe this image in detail."},
                    {"type": "image_url", "image_url": image}
                ]
            )
            description = self.llm.invoke([message]).content
        
        # Embed description
        embedding = self.embeddings.embed_query(description)
        
        # Store in vector DB (pseudo-code - adjust based on your vector store)
        if self.vectorstore is None:
            self.vectorstore = Chroma(embedding_function=self.embeddings)
        
        self.vectorstore.add_texts(
            texts=[description],
            embeddings=[embedding],
            metadatas=[{
                "type": "image",
                "path": image_path,
                **(metadata or {})
            }]
        )
    
    def retrieve_and_answer(self, query: str, image_path: str = None) -> str:
        """Retrieve relevant context and answer query."""
        # Retrieve text context
        if self.vectorstore:
            docs = self.vectorstore.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in docs])
        else:
            context = ""
        
        # Build prompt
        prompt = f"Context: {context}\n\nQuestion: {query}"
        
        # Add image if provided
        content = [{"type": "text", "text": prompt}]
        if image_path:
            image = Image.open(image_path)
            content.append({"type": "image_url", "image_url": image})
        
        message = HumanMessage(content=content)
        response = self.llm.invoke([message])
        return response.content
```

## Vision Models Comparison

| Model | Type | Capabilities | Cost | Best For |
|------|------|--------------|------|----------|
| GPT-4V | Multi-modal | Image analysis, VQA | Paid | General vision tasks |
| Gemini 1.5 Pro | Multi-modal | Image analysis, VQA, video | Paid/Free | Multi-modal RAG |
| YOLOv8 | Object Detection | Object detection | Free | Real-time detection |
| Stable Diffusion | Generation | Image generation | Free | Creative generation |
| DALL-E 3 | Generation | Image generation | Paid | High-quality generation |

## Best Practices

- Use appropriate model size based on accuracy vs. cost needs
- Preprocess images (resize, normalize) before analysis
- Combine object detection with LLM reasoning for better context
- Cache image descriptions for RAG systems
- Use negative prompts in image generation for better control
- Handle multiple images in context when comparing
- Specify image formats and sizes for API compatibility
- Implement error handling for API rate limits

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Sending full-resolution images | Resize to reasonable size (1024px max) |
| No image preprocessing | Normalize, resize before analysis |
| Ignoring API costs | Cache results, use smaller models when possible |
| Single image context | Use multi-image when comparing |
| No error handling | Handle API failures gracefully |
| Hardcoded prompts | Make prompts configurable |
| No object detection context | Combine detection with LLM analysis |

## Related

- Skill: `ocr-processing`
- Skill: `rag-patterns`
- Skill: `advanced-retrieval`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
