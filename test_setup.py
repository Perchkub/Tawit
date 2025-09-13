#!/usr/bin/env python3
"""
Test script to verify the OCR application setup
"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from python_fasthtml.common import *
        print("✓ FastHTML imported successfully")
    except ImportError as e:
        print(f"✗ FastHTML import failed: {e}")
        return False
    
    try:
        from google import genai
        from google.genai import types
        print("✓ Google Gen AI SDK imported successfully")
    except ImportError as e:
        print(f"✗ Google Gen AI SDK import failed: {e}")
        return False
    
    try:
        import io
        import base64
        from PIL import Image
        import PyPDF2
        from pdf2image import convert_from_bytes
        print("✓ All other dependencies imported successfully")
    except ImportError as e:
        print(f"✗ Other dependencies import failed: {e}")
        return False
    
    return True

def test_client_initialization():
    """Test Google Gen AI client initialization"""
    try:
        from google import genai
        client = genai.Client(api_key='AIzaSyB5t3z6QYDrT-9oxvc_qeP-RKx6cDdveVQ')
        print("✓ Google Gen AI client initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Google Gen AI client initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing OCR Application Setup...")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    print()
    
    # Test client initialization
    client_ok = test_client_initialization()
    print()
    
    if imports_ok and client_ok:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: python app.py")
        print("3. Open browser: http://localhost:5000")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        print("\nTo install dependencies:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
