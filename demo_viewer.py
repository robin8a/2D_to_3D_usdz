#!/usr/bin/env python3
"""
Demo script that creates sample USDZ scenes and starts the web viewer.
This provides a complete demonstration of the USDZ visualization system.
"""

import os
import sys
import time
import subprocess
from create_usdz_alternative import create_usdz_alternative

def create_demo_scenes():
    """Create a variety of demo scenes for visualization."""
    print("🎨 Creating demo scenes...")
    print("=" * 50)
    
    demo_scenes = [
        {
            'name': 'basic_garden.usdz',
            'description': 'Basic garden with ground, rock, and tree'
        },
        {
            'name': 'minimal_scene.usdz', 
            'description': 'Minimal scene with essential elements'
        },
        {
            'name': 'garden_scene.usdz',
            'description': 'Enhanced garden scene'
        },
        {
            'name': 'complex_scene.usdz',
            'description': 'Complex scene with multiple objects'
        }
    ]
    
    created_scenes = []
    
    for scene in demo_scenes:
        if not os.path.exists(scene['name']):
            print(f"Creating {scene['name']}...")
            try:
                result = create_usdz_alternative(scene['name'])
                if result:
                    created_scenes.append(scene['name'])
                    print(f"  ✅ Created: {scene['name']}")
                else:
                    print(f"  ❌ Failed: {scene['name']}")
            except Exception as e:
                print(f"  ❌ Error creating {scene['name']}: {e}")
        else:
            print(f"  ✅ Already exists: {scene['name']}")
            created_scenes.append(scene['name'])
    
    print(f"\n📊 Created {len(created_scenes)} demo scenes")
    return created_scenes

def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ required")
        return False
    
    # Check if we can import required modules
    try:
        import http.server
        import socketserver
        import webbrowser
        print("✅ All required modules available")
        return True
    except ImportError as e:
        print(f"❌ Missing required module: {e}")
        return False

def start_web_viewer():
    """Start the web viewer server."""
    print("\n🌐 Starting web viewer...")
    print("=" * 50)
    
    try:
        # Import and run the server
        from serve_viewer import main as serve_main
        serve_main()
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error starting web viewer: {e}")
        print("\nYou can manually start the server by running:")
        print("  python serve_viewer.py")

def show_usage_instructions():
    """Show usage instructions for the web viewer."""
    print("\n📱 Web Viewer Usage Instructions")
    print("=" * 50)
    print("1. The web viewer will open automatically in your browser")
    print("2. You can interact with 3D models using mouse/touch:")
    print("   - Drag to rotate")
    print("   - Scroll to zoom")
    print("   - Right-click and drag to pan")
    print("3. For AR viewing:")
    print("   - On mobile: Tap the 'View in AR' button")
    print("   - Requires ARCore (Android) or ARKit (iOS)")
    print("4. Supported file formats:")
    print("   - USDZ for AR viewing")
    print("   - GLB/GLTF for web viewing")
    print("\n🔗 Useful links:")
    print("   - Model Viewer Documentation: https://modelviewer.dev/")
    print("   - ARCore WebXR: https://developers.google.com/ar/develop/webxr/model-viewer")

def main():
    """Main demo function."""
    print("🌱 USDZ Garden Scene Viewer Demo")
    print("=" * 50)
    print("This demo will create sample USDZ scenes and start a web viewer")
    print("for visualizing them in 3D and AR.")
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install required dependencies and try again")
        return
    
    # Create demo scenes
    scenes = create_demo_scenes()
    
    if not scenes:
        print("\n❌ No scenes were created. Please check the error messages above.")
        return
    
    # Show usage instructions
    show_usage_instructions()
    
    # Ask user if they want to start the web viewer
    print(f"\n🚀 Ready to start web viewer with {len(scenes)} scenes")
    response = input("Start web viewer now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        start_web_viewer()
    else:
        print("\n📝 To start the web viewer manually, run:")
        print("  python serve_viewer.py")
        print("\n📁 Your USDZ files are ready for viewing!")

if __name__ == "__main__":
    main()
