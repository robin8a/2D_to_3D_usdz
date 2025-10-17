#!/usr/bin/env python3
"""
Example script demonstrating different USDZ scene configurations.
"""

import os
from create_usdz_alternative import create_usdz_alternative

def create_garden_scene():
    """Create a more complex garden scene with multiple elements."""
    print("Creating garden scene...")
    
    # This would be an enhanced version of create_usdz_alternative
    # For now, we'll use the basic version
    result = create_usdz_alternative("garden_scene.usdz")
    return result

def create_minimal_scene():
    """Create a minimal scene with just a ground plane."""
    print("Creating minimal scene...")
    
    # This would create a simpler scene
    result = create_usdz_alternative("minimal_scene.usdz")
    return result

def create_complex_scene():
    """Create a complex scene with multiple objects and materials."""
    print("Creating complex scene...")
    
    # This would create a more complex scene
    result = create_usdz_alternative("complex_scene.usdz")
    return result

def main():
    """Create example scenes for testing."""
    print("Creating example USDZ scenes...")
    print("=" * 50)
    
    scenes = [
        ("Basic Scene", create_usdz_alternative),
        ("Garden Scene", create_garden_scene),
        ("Minimal Scene", create_minimal_scene),
        ("Complex Scene", create_complex_scene),
    ]
    
    results = []
    
    for scene_name, scene_func in scenes:
        print(f"\nCreating {scene_name}...")
        try:
            result = scene_func()
            if result and os.path.exists(result):
                file_size = os.path.getsize(result)
                print(f"✓ {scene_name} created successfully: {result}")
                print(f"  File size: {file_size} bytes")
                results.append((scene_name, result, file_size))
            else:
                print(f"✗ {scene_name} creation failed")
        except Exception as e:
            print(f"✗ {scene_name} creation failed with error: {e}")
    
    print("\n" + "=" * 50)
    print("Summary of created scenes:")
    print("=" * 50)
    
    for scene_name, file_path, file_size in results:
        print(f"{scene_name}: {file_path} ({file_size} bytes)")
    
    print(f"\nTotal scenes created: {len(results)}")
    
    # Cleanup option
    cleanup = input("\nDo you want to clean up the created files? (y/n): ").lower().strip()
    if cleanup == 'y':
        for scene_name, file_path, _ in results:
            try:
                os.remove(file_path)
                print(f"✓ Cleaned up {scene_name}")
            except Exception as e:
                print(f"✗ Failed to clean up {scene_name}: {e}")

if __name__ == "__main__":
    main()
