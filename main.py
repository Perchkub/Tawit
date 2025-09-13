from fasthtml.common import *
from google import genai
from google.genai import types
import os
import tempfile
from PIL import Image
import PyPDF2
import io
import base64

# Initialize Google Gen AI client
client = genai.Client(api_key="AIzaSyB5t3z6QYDrT-9oxvc_qeP-RKx6cDdveVQ")

# Create FastHTML app
app = FastHTML()

# Configure upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_image_for_ocr(image_data):
    """Process image data for OCR using Google Gen AI"""
    try:
        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_file.write(image_data)
            tmp_file_path = tmp_file.name
        
        # Upload file to Google Gen AI
        uploaded_file = client.files.upload(file=tmp_file_path)
        
        # Generate content with OCR prompt
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=[
                'Please extract all text from this image using OCR. Return only the extracted text without any additional commentary or formatting.',
                uploaded_file
            ]
        )
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return response.text
        
    except Exception as e:
        return f"Error processing image: {str(e)}"

def extract_images_from_pdf(pdf_data):
    """Extract images from PDF for OCR processing"""
    try:
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        extracted_text = ""
        
        for page_num, page in enumerate(pdf_reader.pages):
            # Try to extract text directly from PDF first
            page_text = page.extract_text()
            if page_text.strip():
                extracted_text += f"Page {page_num + 1}:\n{page_text}\n\n"
            else:
                # If no text found, we would need to extract images from PDF
                # For now, we'll note that OCR is needed
                extracted_text += f"Page {page_num + 1}: [Image content - OCR processing needed]\n\n"
        
        return extracted_text
        
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

@app.route("/")
def index():
    """Main page with file upload form"""
    return Html(
        Head(
            Title("OCR Web Application"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css")
        ),
        Body(
            Div(
                Div(
                    H1("OCR Web Application", Class="text-center mb-4"),
                    P("Upload images or PDF files to extract text using Google Gen AI", Class="text-center text-muted mb-4"),
                    Class="col-md-8 mx-auto"
                ),
                Class="container mt-5"
            ),
            Div(
                Div(
                    Form(
                        Div(
                            Label("Select File", Class="form-label"),
                            Input(type="file", name="file", accept=".jpg,.jpeg,.png,.gif,.pdf", Class="form-control", required=True),
                            Class="mb-3"
                        ),
                        Div(
                            Button("Extract Text", type="submit", Class="btn btn-primary btn-lg"),
                            Class="text-center"
                        ),
                        action="/upload",
                        method="post",
                        enctype="multipart/form-data"
                    ),
                    Class="col-md-6 mx-auto"
                ),
                Class="container"
            ),
            Div(
                Div(
                    Div(id="result", Class="mt-5"),
                    Class="col-md-10 mx-auto"
                ),
                Class="container"
            ),
            Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js")
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
                Div(
                    Div(
                        Div(
                            H4("Error", Class="alert-heading"),
                            P("No file uploaded"),
                            Class="alert alert-danger"
                        ),
                        Class="col-md-8 mx-auto"
                    ),
                    Class="container mt-5"
                )
            )
        
        # Read file data
        file_data = file.read()
        file_extension = file.filename.split('.')[-1].lower()
        
        # Process based on file type
        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            # Process image
            result_text = process_image_for_ocr(file_data)
        elif file_extension == 'pdf':
            # Process PDF
            result_text = extract_images_from_pdf(file_data)
        else:
            result_text = "Unsupported file type. Please upload images (JPG, PNG, GIF) or PDF files."
        
        # Display results
        return Html(
            Div(
                Div(
                    Div(
                        H4("OCR Results", Class="mb-3"),
                        Div(
                            H5("Extracted Text:", Class="mb-2"),
                            Pre(result_text, Class="bg-light p-3 rounded", style="white-space: pre-wrap; max-height: 400px; overflow-y: auto;"),
                            Class="mb-3"
                        ),
                        A("Upload Another File", href="/", Class="btn btn-secondary"),
                        Class="alert alert-success"
                    ),
                    Class="col-md-10 mx-auto"
                ),
                Class="container mt-5"
            )
        )
        
    except Exception as e:
        return Html(
            Div(
                Div(
                    Div(
                        H4("Error", Class="alert-heading"),
                        P(f"An error occurred: {str(e)}"),
                        A("Try Again", href="/", Class="btn btn-secondary"),
                        Class="alert alert-danger"
                    ),
                    Class="col-md-8 mx-auto"
                ),
                Class="container mt-5"
            )
        )

if __name__ == "__main__":
    serve(port=5000)
