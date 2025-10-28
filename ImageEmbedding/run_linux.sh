#!/bin/bash

# MediaPipe Image Embedder - Linux Compatible Setup Script

echo "🚀 Starting MediaPipe Image Embedder with UV (Linux Compatible)..."
echo "================================================================="

# Check if UV is available  
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    source ~/.bashrc 2>/dev/null || true
fi

# Initialize UV project if not already done
if [ ! -f ".python-version" ]; then
    echo "🐍 Setting up Python environment with UV..."
    uv python install 3.11
    uv python pin 3.11
fi

# Install dependencies directly without building the project
echo "📦 Installing dependencies with UV (avoiding build issues)..."
uv add flask mediapipe opencv-python-headless numpy pillow urllib3 matplotlib --no-sync

# Sync to create the virtual environment properly
echo "🔄 Syncing environment..."
uv sync --no-dev --no-build-isolation

# Alternative: Install dependencies directly if sync fails
if [ $? -ne 0 ]; then
    echo "⚠️  Sync failed, trying direct installation..."
    uv pip install flask mediapipe opencv-python-headless numpy pillow urllib3 matplotlib
fi

# Verify key dependencies are installed
echo "🔍 Verifying critical dependencies..."
uv run python -c "
import sys
missing = []
try:
    import flask
    print('✅ Flask imported successfully')
except ImportError:
    missing.append('flask')
    
try:
    import mediapipe
    print('✅ MediaPipe imported successfully')
except ImportError:
    missing.append('mediapipe')
    
try:
    import cv2
    print('✅ OpenCV imported successfully')
except ImportError:
    missing.append('opencv-python-headless')
    
try:
    import numpy
    print('✅ NumPy imported successfully')
except ImportError:
    missing.append('numpy')

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-GUI backend for headless environments
    print('✅ Matplotlib imported successfully')
except ImportError:
    missing.append('matplotlib')

if missing:
    print(f'❌ Missing dependencies: {missing}')
    print('Try running: uv pip install ' + ' '.join(missing))
    sys.exit(1)
else:
    print('✅ All critical dependencies verified')
"

if [ $? -ne 0 ]; then
    echo "❌ Dependency verification failed. Trying alternative installation..."
    echo "📦 Installing with pip as fallback..."
    uv pip install flask mediapipe opencv-python-headless numpy pillow urllib3 matplotlib
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads models static/css static/js templates

# Check if running on EC2 or headless environment
if [ -n "$AWS_EXECUTION_ENV" ] || [ -z "$DISPLAY" ]; then
    echo "🖥️  Detected headless environment - configuring for server deployment..."
    export MPLBACKEND=Agg
fi

# Run the application
echo "🌟 Starting the web application..."
echo "📱 Application will be available at: http://localhost:5001"
echo "🌐 For EC2/remote access, use: http://YOUR_SERVER_IP:5001"
echo "🧠 NEW FEATURE: View image embeddings in the results page!"
echo "   Click 'Image Embeddings Visualization' to see:"
echo "   • Vector dimensions and statistics"
echo "   • Interactive embedding charts"
echo "   • Raw embedding values"
echo "   • Vector distance calculations"
echo "⏹️  Press Ctrl+C to stop the server"
echo "================================================================="

uv run python app.py