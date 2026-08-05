"""
Disease Spread Prediction Routes
Handles village data and spread risk prediction endpoints.
"""

from flask import Blueprint, request, jsonify
from services.spread_service import predict_spread_risk
from services.database_service import save_spread_prediction

spread_bp = Blueprint('spread', __name__)

@spread_bp.route('/predict-spread', methods=['POST'])
def predict_spread():
    """
    Predict disease spread risk for a village.
    
    Expected JSON:
    {
        "village_id": "V001",
        "village_name": "Village Name",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "crop_type": "Tomato",
        "detected_disease": "Early Blight",
        "temperature": 25.5,
        "humidity": 70.0,
        "rainfall": 15.0,
        "wind_speed": 10.0,
        "previous_outbreak_count": 2,
        "distance_from_infected_village": 5.0
    }
    
    Returns: JSON with risk level and probability
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['village_id', 'village_name', 'crop_type', 'detected_disease']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Predict spread risk
        prediction = predict_spread_risk(data)
        
        # Save to database
        prediction_id = save_spread_prediction(
            village_id=data['village_id'],
            village_name=data['village_name'],
            crop_type=data['crop_type'],
            detected_disease=data['detected_disease'],
            risk_level=prediction['risk_level'],
            risk_probability=prediction['risk_probability'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        
        prediction['prediction_id'] = prediction_id
        
        return jsonify({
            'success': True,
            'prediction': prediction
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Spread prediction failed: {str(e)}'
        }), 500

@spread_bp.route('/batch-predict-spread', methods=['POST'])
def batch_predict_spread():
    """
    Predict spread risk for multiple villages at once.
    
    Expected JSON: Array of village data objects
    """
    try:
        villages_data = request.get_json()
        
        if not isinstance(villages_data, list):
            return jsonify({'error': 'Expected an array of village data'}), 400
        
        results = []
        for village_data in villages_data:
            prediction = predict_spread_risk(village_data)
            results.append({
                'village_id': village_data.get('village_id'),
                'village_name': village_data.get('village_name'),
                'prediction': prediction
            })
        
        return jsonify({
            'success': True,
            'predictions': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Batch prediction failed: {str(e)}'
        }), 500
