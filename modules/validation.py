import pandas as pd

def validate_qr_code(qr_data):
    """Validate QR code against the tracker"""
    try:
        # Load the QR validation tracker
        tracker_df = pd.read_excel('data/qr_validation_tracker.xlsx')
        
        # Determine QR code type based on character content
        qr_column = None
        if 'C' in qr_data:
            qr_column = 'Carton_QR_Code'
            print(f"QR code {qr_data} identified as Carton QR code for validation")
        elif 'B' in qr_data:
            qr_column = 'Box_QR_Code'
            print(f"QR code {qr_data} identified as Box QR code for validation")
        elif 'I' in qr_data:
            qr_column = 'Item_QR_Code'
            print(f"QR code {qr_data} identified as Item QR code for validation")
        else:
            print(f"QR code {qr_data} does not contain identifier for any QR code type")
            return "QR code format not recognized. Must contain 'C', 'B', or 'I' to identify type."
        
        # Check if the column exists
        if qr_column not in tracker_df.columns:
            print(f"Column {qr_column} not found in tracker")
            return "QR code column not found in tracking system"
        
        # Check if QR code exists in tracker using only the determined column
        tracker_match = tracker_df[tracker_df[qr_column] == qr_data]
        if tracker_match.empty:
            print(f"QR code {qr_data} not found in {qr_column} for validation")
            return "QR code not found in tracking system"
        
        print(f"Found QR code {qr_data} in column {qr_column} for validation")
        
        # Get the current status from the first matching row
        row = tracker_match.iloc[0]
        
        # Check consumer status (end-user validation)
        if 'Consumer_Status' in row and pd.notna(row['Consumer_Status']):
            return "Product has been validated by consumer"
        elif 'Consumer_Reached_Status' in row and row['Consumer_Reached_Status'] == 'Factory_Reached':
            return "Product has been validated by consumer"
            
        # Check retailer status
        if 'Retailer_Status' in row and row['Retailer_Status'] == 'VALID_ONCE':
            return "Product has been validated at retail level"
        elif 'Retailer_Reached_Status' in row and row['Retailer_Reached_Status'] == 'Retailer_Reached':
            return "Product has reached retailer"
            
        # Check dealer status
        elif 'Dealer_Reached_Status' in row and row['Dealer_Reached_Status'] == 'Dealer_Reached':
            return "Product has reached dealer"
            
        # Check factory status
        elif 'Factory_Reached_Status' in row and row['Factory_Reached_Status'] == 'Factory_Reached':
            return "Product has been verified at factory"
            
        # Default status if no other status found
        else:
            return "Product is valid but not yet in distribution"
            
    except Exception as e:
        print(f"Error validating QR code: {str(e)}")
        import traceback
        traceback.print_exc()
        return "Error validating QR code"

def validate_dealer_code(dealer_code):
    """Validate if the dealer code exists in the Dealer Master file and return dealer info"""
    try:
        dealer_df = pd.read_excel('data/Dealer_Master.xlsx')
        dealer_match = dealer_df[dealer_df['Id'].astype(str) == dealer_code]
        
        if dealer_match.empty:
            return False
            
        dealer_info = dealer_match.iloc[0]
        return {
            'type': dealer_info['Type'],
            'name': dealer_info['Name'],
            'address': dealer_info['Address']
        }
    except Exception as e:
        print(f"Error validating dealer code: {e}")
        return False 