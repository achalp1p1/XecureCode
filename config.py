import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    DATA_FOLDER = 'data'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Use environment variables for sensitive data
    DATABASE_FILES = {
        'PRODUCT_DB': os.path.join('data', 'product_database_new.xlsx'),
        'INVENTORY_DB': os.path.join('data', 'product_inventory_details_new.xlsx'),
        'QR_TRACKER': os.path.join('data', 'qr_validation_tracker.xlsx'),
        'DEALER_MASTER': os.path.join('data', 'Dealer_Master.xlsx')
    }

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_FILES = {
        'PRODUCT_DB': os.path.join('data', 'product_database_new.xlsx'),
        'INVENTORY_DB': os.path.join('data', 'product_inventory_details_new.xlsx'),
        'QR_TRACKER': os.path.join('data', 'qr_validation_tracker.xlsx'),
        'DEALER_MASTER': os.path.join('data', 'Dealer_Master.xlsx')
    }

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 