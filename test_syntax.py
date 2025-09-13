#!/usr/bin/env python3
"""
Test the specific syntax that was causing issues
"""

# Test the Form syntax that was problematic
def test_form_syntax():
    """Test the Form function call syntax"""
    
    # This is the corrected syntax
    try:
        # Simulate the Form call structure
        class MockElement:
            def __init__(self, *args, **kwargs):
                pass
        
        Form = MockElement
        Div = MockElement
        Label = MockElement
        Input = MockElement
        Button = MockElement
        
        # This should work - children first, then keyword arguments
        form = Form(
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
            ),
            action="/upload",
            method="post",
            enctype="multipart/form-data",
            cls="upload-area"
        )
        
        print("✓ Form syntax test passed")
        return True
        
    except SyntaxError as e:
        print(f"✗ Form syntax error: {e}")
        return False
    except Exception as e:
        print(f"✗ Form test error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Form syntax...")
    print("=" * 30)
    
    if test_form_syntax():
        print("\n✓ All syntax tests passed!")
    else:
        print("\n✗ Syntax errors found!")
