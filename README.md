# 2D to 3D USDZ Conversion

This project provides tools for creating 3D USDZ scenes from 2D garden data, specifically designed for AR/VR applications.

## Features

- Create USDZ scenes with ground planes and 3D objects
- Support for multiple object types (cubes, planes, etc.)
- Proper USDZ packaging for AR/VR compatibility
- Two implementation approaches:
  - **USD Core approach**: Full-featured with pxr library (requires macOS 15.0+)
  - **Alternative approach**: Works with standard Python libraries (compatible with older macOS)
- Comprehensive testing suite
- Example scenes for different use cases

## Environment Setup

### Prerequisites

- Python 3.12.0
- pyenv (for virtual environment management)
- macOS (for USD Core compatibility) - **Alternative approach works on any system**

### Quick Setup

```bash
# Run the setup script
./setup_environment.sh
```

### Manual Setup

```bash
# Install pyenv if not already installed
brew install pyenv

# Create virtual environment
pyenv install 3.12.0
pyenv virtualenv 3.12.0 2D_to_3D_usdz
pyenv activate 2D_to_3D_usdz

# Install dependencies
pip install -r requirements.txt
```

### VSCode Setup

1. Open Command Palette (`Cmd + Shift + P`)
2. Select "Python: Select Interpreter"
3. Choose the `2D_to_3D_usdz` environment

## Usage

### Basic Usage

#### Alternative Approach (Recommended - No Dependencies)

```python
from create_usdz_alternative import create_usdz_alternative

# Create a basic USDZ scene
result = create_usdz_alternative("my_scene.usdz")
print(f"USDZ file created: {result}")
```

#### USD Core Approach (macOS 15.0+)

```python
from create_usdz_scene import create_usdz_scene

# Create a basic USDZ scene
result = create_usdz_scene("my_scene.usdz")
print(f"USDZ file created: {result}")
```

### Command Line Usage

#### Alternative Approach (Recommended)

```bash
# Create a basic scene
python create_usdz_alternative.py

# Run tests
python test_alternative.py

# Create example scenes
python example_scenes.py
```

#### USD Core Approach (macOS 15.0+)

```bash
# Create a basic scene
python create_usdz_scene.py

# Run tests
python test_usdz_creation.py

# Create example scenes
python example_scenes.py
```

## File Structure

```
2D_to_3D_usdz/
├── create_usdz_scene.py        # USD Core USDZ creation module
├── create_usdz_alternative.py  # Alternative USDZ creation (no dependencies)
├── test_usdz_creation.py       # USD Core test suite
├── test_alternative.py         # Alternative test suite
├── example_scenes.py           # Example scene configurations
├── setup_environment.sh        # Environment setup script
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## Testing

### Alternative Approach (Recommended)

Run the comprehensive test suite:

```bash
python test_alternative.py
```

### USD Core Approach (macOS 15.0+)

```bash
python test_usdz_creation.py
```

The test suite includes:
- Environment validation
- USDZ file creation
- File format validation
- Cleanup verification

## Scene Configuration

The current implementation creates a scene with:
- A ground plane (100x100 units, green color)
- A rock object (cube, gray color, positioned at 5,1,5)
- A tree object (cube, dark green color, positioned at -5,0.75,-5)

## Dependencies

### Alternative Approach (Recommended)
- **No external dependencies required!**
- Uses only standard Python libraries: `os`, `shutil`, `tempfile`, `zipfile`

### USD Core Approach (macOS 15.0+)
- `usd-core`: USD Python bindings for 3D scene creation
- Standard Python libraries: `os`, `shutil`, `tempfile`

## Troubleshooting

### Common Issues

#### Alternative Approach
1. **Permission Error**: Ensure write permissions in the current directory
2. **ZIP Creation Failed**: Check that the zipfile module is available (standard library)

#### USD Core Approach
1. **Import Error**: Make sure the virtual environment is activated and usd-core is installed
2. **macOS Compatibility**: USD Core requires macOS 15.0+. Use the alternative approach for older versions
3. **Permission Error**: Ensure write permissions in the current directory

### Getting Help

#### Alternative Approach
- Check the test output for specific error messages
- Verify functionality with `python test_alternative.py`
- No dependencies to check!

#### USD Core Approach
- Check the test output for specific error messages
- Verify environment setup with `python test_usdz_creation.py`
- Ensure all dependencies are installed with `pip list`

## Web Visualization

### Using Google's Model Viewer

You can visualize your USDZ scenes in a web browser using Google's `<model-viewer>` component, which provides:

- **3D Model Viewing**: Interactive 3D models with mouse/touch controls
- **AR Support**: View models in augmented reality on mobile devices
- **Cross-platform**: Works on desktop and mobile browsers

### Quick Start with Web Viewer

1. **Start the web server**:
   ```bash
   python serve_viewer.py
   ```

2. **Or use the demo script**:
   ```bash
   python demo_viewer.py
   ```

3. **Open in browser**: The web viewer will open automatically at `http://localhost:8000/web_viewer.html`

### Web Viewer Features

- **Interactive 3D Models**: Rotate, zoom, and pan around your garden scenes
- **AR Button**: Tap to view models in augmented reality (ARCore/ARKit required)
- **Multiple Scenes**: View all your created USDZ files in one interface
- **Real-time Updates**: Refresh to see newly created scenes

### Manual Web Server

If you prefer to start the server manually:

```bash
# Simple HTTP server
python -m http.server 8000

# Then open: http://localhost:8000/web_viewer.html
```

### AR Requirements

- **Android**: ARCore-supported device with Chrome browser
- **iOS**: ARKit-supported device with Safari browser
- **Desktop**: 3D viewing only (no AR)

## Next Steps

- Add support for custom 2D garden data input
- Implement texture mapping
- Add animation support
- Create more complex 3D object types
- Integrate with your existing web applications
