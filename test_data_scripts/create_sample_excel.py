import pandas as pd
import datetime
import random
import os
import hashlib

# Create a directory for data if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Function to generate a 10-digit checksum from product details
def generate_checksum(mfg_date, exp_date, factory_location, manufacturer, item_name, mrp):
    # Combine all details with '&' separator
    combined_data = f"{mfg_date}&{exp_date}&{factory_location}&{manufacturer}&{item_name}&{mrp}"
    
    # Create a hash of the combined data
    hash_object = hashlib.md5(combined_data.encode())
    hash_hex = hash_object.hexdigest()
    
    # Take the first 10 characters of the hash and convert to a number
    # This ensures we get a 10-digit number
    checksum = int(hash_hex[:10], 16) % 10000000000
    
    # Format as a 10-digit string with leading zeros
    return f"{checksum:010d}"

# Function to generate a 10-digit unique number
def generate_unique_number():
    return f"{random.randint(1, 9999999999):010d}"

# Generate sample data first
factory_locations = [
    'HP2 Plant', 'Mumbai Plant', 'Bangalore Plant', 'Delhi Plant', 'Chennai Plant',
    'Hyderabad Plant', 'Kolkata Plant', 'Pune Plant', 'Ahmedabad Plant', 'Lucknow Plant'
]

manufacturers = [
    'Ranbaxy', 'Cipla', 'Sun Pharma', 'Dr. Reddy\'s', 'Aurobindo Pharma',
    'Lupin', 'Glenmark', 'Cadila Healthcare', 'Biocon', 'Divis Laboratories'
]

item_names = [
    'Crocin 500mg', 'Paracetamol 650mg', 'Amoxicillin 250mg', 'Omeprazole 20mg', 'Metformin 500mg',
    'Aspirin 75mg', 'Cetirizine 10mg', 'Pantoprazole 40mg', 'Azithromycin 500mg', 'Metoprolol 25mg'
]

# Generate product details
product_details = []
for i in range(10):
    mfg_date = (datetime.datetime.now() - datetime.timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
    exp_date = (datetime.datetime.now() + datetime.timedelta(days=random.randint(365, 730))).strftime('%Y-%m-%d')
    factory_location = random.choice(factory_locations)
    manufacturer = random.choice(manufacturers)
    item_name = random.choice(item_names)
    mrp = round(random.uniform(10, 500), 2)
    
    product_details.append({
        'Date_of_MFG': mfg_date,
        'Date_of_EXP': exp_date,
        'Origin_Factory_Location': factory_location,
        'Name_of_manufacturer': manufacturer,
        'Name_of_item': item_name,
        'MRP': mrp
    })

# Generate QR codes using the checksum as source info
qr_codes = []
for details in product_details:
    source_info = generate_checksum(
        details['Date_of_MFG'],
        details['Date_of_EXP'],
        details['Origin_Factory_Location'],
        details['Name_of_manufacturer'],
        details['Name_of_item'],
        details['MRP']
    )
    object_code = random.choice(['C', 'B', 'I'])  # C for Carton, B for Box, I for individual item
    object_unique_number = generate_unique_number()
    qr_code = f"{source_info}{object_code}{object_unique_number}"
    qr_codes.append(qr_code)

# Create the complete data dictionary
data = {
    'QR_Code': qr_codes,
    'Date_of_MFG': [details['Date_of_MFG'] for details in product_details],
    'Date_of_EXP': [details['Date_of_EXP'] for details in product_details],
    'Origin_Factory_Location': [details['Origin_Factory_Location'] for details in product_details],
    'Name_of_manufacturer': [details['Name_of_manufacturer'] for details in product_details],
    'Name_of_item': [details['Name_of_item'] for details in product_details],
    'MRP': [details['MRP'] for details in product_details]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel with a new filename
excel_path = 'data/product_database_new.xlsx'

# Save the new file
try:
    df.to_excel(excel_path, index=False)
    print(f"Sample Excel file created successfully at {excel_path}")
    print("\nGenerated QR Codes:")
    for i, qr in enumerate(qr_codes):
        print(f"{i+1}. {qr}")
        print(f"   Source Info (Checksum): {qr[:10]}")
        print(f"   Object Code: {qr[10]}")
        print(f"   Unique Number: {qr[11:]}")
        print(f"   Product: {data['Name_of_item'][i]} by {data['Name_of_manufacturer'][i]}")
        print()
except Exception as e:
    print(f"Error creating Excel file: {e}")
    
    # Try an alternative approach - save as CSV
    csv_path = 'data/product_database_new.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved data as CSV instead: {csv_path}") 