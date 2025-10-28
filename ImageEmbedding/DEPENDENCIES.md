# Dependencies Documentation

## Overview
This document provides comprehensive information about all dependencies used in the MediaPipe Image Embedder Web Application.

## Core Dependencies (Required)

### Web Framework
- **flask (>=3.1.2)**: Core web framework for the application
- **werkzeug (>=3.1.3)**: WSGI toolkit, dependency of Flask
- **jinja2 (>=3.1.6)**: Template engine used by Flask
- **markupsafe (>=3.0.3)**: String handling for templates
- **itsdangerous (>=2.2.0)**: Cryptographic signing for Flask sessions
- **click (>=8.3.0)**: Command line interface toolkit
- **blinker (>=1.9.0)**: Signal support for Flask

### AI/ML and Computer Vision
- **mediapipe (>=0.10.21)**: Google's MediaPipe framework for image embeddings
- **opencv-contrib-python (>=4.11.0)**: Computer vision library with additional modules
- **numpy (>=1.26.4)**: Numerical computing library
- **matplotlib (>=3.10.7)**: Plotting library (used by MediaPipe)

### Image Processing
- **pillow (>=12.0.0)**: Python Imaging Library for image manipulation

### Utilities
- **urllib3 (>=2.5.0)**: HTTP client library for downloading models

## Automatic Dependencies (Installed by MediaPipe/OpenCV)

### MediaPipe Dependencies
- **absl-py**: Google's Abseil Python library
- **attrs**: Classes without boilerplate
- **flatbuffers**: Serialization library
- **protobuf**: Protocol buffers for data serialization

### Machine Learning Dependencies  
- **jax**: Numerical computing library
- **jaxlib**: JAX linear algebra library
- **ml-dtypes**: Machine learning data types
- **opt-einsum**: Optimized Einstein summation
- **scipy**: Scientific computing library

### Visualization Dependencies
- **contourpy**: Contour plotting
- **cycler**: Composable style cycles
- **fonttools**: Font manipulation library
- **kiwisolver**: Constraint solver
- **packaging**: Core utilities for Python packages
- **pyparsing**: Parsing library
- **python-dateutil**: Date handling utilities
- **six**: Python 2/3 compatibility

### Audio Dependencies (MediaPipe)
- **sounddevice**: Audio I/O (used by MediaPipe but optional for our use case)
- **sentencepiece**: Text processing (MediaPipe dependency)

### System Dependencies
- **cffi**: C Foreign Function Interface
- **pycparser**: C parser in Python
- **colorama**: Cross-platform colored terminal output

## Development Dependencies (Optional)

### Code Quality
- **pytest (>=7.0.0)**: Testing framework
- **black (>=23.0.0)**: Code formatter
- **flake8 (>=7.0.0)**: Linting tool

## Dependency Management

### UV Lock File
The `uv.lock` file contains exact versions of all dependencies and their subdependencies, ensuring reproducible installations across different environments.

### Installation Commands

#### Full Installation (Recommended)
```bash
./run_uv.sh
```

#### Manual Installation
```bash
# Install Python 3.11
uv python install 3.11
uv python pin 3.11

# Install dependencies
uv sync --no-dev

# Verify installation
uv run python -c "import flask, mediapipe, cv2, numpy, matplotlib; print('All dependencies OK')"
```

#### Development Installation (with dev tools)
```bash
uv sync  # Includes dev dependencies
```

## Dependency Tree

```
mediapipe-image-embedder
├── flask (web framework)
│   ├── werkzeug (WSGI toolkit)
│   ├── jinja2 (templates)
│   │   └── markupsafe (string safety)
│   ├── itsdangerous (session signing)
│   ├── click (CLI toolkit)
│   └── blinker (signals)
├── mediapipe (AI/ML framework)
│   ├── opencv-contrib-python (computer vision)
│   ├── numpy (numerical computing)
│   ├── matplotlib (plotting)
│   │   ├── contourpy, cycler, fonttools
│   │   ├── kiwisolver, packaging, pyparsing
│   │   └── python-dateutil, six
│   ├── absl-py (Google's Abseil)
│   ├── attrs, flatbuffers, protobuf
│   ├── jax, jaxlib, ml-dtypes, opt-einsum
│   ├── scipy (scientific computing)
│   ├── sounddevice (audio I/O)
│   └── sentencepiece (text processing)
├── pillow (image manipulation)
├── urllib3 (HTTP client)
└── system utilities (cffi, pycparser, colorama)
```

## Platform-Specific Notes

### macOS (Apple Silicon)
- Uses Metal GPU acceleration for MediaPipe
- OpenCV includes optimized ARM64 binaries
- JAX/JAXLib compiled for Apple Silicon

### Linux
- May require additional system packages for OpenCV
- GPU acceleration available with CUDA support

### Windows
- WSL recommended for best compatibility
- Some packages may require Visual C++ build tools

## Size and Performance

### Total Package Size
Approximately **2.5GB** of dependencies when fully installed, including:
- MediaPipe models and libraries: ~1.8GB
- OpenCV with contrib modules: ~400MB  
- Scientific computing stack: ~200MB
- Web framework and utilities: ~100MB

### Installation Time
- With UV (fast): ~30-60 seconds
- With pip (traditional): ~3-5 minutes

## Troubleshooting

### Common Issues

1. **MediaPipe Import Error**
   ```bash
   # Verify MediaPipe installation
   uv run python -c "import mediapipe; print('MediaPipe OK')"
   ```

2. **OpenCV Missing**
   ```bash
   # Reinstall OpenCV
   uv remove opencv-contrib-python
   uv add opencv-contrib-python
   ```

3. **GPU Acceleration Issues**
   ```bash
   # Check GPU support
   uv run python -c "import mediapipe as mp; print(mp.__version__)"
   ```

### Clean Reinstallation
```bash
# Remove virtual environment
rm -rf .venv uv.lock

# Reinstall everything
./run_uv.sh
```

## Version Compatibility

| Component | Minimum Version | Recommended | Notes |
|-----------|----------------|-------------|--------|
| Python | 3.9 | 3.11 | Required for all dependencies |
| Flask | 3.0.0 | 3.1.2+ | Modern Flask features |
| MediaPipe | 0.10.0 | 0.10.21+ | Latest embedder models |
| OpenCV | 4.8.0 | 4.11.0+ | Better performance |
| NumPy | 1.24.0 | 1.26.4+ | MediaPipe compatibility |

## Security Considerations

- All dependencies are pinned to specific versions in `uv.lock`
- Regular security updates through UV package manager
- No known vulnerabilities in current dependency versions
- MediaPipe models downloaded from official Google sources

## License Information

- **Flask**: BSD-3-Clause
- **MediaPipe**: Apache License 2.0  
- **OpenCV**: Apache License 2.0
- **NumPy**: BSD License
- **Most other dependencies**: MIT or BSD licenses

All dependencies are compatible with the Apache 2.0 license of this project.