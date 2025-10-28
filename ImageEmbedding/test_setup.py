#!/usr/bin/env python3
"""
Test script for MediaPipe Image Embedder functionality
"""

import os
import sys
import tempfile
import urllib.request
from pathlib import Path

def test_mediapipe_installation():
    """Test if MediaPipe is installed and working"""
    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        print("✅ MediaPipe installation: OK")
        return True
    except ImportError as e:
        print(f"❌ MediaPipe installation: FAILED - {e}")
        return False

def test_opencv_installation():
    """Test if OpenCV is installed and working"""
    try:
        import cv2
        print("✅ OpenCV installation: OK")
        return True
    except ImportError as e:
        print(f"❌ OpenCV installation: FAILED - {e}")
        return False

def download_test_images():
    """Download test images for similarity comparison"""
    test_images = [
        ('burger.jpg', 'https://storage.googleapis.com/mediapipe-assets/burger.jpg'),
        ('burger_crop.jpg', 'https://storage.googleapis.com/mediapipe-assets/burger_crop.jpg')
    ]
    
    downloaded_files = []
    for filename, url in test_images:
        try:
            print(f"📥 Downloading {filename}...")
            urllib.request.urlretrieve(url, filename)
            downloaded_files.append(filename)
            print(f"✅ Downloaded {filename}")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            return None
    
    return downloaded_files

def download_model():
    """Download MediaPipe model"""
    model_url = "https://storage.googleapis.com/mediapipe-models/image_embedder/mobilenet_v3_small/float32/1/mobilenet_v3_small.tflite"
    model_path = "embedder.tflite"
    
    try:
        print("📥 Downloading MediaPipe model...")
        urllib.request.urlretrieve(model_url, model_path)
        print("✅ Model downloaded successfully")
        return model_path
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        return None

def test_similarity_calculation(model_path, image_files):
    """Test similarity calculation with MediaPipe"""
    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        
        # Create embedder options
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.ImageEmbedderOptions(
            base_options=base_options,
            l2_normalize=True,
            quantize=True
        )
        
        # Create embedder
        with vision.ImageEmbedder.create_from_options(options) as embedder:
            # Load images
            first_image = mp.Image.create_from_file(image_files[0])
            second_image = mp.Image.create_from_file(image_files[1])
            
            # Get embeddings
            first_embedding = embedder.embed(first_image)
            second_embedding = embedder.embed(second_image)
            
            # Calculate similarity
            similarity = vision.ImageEmbedder.cosine_similarity(
                first_embedding.embeddings[0],
                second_embedding.embeddings[0]
            )
            
            print(f"✅ Similarity calculation: OK")
            print(f"📊 Similarity score: {similarity:.4f}")
            
            # Interpret result
            if similarity >= 0.9:
                interpretation = "Very similar images"
            elif similarity >= 0.7:
                interpretation = "Similar images"
            elif similarity >= 0.5:
                interpretation = "Somewhat similar images"
            elif similarity >= 0.3:
                interpretation = "Slightly similar images"
            else:
                interpretation = "Very different images"
            
            print(f"📈 Interpretation: {interpretation}")
            return True
            
    except Exception as e:
        print(f"❌ Similarity calculation: FAILED - {e}")
        return False

def cleanup_test_files(files):
    """Clean up test files"""
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️  Cleaned up {file}")
        except Exception as e:
            print(f"⚠️  Could not clean up {file}: {e}")

def main():
    """Main test function"""
    print("🧪 MediaPipe Image Embedder - Functionality Test")
    print("=" * 50)
    
    # Test installations
    mp_ok = test_mediapipe_installation()
    cv_ok = test_opencv_installation()
    
    if not (mp_ok and cv_ok):
        print("\n❌ Please install missing dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Download test files
    print("\n📥 Downloading test files...")
    test_images = download_test_images()
    if not test_images:
        print("❌ Could not download test images")
        sys.exit(1)
    
    model_path = download_model()
    if not model_path:
        print("❌ Could not download model")
        cleanup_test_files(test_images)
        sys.exit(1)
    
    # Test similarity calculation
    print("\n🧮 Testing similarity calculation...")
    test_files = test_images + [model_path]
    
    if test_similarity_calculation(model_path, test_images):
        print("\n🎉 All tests passed! MediaPipe Image Embedder is working correctly.")
    else:
        print("\n❌ Tests failed. Please check your installation.")
        cleanup_test_files(test_files)
        sys.exit(1)
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    cleanup_test_files(test_files)
    
    print("\n✅ Test completed successfully!")
    print("🚀 You can now run the web application with: python app.py")

if __name__ == "__main__":
    main()