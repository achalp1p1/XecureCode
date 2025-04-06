import pandas as pd

def get_medicine_details(qr_code):
    """Get medicine details from product database using source_info from QR tracker"""
    try:
        # First load the QR validation tracker
        tracker_df = pd.read_excel('data/qr_validation_tracker.xlsx')
        
        # Print available columns for debugging
        print(f"Available columns in tracker: {tracker_df.columns.tolist()}")
        
        # Determine QR code type based on character content
        priority_search = None
        
        if 'C' in qr_code:
            priority_search = 'Carton_QR_Code'
            print(f"QR code {qr_code} identified as Carton QR code for medicine search")
        elif 'B' in qr_code:
            priority_search = 'Box_QR_Code'
            print(f"QR code {qr_code} identified as Box QR code for medicine search")
        elif 'I' in qr_code:
            priority_search = 'Item_QR_Code'
            print(f"QR code {qr_code} identified as Item QR code for medicine search")
        
        # Find the QR code in tracker
        tracker_match = None
        
        # Try to find the QR code in the appropriate column
        if priority_search and priority_search in tracker_df.columns:
            tracker_match = tracker_df[tracker_df[priority_search] == qr_code]
            if not tracker_match.empty:
                print(f"Found medicine match for {priority_search}: {qr_code}")
        
        # If not found, check all other QR code columns
        if tracker_match is None or tracker_match.empty:
            qr_columns = ['Item_QR_Code', 'Box_QR_Code', 'Carton_QR_Code']
            for col in qr_columns:
                if col in tracker_df.columns and col != priority_search:
                    temp_match = tracker_df[tracker_df[col] == qr_code]
                    if not temp_match.empty:
                        tracker_match = temp_match
                        print(f"Found QR code {qr_code} in column {col}")
                        break
            
        if tracker_match is None or tracker_match.empty:
            print(f"QR code {qr_code} not found in any QR code column")
            return None
        
        # Check for source_info column (case insensitive)
        source_info_column = None
        for column in tracker_df.columns:
            if column.lower() == 'source_info' or column.lower() == 'sourceinfo':
                source_info_column = column
                break
                
        if not source_info_column:
            print("No source_info column found in tracker file")
            return None
            
        # Get the source_info for this QR code
        source_info = tracker_match.iloc[0][source_info_column]
        if pd.isna(source_info):
            print(f"No source_info found for QR code {qr_code}")
            return None
            
        print(f"Found source_info: {source_info} for QR code: {qr_code}")
            
        # Load the product database
        product_df = pd.read_excel('data/product_database_new.xlsx')
        
        # Print available columns in product database for debugging
        print(f"Available columns in product database: {product_df.columns.tolist()}")
        
        # Check for SourceInfo column in product database (case insensitive)
        source_info_product_column = None
        for column in product_df.columns:
            if column.lower() == 'sourceinfo' or column.lower() == 'source_info':
                source_info_product_column = column
                break
                
        if not source_info_product_column:
            print("No SourceInfo or source_info column found in product database")
            return None
            
        # Find the medicine details using source_info
        product_match = product_df[product_df[source_info_product_column] == source_info]
        
        if product_match.empty:
            print(f"No product found with {source_info_product_column}: {source_info}")
            return None
            
        # Return the product details as a dictionary
        product = product_match.iloc[0].to_dict()
        print(f"Found product details: {list(product.keys())}")
        
        # Convert dates to string format if they exist and are datetime objects
        date_fields = ['Date_of_MFG', 'Date_of_EXP', 'Manufacturing_Date', 'Expiry_Date']
        
        for date_field in date_fields:
            if date_field in product and pd.notna(product[date_field]):
                if hasattr(product[date_field], 'strftime'):
                    product[date_field] = product[date_field].strftime('%Y-%m-%d')
                elif isinstance(product[date_field], str):
                    # Already a string, keep as is
                    pass
                else:
                    # Try to convert to string in case it's another type
                    product[date_field] = str(product[date_field])
            
        return product
        
    except Exception as e:
        print(f"Error getting medicine details: {str(e)}")
        import traceback
        traceback.print_exc()
        return None 