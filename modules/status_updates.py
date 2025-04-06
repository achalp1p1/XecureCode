import pandas as pd
from datetime import datetime

def update_tracker_based_on_dealer_type(qr_code, dealer_type, dealer_id=None, latitude=None, longitude=None):
    """Update QR tracker based on dealer type"""
    try:
        tracker_path = 'data/qr_validation_tracker.xlsx'
        tracker_df = pd.read_excel(tracker_path)
        
        # Determine QR code type based on character content
        qr_column = None
        if 'C' in qr_code:
            qr_column = 'Carton_QR_Code'
            print(f"QR code {qr_code} identified as Carton QR code")
        elif 'B' in qr_code:
            qr_column = 'Box_QR_Code'
            print(f"QR code {qr_code} identified as Box QR code")
        elif 'I' in qr_code:
            qr_column = 'Item_QR_Code'
            print(f"QR code {qr_code} identified as Item QR code")
        
        # Check if the column exists
        if qr_column not in tracker_df.columns:
            print(f"Column {qr_column} not found in tracker")
            return False
        
        # Find all rows with the matching QR code in the determined column
        qr_idx = tracker_df.index[tracker_df[qr_column] == qr_code]
        if len(qr_idx) == 0:
            print(f"QR code {qr_code} not found in column {qr_column} for update")
            return False
        
        print(f"Found {len(qr_idx)} rows to update for QR code {qr_code} in column {qr_column}")
        
        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format geo location
        geo_location = f"{latitude},{longitude}" if latitude and longitude else "Location not available"
        
        # Update based on dealer type for all matching rows
        if dealer_type == 'Factory':
            for idx in qr_idx:
                tracker_df.at[idx, 'Factory_Reached_Status'] = 'Factory_Reached'
                tracker_df.at[idx, 'Factory_Id'] = str(dealer_id) if dealer_id else ""
                tracker_df.at[idx, 'Factory_Time_Stamp'] = current_time
                tracker_df.at[idx, 'Factory_Geo_Location'] = geo_location
                print(f"Updated factory status for row {idx}")
        elif dealer_type == 'Dealer':
            for idx in qr_idx:
                tracker_df.at[idx, 'Dealer_Reached_Status'] = 'Dealer_Reached'
                tracker_df.at[idx, 'Dealer_Id'] = str(dealer_id) if dealer_id else ""
                tracker_df.at[idx, 'Dealer_Time_Stamp'] = current_time
                tracker_df.at[idx, 'Dealer_Geo_Location'] = geo_location
                print(f"Updated dealer status for row {idx}")
        elif dealer_type == 'Retailer':
            for idx in qr_idx:
                tracker_df.at[idx, 'Retailer_Reached_Status'] = 'Retailer_Reached'
                tracker_df.at[idx, 'Retailer_Id'] = str(dealer_id) if dealer_id else ""
                tracker_df.at[idx, 'Retailer_Time_Stamp'] = current_time
                tracker_df.at[idx, 'Retailer_Geo_Location'] = geo_location
                print(f"Updated retailer status for row {idx}")
        
        # Save updated tracker
        tracker_df.to_excel(tracker_path, index=False)
        return True
        
    except Exception as e:
        print(f"Error updating tracker for QR code {qr_code}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def update_retailer_status(qr_code, retailer_id=None, latitude=None, longitude=None):
    """Update Retailer status when QR code is validated without dealer ID"""
    try:
        tracker_path = 'data/qr_validation_tracker.xlsx'
        tracker_df = pd.read_excel(tracker_path)
        
        # Determine QR code type based on character content
        qr_column = None
        if 'C' in qr_code:
            qr_column = 'Carton_QR_Code'
            print(f"QR code {qr_code} identified as Carton QR code")
        elif 'B' in qr_code:
            qr_column = 'Box_QR_Code'
            print(f"QR code {qr_code} identified as Box QR code")
        elif 'I' in qr_code:
            qr_column = 'Item_QR_Code'
            print(f"QR code {qr_code} identified as Item QR code")
        
        # Check if the column exists
        if qr_column not in tracker_df.columns:
            print(f"Column {qr_column} not found in tracker")
            return False, None
        
        # Find all rows with the matching QR code in the determined column
        qr_idx = tracker_df.index[tracker_df[qr_column] == qr_code]
        if len(qr_idx) == 0:
            print(f"QR code {qr_code} not found in column {qr_column} for retailer update")
            return False, None
        
        print(f"Found {len(qr_idx)} rows to update for QR code {qr_code} in column {qr_column}")
        
        # Check if all rows have already been validated
        already_validated = True
        for idx in qr_idx:
            if tracker_df.at[idx, 'Retailer_Status'] != 'VALID_ONCE':
                already_validated = False
                break
                
        if already_validated and len(qr_idx) > 0:
            print(f"All rows for QR code {qr_code} have already been validated")
            return False, "duplicate"
        
        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format geo location
        geo_location = f"{latitude},{longitude}" if latitude and longitude else "Location not available"
        
        # Update retailer status for all matching rows
        for idx in qr_idx:
            # Only update if not already validated
            if tracker_df.at[idx, 'Retailer_Status'] != 'VALID_ONCE':
                tracker_df.at[idx, 'Retailer_Status'] = 'VALID_ONCE'
                tracker_df.at[idx, 'Retailer_Id'] = str(retailer_id) if retailer_id else ""
                tracker_df.at[idx, 'Retailer_Time_Stamp'] = current_time
                tracker_df.at[idx, 'Retailer_Geo_Location'] = geo_location
                print(f"Updated retailer status for row {idx}")
        
        # Save updated tracker
        tracker_df.to_excel(tracker_path, index=False)
        return True, None
        
    except Exception as e:
        print(f"Error updating retailer status for QR code {qr_code}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def update_consumer_status(qr_code, latitude=None, longitude=None):
    """Update Consumer status when QR code is validated by a consumer (guest user)"""
    try:
        tracker_path = 'data/qr_validation_tracker.xlsx'
        tracker_df = pd.read_excel(tracker_path)
        
        # Determine QR code type based on character content
        qr_column = None
        if 'C' in qr_code:
            qr_column = 'Carton_QR_Code'
            print(f"QR code {qr_code} identified as Carton QR code for consumer update")
        elif 'B' in qr_code:
            qr_column = 'Box_QR_Code'
            print(f"QR code {qr_code} identified as Box QR code for consumer update")
        elif 'I' in qr_code:
            qr_column = 'Item_QR_Code'
            print(f"QR code {qr_code} identified as Item QR code for consumer update")
        
        # Check if the column exists
        if qr_column not in tracker_df.columns:
            print(f"Column {qr_column} not found in tracker for consumer update")
            return False, None
        
        # Find all rows with the matching QR code in the determined column
        qr_idx = tracker_df.index[tracker_df[qr_column] == qr_code]
        if len(qr_idx) == 0:
            print(f"QR code {qr_code} not found in column {qr_column} for consumer update")
            return False, None
        
        print(f"Found {len(qr_idx)} rows to update for QR code {qr_code} in column {qr_column} for consumer")
        
        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format geo location
        geo_location = f"{latitude},{longitude}" if latitude and longitude else "Location not available"
        
        # Update consumer status for all matching rows
        for idx in qr_idx:
            tracker_df.at[idx, 'Consumer_Reached_Status'] = 'Factory_Reached'
            tracker_df.at[idx, 'Consumer_Time_Stamp'] = current_time
            tracker_df.at[idx, 'Consumer_Geo_Location'] = geo_location
            print(f"Updated consumer status for row {idx}")
        
        # Save updated tracker
        tracker_df.to_excel(tracker_path, index=False)
        return True, None
        
    except Exception as e:
        print(f"Error updating consumer status for QR code {qr_code}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, "error" 