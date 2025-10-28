# MediaPipe Image Embedder - Setup Guide

## Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Test Installation
```bash
# Run test script to verify everything works
python test_setup.py
```

### Step 3: Start Application
```bash
# Option 1: Use the run script
./run.sh

# Option 2: Run directly
python app.py
```

Then open http://localhost:5000 in your browser.

## What You'll See

1. **Upload Page**: Drag and drop or click to upload two images
2. **Processing**: The app downloads the MediaPipe model (first time only)
3. **Results**: View similarity score and comparison visualization

## Troubleshooting

If you encounter issues:

1. **Python/pip not found**: Install Python 3.8+ from python.org
2. **MediaPipe installation fails**: Try `pip install --upgrade pip` first
3. **OpenCV issues on Linux**: `sudo apt-get install libgl1-mesa-glx libglib2.0-0`
4. **Permission errors**: `chmod +x run.sh` and ensure write access to uploads/

## Features Overview

- ✅ Web-based image similarity comparison
- ✅ Powered by Google MediaPipe
- ✅ Responsive design for mobile/desktop
- ✅ REST API for programmatic access
- ✅ Drag & drop file uploads
- ✅ Real-time similarity scoring
- ✅ Automatic model download

Enjoy comparing your images! 🖼️✨