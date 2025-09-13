from fasthtml.common import *
from google import genai
from google.genai import types
import io
import base64
from PIL import Image
import PyPDF2
from pdf2image import convert_from_bytes
import tempfile
import os

# Initialize Google Gen AI client
client = genai.Client(api_key='AIzaSyB5t3z6QYDrT-9oxvc_qeP-RKx6cDdveVQ')

# Create FastHTML app
app = FastHTML()

def extract_text_from_image(image_bytes):
    """Extract text from image using Google Gen AI OCR"""
    try:
        # Convert bytes to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Create image part for the API
        image_part = types.Part.from_uri(
            file_uri=f"data:image/jpeg;base64,{image_base64}",
            mime_type="image/jpeg"
        )
        
        # Generate content with OCR prompt
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=[
                "Please extract all text from this image. Return only the extracted text without any additional commentary or formatting.",
                image_part
            ]
        )
        
        return response.text
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF using Google Gen AI OCR"""
    try:
        # First try to extract text directly from PDF
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text_content = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text()
        
        # If no text was extracted (scanned PDF), use OCR
        if not text_content.strip():
            # Convert PDF pages to images
            images = convert_from_bytes(pdf_bytes)
            text_content = ""
            
            for i, image in enumerate(images):
                # Convert PIL image to bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Extract text from image
                page_text = extract_text_from_image(img_byte_arr)
                text_content += f"\n--- Page {i+1} ---\n{page_text}\n"
        
        return text_content
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

@app.route("/")
def index():
    """Main page with file upload form"""
    return Html(
        Head(
            Title("OCR Text Extraction"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Style("""
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .container { background: #f5f5f5; padding: 30px; border-radius: 10px; }
                .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
                .upload-area:hover { border-color: #007bff; }
                .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
                .btn:hover { background: #0056b3; }
                .result { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #007bff; }
                .error { border-left-color: #dc3545; }
                .loading { text-align: center; color: #666; }
            """)
        ),
        Body(
            Div(
                H1("OCR Text Extraction", style="text-align: center; color: #333;"),
                P("Upload an image or PDF file to extract text using Google Gen AI OCR", style="text-align: center; color: #666;"),
                
                Form(
                    action="/upload",
                    method="post",
                    enctype="multipart/form-data",
                    cls="upload-area",
                    children=[
                        Div(
                            Div(
                                Label("Choose File:", style="display: block; margin-bottom: 10px; font-weight: bold;"),
                                Input(
                                    type="file",
                                    name="file",
                                    accept=".jpg,.jpeg,.png,.gif,.bmp,.pdf",
                                    required=True,
                                    style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;"
                                ),
                                style="margin-bottom: 20px;"
                            ),
                            Button(
                                "Extract Text",
                                type="submit",
                                cls="btn",
                                style="width: 100%;"
                            )
                        )
                    ]
                ),
                
                cls="container"
            )
        )
    )

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and OCR processing"""
    try:
        # Get uploaded file
        file = request.files.get("file")
        if not file:
            return Html(
                Body(
                    Div(
                        H1("Error"),
                        P("No file uploaded"),
                        A("Back to Upload", href="/", cls="btn")
                    )
                )
            )
        
        # Read file content
        file_content = file.read()
        file_extension = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        
        # Show loading message
        loading_html = Html(
            Head(
                Title("Processing..."),
                Meta(charset="utf-8"),
                Style("""
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; text-align: center; }
                    .loading { color: #666; }
                """)
            ),
            Body(
                Div(
                    H1("Processing File...", cls="loading"),
                    P("Please wait while we extract text from your file", cls="loading"),
                    Div(
                        style="width: 50px; height: 50px; border: 5px solid #f3f3f3; border-top: 5px solid #007bff; border-radius: 50%; animation: spin 1s linear infinite; margin: 20px auto;"
                    ),
                    Style("""
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    """)
                )
            )
        )
        
        # Process file based on type
        if file_extension in ['pdf']:
            extracted_text = extract_text_from_pdf(file_content)
        elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            extracted_text = extract_text_from_image(file_content)
        else:
            extracted_text = "Unsupported file type. Please upload an image (JPG, PNG, GIF, BMP) or PDF file."
        
        # Display results
        return Html(
            Head(
                Title("OCR Results"),
                Meta(charset="utf-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1"),
                Style("""
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .container { background: #f5f5f5; padding: 30px; border-radius: 10px; }
                    .result { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #007bff; }
                    .error { border-left-color: #dc3545; }
                    .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px 5px; }
                    .btn:hover { background: #0056b3; }
                    .text-content { white-space: pre-wrap; word-wrap: break-word; max-height: 400px; overflow-y: auto; }
                """)
            ),
            Body(
                Div(
                    H1("OCR Results"),
                    P(f"File: {file.filename}"),
                    
                    Div(
                        H3("Extracted Text:"),
                        Div(
                            extracted_text,
                            cls="text-content"
                        ),
                        cls="result"
                    ),
                    
                    Div(
                        A("Upload Another File", href="/", cls="btn"),
                        Button(
                            "Copy Text",
                            onclick="navigator.clipboard.writeText(document.querySelector('.text-content').textContent)",
                            cls="btn"
                        )
                    ),
                    
                    cls="container"
                )
            )
        )
        
    except Exception as e:
        return Html(
            Head(
                Title("Error"),
                Meta(charset="utf-8"),
                Style("""
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .error { color: #dc3545; }
                    .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
                """)
            ),
            Body(
                Div(
                    H1("Error", cls="error"),
                    P(f"An error occurred: {str(e)}", cls="error"),
                    A("Back to Upload", href="/", cls="btn")
                )
            )
        )

if __name__ == "__main__":
    # Run on port 5000 as specified in FastHTML documentation
    serve(port=5000)
