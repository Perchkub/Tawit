#!/usr/bin/env python3
"""
Simple syntax checker for app.py
"""

import ast
import sys

def check_syntax(filename):
    """Check if a Python file has valid syntax"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the source code
        ast.parse(source)
        print(f"✓ {filename} - Syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"✗ {filename} - Syntax Error:")
        print(f"  Line {e.lineno}: {e.text}")
        print(f"  Error: {e.msg}")
        return False
        
    except Exception as e:
        print(f"✗ {filename} - Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "app.py"
    
    print("Checking Python syntax...")
    print("=" * 40)
    
    if check_syntax(filename):
        print("\n✓ All syntax checks passed!")
    else:
        print("\n✗ Syntax errors found!")
        sys.exit(1)
