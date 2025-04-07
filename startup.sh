#!/bin/bash

# Make script executable
chmod +x "$0"

# Create necessary directories if they don't exist
mkdir -p /home/site/wwwroot/logs
mkdir -p /home/site/wwwroot/data
mkdir -p /home/site/wwwroot/uploads

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export PORT="${PORT:-8000}"

# Activate virtual environment if it exists
if [ -d "/home/site/wwwroot/env" ]; then
    source /home/site/wwwroot/env/bin/activate
fi

# Start Gunicorn
cd /home/site/wwwroot
exec gunicorn --bind=0.0.0.0:${PORT} --timeout 600 --access-logfile /home/site/wwwroot/logs/access.log --error-logfile /home/site/wwwroot/logs/error.log wsgi:app 