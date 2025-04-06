import pandas as pd
import os
import shutil
import time

def remove_qr_code_column():
    """Remove the QR_Code column from qr_validation_tracker.xlsx"""
    try:
        # Path to the tracker file
        tracker_path = 'data/qr_validation_tracker.xlsx'
        
        # Create backup
        backup_path = 'data/qr_validation_tracker_backup.xlsx'
        try:
            shutil.copy2(tracker_path, backup_path)
            print(f"Created backup at {backup_path}")
        except Exception as e:
            print(f"Warning: Could not create backup: {str(e)}")
        
        # Load the tracker file
        tracker_df = pd.read_excel(tracker_path)
        
        # Print original columns
        print(f"Original columns: {tracker_df.columns.tolist()}")
        
        # Check if QR_Code column exists
        if 'QR_Code' in tracker_df.columns:
            # Remove the QR_Code column
            tracker_df = tracker_df.drop(columns=['QR_Code'])
            
            # Save to a temporary file first
            temp_path = 'data/qr_validation_tracker_temp.xlsx'
            tracker_df.to_excel(temp_path, index=False)
            
            # Wait a moment to ensure file is written
            time.sleep(1)
            
            # Try to replace the original file
            try:
                if os.path.exists(tracker_path):
                    os.remove(tracker_path)
                os.rename(temp_path, tracker_path)
                print(f"QR_Code column removed successfully.")
                print(f"Updated columns: {tracker_df.columns.tolist()}")
                return True
            except Exception as e:
                print(f"Could not replace original file: {str(e)}")
                print(f"Updated file available at: {temp_path}")
                print(f"Please manually rename {temp_path} to {tracker_path}")
                return False
        else:
            print("QR_Code column not found in the tracker file.")
            return False
            
    except Exception as e:
        print(f"Error removing QR_Code column: {str(e)}")
        return False

if __name__ == "__main__":
    remove_qr_code_column() 