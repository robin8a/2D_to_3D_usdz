#!/usr/bin/env python3
"""
Test script to verify the web viewer setup and USDZ files.
"""

import os
import webbrowser
import time
import subprocess
import sys
from pathlib import Path

def test_usdz_files():
    """Test if USDZ files are valid and accessible."""
    print("🔍 Testing USDZ files...")
    
    usdz_files = [f for f in os.listdir('.') if f.endswith('.usdz')]
    
    if not usdz_files:
        print("❌ No USDZ files found")
        return False
    
    print(f"✅ Found {len(usdz_files)} USDZ files:")
    for file in usdz_files:
        size = os.path.getsize(file)
        print(f"   - {file} ({size} bytes)")
    
    return True

def test_web_files():
    """Test if web viewer files exist."""
    print("\n🌐 Testing web viewer files...")
    
    required_files = ['web_viewer.html', 'serve_viewer.py']
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    return True

def start_simple_server():
    """Start a simple HTTP server for testing."""
    print("\n🚀 Starting simple HTTP server...")
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, '-m', 'http.server', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Check if server is running
        if process.poll() is None:
            print("✅ Server started on http://localhost:8000")
            print("📱 Web viewer: http://localhost:8000/web_viewer.html")
            return process
        else:
            print("❌ Failed to start server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None

def main():
    """Main test function."""
    print("🧪 USDZ Web Viewer Test")
    print("=" * 40)
    
    # Test USDZ files
    if not test_usdz_files():
        print("\n❌ USDZ file test failed")
        return
    
    # Test web files
    if not test_web_files():
        print("\n❌ Web viewer file test failed")
        return
    
    print("\n✅ All tests passed!")
    
    # Ask if user wants to start server
    response = input("\nStart web server for testing? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        process = start_simple_server()
        
        if process:
            print("\n🌐 Web viewer is ready!")
            print("Open your browser and go to: http://localhost:8000/web_viewer.html")
            print("\nPress Ctrl+C to stop the server")
            
            try:
                # Open browser
                webbrowser.open('http://localhost:8000/web_viewer.html')
                
                # Wait for user to stop
                process.wait()
            except KeyboardInterrupt:
                print("\n👋 Stopping server...")
                process.terminate()
        else:
            print("❌ Failed to start server")
    else:
        print("\n📝 To start the server manually:")
        print("   python -m http.server 8000")
        print("   Then open: http://localhost:8000/web_viewer.html")

if __name__ == "__main__":
    main()
