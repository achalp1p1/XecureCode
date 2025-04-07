#!/bin/bash
set -e

echo "Starting deployment script..."

# Set up environment variables
export PYTHONPATH=/home/site/wwwroot
export PORT="${PORT:-8000}"
export FLASK_APP=wsgi.py
export FLASK_ENV=production

echo "Creating necessary directories..."
# Create necessary directories
mkdir -p /home/site/wwwroot/logs
mkdir -p /home/site/wwwroot/data
mkdir -p /home/site/wwwroot/uploads

echo "Setting up permissions..."
# Set proper permissions
chmod 755 /home/site/wwwroot/logs
chmod 755 /home/site/wwwroot/data
chmod 755 /home/site/wwwroot/uploads

echo "Checking Python environment..."
# Check Python installation
which python
python --version

echo "Checking pip installation..."
# Check pip installation
which pip
pip --version

echo "Installing/Upgrading pip..."
# Ensure pip is up to date
python -m pip install --upgrade pip

echo "Installing dependencies..."
# Install dependencies
pip install --no-cache-dir -r requirements.txt

echo "Starting Gunicorn..."
# Start Gunicorn with proper settings
cd /home/site/wwwroot
exec gunicorn \
    --bind=0.0.0.0:${PORT} \
    --timeout 600 \
    --workers 4 \
    --access-logfile /home/site/wwwroot/logs/access.log \
    --error-logfile /home/site/wwwroot/logs/error.log \
    --log-level info \
    wsgi:app 