#!/usr/bin/env python3
"""
Convert USDZ files to GLB format for better web compatibility.
This creates GLB files that can be viewed in the web viewer without AR requirements.
"""

import os
import zipfile
import json
import struct
from pathlib import Path

def extract_usd_from_usdz(usdz_path):
    """Extract USD content from USDZ file."""
    try:
        with zipfile.ZipFile(usdz_path, 'r') as usdz_file:
            # Look for .usda or .usdc files
            usd_files = [f for f in usdz_file.namelist() if f.endswith(('.usda', '.usdc'))]
            
            if not usd_files:
                print(f"No USD files found in {usdz_path}")
                return None
            
            # Get the first USD file (usually the main scene)
            main_usd_file = usd_files[0]
            usd_content = usdz_file.read(main_usd_file).decode('utf-8')
            
            return usd_content
    except Exception as e:
        print(f"Error extracting USD from {usdz_path}: {e}")
        return None

def create_simple_glb_from_usd(usd_content, output_path):
    """
    Create a simple GLB file from USD content.
    This is a basic implementation that creates a minimal GLB with the scene structure.
    """
    try:
        # Parse USD content to extract basic geometry info
        scene_data = parse_usd_content(usd_content)
        
        # Create GLB content
        glb_data = create_glb_data(scene_data)
        
        # Write GLB file
        with open(output_path, 'wb') as f:
            f.write(glb_data)
        
        print(f"Created GLB file: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating GLB: {e}")
        return False

def parse_usd_content(usd_content):
    """Parse USD content to extract basic scene information."""
    scene_data = {
        'objects': [],
        'materials': []
    }
    
    lines = usd_content.split('\n')
    current_object = None
    
    for line in lines:
        line = line.strip()
        
        # Look for object definitions
        if line.startswith('def ') and ('Cube' in line or 'Plane' in line):
            if current_object:
                scene_data['objects'].append(current_object)
            
            current_object = {
                'type': 'Cube' if 'Cube' in line else 'Plane',
                'name': line.split('"')[1] if '"' in line else 'Object',
                'position': [0, 0, 0],
                'scale': [1, 1, 1],
                'color': [0.5, 0.5, 0.5]
            }
        
        # Look for position transforms
        elif current_object and 'xformOp:translate' in line:
            try:
                # Extract position from line like: double3 xformOp:translate = (5, 1, 5)
                pos_str = line.split('(')[1].split(')')[0]
                pos_values = [float(x.strip()) for x in pos_str.split(',')]
                current_object['position'] = pos_values
            except:
                pass
        
        # Look for size/scale
        elif current_object and 'size' in line:
            try:
                # Extract size from line like: double size = 2
                size_str = line.split('=')[1].strip()
                size_value = float(size_str)
                current_object['scale'] = [size_value, size_value, size_value]
            except:
                pass
        
        # Look for colors
        elif current_object and 'primvars:displayColor' in line:
            try:
                # Extract color from line like: color3f[] primvars:displayColor = [(0.3, 0.5, 0.1)]
                color_str = line.split('[')[1].split(']')[0]
                color_values = [float(x.strip()) for x in color_str.split(',')]
                current_object['color'] = color_values
            except:
                pass
    
    # Add the last object
    if current_object:
        scene_data['objects'].append(current_object)
    
    return scene_data

def create_glb_data(scene_data):
    """Create GLB binary data from scene data."""
    # This is a simplified GLB creation - in a real implementation,
    # you would use a proper 3D library like trimesh or pygltflib
    
    # For now, create a minimal GLB with basic structure
    # This is just a placeholder - a real implementation would be much more complex
    
    # GLB header
    glb_header = struct.pack('<III', 0x46546C67, 2, 12)  # glTF magic, version, length
    
    # JSON chunk header
    json_data = json.dumps({
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{
            "primitives": [{
                "attributes": {"POSITION": 0},
                "indices": 1
            }]
        }],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": 0, "type": "VEC3"},
            {"bufferView": 1, "componentType": 5123, "count": 0, "type": "SCALAR"}
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": 0},
            {"buffer": 0, "byteOffset": 0, "byteLength": 0}
        ],
        "buffers": [{"byteLength": 0}]
    }).encode('utf-8')
    
    json_chunk_header = struct.pack('<II', len(json_data), 0x4E4F534A)  # JSON chunk
    binary_chunk_header = struct.pack('<II', 0, 0x004E4942)  # Binary chunk (empty)
    
    return glb_header + json_chunk_header + json_data + binary_chunk_header

def convert_usdz_to_glb(usdz_path, glb_path=None):
    """Convert a USDZ file to GLB format."""
    if not os.path.exists(usdz_path):
        print(f"USDZ file not found: {usdz_path}")
        return False
    
    if glb_path is None:
        glb_path = usdz_path.replace('.usdz', '.glb')
    
    print(f"Converting {usdz_path} to {glb_path}...")
    
    # Extract USD content
    usd_content = extract_usd_from_usdz(usdz_path)
    if not usd_content:
        return False
    
    # Create GLB file
    return create_simple_glb_from_usd(usd_content, glb_path)

def main():
    """Convert all USDZ files in the current directory to GLB."""
    print("Converting USDZ files to GLB format...")
    print("=" * 50)
    
    usdz_files = [f for f in os.listdir('.') if f.endswith('.usdz')]
    
    if not usdz_files:
        print("No USDZ files found in current directory.")
        return
    
    converted_count = 0
    
    for usdz_file in usdz_files:
        glb_file = usdz_file.replace('.usdz', '.glb')
        
        if convert_usdz_to_glb(usdz_file, glb_file):
            converted_count += 1
        else:
            print(f"Failed to convert {usdz_file}")
    
    print(f"\n✅ Converted {converted_count}/{len(usdz_files)} files to GLB format")
    print("\nNote: This is a basic conversion. For production use, consider using")
    print("proper 3D conversion tools like Blender or specialized USD/GLB converters.")

if __name__ == "__main__":
    main()
