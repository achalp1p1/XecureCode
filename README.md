# XecureCode - Hybrid QR Code Validator

A Flask web application that generates and validates hybrid QR codes with both visible and UV-sensitive elements for secure product tracking and authentication.

## Features

- Generate hybrid QR codes with embedded UV elements
- Read both visible and UV-sensitive QR codes
- Modern, responsive web interface
- Real-time QR code preview
- Secure file handling
- Product tracking and validation
- Multi-level dealer authentication
- Reporting and analytics

## Requirements

- Python 3.7+
- Flask
- OpenCV
- Pillow
- qrcode
- pyzbar
- pandas
- openpyxl

## Installation

1. Clone this repository:
```bash
git clone https://github.com/achalp1p1/XecureCode.git
cd XecureCode
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

3. To validate a QR code:
   - Upload an image containing a QR code
   - Click "Validate QR Code"
   - The validation status and product details will be displayed

## UV Elements

The QR codes include several UV-sensitive elements:
- A serial number in the top-left corner
- A validation icon in the top-right corner
- These elements are visible under UV light but remain hidden under normal lighting

## Security Features

- Multi-level dealer authentication (Factory, Dealer, Retailer)
- UV elements for counterfeit prevention
- Hierarchical QR code tracking
- Real-time validation status updates
- Counterfeit attempt logging

## Project Structure

The project is organized as follows:

- `src/` - Python source code
  - `app.py` - Main Flask application file
  - `modules/` - Modular components
    - `qr_operations.py` - QR code generation and reading
    - `product_details.py` - Product information handling
    - `validation.py` - QR code validation
    - `status_updates.py` - Status tracking updates
    - `counterfeit.py` - Counterfeit detection
    - `hierarchy.py` - Hierarchical tracking
    - `reports.py` - Report generation
- `requirements.txt` - Python dependencies
- `data/` - Excel files for product and tracking data
- `templates/` - HTML templates
- `uploads/` - Temporary file uploads
- `test_data_scripts/` - Data management scripts

## License

This project is licensed under the MIT License - see the LICENSE file for details.
