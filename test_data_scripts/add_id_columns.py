import pandas as pd
import os
import shutil
import time

def add_id_columns():
    """Add Factory_Id, Dealer_Id, and Retailer_Id columns to qr_validation_tracker.xlsx"""
    try:
        # Path to the tracker file
        tracker_path = 'data/qr_validation_tracker.xlsx'
        
        # Create backup
        backup_path = 'data/qr_validation_tracker_backup_ids.xlsx'
        try:
            shutil.copy2(tracker_path, backup_path)
            print(f"Created backup at {backup_path}")
        except Exception as e:
            print(f"Warning: Could not create backup: {str(e)}")
        
        # Load the tracker file
        tracker_df = pd.read_excel(tracker_path)
        
        # Print original columns
        print(f"Original columns: {tracker_df.columns.tolist()}")
        
        # Get original column order
        original_columns = tracker_df.columns.tolist()
        
        # Define the new columns and their positions
        new_columns = {
            'Factory_Id': original_columns.index('Factory_Reached_Status') + 1,
            'Dealer_Id': original_columns.index('Dealer_Reached_Status') + 1,
            'Retailer_Id': original_columns.index('Retailer_Reached_Status') + 1
        }
        
        # Create a new column list with the new columns in the correct positions
        new_column_list = []
        for i, col in enumerate(original_columns):
            new_column_list.append(col)
            # Check if we need to insert a new column after this one
            for new_col, pos in new_columns.items():
                if i + 1 == pos:
                    new_column_list.append(new_col)
        
        # Create a new DataFrame with the new columns
        new_df = pd.DataFrame(columns=new_column_list)
        
        # Copy data from original DataFrame
        for col in original_columns:
            new_df[col] = tracker_df[col]
        
        # Initialize new columns with empty values
        for col in new_columns.keys():
            new_df[col] = ""
        
        # Print new columns
        print(f"New columns: {new_df.columns.tolist()}")
        
        # Save to a temporary file first
        temp_path = 'data/qr_validation_tracker_temp.xlsx'
        new_df.to_excel(temp_path, index=False)
        
        # Wait a moment to ensure file is written
        time.sleep(1)
        
        # Try to replace the original file
        try:
            if os.path.exists(tracker_path):
                os.remove(tracker_path)
            os.rename(temp_path, tracker_path)
            print(f"Added ID columns successfully.")
            print(f"Updated columns: {new_df.columns.tolist()}")
            return True
        except Exception as e:
            print(f"Could not replace original file: {str(e)}")
            print(f"Updated file available at: {temp_path}")
            print(f"Please manually rename {temp_path} to {tracker_path}")
            return False
            
    except Exception as e:
        print(f"Error adding ID columns: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_id_columns() 