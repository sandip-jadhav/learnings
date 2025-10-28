// MediaPipe Image Embedder - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // File upload handling
    setupFileUpload();
    
    // Drag and drop functionality
    setupDragAndDrop();
    
    // Form validation
    setupFormValidation();
    
    // Animations
    setupAnimations();
});

/**
 * Setup file upload handling with preview
 */
function setupFileUpload() {
    const fileInputs = document.querySelectorAll('.file-input');
    
    fileInputs.forEach((input, index) => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                displayImagePreview(file, index + 1);
                checkFormCompletion();
            }
        });
    });
}

/**
 * Setup drag and drop functionality
 */
function setupDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach((area, index) => {
        const input = area.querySelector('.file-input');
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, () => area.classList.add('dragover'), false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, () => area.classList.remove('dragover'), false);
        });
        
        // Handle dropped files
        area.addEventListener('drop', function(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                const file = files[0];
                if (isValidFileType(file)) {
                    input.files = files;
                    displayImagePreview(file, index + 1);
                    checkFormCompletion();
                } else {
                    showAlert('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.', 'error');
                }
            }
        }, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
}

/**
 * Display image preview
 */
function displayImagePreview(file, imageNumber) {
    const uploadArea = document.getElementById(`uploadArea${imageNumber}`);
    const preview = document.getElementById(`preview${imageNumber}`);
    const uploadContent = uploadArea.querySelector('.upload-content');
    const previewImg = preview.querySelector('.preview-image');
    
    if (!isValidFileType(file)) {
        showAlert('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.', 'error');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) { // 16MB
        showAlert('File is too large. Maximum size is 16MB.', 'error');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        uploadContent.style.display = 'none';
        preview.style.display = 'block';
        
        // Add fade-in animation
        preview.classList.add('fade-in');
    };
    reader.readAsDataURL(file);
    
    // Setup remove button
    const removeBtn = preview.querySelector('.remove-image');
    removeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        removeImagePreview(imageNumber);
    });
}

/**
 * Remove image preview
 */
function removeImagePreview(imageNumber) {
    const uploadArea = document.getElementById(`uploadArea${imageNumber}`);
    const preview = document.getElementById(`preview${imageNumber}`);
    const uploadContent = uploadArea.querySelector('.upload-content');
    const input = document.getElementById(`image${imageNumber}`);
    
    // Clear file input
    input.value = '';
    
    // Show upload content, hide preview
    uploadContent.style.display = 'block';
    preview.style.display = 'none';
    preview.classList.remove('fade-in');
    
    checkFormCompletion();
}

/**
 * Check if file type is valid
 */
function isValidFileType(file) {
    const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/bmp'];
    return allowedTypes.includes(file.type);
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    const form = document.getElementById('uploadForm');
    const compareBtn = document.getElementById('compareBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    
    if (form && compareBtn) {
        form.addEventListener('submit', function(e) {
            const image1 = document.getElementById('image1');
            const image2 = document.getElementById('image2');
            
            if (!image1.files.length || !image2.files.length) {
                e.preventDefault();
                showAlert('Please select both images before comparing.', 'error');
                return;
            }
            
            // Show loading indicator
            compareBtn.disabled = true;
            compareBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            
            if (loadingIndicator) {
                loadingIndicator.style.display = 'block';
            }
        });
    }
}

/**
 * Check form completion and enable/disable submit button
 */
function checkFormCompletion() {
    const image1 = document.getElementById('image1');
    const image2 = document.getElementById('image2');
    const compareBtn = document.getElementById('compareBtn');
    
    if (image1 && image2 && compareBtn) {
        const hasImage1 = image1.files.length > 0;
        const hasImage2 = image2.files.length > 0;
        
        compareBtn.disabled = !(hasImage1 && hasImage2);
        
        if (hasImage1 && hasImage2) {
            compareBtn.classList.add('pulse-btn');
        } else {
            compareBtn.classList.remove('pulse-btn');
        }
    }
}

/**
 * Setup animations
 */
function setupAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.card, .upload-area').forEach(el => {
        observer.observe(el);
    });
    
    // Animate similarity circle if present
    animateSimilarityCircle();
}

/**
 * Animate similarity circle
 */
function animateSimilarityCircle() {
    const circle = document.querySelector('.similarity-circle');
    if (!circle) return;
    
    const score = parseFloat(circle.dataset.score) || 0;
    const normalizedScore = Math.max(0, (score + 1) / 2); // Convert -1 to 1 range to 0 to 1
    
    // Set CSS custom property for the score
    circle.style.setProperty('--score', normalizedScore);
    
    // Add appropriate class based on score
    if (score >= 0.9) {
        circle.classList.add('very-similar');
    } else if (score >= 0.7) {
        circle.classList.add('similar');
    } else if (score >= 0.5) {
        circle.classList.add('somewhat-similar');
    } else {
        circle.classList.add('different');
    }
    
    // Trigger animation
    setTimeout(() => {
        circle.classList.add('animate');
    }, 500);
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

/**
 * Utility function to format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * API for programmatic similarity calculation
 */
class ImageSimilarityAPI {
    constructor() {
        this.endpoint = '/api/similarity';
    }
    
    async calculateSimilarity(file1, file2) {
        const formData = new FormData();
        formData.append('image1', file1);
        formData.append('image2', file2);
        
        try {
            const response = await fetch(this.endpoint, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error calculating similarity:', error);
            throw error;
        }
    }
}

// Export API for external use
window.ImageSimilarityAPI = ImageSimilarityAPI;

// Add pulse animation class
const style = document.createElement('style');
style.textContent = `
    .pulse-btn {
        animation: pulseButton 1.5s infinite;
    }
    
    @keyframes pulseButton {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(0, 123, 255, 0.7);
        }
        70% {
            transform: scale(1.02);
            box-shadow: 0 0 0 10px rgba(0, 123, 255, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(0, 123, 255, 0);
        }
    }
`;
document.head.appendChild(style);