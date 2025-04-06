import pandas as pd
from datetime import datetime
import os

def log_counterfeit_attempt(qr_code, latitude=None, longitude=None):
    """Log counterfeit QR code attempts to a separate Excel file"""
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Format geo location
        geo_location = f"{latitude},{longitude}" if latitude and longitude else "Location not available"
        
        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine QR code type based on character content
        qr_type = "Standard"
        if 'C' in qr_code:
            qr_type = "Carton"
        elif 'B' in qr_code:
            qr_type = "Box"
        elif 'I' in qr_code:
            qr_type = "Item"
            
        # Prepare the data for the new entry
        new_entry = {
            'QR_Code': [qr_code],
            'QR_Type': [qr_type],
            'Retailer_Geo_Location': [geo_location],
            'Retailer_Time_Stamp': [current_time],
            'Detection_Time': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        
        # Create DataFrame from the new entry
        new_df = pd.DataFrame(new_entry)
        
        # Path to the counterfeit log file
        counterfeit_path = 'data/Counterfeit_Retailer_Details.xlsx'
        
        # Check if the file already exists
        if os.path.exists(counterfeit_path):
            # Load existing data
            existing_df = pd.read_excel(counterfeit_path)
            # Append the new entry
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            # Create new file with the entry
            updated_df = new_df
        
        # Save to Excel file
        updated_df.to_excel(counterfeit_path, index=False)
        print(f"Logged counterfeit attempt for {qr_type} QR code: {qr_code}")
        return True
        
    except Exception as e:
        print(f"Error logging counterfeit attempt: {str(e)}")
        import traceback
        traceback.print_exc()
        return False 