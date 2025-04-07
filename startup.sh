#!/bin/bash
set -e

echo "Starting application setup..."

# Create necessary directories
mkdir -p /home/site/wwwroot/logs
mkdir -p /home/site/wwwroot/data
mkdir -p /home/site/wwwroot/uploads

# Set proper permissions
chmod 755 /home/site/wwwroot/logs
chmod 755 /home/site/wwwroot/data
chmod 755 /home/site/wwwroot/uploads

# Start Gunicorn
cd /home/site/wwwroot
gunicorn --bind=0.0.0.0:8000 \
         --timeout 600 \
         --workers 4 \
         --access-logfile /home/site/wwwroot/logs/access.log \
         --error-logfile /home/site/wwwroot/logs/error.log \
         --log-level info \
         application:app 