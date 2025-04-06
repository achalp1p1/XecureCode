# Hybrid QR Code Generator & Reader

This Flask web application generates and reads hybrid QR codes that contain both visible and UV-sensitive elements. The QR codes include:
- A visible QR code for normal scanning
- A hidden serial number that becomes visible under UV light
- A UV watermark for validation
- A UV-sensitive validation icon

## Features

- Generate hybrid QR codes with embedded UV elements
- Read both visible and UV-sensitive QR codes
- Modern, responsive web interface
- Real-time QR code preview
- Secure file handling

## Requirements

- Python 3.7+
- Flask
- OpenCV
- Pillow
- qrcode
- pyzbar

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. To generate a QR code:
   - Enter the data you want to encode
   - Click "Generate QR Code"
   - The QR code will be displayed and can be downloaded

4. To read a QR code:
   - Upload an image containing a QR code
   - Click "Read QR Code"
   - The decoded data will be displayed

## UV Elements

The generated QR codes include several UV-sensitive elements:
- A serial number in the top-left corner
- A validation icon in the top-right corner
- These elements are visible under UV light but remain hidden under normal lighting

## Security Notes

- The application generates unique serial numbers for each QR code
- UV elements help prevent counterfeiting
- The validation icon provides an additional layer of security

## Project Structure

The project is organized as follows:

- `app.py` - Main Flask application file
- `requirements.txt` - Python dependencies
- `data/` - Directory containing Excel files for product and tracking data
- `templates/` - HTML templates for the web interface
- `uploads/` - Directory for temporary file uploads
- `test_data_scripts/` - Scripts for generating and managing test data:
  - `create_sample_excel.py` - Creates initial sample product data
  - `create_detailed_excel.py` - Generates detailed product inventory
  - `generate_hierarchical_qr_codes.py` - Creates hierarchical QR codes for products
  - `qr_validation_tracker.py` - Manages QR code validation tracking
  - `update_product_database.py` - Updates product database entries
  - `create_dealer_master.py` - Creates dealer master data
  - `add_id_columns.py` - Adds ID columns to existing data
  - `remove_qr_code_column.py` - Removes QR code columns from data files

## License

This project is licensed under the MIT License - see the LICENSE file for details. 