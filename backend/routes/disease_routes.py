"""
Disease Detection Routes
Handles image upload and disease prediction endpoints.
"""

from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from services.disease_service import predict_disease_from_image
from services.database_service import save_disease_prediction

disease_bp = Blueprint('disease', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@disease_bp.route('/predict-disease', methods=['POST'])
def predict_disease():
    """
    Predict crop disease from uploaded leaf image.
    
    Expected: multipart/form-data with 'image' file
    Returns: JSON with disease name, confidence, and crop type
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    crop_type = request.form.get('crop_type', 'Unknown')
    village_id = request.form.get('village_id', None)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join('uploads', filename)
        file.save(upload_path)
        
        # Predict disease
        result = predict_disease_from_image(upload_path)
        
        # Save to database
        prediction_id = save_disease_prediction(
            image_filename=filename,
            predicted_disease=result['disease'],
            confidence_score=result['confidence'],
            crop_type=crop_type,
            village_id=village_id
        )
        
        result['prediction_id'] = prediction_id
        result['image_filename'] = filename
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@disease_bp.route('/recent-predictions', methods=['GET'])
def get_recent_predictions():
    """Get recent disease predictions."""
    from services.database_service import get_recent_predictions
    
    limit = request.args.get('limit', 10, type=int)
    predictions = get_recent_predictions(limit)
    
    return jsonify({
        'success': True,
        'predictions': predictions
    }), 200
