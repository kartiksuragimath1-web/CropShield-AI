"""
Database Service Module
Handles all database operations for CropShield AI.
Uses SQLite for simplicity and portability.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = 'cropshield.db'

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table for disease predictions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disease_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_filename TEXT NOT NULL,
            predicted_disease TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            crop_type TEXT,
            village_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for spread predictions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spread_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            village_id TEXT NOT NULL,
            village_name TEXT NOT NULL,
            crop_type TEXT NOT NULL,
            detected_disease TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            risk_probability REAL NOT NULL,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for village data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS villages (
            village_id TEXT PRIMARY KEY,
            village_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            crop_type TEXT,
            last_detected_disease TEXT,
            risk_level TEXT DEFAULT 'Low',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")

def save_disease_prediction(image_filename, predicted_disease, confidence_score, crop_type=None, village_id=None):
    """Save a disease prediction to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO disease_predictions 
        (image_filename, predicted_disease, confidence_score, crop_type, village_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (image_filename, predicted_disease, confidence_score, crop_type, village_id))
    
    conn.commit()
    prediction_id = cursor.lastrowid
    conn.close()
    return prediction_id

def save_spread_prediction(village_id, village_name, crop_type, detected_disease, 
                          risk_level, risk_probability, latitude=None, longitude=None):
    """Save a spread prediction to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update or insert village data
    cursor.execute('''
        INSERT OR REPLACE INTO villages 
        (village_id, village_name, latitude, longitude, crop_type, last_detected_disease, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (village_id, village_name, latitude, longitude, crop_type, detected_disease, risk_level))
    
    # Save spread prediction
    cursor.execute('''
        INSERT INTO spread_predictions 
        (village_id, village_name, crop_type, detected_disease, risk_level, risk_probability, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (village_id, village_name, crop_type, detected_disease, risk_level, risk_probability, latitude, longitude))
    
    conn.commit()
    prediction_id = cursor.lastrowid
    conn.close()
    return prediction_id

def get_recent_predictions(limit=10):
    """Get recent disease predictions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM disease_predictions 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    
    predictions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return predictions

def get_all_villages():
    """Get all villages with their risk levels."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM villages ORDER BY village_name')
    villages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return villages

def get_dashboard_stats():
    """Get statistics for the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total predictions
    cursor.execute('SELECT COUNT(*) as count FROM disease_predictions')
    total_predictions = cursor.fetchone()['count']
    
    # Total villages
    cursor.execute('SELECT COUNT(*) as count FROM villages')
    total_villages = cursor.fetchone()['count']
    
    # High risk villages
    cursor.execute("SELECT COUNT(*) as count FROM villages WHERE risk_level = 'High'")
    high_risk_villages = cursor.fetchone()['count']
    
    # Disease frequency
    cursor.execute('''
        SELECT detected_disease, COUNT(*) as count 
        FROM spread_predictions 
        GROUP BY detected_disease 
        ORDER BY count DESC 
        LIMIT 5
    ''')
    disease_frequency = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        'total_predictions': total_predictions,
        'total_villages': total_villages,
        'high_risk_villages': high_risk_villages,
        'disease_frequency': disease_frequency
    }
