#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p logs
mkdir -p data
mkdir -p uploads

# Mount Azure File Share for persistent storage (will be configured in Azure)
# This will be handled by Azure App Service configuration

# Start Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 wsgi:app 