"""
Disease Detection Model Training Script
Trains a CNN model for crop disease classification using PlantVillage dataset structure.

This script:
1. Loads images from PlantVillage dataset structure
2. Preprocesses images
3. Trains a CNN model
4. Evaluates and saves the model
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import pickle

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 25  # Based on PlantVillage classes

# Disease classes
DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Corn___Cercospora_leaf_spot',
    'Corn___Common_rust',
    'Corn___Northern_Leaf_Blight',
    'Corn___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites_(Two-spotted_spider_mite)',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

def create_cnn_model(input_shape=(IMG_SIZE, IMG_SIZE, 3), num_classes=NUM_CLASSES):
    """
    Create a CNN model for disease classification.
    
    Architecture:
    - Convolutional layers with max pooling
    - Dropout for regularization
    - Dense layers for classification
    """
    model = keras.Sequential([
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(0.25),
        
        # Fourth convolutional block
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(0.25),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model_with_generator(data_dir, model_save_path='../backend/models/disease_detection_model.h5'):
    """
    Train model using ImageDataGenerator for data augmentation.
    
    Args:
        data_dir: Directory containing PlantVillage dataset
        model_save_path: Path to save trained model
    """
    # Create data generators with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        validation_split=0.2
    )
    
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    validation_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    # Create model
    model = create_cnn_model()
    
    # Callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            model_save_path,
            save_best_only=True,
            monitor='val_accuracy',
            mode='max'
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=0.00001
        )
    ]
    
    # Train model
    print("=" * 60)
    print("Training Disease Detection Model...")
    print("=" * 60)
    
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Load best model weights (saved by ModelCheckpoint)
    model.load_weights(model_save_path)
    
    # Evaluate model
    print("\n" + "=" * 60)
    print("Evaluating Model...")
    print("=" * 60)
    
    test_loss, test_accuracy = model.evaluate(validation_generator, verbose=0)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    return model, history

def train_with_synthetic_data(model_save_path='../backend/models/disease_detection_model.h5'):
    """
    Train model with synthetic data for demo purposes.
    Creates a simple model that can be used for testing.
    """
    print("=" * 60)
    print("Training with Synthetic Data (Demo Mode)")
    print("=" * 60)
    print("Note: For production, use actual PlantVillage dataset")
    print("=" * 60)
    
    # Create model
    model = create_cnn_model()
    
    # Generate synthetic training data
    print("Generating synthetic training data...")
    num_samples = 1000
    X_train = np.random.random((num_samples, IMG_SIZE, IMG_SIZE, 3))
    y_train = keras.utils.to_categorical(
        np.random.randint(0, NUM_CLASSES, num_samples),
        NUM_CLASSES
    )
    
    X_val = np.random.random((200, IMG_SIZE, IMG_SIZE, 3))
    y_val = keras.utils.to_categorical(
        np.random.randint(0, NUM_CLASSES, 200),
        NUM_CLASSES
    )
    
    # Train model
    history = model.fit(
        X_train, y_train,
        batch_size=BATCH_SIZE,
        epochs=5,
        validation_data=(X_val, y_val),
        verbose=1
    )
    
    # Save model
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    model.save(model_save_path)
    print(f"\nModel saved to: {model_save_path}")
    
    return model, history

if __name__ == '__main__':
    import sys
    
    # Check if PlantVillage dataset directory is provided
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
        if os.path.exists(data_dir):
            print(f"Using PlantVillage dataset from: {data_dir}")
            train_model_with_generator(data_dir)
        else:
            print(f"Dataset directory not found: {data_dir}")
            print("Training with synthetic data instead...")
            train_with_synthetic_data()
    else:
        print("No dataset directory provided.")
        print("Usage: python train_disease_model.py <path_to_plantvillage_dataset>")
        print("Training with synthetic data for demo...")
        train_with_synthetic_data()
