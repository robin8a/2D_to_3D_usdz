import os
import shutil
from pxr import Usd, UsdGeom, Sdf, Gf, UsdUtils

# Global variable to store the path of the created USDZ file for debugging
global_usdz_path = None

def create_usdz_scene(output_filename="colab_scene.usdz"):
    """
    Creates a simple USD scene with a ground plane and a cube, and saves the .usda file.

    Args:
        output_filename (str): The desired name for the final USDZ file (used for naming the .usda file).
    """
    global global_usdz_path
    temp_dir = "temp_usdz_content"

    # 1. Setup the working directory
    # Create a temporary directory to hold the USD files and textures
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # Define the output path for the scene description file (.usda) within the temp directory
    # Use a fixed name 'scene.usda' for the primary USD file within the temp directory for usdzip
    usd_filepath = os.path.join(temp_dir, "scene.usda")
    # The final USDZ path will be in /content/
    global_usdz_path = os.path.join("/content", output_filename)


    # 2. Create the USD Stage in memory and then save it
    stage = Usd.Stage.CreateInMemory()
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(0)

    # Set the up axis (Y is common in AR/USD)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    # 3. Create the Ground Plane
    plane_prim = UsdGeom.Plane.Define(stage, Sdf.Path("/World/Ground"))
    plane_prim.GetExtentAttr().Set([(-100,-0.01,-100), (100,0,100)])
    plane_prim.GetPrim().CreateAttribute("primvars:displayColor", Sdf.ValueTypeNames.Color3fArray).Set([Gf.Vec3f(0.3, 0.5, 0.1)]) # Green color for 'grass'

    # 4. Create an Asset (a Cube, representing a Rock/Tree)
    # The 'rock' is placed at X=0, Y=0, Z=0 and is a basic cube.
    cube_prim = UsdGeom.Cube.Define(stage, Sdf.Path("/World/Rock1"))
    cube_prim.GetSizeAttr().Set(2.0)
    UsdGeom.Xformable(cube_prim).AddTranslateOp().Set(Gf.Vec3d(5.0, 1.0, 5.0)) # Move slightly up from ground
    cube_prim.GetPrim().CreateAttribute("primvars:displayColor", Sdf.ValueTypeNames.Color3fArray).Set([Gf.Vec3f(0.5, 0.5, 0.5)]) # Gray color

    # 5. Create a Second Asset Instance (representing another Tree)
    # Demonstrate instancing by moving the same cube model to a new location
    cube2_prim = UsdGeom.Cube.Define(stage, Sdf.Path("/World/Tree1"))
    cube2_prim.GetSizeAttr().Set(1.5)
    UsdGeom.Xformable(cube2_prim).AddTranslateOp().Set(Gf.Vec3d(-5.0, 0.75, -5.0)) # New position
    cube2_prim.GetPrim().CreateAttribute("primvars:displayColor", Sdf.ValueTypeNames.Color3fArray).Set([Gf.Vec3f(0.1, 0.3, 0.1)]) # Darker green color

    # Save the USD scene description to the temporary file
    stage.Export(usd_filepath)
    print(f"USD Scene saved to: {usd_filepath}")

    # 6. Package as USDZ using UsdUtils
    try:
        # Create the final USDZ file
        final_usdz_path = os.path.join(os.getcwd(), output_filename)
        UsdUtils.CreateNewUsdzPackage(usd_filepath, final_usdz_path)
        print(f"USDZ file created successfully: {final_usdz_path}")
        global_usdz_path = final_usdz_path
        return final_usdz_path
    except Exception as e:
        print(f"Error creating USDZ file: {e}")
        return None
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")


def main():
    """Main function to create and test the USDZ scene."""
    print("Creating USDZ scene...")
    result = create_usdz_scene("test_scene.usdz")
    if result:
        print(f"Success! USDZ file created at: {result}")
        print(f"File size: {os.path.getsize(result)} bytes")
    else:
        print("Failed to create USDZ file")

if __name__ == "__main__":
    main()