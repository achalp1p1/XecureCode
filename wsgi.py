from src.app import app

# This is the WSGI entry point
application = app

if __name__ == '__main__':
    app.run() 