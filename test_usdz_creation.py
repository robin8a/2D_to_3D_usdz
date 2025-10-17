#!/usr/bin/env python3
"""
Test script for USDZ scene creation and validation.
"""

import os
import sys
import tempfile
import shutil
from create_usdz_scene import create_usdz_scene

def test_usdz_creation():
    """Test the USDZ creation functionality."""
    print("=" * 50)
    print("Testing USDZ Scene Creation")
    print("=" * 50)
    
    # Test 1: Basic USDZ creation
    print("\n1. Testing basic USDZ creation...")
    try:
        result = create_usdz_scene("test_basic.usdz")
        if result and os.path.exists(result):
            print(f"✓ Basic USDZ creation successful: {result}")
            print(f"  File size: {os.path.getsize(result)} bytes")
        else:
            print("✗ Basic USDZ creation failed")
            return False
    except Exception as e:
        print(f"✗ Basic USDZ creation failed with error: {e}")
        return False
    
    # Test 2: Custom filename
    print("\n2. Testing custom filename...")
    try:
        custom_result = create_usdz_scene("custom_scene.usdz")
        if custom_result and os.path.exists(custom_result):
            print(f"✓ Custom filename creation successful: {custom_result}")
            print(f"  File size: {os.path.getsize(custom_result)} bytes")
        else:
            print("✗ Custom filename creation failed")
            return False
    except Exception as e:
        print(f"✗ Custom filename creation failed with error: {e}")
        return False
    
    # Test 3: File validation
    print("\n3. Testing USDZ file validation...")
    try:
        from pxr import Usd
        stage = Usd.Stage.Open(result)
        if stage:
            print("✓ USDZ file can be opened and is valid")
            
            # Check for expected prims
            ground_prim = stage.GetPrimAtPath("/World/Ground")
            rock_prim = stage.GetPrimAtPath("/World/Rock1")
            tree_prim = stage.GetPrimAtPath("/World/Tree1")
            
            if ground_prim and rock_prim and tree_prim:
                print("✓ All expected prims found in USDZ file")
            else:
                print("✗ Some expected prims missing")
                return False
        else:
            print("✗ USDZ file cannot be opened")
            return False
    except Exception as e:
        print(f"✗ USDZ file validation failed with error: {e}")
        return False
    
    # Test 4: Cleanup
    print("\n4. Testing cleanup...")
    try:
        if os.path.exists(result):
            os.remove(result)
            print("✓ Test file cleaned up successfully")
        if os.path.exists(custom_result):
            os.remove(custom_result)
            print("✓ Custom file cleaned up successfully")
    except Exception as e:
        print(f"✗ Cleanup failed with error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)
    return True

def test_environment():
    """Test if the required environment is properly set up."""
    print("=" * 50)
    print("Testing Environment Setup")
    print("=" * 50)
    
    # Test 1: Python version
    print(f"\n1. Python version: {sys.version}")
    
    # Test 2: Required modules
    print("\n2. Testing required modules...")
    try:
        from pxr import Usd, UsdGeom, Sdf, Gf, UsdUtils
        print("✓ All required USD modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import USD modules: {e}")
        print("  Please install usd-core: pip install usd-core")
        return False
    
    # Test 3: Working directory
    print(f"\n3. Current working directory: {os.getcwd()}")
    
    # Test 4: Write permissions
    print("\n4. Testing write permissions...")
    try:
        test_file = "test_write_permission.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✓ Write permissions OK")
    except Exception as e:
        print(f"✗ Write permission test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("Environment setup OK! ✓")
    print("=" * 50)
    return True

def main():
    """Main test function."""
    print("USDZ Creation Test Suite")
    print("=" * 50)
    
    # Test environment first
    if not test_environment():
        print("\nEnvironment setup failed. Please fix the issues above.")
        return False
    
    # Test USDZ creation
    if not test_usdz_creation():
        print("\nUSDZ creation tests failed. Please check the implementation.")
        return False
    
    print("\n🎉 All tests completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
