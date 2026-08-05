"""
Disease Spread Prediction Model Training Script
Trains a Random Forest model to predict disease spread risk across villages.

This script:
1. Loads village dataset with features
2. Trains Random Forest classifier
3. Evaluates and saves the model
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

def load_training_data(csv_path=None):
    """
    Load training data from CSV file.
    
    Expected columns:
    - temperature, humidity, rainfall, wind_speed
    - previous_outbreak_count, distance_from_infected_village
    - spread_risk_level (target variable)
    """
    if csv_path is None:
        # Get absolute path relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, '..', 'datasets', 'village_dataset.csv')
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Feature columns
    feature_columns = [
        'temperature',
        'humidity',
        'rainfall',
        'wind_speed',
        'previous_outbreak_count',
        'distance_from_infected_village'
    ]
    
    # Check if all required columns exist
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Extract features and target
    X = df[feature_columns].values
    y = df['spread_risk_level'].values
    
    return X, y, feature_columns

def train_spread_model(csv_path='../datasets/village_dataset.csv',
                      model_save_path='../backend/models/spread_prediction_model.pkl',
                      encoder_save_path='../backend/models/label_encoder.pkl'):
    """
    Train Random Forest model for spread prediction.
    
    Args:
        csv_path: Path to training dataset CSV
        model_save_path: Path to save trained model
        encoder_save_path: Path to save label encoder
    """
    print("=" * 60)
    print("Training Disease Spread Prediction Model")
    print("=" * 60)
    
    # Load data
    print(f"Loading data from: {csv_path}")
    X, y, feature_names = load_training_data(csv_path)
    
    # Encode target labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    print(f"Dataset shape: {X.shape}")
    print(f"Classes: {label_encoder.classes_}")
    print(f"Class distribution:")
    unique, counts = np.unique(y, return_counts=True)
    for cls, count in zip(unique, counts):
        print(f"  {cls}: {count}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Create and train model
    print("\nTraining Random Forest classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    print("\n" + "=" * 60)
    print("Model Evaluation")
    print("=" * 60)
    
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    print(f"Training Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_test_pred, 
                                target_names=label_encoder.classes_))
    
    print("\nFeature Importance:")
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.to_string(index=False))
    
    # Save model and encoder
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    
    with open(model_save_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved to: {model_save_path}")
    
    with open(encoder_save_path, 'wb') as f:
        pickle.dump(label_encoder, f)
    print(f"Label encoder saved to: {encoder_save_path}")
    
    return model, label_encoder

if __name__ == '__main__':
    import sys
    
    csv_path = sys.argv[1] if len(sys.argv) > 1 else '../datasets/village_dataset.csv'
    
    try:
        train_spread_model(csv_path)
        print("\n" + "=" * 60)
        print("Training completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
