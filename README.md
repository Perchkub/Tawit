# OCR Web Application

A web application built with FastHTML and Google Gen AI SDK for extracting text from images and PDFs using OCR (Optical Character Recognition).

## Features

- Upload images (JPG, PNG, GIF, BMP) or PDF files
- Extract text using Google Gen AI OCR capabilities
- Clean, responsive web interface
- Docker support for easy deployment

## Prerequisites

- Python 3.11+
- Google Gen AI API key
- Docker (optional, for containerized deployment)

## Installation

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t ocr-app .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 ocr-app
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Navigate to the web application
2. Click "Choose File" and select an image or PDF file
3. Click "Extract Text" to process the file
4. View the extracted text on the results page
5. Use "Copy Text" button to copy the extracted text to clipboard

## API Key Configuration

The application is configured with the provided Google Gen AI API key. For production use, consider using environment variables:

```python
import os
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
```

## Supported File Types

- **Images**: JPG, JPEG, PNG, GIF, BMP
- **Documents**: PDF (both text-based and scanned)

## Technologies Used

- **FastHTML**: Web framework for Python
- **Google Gen AI SDK**: OCR and text extraction
- **Pillow**: Image processing
- **PyPDF2**: PDF text extraction
- **pdf2image**: PDF to image conversion
- **Docker**: Containerization

## Docker Image Details

- Base: Python 3.11 on Debian
- Dependencies: libxrender1, poppler-utils, tesseract-ocr
- Port: 5000
- Optimized for OCR processing
