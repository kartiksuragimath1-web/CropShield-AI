"""
Disease Spread Prediction Service
Handles ML-based prediction of disease spread risk across villages.
"""

import pickle
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = 'models/spread_prediction_model.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'

# Feature names for the model
FEATURE_NAMES = [
    'temperature',
    'humidity',
    'rainfall',
    'wind_speed',
    'previous_outbreak_count',
    'distance_from_infected_village'
]

def load_spread_model():
    """
    Load the trained spread prediction model.
    If model doesn't exist, return None (will use fallback prediction).
    """
    if os.path.exists(MODEL_PATH) and os.path.exists(LABEL_ENCODER_PATH):
        try:
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            with open(LABEL_ENCODER_PATH, 'rb') as f:
                label_encoder = pickle.load(f)
            return model, label_encoder
        except Exception as e:
            print(f"Warning: Could not load spread model: {e}")
            return None, None
    return None, None

def extract_features(village_data):
    """
    Extract features from village data for model prediction.
    
    Args:
        village_data: Dictionary containing village information
    
    Returns:
        Feature array for model prediction
    """
    features = []
    
    # Extract numeric features
    for feature_name in FEATURE_NAMES:
        value = village_data.get(feature_name, 0)
        # Handle missing values
        if value is None:
            value = 0
        features.append(float(value))
    
    return np.array(features).reshape(1, -1)

def predict_spread_risk(village_data):
    """
    Predict disease spread risk for a village.
    
    Args:
        village_data: Dictionary containing:
            - temperature: float
            - humidity: float
            - rainfall: float
            - wind_speed: float
            - previous_outbreak_count: int
            - distance_from_infected_village: float
            - crop_type: string
            - detected_disease: string
    
    Returns:
        Dictionary with risk_level and risk_probability
    """
    try:
        # Load model
        model, label_encoder = load_spread_model()
        
        if model is not None and label_encoder is not None:
            # Extract features
            features = extract_features(village_data)
            
            # Predict risk level
            risk_level_encoded = model.predict(features)[0]
            risk_level = label_encoder.inverse_transform([risk_level_encoded])[0]
            
            # Get probability
            probabilities = model.predict_proba(features)[0]
            risk_probability = float(max(probabilities))
            
        else:
            # Fallback: Use rule-based prediction
            risk_level, risk_probability = fallback_spread_prediction(village_data)
        
        return {
            'risk_level': risk_level,
            'risk_probability': round(risk_probability * 100, 2)
        }
        
    except Exception as e:
        # Fallback on error
        risk_level, risk_probability = fallback_spread_prediction(village_data)
        return {
            'risk_level': risk_level,
            'risk_probability': round(risk_probability * 100, 2)
        }

def fallback_spread_prediction(village_data):
    """
    Fallback prediction method using rule-based logic.
    Used when ML model is not available.
    """
    temperature = village_data.get('temperature', 25)
    humidity = village_data.get('humidity', 60)
    rainfall = village_data.get('rainfall', 10)
    wind_speed = village_data.get('wind_speed', 5)
    previous_outbreak = village_data.get('previous_outbreak_count', 0)
    distance = village_data.get('distance_from_infected_village', 10)
    
    # Calculate risk score
    risk_score = 0
    
    # Temperature factor (optimal: 20-30°C increases risk)
    if 20 <= temperature <= 30:
        risk_score += 2
    elif 15 <= temperature <= 35:
        risk_score += 1
    
    # Humidity factor (high humidity increases risk)
    if humidity > 70:
        risk_score += 2
    elif humidity > 60:
        risk_score += 1
    
    # Rainfall factor
    if rainfall > 20:
        risk_score += 2
    elif rainfall > 10:
        risk_score += 1
    
    # Wind speed factor (moderate wind spreads disease)
    if 5 <= wind_speed <= 15:
        risk_score += 2
    
    # Previous outbreak factor
    risk_score += min(previous_outbreak, 3)
    
    # Distance factor (closer = higher risk)
    if distance < 5:
        risk_score += 3
    elif distance < 10:
        risk_score += 2
    elif distance < 20:
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 8:
        risk_level = 'High'
        probability = 0.85
    elif risk_score >= 5:
        risk_level = 'Medium'
        probability = 0.60
    else:
        risk_level = 'Low'
        probability = 0.30
    
    return risk_level, probability
