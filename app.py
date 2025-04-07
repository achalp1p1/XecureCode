from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
import io
import pandas as pd
import os

# Import modular components
from modules.qr_operations import generate_qr, decode_qr
from modules.product_details import get_medicine_details
from modules.validation import validate_qr_code, validate_dealer_code
from modules.status_updates import update_tracker_based_on_dealer_type, update_retailer_status, update_consumer_status
from modules.counterfeit import log_counterfeit_attempt
from modules.hierarchy import get_hierarchy_info
from modules.reports import generate_reports

app = Flask(__name__)
app.secret_key = 'qrcodesystem2023'  # For session management

@app.route('/')
def index():
    # If user is already logged in, redirect to dashboard
    if 'dealer_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    dealer_id = request.form.get('dealerId')
    # No validation for password as per requirements
    
    if dealer_id:
        # Check if dealer ID exists in Dealer Master
        dealer_info = validate_dealer_code(dealer_id)
        if dealer_info:
            # Store dealer ID in session
            session['dealer_id'] = dealer_id
            session['dealer_type'] = dealer_info['type']
            session['dealer_name'] = dealer_info['name']
        else:
            # Store as unknown dealer
            session['dealer_id'] = dealer_id
            session['dealer_type'] = 'Unknown'
            session['dealer_name'] = 'Unknown Dealer'
    
    return redirect(url_for('validate'))

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Handle guest access
    if request.args.get('guest') == 'true':
        session.clear()  # Ensure no previous session data
        return render_template('dashboard.html')
    
    # Pass dealer info to template if logged in
    dealer_id = session.get('dealer_id')
    return render_template('dashboard.html', dealer_id=dealer_id)

@app.route('/generate')
def generate():
    return render_template('index.html', dealer_id=session.get('dealer_id'))

@app.route('/validate')
def validate():
    # Handle guest access
    if request.args.get('guest') == 'true':
        session.clear()  # Ensure no previous session data
    
    # Pass dealer info to template if logged in
    dealer_id = session.get('dealer_id')
    return render_template('validate.html', dealer_id=dealer_id)

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    data = request.form.get('data', '')
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Generate the QR code
    qr_image = generate_qr(data)
    
    # Save the image to a bytes buffer
    img_buffer = io.BytesIO()
    qr_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return send_file(
        img_buffer,
        mimetype='image/png',
        as_attachment=True,
        download_name='qr_code.png'
    )

@app.route('/read', methods=['POST'])
def read_qr():
    """Read and validate QR code"""
    if 'qrImage' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['qrImage']
    
    # Get dealer ID from form or session if available
    dealer_id = request.form.get('dealerId')
    if not dealer_id and 'dealer_id' in session:
        dealer_id = session.get('dealer_id')
        
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    try:
        # Read and decode QR code
        qr_code = decode_qr(file)
        if not qr_code:
            return jsonify({'success': False, 'error': 'Failed to read Xecure code'})
        
        # Validate QR code against tracker
        status = validate_qr_code(qr_code)
        
        # Get medicine details
        medicine_details = get_medicine_details(qr_code)
        
        # Get additional hierarchical information
        hierarchy_info = get_hierarchy_info(qr_code)
        
        # If dealer ID is provided, validate it and include dealer info
        if dealer_id:
            dealer_info = validate_dealer_code(dealer_id)
            if dealer_info:
                # Update tracker based on dealer type
                update_tracker_based_on_dealer_type(
                    qr_code, 
                    dealer_info['type'],
                    dealer_id,
                    latitude,
                    longitude
                )
                
                return jsonify({
                    'success': True,
                    'qr_code': qr_code,
                    'status': status,
                    'dealer_type': dealer_info['type'],
                    'dealer_name': dealer_info['name'],
                    'dealer_address': dealer_info['address'],
                    'location_updated': True,
                    'medicine_details': medicine_details,
                    'hierarchy_info': hierarchy_info
                })
        else:
            # No dealer ID provided, update as consumer validation
            update_success, error_type = update_consumer_status(qr_code, latitude, longitude)
            
            # Check if this is a duplicate QR code
            if error_type == "duplicate":
                # Log the counterfeit attempt
                log_counterfeit_attempt(qr_code, latitude, longitude)
                
                return jsonify({
                    'success': False, 
                    'error': 'Duplicate Xecure code: This Xecure code has already been validated',
                    'qr_code': qr_code,
                    'counterfeit_logged': True,
                    'medicine_details': medicine_details,
                    'hierarchy_info': hierarchy_info
                })
            
            return jsonify({
                'success': True,
                'qr_code': qr_code,
                'status': status,
                'location_updated': update_success,
                'update_type': 'consumer',
                'medicine_details': medicine_details,
                'hierarchy_info': hierarchy_info
            })
        
        # If dealer ID validation failed, return just QR code info
        return jsonify({
            'success': True,
            'qr_code': qr_code,
            'status': status,
            'medicine_details': medicine_details,
            'hierarchy_info': hierarchy_info
        })
        
    except Exception as e:
        print(f"Error processing Xecure code: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/reports')
def reports():
    if 'dealer_id' not in session:
        return redirect(url_for('login'))
    reports_data = generate_reports()
    return render_template('reports.html', reports=reports_data)

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    # Handle guest access
    if request.args.get('guest') == 'true':
        session.clear()  # Ensure no previous session data
        try:
            # Read the QR validation tracker Excel file
            file_path = os.path.join('data', 'qr_validation_tracker.xlsx')
            if not os.path.exists(file_path):
                flash('Tracker file not found. Please ensure qr_validation_tracker.xlsx exists in the data directory.', 'error')
                return redirect(url_for('dashboard'))
                
            df = pd.read_excel(file_path)
            if df.empty:
                flash('No validation records found in the tracker.', 'info')
                return render_template('tracker.html', records=[], columns=[])
                
            # Get column names
            columns = df.columns.tolist()
            
            # Convert DataFrame to list of dictionaries for template
            records = df.to_dict('records')
                
            return render_template('tracker.html', records=records, columns=columns)
        except Exception as e:
            print(f"Error in tracker route: {str(e)}")  # Add logging
            flash(f'Error loading tracker data: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
    
    # For logged-in users
    if 'dealer_id' not in session:
        return redirect(url_for('login'))
        
    try:
        # Read the QR validation tracker Excel file
        file_path = os.path.join('data', 'qr_validation_tracker.xlsx')
        if not os.path.exists(file_path):
            flash('Tracker file not found. Please ensure qr_validation_tracker.xlsx exists in the data directory.', 'error')
            return redirect(url_for('dashboard'))
            
        df = pd.read_excel(file_path)
        if df.empty:
            flash('No validation records found in the tracker.', 'info')
            return render_template('tracker.html', records=[], columns=[])
            
        # Get column names
        columns = df.columns.tolist()
        
        # Convert DataFrame to list of dictionaries for template
        records = df.to_dict('records')
            
        return render_template('tracker.html', records=records, columns=columns)
    except Exception as e:
        print(f"Error in tracker route: {str(e)}")  # Add logging
        flash(f'Error loading tracker data: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True) 