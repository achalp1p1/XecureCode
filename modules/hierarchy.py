import pandas as pd

def get_hierarchy_info(qr_code):
    """Get hierarchical information for a QR code"""
    try:
        # Load the QR validation tracker
        tracker_df = pd.read_excel('data/qr_validation_tracker.xlsx')
        
        # Print available columns for debugging
        print(f"Available columns in hierarchy search: {tracker_df.columns.tolist()}")
        
        # Determine QR code type based on character content
        priority_search = None
        
        if 'C' in qr_code:
            priority_search = 'Carton_QR_Code'
            print(f"QR code {qr_code} identified as Carton QR code for hierarchy search")
        elif 'B' in qr_code:
            priority_search = 'Box_QR_Code'
            print(f"QR code {qr_code} identified as Box QR code for hierarchy search")
        elif 'I' in qr_code:
            priority_search = 'Item_QR_Code'
            print(f"QR code {qr_code} identified as Item QR code for hierarchy search")
        
        # Find the QR code in tracker
        tracker_match = None
        
        # Try the priority column first if determined
        if priority_search and priority_search in tracker_df.columns:
            tracker_match = tracker_df[tracker_df[priority_search] == qr_code]
            if not tracker_match.empty:
                print(f"Found hierarchy match for {priority_search}: {qr_code}")
        
        # If not found or no priority, try other QR code columns
        if tracker_match is None or tracker_match.empty:
            # First check if it's an Item QR code
            if 'Item_QR_Code' in tracker_df.columns and priority_search != 'Item_QR_Code':
                tracker_match = tracker_df[tracker_df['Item_QR_Code'] == qr_code]
                if not tracker_match.empty:
                    print(f"Found hierarchy match for Item_QR_Code: {qr_code}")
            
            # If not found, check if it's a Box QR code
            if (tracker_match is None or tracker_match.empty) and 'Box_QR_Code' in tracker_df.columns and priority_search != 'Box_QR_Code':
                tracker_match = tracker_df[tracker_df['Box_QR_Code'] == qr_code]
                if not tracker_match.empty:
                    print(f"Found hierarchy match for Box_QR_Code: {qr_code}")
            
            # If not found, check if it's a Carton QR code
            if (tracker_match is None or tracker_match.empty) and 'Carton_QR_Code' in tracker_df.columns and priority_search != 'Carton_QR_Code':
                tracker_match = tracker_df[tracker_df['Carton_QR_Code'] == qr_code]
                if not tracker_match.empty:
                    print(f"Found hierarchy match for Carton_QR_Code: {qr_code}")
        
        if tracker_match is None or tracker_match.empty:
            print(f"QR code {qr_code} not found in any QR code column for hierarchy lookup")
            return None
            
        # Extract hierarchy information
        hierarchy = {}
        row = tracker_match.iloc[0]
        
        # Check for each hierarchy level in columns
        if 'Carton_QR_Code' in tracker_df.columns and pd.notna(row.get('Carton_QR_Code')):
            hierarchy['carton'] = row['Carton_QR_Code']
            
        if 'Box_QR_Code' in tracker_df.columns and pd.notna(row.get('Box_QR_Code')):
            hierarchy['box'] = row['Box_QR_Code']
            
        if 'Item_QR_Code' in tracker_df.columns and pd.notna(row.get('Item_QR_Code')):
            hierarchy['item'] = row['Item_QR_Code']
            
        return hierarchy
        
    except Exception as e:
        print(f"Error getting hierarchy info: {str(e)}")
        import traceback
        traceback.print_exc()
        return None 