# MediaPipe Image Embedder Web Application

A modern, responsive web application for comparing image similarity using Google's MediaPipe Tasks Python API. This application provides an intuitive interface to upload two images, get their similarity score, and visualize the underlying embedding vectors used in the analysis.

![MediaPipe Image Embedder](https://img.shields.io/badge/MediaPipe-Image%20Embedder-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![UV](https://img.shields.io/badge/UV-Package%20Manager-purple)
![License](https://img.shields.io/badge/License-Apache%202.0-yellow)

## 🌟 Features

- **🖼️ Drag & Drop Interface**: Intuitive drag-and-drop or click-to-upload functionality
- **📊 Real-time Similarity Analysis**: Instant similarity scoring using MediaPipe's MobileNet v3 Small model
- **📱 Responsive Design**: Beautiful, mobile-friendly interface built with Bootstrap 5
- **🎯 Visual Feedback**: Animated similarity circles and visual progress indicators
- **🔍 Image Preview**: Live preview of uploaded images with editing capabilities
- **📈 Detailed Results**: Comprehensive similarity analysis with technical details
- **🧠 Embedding Visualization**: Interactive charts showing image embeddings and vector analysis
- **📊 Vector Analytics**: Detailed embedding statistics, dimensions, and distance calculations
- **🚀 RESTful API**: Programmatic access via REST API endpoints
- **⚡ Performance Optimized**: Efficient image processing and caching

## 🏗️ Architecture

```
ImageEmbedding/
├── app.py                 # Main Flask application with embedding API
├── pyproject.toml         # UV project configuration
├── requirements.txt       # Python dependencies (legacy)
├── run_uv.sh             # UV-based launch script
├── test_imports.py       # MediaPipe installation test
├── README.md             # This comprehensive guide
├── .venv/                # UV-managed virtual environment
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles with embedding visualization
│   └── js/
│       └── main.js       # JavaScript with Chart.js integration
├── templates/            # HTML templates
│   ├── base.html         # Base template with Chart.js
│   ├── index.html        # Main upload page
│   └── result.html       # Results with embedding visualization
├── uploads/              # Uploaded images storage
└── models/               # MediaPipe models (auto-downloaded)
    └── embedder.tflite   # MobileNet v3 Small model
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher (Python 3.11 recommended)
- UV (Ultra-fast Python package installer) - [Install UV](https://github.com/astral-sh/uv)
- macOS, Linux, or Windows with WSL

### Installation (Recommended - Using UV)

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Navigate to the project directory**:
   ```bash
   cd ImageEmbedding
   ```

3. **Run the application** (UV handles everything automatically):
   ```bash
   ./run_uv.sh
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5001
   ```

### Alternative Installation (Traditional pip)

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

## 📖 Usage Guide

### Web Interface

1. **Upload Images**:
   - Click on the upload areas or drag and drop images
   - Supported formats: PNG, JPG, JPEG, GIF, BMP
   - Maximum file size: 16MB per image

2. **Compare Images**:
   - Once both images are uploaded, click "Compare Images"
   - The system will process the images using MediaPipe
   - View results with similarity score and interpretation

3. **Interpret Results**:
   - **0.9 - 1.0**: Very Similar Images
   - **0.7 - 0.9**: Similar Images
   - **0.5 - 0.7**: Somewhat Similar
   - **< 0.5**: Different Images

4. **Explore Embeddings** (NEW FEATURE):
   - Click "Image Embeddings Visualization" to expand
   - View interactive charts of embedding vectors
   - Examine vector statistics (dimensions, L2 norm, mean)
   - See raw embedding data and Euclidean distance

### API Usage

The application provides comprehensive REST APIs for programmatic access:

#### Similarity Analysis API
```python
import requests

# Prepare files
files = {
    'image1': ('image1.jpg', open('path/to/image1.jpg', 'rb')),
    'image2': ('image2.jpg', open('path/to/image2.jpg', 'rb'))
}

# Make request
response = requests.post('http://localhost:5001/api/similarity', files=files)
result = response.json()

print(f"Similarity: {result['similarity']}")
print(f"Interpretation: {result['interpretation']}")
```

#### Embeddings API (NEW)
```python
import requests

# Get embeddings for uploaded images
data = {
    'image1': 'uploaded_image1.jpg',
    'image2': 'uploaded_image2.jpg'
}

response = requests.post('http://localhost:5001/api/embeddings', json=data)
result = response.json()

print(f"Embedding dimensions: {result['dimensions']}")
print(f"First embedding shape: {len(result['embedding1'])}")
print(f"Second embedding shape: {len(result['embedding2'])}")
```

### JavaScript API

For client-side integration:

```javascript
const api = new ImageSimilarityAPI();

try {
    const result = await api.calculateSimilarity(file1, file2);
    console.log('Similarity:', result.similarity);
    console.log('Percentage:', result.similarity_percentage);
} catch (error) {
    console.error('Error:', error);
}
```

## 🔧 Configuration

### Environment Variables

You can customize the application using environment variables:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
export SECRET_KEY=your-secret-key-here
export MAX_FILE_SIZE=16777216  # 16MB in bytes
export FLASK_RUN_PORT=5001     # Default port
```

### UV Configuration

The application uses UV with the following configuration in `pyproject.toml`:

```toml
[project]
name = "mediapipe-image-embedder"
requires-python = ">=3.9"
dependencies = [
    "flask>=2.3.0",
    "mediapipe>=0.10.8",
    "opencv-python-headless>=4.8.0",
    # ... other dependencies
]
```

### Model Configuration

The application automatically downloads the MediaPipe model on first run. You can specify a different model by modifying the `ImageEmbedderService` class in `app.py`:

```python
def __init__(self, model_path='models/custom_embedder.tflite'):
    # Use custom model path
```

## 🧪 Technical Details

### MediaPipe Implementation

The application uses Google's MediaPipe Tasks with the following configuration:

- **Model**: MobileNet v3 Small (Float32)
- **L2 Normalization**: Enabled
- **Quantization**: Enabled
- **Similarity Metric**: Cosine Similarity

### Image Processing Pipeline

1. **Upload & Validation**: Images are validated for type and size
2. **MediaPipe Processing**: Images converted to MediaPipe Image format
3. **Embedding Extraction**: Feature embeddings generated using MobileNet v3
4. **Similarity Calculation**: Cosine similarity computed between embedding vectors
5. **Result Presentation**: Similarity score and interpretation returned

### Performance Considerations

- **UV Package Management**: Ultra-fast dependency resolution and installation
- **Model Caching**: MediaPipe model loaded once and reused across requests
- **GPU Acceleration**: Automatic Metal GPU acceleration on Apple Silicon
- **TensorFlow Lite**: XNNPACK delegate for optimized CPU inference
- **Image Resizing**: Automatic resizing for display optimization
- **Memory Management**: Temporary files cleaned up automatically
- **Embedding Caching**: Vectors cached for visualization requests
- **Error Handling**: Comprehensive error handling and user feedback

## 🛡️ Security Features

- **File Type Validation**: Only allows image file types
- **File Size Limits**: Prevents large file uploads
- **Secure Filenames**: Uses secure filename handling
- **Input Sanitization**: All user inputs are sanitized
- **CSRF Protection**: Built-in Flask security features

## 🚀 Deployment

### Development Server

For development, use the built-in Flask server:

```bash
python app.py
```

### Production Deployment

For production, use a WSGI server like Gunicorn:

1. **Using UV**:
   ```bash
   uv add gunicorn
   uv run gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

2. **Traditional approach**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

3. **Use with Nginx** (recommended):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static {
           alias /path/to/ImageEmbedding/static;
       }
   }
   ```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t mediapipe-embedder .
docker run -p 5000:5000 mediapipe-embedder
```

## 🔍 Troubleshooting

### Common Issues

1. **Model Download Fails**:
   ```bash
   # Manually download the model
   wget -O models/embedder.tflite https://storage.googleapis.com/mediapipe-models/image_embedder/mobilenet_v3_small/float32/1/mobilenet_v3_small.tflite
   ```

2. **OpenCV Installation Issues**:
   ```bash
   # Install system dependencies (Ubuntu/Debian)
   sudo apt-get install libgl1-mesa-glx libglib2.0-0
   
   # Or use headless version
   pip install opencv-python-headless
   ```

3. **Memory Issues with Large Images**:
   - Reduce MAX_FILE_SIZE in configuration
   - Implement image compression before processing

4. **Permission Issues**:
   ```bash
   # Ensure proper permissions for uploads directory
   chmod 755 uploads/
   ```

### Debug Mode

Enable debug mode for development:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📚 API Reference

### Endpoints

#### `GET /`
Main application page with upload interface.

#### `POST /upload`
Handle image upload and similarity calculation.

**Parameters**:
- `image1`: First image file (multipart/form-data)
- `image2`: Second image file (multipart/form-data)

**Response**: HTML page with results including embedding visualization

#### `POST /api/similarity`
API endpoint for similarity calculation.

**Parameters**:
- `image1`: First image file (multipart/form-data)
- `image2`: Second image file (multipart/form-data)

**Response**:
```json
{
    "similarity": 0.8745,
    "similarity_percentage": 87.45,
    "interpretation": "Similar images"
}
```

#### `POST /api/embeddings` (NEW)
API endpoint for retrieving image embeddings.

**Parameters**:
```json
{
    "image1": "filename1.jpg",
    "image2": "filename2.jpg"
}
```

**Response**:
```json
{
    "embedding1": [0.123, -0.456, 0.789, ...],
    "embedding2": [0.234, -0.567, 0.890, ...],
    "dimensions": 1024,
    "success": true
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google MediaPipe Team** for the excellent MediaPipe framework
- **Flask Community** for the robust web framework
- **Bootstrap Team** for the responsive CSS framework
- **FontAwesome** for the beautiful icons

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the troubleshooting section
- Review MediaPipe documentation: https://developers.google.com/mediapipe

## 🆕 Latest Features

### Version 2.0.0 - Embedding Visualization Update

- **🧠 Interactive Embedding Visualization**: View and analyze image embeddings with Chart.js
- **� Vector Statistics**: Comprehensive embedding metrics (dimensions, L2 norm, mean values)
- **🔍 Raw Data Access**: Complete embedding vectors with dimension indices
- **📈 Advanced Analytics**: Euclidean distance calculations and vector comparisons
- **⚡ UV Package Management**: Ultra-fast dependency management and installation
- **🚀 Enhanced APIs**: New `/api/embeddings` endpoint for programmatic access
- **🎨 Improved UI/UX**: Modern, responsive design with collapsible sections
- **🔧 Better Performance**: GPU acceleration and optimized model loading

### Previous Versions

- **v1.0.0** - Initial release with basic functionality
- **v1.1.0** - Added API endpoints and improved UI
- **v1.2.0** - Enhanced error handling and documentation

---

**Built with ❤️ using MediaPipe, Flask, and modern web technologies**