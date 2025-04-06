import pandas as pd
import os

def update_product_database():
    """Update the product database by removing QR code columns and making SourceInfo the first column"""
    # Path to the Excel database
    excel_path = 'data/product_database_new.xlsx'
    
    # Check if the file exists
    if not os.path.exists(excel_path):
        print(f"Error: Database file not found at {excel_path}")
        return False
    
    try:
        # Load the product database
        df = pd.read_excel(excel_path)
        
        # Remove QR code columns if they exist
        columns_to_remove = ['QR_Code_Carton', 'QR_Code_Box', 'QR_Code_Item']
        for col in columns_to_remove:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        # Make sure SourceInfo exists
        if 'SourceInfo' not in df.columns:
            print("Error: SourceInfo column not found in the database")
            return False
        
        # Reorder columns to make SourceInfo the first column
        columns = df.columns.tolist()
        columns.remove('SourceInfo')
        new_columns = ['SourceInfo'] + columns
        df = df[new_columns]
        
        # Save the updated database
        df.to_excel(excel_path, index=False)
        print(f"Product database updated successfully. SourceInfo is now the first column.")
        print(f"Removed columns: {columns_to_remove}")
        return True
        
    except Exception as e:
        print(f"Error updating product database: {e}")
        return False

if __name__ == "__main__":
    update_product_database() 