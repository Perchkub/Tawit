# OCR Web Application

A web application built with FastHTML and Google Gen AI SDK for Optical Character Recognition (OCR) from uploaded images and PDF files.

## Features

- Upload images (JPG, PNG, GIF) and PDF files
- Extract text using Google Gen AI (Gemini 2.0 Flash)
- Clean, responsive web interface
- Docker support

## Requirements

- Python 3.11+
- Google Gen AI API key
- Docker (optional)

## Installation

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

### Docker

1. Build the Docker image:
```bash
docker build -t ocr-web-app .
```

2. Run the container:
```bash
docker run -p 5000:5000 ocr-web-app
```

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Click "Choose File" and select an image or PDF file
3. Click "Extract Text" to process the file
4. View the extracted text in the results section

## API Key

The application uses the provided Google Gen AI API key. For production use, consider using environment variables for security.

## File Support

- **Images**: JPG, JPEG, PNG, GIF
- **Documents**: PDF

## Technology Stack

- **Backend**: FastHTML (Python web framework)
- **AI/OCR**: Google Gen AI SDK (Gemini 2.0 Flash)
- **Frontend**: Bootstrap 5
- **Containerization**: Docker with Debian base
