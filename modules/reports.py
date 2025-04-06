import pandas as pd
from datetime import datetime

def generate_reports():
    """Generate simple reports from product database, inventory and QR validation data"""
    reports = {}
    
    try:
        # Load all data sources
        product_df = pd.read_excel('data/product_database_new.xlsx')
        inventory_df = pd.read_excel('data/product_inventory_details_new.xlsx')
        tracker_df = pd.read_excel('data/qr_validation_tracker.xlsx')
        dealer_df = pd.read_excel('data/Dealer_Master.xlsx')
        
        # 1. Product Count Report
        reports['product_count'] = {
            'Total Products': len(product_df),
            'Products by Manufacturer': product_df.groupby('Name_of_manufacturer').size().to_dict()
        }
        
        # 2. Inventory Summary Report
        reports['inventory_summary'] = {
            'Total Items in Inventory': inventory_df['Quantity'].sum(),
            'Items by Type': inventory_df.groupby('QR_Code_Type').sum()['Quantity'].to_dict()
        }
        
        # 3. Product Validation Status Report
        validation_statuses = {
            'Factory': tracker_df['Factory_Reached_Status'].notna().sum(),
            'Dealer': tracker_df['Dealer_Reached_Status'].notna().sum(),
            'Retailer': tracker_df['Retailer_Reached_Status'].notna().sum(),
            'Consumer': tracker_df['Consumer_Reached_Status'].notna().sum()
        }
        reports['validation_status'] = validation_statuses
        
        # 4. Dealer Activity Report
        dealer_activities = {}
        for dealer_type in dealer_df['Type'].unique():
            if dealer_type == 'Factory':
                count = tracker_df['Factory_Id'].notna().sum()
            elif dealer_type == 'Dealer':
                count = tracker_df['Dealer_Id'].notna().sum()
            elif dealer_type == 'Retailer':
                count = tracker_df['Retailer_Id'].notna().sum()
            else:
                count = 0
            dealer_activities[dealer_type] = count
        reports['dealer_activity'] = dealer_activities
        
        # 5. Product Expiry Report (products nearing expiry)
        try:
            inventory_df['Date_of_EXP'] = pd.to_datetime(inventory_df['Date_of_EXP'])
            today = datetime.now()
            expiring_soon = inventory_df[inventory_df['Date_of_EXP'] < (today + pd.Timedelta(days=90))]
            reports['expiring_soon'] = {
                'Count': len(expiring_soon),
                'Products': expiring_soon[['Name_of_Item', 'Date_of_EXP', 'Quantity']].to_dict('records')
            }
        except:
            reports['expiring_soon'] = {'Count': 0, 'Products': []}
        
        # 6. Consumer Feedback Summary (if available)
        consumer_validations = tracker_df['Consumer_Reached_Status'].notna().sum()
        reports['consumer_feedback'] = {
            'Total Validations': consumer_validations
        }
    
    except Exception as e:
        print(f"Error generating reports: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return reports 