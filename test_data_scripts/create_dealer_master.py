import pandas as pd
import os

def create_dealer_master():
    """Create a new Excel file for Dealer Master with sample data"""
    # Sample data for Dealer Master
    data = {
        'Id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'Type': ['Factory', 'Dealer', 'Retailer', 'Factory', 'Dealer', 'Retailer', 'Factory', 'Dealer', 'Retailer'],
        'Name': [
            'Pharma Manufacturing Ltd',
            'MediSupply Distributors',
            'Health First Pharmacy',
            'Global Pharma Factory',
            'Regional MedTech Solutions',
            'City Medical Store',
            'BioTech Laboratories',
            'District Medical Suppliers',
            'Community Health Center'
        ],
        'Address': [
            '123 Industrial Zone, Sector 1, New Delhi - 110001',
            '456 Market Street, Mumbai - 400001',
            '789 Local Mall, Bangalore - 560001',
            '321 Manufacturing Hub, Hyderabad - 500001',
            '654 Distribution Center, Chennai - 600001',
            '987 Shopping Complex, Kolkata - 700001',
            '147 Pharma Park, Ahmedabad - 380001',
            '258 Business Tower, Pune - 411001',
            '369 Retail Avenue, Jaipur - 302001'
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Save to Excel file
    excel_path = 'data/Dealer_Master.xlsx'
    df.to_excel(excel_path, index=False)
    print(f"Dealer Master Excel file created successfully at {excel_path}")
    print("\nSample data created with the following records:")
    print(df.to_string())
    
    return True

if __name__ == "__main__":
    create_dealer_master() 