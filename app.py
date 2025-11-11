"""
Flask application for KU Cancer Prediction Model serving
"""
import os
import json
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import logging
from typing import Dict, Any, List
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
           template_folder='frontend/templates',
           static_folder='frontend/static')
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Import custom modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import DataLoader
from src.model import XGBoostModel
from src.utils import generate_synthetic_data

# Global model instance
model = None
data_loader = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_model():
    """Load trained model from disk"""
    global model
    model_path = 'models/xgboost_model.pkl'
    
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            logger.info("✓ Model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    else:
        logger.warning(f"Model not found at {model_path}. Using in-memory model.")
        # Create a new model if one doesn't exist
        create_demo_model()
        return True

def create_demo_model():
    """Create and train a demo model"""
    global model, data_loader
    logger.info("Creating demo model...")
    
    try:
        # Generate synthetic data
        df = generate_synthetic_data(n_samples=300, n_features=10, task='classification')
        
        # Prepare data
        data_loader = DataLoader(random_state=42)
        X_train, X_test, y_train, y_test = data_loader.prepare_data(
            df, target_column='target', test_size=0.2
        )
        
        # Train model
        model = XGBoostModel(model_type='classification', n_estimators=100)
        model.train(X_train, y_train)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/xgboost_model.pkl')
        
        logger.info("✓ Demo model created and trained")
        return True
    except Exception as e:
        logger.error(f"Error creating demo model: {str(e)}")
        return False

def validate_prediction_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate prediction input data"""
    if not data:
        return False, "No data provided"
    
    if 'features' not in data:
        return False, "Missing 'features' field"
    
    features = data.get('features')
    if not isinstance(features, (list, dict)):
        return False, "Features must be a list or dictionary"
    
    if isinstance(features, list) and len(features) != 10:
        return False, f"Expected 10 features, got {len(features)}"
    
    return True, "Valid"

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'version': '1.0.0'
    }), 200

@app.route('/api/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        info = {
            'type': model.model_type,
            'is_trained': model.is_trained,
            'parameters': model.get_params(),
            'feature_count': 10,
            'feature_names': [f'feature_{i}' for i in range(10)]
        }
        
        if model.is_trained:
            importance = model.get_feature_importance()
            info['feature_importance'] = importance
        
        return jsonify(info), 200
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make prediction on input data"""
    if model is None or not model.is_trained:
        return jsonify({'error': 'Model not ready'}), 500
    
    try:
        data = request.get_json()
        
        # Validate input
        valid, message = validate_prediction_data(data)
        if not valid:
            return jsonify({'error': message}), 400
        
        # Prepare data
        features = data.get('features')
        if isinstance(features, list):
            X = pd.DataFrame([features], columns=[f'feature_{i}' for i in range(len(features))])
        else:
            X = pd.DataFrame([features])
        
        # Scale features if needed
        if data_loader and hasattr(data_loader, 'scaler'):
            X_scaled = data_loader.scaler.transform(X)
            X = pd.DataFrame(X_scaled, columns=X.columns)
        
        # Make prediction
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0].tolist()
        
        result = {
            'prediction': int(prediction),
            'probabilities': {
                'class_0': float(probabilities[0]),
                'class_1': float(probabilities[1])
            },
            'confidence': float(max(probabilities))
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Make batch predictions"""
    if model is None or not model.is_trained:
        return jsonify({'error': 'Model not ready'}), 500
    
    try:
        data = request.get_json()
        
        if 'records' not in data or not isinstance(data['records'], list):
            return jsonify({'error': 'Expected "records" as a list'}), 400
        
        records = data['records']
        predictions = []
        
        for record in records:
            X = pd.DataFrame([record], columns=[f'feature_{i}' for i in range(len(record))])
            
            if data_loader and hasattr(data_loader, 'scaler'):
                X_scaled = data_loader.scaler.transform(X)
                X = pd.DataFrame(X_scaled, columns=X.columns)
            
            pred = model.predict(X)[0]
            proba = model.predict_proba(X)[0]
            
            predictions.append({
                'prediction': int(pred),
                'probability': float(max(proba)),
                'probabilities': {'class_0': float(proba[0]), 'class_1': float(proba[1])}
            })
        
        return jsonify({'predictions': predictions}), 200
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-sample', methods=['GET'])
def generate_sample():
    """Generate sample data for demonstration"""
    try:
        # Generate random sample
        sample = np.random.randn(10).tolist()
        return jsonify({'features': sample}), 200
    except Exception as e:
        logger.error(f"Sample generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    """Get feature importance"""
    if model is None or not model.is_trained:
        return jsonify({'error': 'Model not trained'}), 500
    
    try:
        importance = model.get_feature_importance()
        
        # Sort by importance
        sorted_importance = dict(sorted(
            importance.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        return jsonify({
            'importance': sorted_importance,
            'top_10': dict(list(sorted_importance.items())[:10])
        }), 200
    
    except Exception as e:
        logger.error(f"Feature importance error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get model metrics"""
    if model is None or not model.is_trained:
        return jsonify({'error': 'Model not trained'}), 500
    
    try:
        metrics = model.metrics if model.metrics else {
            'accuracy': 0.0,
            'precision': 0.0,
            'recall': 0.0,
            'f1': 0.0
        }
        
        return jsonify(metrics), 200
    
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# STATIC FILES
# ============================================================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('frontend/static', filename)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({'error': 'Bad request'}), 400

# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

def init_app():
    """Initialize the application"""
    logger.info("Initializing KU Cancer Prediction Flask App...")
    
    # Load or create model
    if not load_model():
        logger.warning("Could not load model, creating demo model...")
        create_demo_model()
    
    logger.info("✓ Application initialized successfully")
    logger.info(f"Model status: {'Loaded' if model else 'Not loaded'}")

if __name__ == '__main__':
    init_app()
    
    # Development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
