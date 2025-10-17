#!/usr/bin/env python3
"""
Test script for the alternative USDZ creation method.
This works without requiring USD Core, making it compatible with older macOS versions.
"""

import os
import sys
import tempfile
import shutil
from create_usdz_alternative import create_usdz_alternative, validate_usdz_file

def test_alternative_usdz_creation():
    """Test the alternative USDZ creation functionality."""
    print("=" * 60)
    print("Testing Alternative USDZ Creation")
    print("=" * 60)
    
    # Test 1: Basic USDZ creation
    print("\n1. Testing basic USDZ creation...")
    try:
        result = create_usdz_alternative("test_alternative_basic.usdz")
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
        custom_result = create_usdz_alternative("custom_alternative_scene.usdz")
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
        if validate_usdz_file(result):
            print("✓ USDZ file validation passed")
        else:
            print("✗ USDZ file validation failed")
            return False
    except Exception as e:
        print(f"✗ USDZ file validation failed with error: {e}")
        return False
    
    # Test 4: Multiple scene creation
    print("\n4. Testing multiple scene creation...")
    try:
        scenes = []
        for i in range(3):
            scene_name = f"test_scene_{i}.usdz"
            scene_result = create_usdz_alternative(scene_name)
            if scene_result and os.path.exists(scene_result):
                scenes.append(scene_result)
                print(f"  ✓ Created {scene_name}")
            else:
                print(f"  ✗ Failed to create {scene_name}")
                return False
        
        print(f"✓ Successfully created {len(scenes)} scenes")
    except Exception as e:
        print(f"✗ Multiple scene creation failed with error: {e}")
        return False
    
    # Test 5: Cleanup
    print("\n5. Testing cleanup...")
    try:
        test_files = [result, custom_result] + scenes
        for file_path in test_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"  ✓ Cleaned up {os.path.basename(file_path)}")
    except Exception as e:
        print(f"✗ Cleanup failed with error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("All alternative tests passed! ✓")
    print("=" * 60)
    return True

def test_environment_compatibility():
    """Test environment compatibility without USD Core."""
    print("=" * 60)
    print("Testing Environment Compatibility")
    print("=" * 60)
    
    # Test 1: Python version
    print(f"\n1. Python version: {sys.version}")
    
    # Test 2: Required standard modules
    print("\n2. Testing required standard modules...")
    try:
        import os
        import shutil
        import zipfile
        import tempfile
        print("✓ All required standard modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import required modules: {e}")
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
    
    # Test 5: ZIP functionality
    print("\n5. Testing ZIP functionality...")
    try:
        test_zip = "test_zip.zip"
        with zipfile.ZipFile(test_zip, 'w') as zf:
            zf.writestr("test.txt", "test content")
        
        with zipfile.ZipFile(test_zip, 'r') as zf:
            content = zf.read("test.txt").decode('utf-8')
            if content == "test content":
                print("✓ ZIP functionality OK")
            else:
                print("✗ ZIP content validation failed")
                return False
        
        os.remove(test_zip)
    except Exception as e:
        print(f"✗ ZIP functionality test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("Environment compatibility OK! ✓")
    print("=" * 60)
    return True

def test_usd_content_validation():
    """Test the USD content structure."""
    print("=" * 60)
    print("Testing USD Content Validation")
    print("=" * 60)
    
    try:
        from create_usdz_alternative import create_usd_content
        usd_content = create_usd_content()
        
        # Check for required USD elements
        required_elements = [
            "#usda 1.0",
            "defaultPrim = \"World\"",
            "upAxis = \"Y\"",
            "def Xform \"World\"",
            "def Plane \"Ground\"",
            "def Cube \"Rock1\"",
            "def Cube \"Tree1\"",
            "primvars:displayColor"
        ]
        
        print("\nChecking USD content structure...")
        for element in required_elements:
            if element in usd_content:
                print(f"  ✓ Found: {element}")
            else:
                print(f"  ✗ Missing: {element}")
                return False
        
        print("\n✓ USD content structure validation passed")
        return True
        
    except Exception as e:
        print(f"✗ USD content validation failed with error: {e}")
        return False

def main():
    """Main test function."""
    print("Alternative USDZ Creation Test Suite")
    print("=" * 60)
    
    # Test environment compatibility first
    if not test_environment_compatibility():
        print("\nEnvironment compatibility test failed.")
        return False
    
    # Test USD content validation
    if not test_usd_content_validation():
        print("\nUSD content validation failed.")
        return False
    
    # Test USDZ creation
    if not test_alternative_usdz_creation():
        print("\nUSDZ creation tests failed.")
        return False
    
    print("\n🎉 All tests completed successfully!")
    print("\nThe alternative implementation works without USD Core and is compatible")
    print("with older macOS versions. You can now create USDZ files using:")
    print("  python create_usdz_alternative.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
