#!/usr/bin/env python3
"""
Simple script to test if all requirements can be installed
"""

import subprocess
import sys

def test_package_installation():
    """Test if packages can be installed"""
    packages = [
        "python-fasthtml==0.12.25",
        "google-genai==0.8.0", 
        "python-multipart==0.0.6",
        "Pillow==10.1.0",
        "PyPDF2==3.0.1",
        "pdf2image==1.16.3"
    ]
    
    print("Testing package installation...")
    print("=" * 50)
    
    for package in packages:
        try:
            print(f"Testing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--dry-run", package
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✓ {package} - Available")
            else:
                print(f"✗ {package} - Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"✗ {package} - Timeout")
        except Exception as e:
            print(f"✗ {package} - Exception: {e}")
    
    print("\n" + "=" * 50)
    print("Package availability test completed!")

if __name__ == "__main__":
    test_package_installation()
