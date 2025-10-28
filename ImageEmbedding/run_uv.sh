#!/bin/bash

# MediaPipe Image Embedder - UV Setup and Run Script

echo "🚀 Starting MediaPipe Image Embedder with UV..."
echo "=============================================="

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.bashrc
fi

# Initialize UV project if not already done
if [ ! -f ".python-version" ]; then
    echo "🐍 Setting up Python environment with UV..."
    uv python install 3.11
    uv python pin 3.11
fi

# Install dependencies
echo "📦 Installing dependencies with UV..."
uv sync

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads models static/css static/js templates

# Run the application
echo "🌟 Starting the web application..."
echo "📱 Open your browser and go to: http://localhost:5001"
echo "🧠 NEW FEATURE: View image embeddings in the results page!"
echo "   Click 'Image Embeddings Visualization' to see:"
echo "   • Vector dimensions and statistics"
echo "   • Interactive embedding charts"
echo "   • Raw embedding values"
echo "   • Vector distance calculations"
echo "⏹️  Press Ctrl+C to stop the server"
echo "=============================================="

uv run python app.py