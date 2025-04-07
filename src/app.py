import sys
import os

@app.route('/test')
def test():
    return 'Application is running successfully!'

# Add this near the top of your routes
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'python_path': sys.path,
        'current_dir': os.getcwd(),
        'files_in_dir': os.listdir('.')
    } 