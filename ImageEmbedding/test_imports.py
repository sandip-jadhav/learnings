#!/usr/bin/env python3
"""
Simple test to check if MediaPipe works
"""

print("Testing MediaPipe installation...")

try:
    print("1. Testing basic MediaPipe import...")
    import mediapipe as mp
    print("✅ MediaPipe imported successfully")
    
    print("2. Testing MediaPipe tasks...")
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    print("✅ MediaPipe tasks imported successfully")
    
    print("3. Testing OpenCV...")
    import cv2
    print("✅ OpenCV imported successfully")
    
    print("\n🎉 All imports successful! MediaPipe is ready to use.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your installation.")