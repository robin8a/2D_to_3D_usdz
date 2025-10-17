#!/usr/bin/env python3
"""
Alternative USDZ creation implementation that doesn't require USD Core.
This creates a basic USDZ file by manually creating the USD content and packaging it.
"""

import os
import shutil
import zipfile
import tempfile
from datetime import datetime

def create_usd_content():
    """Create the USD content as a string."""
    usd_content = '''#usda 1.0
(
    defaultPrim = "World"
    upAxis = "Y"
)

def Xform "World" (
    kind = "group"
)
{
    def Plane "Ground" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {
        double3 xformOp:translate = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
        
        float3[] extent = [(-100, -0.01, -100), (100, 0, 100)]
        
        color3f[] primvars:displayColor = [(0.3, 0.5, 0.1)]
        uniform token primvars:displayColorInterpolation = "constant"
    }
    
    def Cube "Rock1" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {
        double3 xformOp:translate = (5, 1, 5)
        uniform token[] xformOpOrder = ["xformOp:translate"]
        
        double size = 2
        
        color3f[] primvars:displayColor = [(0.5, 0.5, 0.5)]
        uniform token primvars:displayColorInterpolation = "constant"
    }
    
    def Cube "Tree1" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {
        double3 xformOp:translate = (-5, 0.75, -5)
        uniform token[] xformOpOrder = ["xformOp:translate"]
        
        double size = 1.5
        
        color3f[] primvars:displayColor = [(0.1, 0.3, 0.1)]
        uniform token primvars:displayColorInterpolation = "constant"
    }
}
'''
    return usd_content

def create_usdz_alternative(output_filename="alternative_scene.usdz"):
    """
    Creates a USDZ file using an alternative method that doesn't require USD Core.
    
    Args:
        output_filename (str): The desired name for the final USDZ file.
    
    Returns:
        str: Path to the created USDZ file, or None if failed.
    """
    print(f"Creating USDZ file: {output_filename}")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="usdz_temp_")
    print(f"Using temporary directory: {temp_dir}")
    
    try:
        # Create the main USD file
        usd_file_path = os.path.join(temp_dir, "scene.usda")
        usd_content = create_usd_content()
        
        with open(usd_file_path, 'w') as f:
            f.write(usd_content)
        
        print(f"USD content written to: {usd_file_path}")
        
        # Create the final USDZ file
        final_usdz_path = os.path.join(os.getcwd(), output_filename)
        
        with zipfile.ZipFile(final_usdz_path, 'w', zipfile.ZIP_DEFLATED) as usdz_file:
            # Add the main USD file
            usdz_file.write(usd_file_path, "scene.usda")
            
            # Add any additional files that might be needed
            # For now, we'll just add the main scene file
        
        print(f"USDZ file created successfully: {final_usdz_path}")
        print(f"File size: {os.path.getsize(final_usdz_path)} bytes")
        
        return final_usdz_path
        
    except Exception as e:
        print(f"Error creating USDZ file: {e}")
        return None
    
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            print(f"Warning: Failed to clean up temporary directory: {e}")

def validate_usdz_file(file_path):
    """
    Basic validation of the created USDZ file.
    
    Args:
        file_path (str): Path to the USDZ file to validate.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return False
    
    try:
        # Check if it's a valid ZIP file
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            file_list = zip_file.namelist()
            print(f"USDZ contains files: {file_list}")
            
            # Check for the main USD file
            if "scene.usda" in file_list:
                print("✓ Main USD file found in USDZ")
                
                # Read and validate the USD content
                usd_content = zip_file.read("scene.usda").decode('utf-8')
                if "#usda 1.0" in usd_content:
                    print("✓ Valid USD format detected")
                    return True
                else:
                    print("✗ Invalid USD format")
                    return False
            else:
                print("✗ Main USD file not found in USDZ")
                return False
                
    except zipfile.BadZipFile:
        print("✗ Invalid ZIP file format")
        return False
    except Exception as e:
        print(f"✗ Error validating USDZ file: {e}")
        return False

def main():
    """Main function to create and validate the alternative USDZ file."""
    print("=" * 60)
    print("Alternative USDZ Creation (No USD Core Required)")
    print("=" * 60)
    
    # Create the USDZ file
    result = create_usdz_alternative("test_alternative.usdz")
    
    if result:
        print(f"\n✓ USDZ file created successfully: {result}")
        
        # Validate the file
        print("\nValidating USDZ file...")
        if validate_usdz_file(result):
            print("✓ USDZ file validation passed")
        else:
            print("✗ USDZ file validation failed")
    else:
        print("\n✗ Failed to create USDZ file")

if __name__ == "__main__":
    main()
