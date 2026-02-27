---
agents:
- none
category: chain
description: Image-to-text with various engines (Tesseract, EasyOCR, cloud APIs),
  PDF text extraction, table recognition, and layout analysis
knowledge:
- none
name: processing-ocr
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Ocr Processing

Image-to-text with various engines (Tesseract, EasyOCR, cloud APIs), PDF text extraction, table recognition, and layout analysis

Extract text from images and PDFs using multiple OCR engines, recognize tables, and analyze document layouts.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Basic Tesseract OCR

```python
import pytesseract
from PIL import Image
import io

def extract_text_tesseract(image_path: str, lang: str = "eng") -> str:
    """Extract text using Tesseract OCR.

    Args:
        image_path: Path to image file
        lang: Language code (e.g., 'eng', 'spa', 'fra')
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()

# With image preprocessing
def extract_text_preprocessed(image_path: str) -> str:
    """Extract text with image preprocessing for better accuracy."""
    import cv2
    import numpy as np

    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Denoise
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)

    # Convert to PIL Image
    pil_image = Image.fromarray(denoised)

    # Extract text
    text = pytesseract.image_to_string(pil_image)
    return text.strip()

# Usage
text = extract_text_tesseract("document.png")
```

### Step 2: EasyOCR for Better Accuracy

```python
import easyocr

def extract_text_easyocr(image_path: str, languages: list = ["en"]) -> str:
    """Extract text using EasyOCR (often more accurate than Tesseract).

    Args:
        image_path: Path to image file
        languages: List of language codes (e.g., ['en', 'es'])
    """
    reader = easyocr.Reader(languages, gpu=False)
    results = reader.readtext(image_path)

    # Combine all detected text
    text = "\n".join([result[1] for result in results])
    return text

# With confidence filtering
def extract_text_with_confidence(image_path: str, min_confidence: float = 0.5) -> list:
    """Extract text with confidence scores and bounding boxes."""
    reader = easyocr.Reader(["en"], gpu=False)
    results = reader.readtext(image_path)

    filtered = [
        {
            "text": result[1],
            "confidence": result[2],
            "bbox": result[0]
        }
        for result in results
        if result[2] >= min_confidence
    ]
    return filtered

# Usage
text = extract_text_easyocr("document.png")
detections = extract_text_with_confidence("document.png", min_confidence=0.7)
```

### Step 3: PDF Text Extraction

```python
from pdf2image import convert_from_path
import pytesseract
from pymupdf import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str, method: str = "native") -> dict:
    """Extract text from PDF using different methods.

    Args:
        pdf_path: Path to PDF file
        method: 'native' (text layer) or 'ocr' (image-based)
    """
    if method == "native":
        # Extract from text layer (faster, but only works if PDF has text)
        doc = fitz.open(pdf_path)
        pages_text = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            pages_text.append({
                "page": page_num + 1,
                "text": text
            })

        doc.close()
        return {"pages": pages_text}

    else:  # OCR method
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, dpi=300)
        pages_text = []

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            pages_text.append({
                "page": i + 1,
                "text": text
            })

        return {"pages": pages_text}

# Hybrid approach: try native first, fallback to OCR
def extract_pdf_hybrid(pdf_path: str) -> dict:
    """Try native extraction first, use OCR if text is sparse."""
    doc = fitz.open(pdf_path)
    pages_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        native_text = page.get_text()

        # If text is too short, likely scanned image
        if len(native_text.strip()) < 100:
            # Convert page to image and OCR
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img)
            pages_text.append({
                "page": page_num + 1,
                "text": ocr_text,
                "method": "ocr"
            })
        else:
            pages_text.append({
                "page": page_num + 1,
                "text": native_text,
                "method": "native"
            })

    doc.close()
    return {"pages": pages_text}
```

### Step 4: Table Recognition and Extraction

```python
import cv2
import numpy as np
from PIL import Image
import pytesseract

def detect_tables(image_path: str) -> list:
    """Detect table boundaries in an image."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    detected_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    detected_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts2 = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = cnts2[0] if len(cnts2) == 2 else cnts2[1]

    # Combine contours
    all_cnts = list(cnts) + list(cnts2)

    # Find bounding boxes
    tables = []
    for cnt in all_cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 100 and h > 50:  # Filter small detections
            tables.append({"x": x, "y": y, "width": w, "height": h})

    return tables

def extract_table_cells(image_path: str, table_bbox: dict) -> list[list[str]]:
    """Extract text from table cells."""
    img = cv2.imread(image_path)

    # Crop table region
    x, y, w, h = table_bbox["x"], table_bbox["y"], table_bbox["width"], table_bbox["height"]
    table_img = img[y:y+h, x:x+w]

    # Convert to PIL
    pil_img = Image.fromarray(cv2.cvtColor(table_img, cv2.COLOR_BGR2RGB))

    # Use Tesseract with table structure detection
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_img, config=custom_config)

    # Parse into rows (simple approach)
    rows = []
    for line in text.strip().split('\n'):
        if line.strip():
            # Split by multiple spaces (assuming tabular format)
            cells = [cell.strip() for cell in line.split('  ') if cell.strip()]
            if cells:
                rows.append(cells)

    return rows

# Using unstructured library for better table extraction
def extract_tables_unstructured(pdf_path: str) -> list:
    """Extract tables using unstructured library."""
    from unstructured.partition.pdf import partition_pdf

    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        infer_table_structure=True
    )

    tables = []
    for element in elements:
        if hasattr(element, "metadata") and element.metadata.text_as_html:
            tables.append({
                "text": element.text,
                "html": element.metadata.text_as_html,
                "type": "table"
            })

    return tables
```

