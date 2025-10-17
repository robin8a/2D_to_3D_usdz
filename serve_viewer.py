#!/usr/bin/env python3
"""
Simple HTTP server to serve the USDZ web viewer and files.
This allows you to view the USDZ scenes in a web browser with AR support.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class USDZHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve USDZ files with proper MIME types."""
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Set proper MIME type for USDZ files
        if self.path.endswith('.usdz'):
            self.send_header('Content-Type', 'model/vnd.usdz+zip')
        elif self.path.endswith('.usda'):
            self.send_header('Content-Type', 'model/vnd.usd')
        elif self.path.endswith('.glb'):
            self.send_header('Content-Type', 'model/gltf-binary')
        elif self.path.endswith('.gltf'):
            self.send_header('Content-Type', 'model/gltf+json')
        
        super().end_headers()

def find_available_port(start_port=8000, max_port=8010):
    """Find an available port starting from start_port."""
    for port in range(start_port, max_port + 1):
        try:
            with socketserver.TCPServer(("", port), USDZHandler) as httpd:
                return port
        except OSError:
            continue
    return None

def create_sample_scenes():
    """Create sample USDZ scenes if they don't exist."""
    from create_usdz_alternative import create_usdz_alternative
    
    sample_scenes = [
        "test_alternative.usdz",
        "garden_scene.usdz", 
        "minimal_scene.usdz",
        "complex_scene.usdz"
    ]
    
    created_scenes = []
    for scene_file in sample_scenes:
        if not os.path.exists(scene_file):
            print(f"Creating sample scene: {scene_file}")
            try:
                result = create_usdz_alternative(scene_file)
                if result:
                    created_scenes.append(scene_file)
            except Exception as e:
                print(f"Failed to create {scene_file}: {e}")
        else:
            print(f"Scene already exists: {scene_file}")
            created_scenes.append(scene_file)
    
    return created_scenes

def main():
    """Start the HTTP server and open the web viewer."""
    print("🌱 USDZ Garden Scene Viewer Server")
    print("=" * 50)
    
    # Create sample scenes if they don't exist
    print("Creating sample scenes...")
    available_scenes = create_sample_scenes()
    
    if not available_scenes:
        print("❌ No scenes available. Please create some USDZ files first.")
        return
    
    print(f"✅ Found {len(available_scenes)} scenes:")
    for scene in available_scenes:
        print(f"   - {scene}")
    
    # Find available port
    port = find_available_port()
    if not port:
        print("❌ No available ports found. Please try again.")
        return
    
    # Start server
    print(f"\n🚀 Starting server on port {port}...")
    print(f"📱 Web viewer: http://localhost:{port}/web_viewer.html")
    print(f"📁 File server: http://localhost:{port}/")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", port), USDZHandler) as httpd:
            # Open browser automatically
            webbrowser.open(f'http://localhost:{port}/web_viewer.html')
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == "__main__":
    main()
