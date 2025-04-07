import sys
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Test routes for diagnostics
@app.route('/test')
def test():
    return 'Application is running successfully!'

@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'python_path': sys.path,
        'current_dir': os.getcwd(),
        'files_in_dir': os.listdir('.')
    }

# Basic route
@app.route('/')
def index():
    return 'XecureCode QR Validation System' 