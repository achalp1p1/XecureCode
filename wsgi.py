import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Add the src directory to Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Import the Flask app
    from src.app import app
    
    # This is the WSGI entry point
    application = app
    
    logger.info("Successfully loaded the application")
except Exception as e:
    logger.error(f"Failed to load application: {str(e)}")
    raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000))) 