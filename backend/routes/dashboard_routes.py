"""
Dashboard Routes
Handles dashboard statistics and map data endpoints.
"""

from flask import Blueprint, request, jsonify
from services.database_service import get_all_villages, get_dashboard_stats

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/risk-map', methods=['GET'])
def get_risk_map():
    """
    Get village data for risk map visualization.
    
    Returns: JSON with all villages and their risk levels
    """
    try:
        villages = get_all_villages()
        
        # Format for map visualization
        map_data = []
        for village in villages:
            map_data.append({
                'village_id': village['village_id'],
                'village_name': village['village_name'],
                'latitude': village['latitude'],
                'longitude': village['longitude'],
                'risk_level': village['risk_level'],
                'crop_type': village.get('crop_type', 'Unknown'),
                'last_detected_disease': village.get('last_detected_disease', 'None')
            })
        
        return jsonify({
            'success': True,
            'villages': map_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch risk map data: {str(e)}'
        }), 500

@dashboard_bp.route('/dashboard-stats', methods=['GET'])
def get_dashboard_stats_endpoint():
    """
    Get dashboard statistics.
    
    Returns: JSON with various statistics
    """
    try:
        stats = get_dashboard_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch dashboard stats: {str(e)}'
        }), 500

@dashboard_bp.route('/villages', methods=['GET'])
def get_villages():
    """Get all villages."""
    try:
        villages = get_all_villages()
        
        return jsonify({
            'success': True,
            'villages': villages
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch villages: {str(e)}'
        }), 500
