#!/bin/bash

# Setup script for 2D to 3D USDZ conversion environment
# This script helps set up the pyenv environment and install dependencies

echo "Setting up 2D to 3D USDZ conversion environment..."

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "Error: pyenv is not installed. Please install pyenv first:"
    echo "  brew install pyenv"
    exit 1
fi

# Check if the virtual environment exists
if ! pyenv versions | grep -q "2D_to_3D_usdz"; then
    echo "Creating pyenv virtual environment '2D_to_3D_usdz'..."
    pyenv install 3.12.0
    pyenv virtualenv 3.12.0 2D_to_3D_usdz
else
    echo "Virtual environment '2D_to_3D_usdz' already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
eval "$(pyenv init -)"
pyenv activate 2D_to_3D_usdz

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
echo "Verifying installation..."
python -c "from pxr import Usd, UsdGeom, Sdf, Gf, UsdUtils; print('✓ USD modules imported successfully')"

echo ""
echo "Setup complete! To use this environment:"
echo "1. Run: pyenv activate 2D_to_3D_usdz"
echo "2. Run: python create_usdz_scene.py"
echo "3. Run: python test_usdz_creation.py"
echo ""
echo "Or run the test script directly:"
echo "python test_usdz_creation.py"
