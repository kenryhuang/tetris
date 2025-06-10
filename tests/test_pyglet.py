#!/usr/bin/env python3
"""Simple test script to check if Pyglet works in the current environment."""

import os
import sys

def test_pyglet_basic():
    """Test basic Pyglet functionality."""
    print("Testing Pyglet compatibility...")
    print(f"Python version: {sys.version}")
    print(f"Operating system: {os.name}")
    print(f"DISPLAY environment: {os.environ.get('DISPLAY', 'Not set')}")
    
    try:
        import pyglet
        print(f"Pyglet version: {pyglet.version}")
        
        # Test if we can get platform info
        platform = pyglet.window.get_platform()
        print(f"Platform: {platform}")
        
        # Test if we can get display
        try:
            display = platform.get_default_display()
            print(f"Default display: {display}")
            
            # Test if we can get screen
            screen = display.get_default_screen()
            print(f"Default screen: {screen}")
            print(f"Screen size: {screen.width}x{screen.height}")
            
            print("✓ Pyglet basic functionality works!")
            return True
            
        except Exception as e:
            print(f"✗ Display/Screen error: {e}")
            return False
            
    except ImportError as e:
        print(f"✗ Pyglet import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_pyglet_window():
    """Test if we can create a Pyglet window."""
    print("\nTesting Pyglet window creation...")
    
    try:
        import pyglet
        
        # Try to create a minimal window
        config = pyglet.gl.Config(double_buffer=False)
        window = pyglet.window.Window(
            width=100, 
            height=100, 
            visible=False,
            config=config
        )
        
        print("✓ Window creation successful!")
        window.close()
        return True
        
    except Exception as e:
        print(f"✗ Window creation failed: {e}")
        
        # Try alternative configurations
        try:
            print("Trying alternative configuration...")
            window = pyglet.window.Window(
                width=100, 
                height=100, 
                visible=False
            )
            print("✓ Alternative window creation successful!")
            window.close()
            return True
        except Exception as e2:
            print(f"✗ Alternative configuration also failed: {e2}")
            return False

def main():
    """Main test function."""
    print("Pyglet Environment Test")
    print("=======================")
    
    basic_ok = test_pyglet_basic()
    
    if basic_ok:
        window_ok = test_pyglet_window()
        
        if window_ok:
            print("\n🎉 All tests passed! Pyglet should work in this environment.")
            print("You can now run: python main_pyglet.py")
        else:
            print("\n⚠️  Basic Pyglet works, but window creation failed.")
            print("This might be due to:")
            print("  - No X11 display available (SSH without X forwarding)")
            print("  - Missing graphics drivers")
            print("  - Headless environment")
            print("\nTry running with X11 forwarding: ssh -X username@hostname")
    else:
        print("\n❌ Pyglet basic functionality failed.")
        print("Please install Pyglet: pip install pyglet")
    
    return basic_ok and window_ok if basic_ok else False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)