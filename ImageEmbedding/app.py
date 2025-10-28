#!/usr/bin/env python3
"""
MediaPipe Image Embedder Web Application
Based on Google's MediaPipe Tasks Python API for image similarity comparison
"""

import os
import sys
import math
import urllib.request
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

# Set matplotlib to use non-GUI backend before importing MediaPipe
import matplotlib
matplotlib.use('Agg')

# Import MediaPipe with error handling
try:
    import cv2
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    MEDIAPIPE_AVAILABLE = True
    print("MediaPipe and dependencies loaded successfully")
except ImportError as e:
    print(f"Warning: MediaPipe or OpenCV not available: {e}")
    MEDIAPIPE_AVAILABLE = False


app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ImageEmbedderService:
    """Service class for handling image embeddings using MediaPipe"""
    
    def __init__(self, model_path='models/embedder.tflite'):
        self.model_path = model_path
        self.embedder = None
        self._download_model_if_needed()
        self._initialize_embedder()
    
    def _download_model_if_needed(self):
        """Download the MediaPipe model if it doesn't exist"""
        model_dir = os.path.dirname(self.model_path)
        os.makedirs(model_dir, exist_ok=True)
        
        if not os.path.exists(self.model_path):
            print("Downloading MediaPipe image embedder model...")
            model_url = "https://storage.googleapis.com/mediapipe-models/image_embedder/mobilenet_v3_small/float32/1/mobilenet_v3_small.tflite"
            try:
                urllib.request.urlretrieve(model_url, self.model_path)
                print(f"Model downloaded successfully to {self.model_path}")
            except Exception as e:
                print(f"Error downloading model: {e}")
                raise
    
    def _initialize_embedder(self):
        """Initialize the MediaPipe Image Embedder"""
        try:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.ImageEmbedderOptions(
                base_options=base_options,
                l2_normalize=True,
                quantize=True
            )
            self.embedder = vision.ImageEmbedder.create_from_options(options)
            print("MediaPipe Image Embedder initialized successfully")
        except Exception as e:
            print(f"Error initializing embedder: {e}")
            raise
    
    def get_embedding(self, image_path):
        """Get embedding for a single image"""
        try:
            # Create MediaPipe Image from file
            mp_image = mp.Image.create_from_file(image_path)
            
            # Get embedding
            embedding_result = self.embedder.embed(mp_image)
            return embedding_result
        except Exception as e:
            print(f"Error getting embedding for {image_path}: {e}")
            raise
    
    def calculate_similarity(self, image_path1, image_path2):
        """Calculate cosine similarity between two images"""
        try:
            # Get embeddings for both images
            embedding1 = self.get_embedding(image_path1)
            embedding2 = self.get_embedding(image_path2)
            
            # Calculate cosine similarity
            similarity = vision.ImageEmbedder.cosine_similarity(
                embedding1.embeddings[0],
                embedding2.embeddings[0]
            )
            
            return float(similarity)
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            raise
    
    def resize_image_for_display(self, image_path, desired_height=480, desired_width=480):
        """Resize image for web display while maintaining aspect ratio"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            h, w = image.shape[:2]
            if h < w:
                new_width = desired_width
                new_height = math.floor(h / (w / desired_width))
            else:
                new_height = desired_height
                new_width = math.floor(w / (h / desired_height))
            
            resized_image = cv2.resize(image, (new_width, new_height))
            
            # Save resized image for web display
            display_path = image_path.replace('.', '_display.')
            cv2.imwrite(display_path, resized_image)
            
            return display_path, (new_width, new_height)
        except Exception as e:
            print(f"Error resizing image: {e}")
            return image_path, None


# Initialize the image embedder service
embedder_service = None
if MEDIAPIPE_AVAILABLE:
    try:
        embedder_service = ImageEmbedderService()
        print("MediaPipe Image Embedder initialized successfully")
    except Exception as e:
        print(f"Failed to initialize MediaPipe service: {e}")
        embedder_service = None
else:
    print("MediaPipe not available - running in demo mode")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page with image upload form"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle image upload and similarity calculation"""
    if embedder_service is None:
        flash('MediaPipe service is not available. Please check the server logs.', 'error')
        return redirect(url_for('index'))
    
    # Check if files were uploaded
    if 'image1' not in request.files or 'image2' not in request.files:
        flash('Please select both images', 'error')
        return redirect(url_for('index'))
    
    file1 = request.files['image1']
    file2 = request.files['image2']
    
    # Check if files are selected
    if file1.filename == '' or file2.filename == '':
        flash('Please select both images', 'error')
        return redirect(url_for('index'))
    
    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        try:
            # Secure the filenames
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            
            # Add timestamp to avoid conflicts
            import time
            timestamp = str(int(time.time()))
            filename1 = f"{timestamp}_1_{filename1}"
            filename2 = f"{timestamp}_2_{filename2}"
            
            # Save files
            filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            
            file1.save(filepath1)
            file2.save(filepath2)
            
            # Calculate similarity
            similarity = embedder_service.calculate_similarity(filepath1, filepath2)
            
            # Resize images for display
            display_path1, size1 = embedder_service.resize_image_for_display(filepath1)
            display_path2, size2 = embedder_service.resize_image_for_display(filepath2)
            
            # Prepare result data
            result = {
                'similarity': similarity,
                'similarity_percentage': round(similarity * 100, 2),
                'image1': {
                    'path': display_path1,
                    'filename': file1.filename,
                    'size': size1
                },
                'image2': {
                    'path': display_path2,
                    'filename': file2.filename,
                    'size': size2
                }
            }
            
            return render_template('result.html', result=result)
            
        except Exception as e:
            flash(f'Error processing images: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.', 'error')
        return redirect(url_for('index'))


