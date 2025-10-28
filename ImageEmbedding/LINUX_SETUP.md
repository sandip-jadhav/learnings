# Linux Setup Guide for MediaPipe Image Embedder

## Quick Setup (Recommended)

### Option 1: UV Package Manager (Fastest)
```bash
# Make the script executable (if not already)
chmod +x run_linux.sh

# Run the application
./run_linux.sh
```

### Option 2: Traditional pip Installation
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## Troubleshooting Linux Issues

### Issue 1: Build Backend Error
**Error**: `Failed to build mediapipe-image-embedder`
**Solution**: Use the Linux-specific run script that avoids build issues:
```bash
./run_linux.sh
```

### Issue 2: UV Installation Issues
```bash
# Install UV manually
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### Issue 3: Python Version Issues
```bash
# Check Python version
python3 --version

# Install Python 3.11 on Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install Python 3.11 on Amazon Linux/RHEL/CentOS
sudo yum install python3.11 python3.11-devel
```

### Issue 4: System Dependencies Missing
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y \
    python3-dev \
    python3-pip \
    build-essential \
    cmake \
    pkg-config \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0

# Amazon Linux/RHEL/CentOS
sudo yum update -y
sudo yum groupinstall -y "Development Tools"
sudo yum install -y \
    python3-devel \
    cmake \
    pkg-config \
    mesa-libGL \
    glib2 \
    libSM \
    libXext \
    libXrender \
    libgomp \
    gstreamer1 \
    gstreamer1-plugins-base
```

### Issue 5: OpenCV Issues
```bash
# If opencv-contrib-python fails, try headless version
uv pip uninstall opencv-contrib-python
uv pip install opencv-python-headless
```

### Issue 6: MediaPipe GPU Issues
```bash
# For CPU-only MediaPipe (recommended for servers)
export MEDIAPIPE_DISABLE_GPU=1
```

### Issue 7: Matplotlib Backend Issues
```bash
# Set non-GUI backend for headless environments
export MPLBACKEND=Agg
```

## EC2/Cloud Server Setup

### Security Group Settings
- **Inbound Rules**: Allow TCP port 5001 from your IP
- **Type**: Custom TCP Rule
- **Port Range**: 5001
- **Source**: Your IP address or 0.0.0.0/0 (less secure)

### Running on EC2
```bash
# Clone the repository
git clone <your-repo-url>
cd ImageEmbedding

# Run the Linux setup script
./run_linux.sh

# Application will be available at:
# http://YOUR_EC2_PUBLIC_IP:5001
```

### Running as a Service (Optional)
```bash
# Create systemd service file
sudo tee /etc/systemd/system/mediapipe-embedder.service > /dev/null <<EOF
[Unit]
Description=MediaPipe Image Embedder
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/ImageEmbedding
Environment=PATH=/home/ec2-user/.local/bin:/usr/local/bin:/usr/bin:/bin
Environment=MPLBACKEND=Agg
ExecStart=/home/ec2-user/.local/bin/uv run python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable mediapipe-embedder
sudo systemctl start mediapipe-embedder

# Check status
sudo systemctl status mediapipe-embedder
```

## Performance Optimization for Linux

### Memory Optimization
```bash
# Increase swap if needed (for low-memory instances)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### CPU Optimization
```bash
# Set CPU affinity for better performance
taskset -c 0-3 uv run python app.py
```

## Testing Installation

### Quick Test
```bash
# Test imports
uv run python -c "
import flask
import mediapipe  
import cv2
import numpy
import matplotlib
print('✅ All dependencies working!')
"
```

### Full Application Test
```bash
# Run the application
./run_linux.sh

# In another terminal, test the API
curl -X GET http://localhost:5001/

# Should return the HTML page
```

## Common Linux Distributions

### Ubuntu 20.04/22.04 LTS
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev build-essential
./run_linux.sh
```

### Amazon Linux 2023
```bash
sudo yum update -y
sudo yum install python3.11 python3.11-devel gcc gcc-c++ make
./run_linux.sh
```

### CentOS/RHEL 8/9
```bash
sudo dnf update -y
sudo dnf install python3.11 python3.11-devel gcc gcc-c++ make
./run_linux.sh
```

### Alpine Linux (Docker)
```bash
apk add --no-cache python3 python3-dev py3-pip build-base cmake
./run_linux.sh
```

## Docker Support

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy application files
COPY . .

# Install dependencies
RUN uv pip install -r requirements.txt

# Expose port
EXPOSE 5001

# Set environment variables
ENV MPLBACKEND=Agg
ENV MEDIAPIPE_DISABLE_GPU=1

# Run application
CMD ["uv", "run", "python", "app.py"]
```

### Build and Run Docker
```bash
docker build -t mediapipe-embedder .
docker run -p 5001:5001 mediapipe-embedder
```

## Support

If you encounter issues not covered here:

1. Check the console output for specific error messages
2. Verify all system dependencies are installed
3. Try the traditional pip installation method
4. Check Python version compatibility (3.11+ required)
5. Ensure sufficient memory (4GB+ recommended for MediaPipe)