### Step 5: Layout Analysis

```python
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

def analyze_document_layout(pdf_path: str) -> dict:
    """Analyze document structure and layout."""
    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        infer_table_structure=True,
        include_page_breaks=True
    )

    layout = {
        "pages": [],
        "tables": [],
        "titles": [],
        "paragraphs": []
    }

    current_page = 1
    for element in elements:
        element_type = type(element).__name__

        if "PageBreak" in element_type:
            current_page += 1
            continue

        element_data = {
            "page": current_page,
            "type": element_type,
            "text": element.text[:200] if element.text else "",
        }

        if element_type == "Table":
            layout["tables"].append(element_data)
            if hasattr(element.metadata, "text_as_html"):
                element_data["html"] = element.metadata.text_as_html
        elif element_type == "Title":
            layout["titles"].append(element_data)
        elif element_type == "NarrativeText":
            layout["paragraphs"].append(element_data)

    return layout

def chunk_by_sections(pdf_path: str) -> list:
    """Chunk document by sections using title detection."""
    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        infer_table_structure=True
    )

    chunks = chunk_by_title(
        elements,
        max_characters=2000,
        combine_text_under_n_chars=500
    )

    return [
        {
            "text": chunk.text,
            "metadata": chunk.metadata.to_dict() if hasattr(chunk, "metadata") else {}
        }
        for chunk in chunks
    ]
```

### Step 6: Cloud OCR APIs Integration

```python
from google.cloud import vision
import boto3
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

def extract_text_google_vision(image_path: str, credentials_path: str) -> str:
    """Extract text using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient.from_service_account_file(credentials_path)

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""

def extract_text_aws_textract(image_path: str, aws_region: str = "us-east-1") -> dict:
    """Extract text using AWS Textract."""
    textract = boto3.client("textract", region_name=aws_region)

    with open(image_path, "rb") as document:
        response = textract.detect_document_text(
            Document={"Bytes": document.read()}
        )

    blocks = response["Blocks"]
    text_blocks = [
        block["Text"]
        for block in blocks
        if block["BlockType"] == "LINE"
    ]

    return {
        "text": "\n".join(text_blocks),
        "blocks": blocks
    }

def extract_text_azure_vision(image_path: str, endpoint: str, key: str) -> str:
    """Extract text using Azure Computer Vision."""
    client = ComputerVisionClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(key)
    )

    with open(image_path, "rb") as image_stream:
        ocr_result = client.read_in_stream(image_stream, raw=True)

    # Get operation ID
    operation_id = ocr_result.headers["Operation-Location"].split("/")[-1]

    # Wait for result
    import time
    while True:
        result = client.get_read_result(operation_id)
        if result.status not in ["notStarted", "running"]:
            break
        time.sleep(1)

    # Extract text
    text_lines = []
    if result.status == "succeeded":
        for page in result.analyze_result.read_results:
            for line in page.lines:
                text_lines.append(line.text)

    return "\n".join(text_lines)
```

## OCR Engines Comparison

| Engine | Accuracy | Speed | Languages | Cost |
|--------|----------|-------|-----------|------|
| Tesseract | Medium | Fast | 100+ | Free |
| EasyOCR | High | Medium | 80+ | Free |
| Google Vision | Very High | Fast | 50+ | Paid |
| AWS Textract | Very High | Fast | 50+ | Paid |
| Azure Vision | Very High | Fast | 50+ | Paid |

## Best Practices

- Preprocess images (grayscale, thresholding, denoising) before OCR
- Use native PDF text extraction when available, OCR as fallback
- Set appropriate DPI (300+) when converting PDFs to images
- Filter low-confidence detections to reduce noise
- Use layout analysis to preserve document structure
- Cache OCR results for repeated processing
- Choose engine based on accuracy needs vs. cost constraints
- Handle multi-language documents with language detection

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| OCR without preprocessing | Apply grayscale, thresholding, denoising |
| Low DPI PDF conversion | Use 300+ DPI for better accuracy |
| Ignoring confidence scores | Filter results below threshold |
| No fallback for native PDF | Try native first, OCR if sparse |
| Processing entire page | Crop to regions of interest |
| No layout preservation | Use structured extraction tools |
| Single language assumption | Detect and specify language codes |

## Related

- Skill: `vision-agents`
- Skill: `applying-rag-patterns`
- Skill: `retrieving-advanced`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
