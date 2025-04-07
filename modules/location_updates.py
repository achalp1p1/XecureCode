import pandas as pd
from datetime import datetime
import os

def update_tracker_with_location(qr_data, dealer_id=None, dealer_type=None, location=None):
    """
    Update the QR validation tracker with location and status information based on dealer type.
    
    Args:
        qr_data (str): The QR code data to search for
        dealer_id (str, optional): The ID of the dealer making the validation
        dealer_type (str, optional): The type of dealer (Factory, Dealer, Retailer)
        location (str, optional): The current geo location
    """
    try:
        # Read the tracker file
        file_path = os.path.join('data', 'qr_validation_tracker.xlsx')
        if not os.path.exists(file_path):
            return False, "Tracker file not found"
            
        df = pd.read_excel(file_path)
        if df.empty:
            return False, "No records found in tracker"
            
        # Find matching rows
        matching_rows = df[df['QR_Code_Data'] == qr_data]
        if matching_rows.empty:
            return False, "No matching QR codes found"
            
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Update based on dealer type
        if dealer_type == "Factory":
            df.loc[df['QR_Code_Data'] == qr_data, 'Factory_Reached_Status'] = "Factory_Reached"
            df.loc[df['QR_Code_Data'] == qr_data, 'Factory_Id'] = dealer_id
            df.loc[df['QR_Code_Data'] == qr_data, 'Factory_Time_Stamp'] = current_time
            df.loc[df['QR_Code_Data'] == qr_data, 'Factory_Geo_Location'] = location
        elif dealer_type == "Dealer":
            df.loc[df['QR_Code_Data'] == qr_data, 'Dealer_Reached_Status'] = "Dealer_Reached"
            df.loc[df['QR_Code_Data'] == qr_data, 'Dealer_Id'] = dealer_id
            df.loc[df['QR_Code_Data'] == qr_data, 'Dealer_Time_Stamp'] = current_time
            df.loc[df['QR_Code_Data'] == qr_data, 'Dealer_Geo_Location'] = location
        elif dealer_type == "Retailer":
            df.loc[df['QR_Code_Data'] == qr_data, 'Retailer_Reached_Status'] = "Retailer_Reached"
            df.loc[df['QR_Code_Data'] == qr_data, 'Retailer_Id'] = dealer_id
            df.loc[df['QR_Code_Data'] == qr_data, 'Retailer_Time_Stamp'] = current_time
            df.loc[df['QR_Code_Data'] == qr_data, 'Retailer_Geo_Location'] = location
        else:  # Consumer
            df.loc[df['QR_Code_Data'] == qr_data, 'Consumer_Reached_Status'] = "Consumer_Reached"
            df.loc[df['QR_Code_Data'] == qr_data, 'Consumer_Time_Stamp'] = current_time
            df.loc[df['QR_Code_Data'] == qr_data, 'Consumer_Geo_Location'] = location
            
        # Save the updated tracker
        df.to_excel(file_path, index=False)
        return True, "Tracker updated successfully"
        
    except Exception as e:
        return False, f"Error updating tracker: {str(e)}" 