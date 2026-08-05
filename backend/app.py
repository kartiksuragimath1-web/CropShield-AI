"""
CropShield AI - Main Flask Application
Main entry point for the CropShield AI backend server.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime
import json

from routes.disease_routes import disease_bp
from routes.spread_routes import spread_bp
from routes.dashboard_routes import dashboard_bp
from services.database_service import init_db, get_db_connection

# Get absolute paths for templates and static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'static')

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'cropshield-ai-secret-key-2024'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('models', exist_ok=True)

# Register blueprints
app.register_blueprint(disease_bp, url_prefix='/api')
app.register_blueprint(spread_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')

# Initialize database
init_db()

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """Render the image upload page."""
    return render_template('upload.html')

@app.route('/predict-spread')
def predict_spread_page():
    """Render the disease spread prediction page."""
    return render_template('predict_spread.html')

@app.route('/map-dashboard')
def map_dashboard():
    """Render the interactive map dashboard."""
    return render_template('map_dashboard.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    """Render the admin analytics dashboard."""
    return render_template('admin_dashboard.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("CropShield AI - Starting Server...")
    print("=" * 60)
    print("Access the application at: http://localhost:5000")
    print("API endpoints available at: http://localhost:5000/api/")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
