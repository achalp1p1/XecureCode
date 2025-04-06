import pandas as pd
import os
from datetime import datetime
import time

def generate_hierarchical_qr_codes():
    """
    Generate hierarchical QR codes for products:
    - 1 Carton per product
    - 2 Boxes per carton
    - 2 Items per box (4 items total per product)
    
    QR code format: 
    - Carton: SourceInfo + C + 10 digit sequence
    - Box: SourceInfo + B + 10 digit sequence
    - Item: SourceInfo + I + 10 digit sequence
    """
    print("Starting QR code generation process...")
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created data directory")
    
    try:
        # Load the product database
        product_df = pd.read_excel('data/product_database_new.xlsx')
        print(f"Loaded product database with {len(product_df)} products")
        
        # Initialize lists to store QR codes and related info
        qr_data = []
        
        # Process each product
        for idx, product in product_df.iterrows():
            source_info = str(product['SourceInfo'])
            print(f"Processing product {idx+1}/{len(product_df)} with SourceInfo: {source_info}")
            
            # Generate 1 carton QR code
            carton_qr = f"{source_info}C0000000001"
            
            # For each carton, generate 2 box QR codes
            for box_num in range(1, 3):
                box_qr = f"{source_info}B000000000{box_num}"
                
                # For each box, generate 2 item QR codes
                for item_num in range(1, 3):
                    # Calculate the global item number (2 items per box)
                    global_item_num = (box_num - 1) * 2 + item_num
                    item_qr = f"{source_info}I000000000{global_item_num}"
                    
                    # Add entry to tracker data
                    qr_data.append({
                        'Carton_QR_Code': carton_qr,  # Carton this item belongs to
                        'Box_QR_Code': box_qr,  # Box this item belongs to
                        'Item_QR_Code': item_qr,  # Item QR code
                        'SourceInfo': source_info,
                        # New Factory columns
                        'Factory_Reached_Status': '',
                        'Factory_Time_Stamp': '',
                        'Factory_Geo_Location': '',
                        # Renamed from Distributor to Dealer
                        'Dealer_Reached_Status': '',
                        'Dealer_Time_Stamp': '',
                        'Dealer_Geo_Location': '',
                        # Renamed from Dealer to Retailer
                        'Retailer_Reached_Status': '',
                        'Retailer_Time_Stamp': '',
                        'Retailer_Geo_Location': '',
                        # Renamed from Retailer to Consumer
                        'Consumer_Status': '',
                        'Consumer_Time_Stamp': '',
                        'Consumer_Geo_Location': ''
                    })
        
        # Create the QR validation tracker DataFrame
        tracker_df = pd.DataFrame(qr_data)
        
        # Print an example of the hierarchy for the first product
        if qr_data:
            print("\nExample hierarchy for first product:")
            carton = qr_data[0]['Carton_QR_Code']
            print(f"Carton: {carton}")
            
            boxes = set()
            for entry in qr_data[:4]:  # First 4 entries are for first product
                if entry['Carton_QR_Code'] == carton:
                    boxes.add(entry['Box_QR_Code'])
            
            for box in sorted(boxes):
                print(f"  Box: {box}")
                items = []
                for entry in qr_data[:4]:
                    if entry['Box_QR_Code'] == box:
                        items.append(entry['Item_QR_Code'])
                for item in items:
                    print(f"    Item: {item}")
        
        # Save the tracker with appropriate permissions handling
        tracker_path = 'data/qr_validation_tracker.xlsx'
        
        # Create backup first
        if os.path.exists(tracker_path):
            backup_path = f'data/qr_validation_tracker_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            try:
                # Try to create a backup
                backup_df = pd.read_excel(tracker_path)
                backup_df.to_excel(backup_path, index=False)
                print(f"Backed up existing tracker to {backup_path}")
            except Exception as e:
                print(f"Warning: Could not backup existing file: {str(e)}")
        
        # Ensure column order is preserved in the output file
        if 'Item_QR_Code' in tracker_df.columns and 'QR_Code' not in tracker_df.columns:
            # Create a copy of Item_QR_Code to preserve compatibility with existing code
            tracker_df['QR_Code'] = tracker_df['Item_QR_Code']
        
        # Define column order
        column_order = [
            'Carton_QR_Code', 'Box_QR_Code', 'Item_QR_Code', 'SourceInfo',
            'Factory_Reached_Status', 'Factory_Time_Stamp', 'Factory_Geo_Location',
            'Dealer_Reached_Status', 'Dealer_Time_Stamp', 'Dealer_Geo_Location',
            'Retailer_Reached_Status', 'Retailer_Time_Stamp', 'Retailer_Geo_Location',
            'Consumer_Status', 'Consumer_Time_Stamp', 'Consumer_Geo_Location'
        ]
        
        # Add any remaining columns not explicitly ordered
        all_columns = column_order + [col for col in tracker_df.columns if col not in column_order and col != 'QR_Code']
        if 'QR_Code' in tracker_df.columns:
            all_columns.append('QR_Code')  # Add QR_Code at the end for compatibility
        
        # Reorder columns
        tracker_df = tracker_df[all_columns]
        
        # Try to save the new tracker file with retries
        max_retries = 5
        for attempt in range(max_retries):
            try:
                # Try to save to a temporary file first
                temp_path = f'data/qr_validation_tracker_temp.xlsx'
                tracker_df.to_excel(temp_path, index=False)
                
                # If successful, try to rename to the final file
                if os.path.exists(tracker_path):
                    os.remove(tracker_path)
                os.rename(temp_path, tracker_path)
                
                print(f"Successfully created qr_validation_tracker.xlsx with {len(tracker_df)} QR codes")
                print(f"Columns in order: {', '.join(tracker_df.columns[:10])}")
                break
            except Exception as e:
                print(f"Attempt {attempt+1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    print("Could not save tracker file after multiple attempts.")
                    # Save to an alternative location as a last resort
                    alt_path = f'data/qr_validation_tracker_new_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
                    tracker_df.to_excel(alt_path, index=False)
                    print(f"Saved tracker to alternative location: {alt_path}")
        
        print("\nQR code generation completed successfully")
        return True
        
    except Exception as e:
        print(f"Error generating QR codes: {str(e)}")
        return False

if __name__ == "__main__":
    generate_hierarchical_qr_codes() 