@app.route('/api/similarity', methods=['POST'])
def api_similarity():
    """API endpoint for image similarity calculation"""
    if embedder_service is None:
        return jsonify({'error': 'MediaPipe service is not available'}), 500
    
    try:
        # Handle file uploads via API
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Both images are required'}), 400
        
        file1 = request.files['image1']
        file2 = request.files['image2']
        
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save temporary files
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp1, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp2:
            
            file1.save(tmp1.name)
            file2.save(tmp2.name)
            
            # Calculate similarity
            similarity = embedder_service.calculate_similarity(tmp1.name, tmp2.name)
            
            # Clean up temporary files
            os.unlink(tmp1.name)
            os.unlink(tmp2.name)
            
            return jsonify({
                'similarity': float(similarity),
                'similarity_percentage': round(similarity * 100, 2),
                'interpretation': get_similarity_interpretation(similarity)
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/embeddings', methods=['POST'])
def api_embeddings():
    """API endpoint for retrieving image embeddings"""
    if embedder_service is None:
        return jsonify({'error': 'MediaPipe service is not available'}), 500
    
    try:
        data = request.get_json()
        if not data or 'image1' not in data or 'image2' not in data:
            return jsonify({'error': 'Image filenames are required'}), 400
        
        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], data['image1'])
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], data['image2'])
        
        # Check if files exist
        if not (os.path.exists(image1_path) and os.path.exists(image2_path)):
            return jsonify({'error': 'Image files not found'}), 404
        
        # Get embeddings
        embedding1_result = embedder_service.get_embedding(image1_path)
        embedding2_result = embedder_service.get_embedding(image2_path)
        
        # Extract embedding vectors
        embedding1 = embedding1_result.embeddings[0].embedding
        embedding2 = embedding2_result.embeddings[0].embedding
        
        # Convert to Python lists for JSON serialization
        embedding1_list = [float(x) for x in embedding1]
        embedding2_list = [float(x) for x in embedding2]
        
        return jsonify({
            'embedding1': embedding1_list,
            'embedding2': embedding2_list,
            'dimensions': len(embedding1_list),
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_similarity_interpretation(similarity):
    """Get human-readable interpretation of similarity score"""
    if similarity >= 0.9:
        return "Very similar images"
    elif similarity >= 0.7:
        return "Similar images"
    elif similarity >= 0.5:
        return "Somewhat similar images"
    elif similarity >= 0.3:
        return "Slightly similar images" 
    else:
        return "Very different images"


@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("Starting MediaPipe Image Embedder Web Application...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Use port 5001 to avoid conflicts with AirPlay Receiver
    port = 5001
    print(f"Starting server on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)