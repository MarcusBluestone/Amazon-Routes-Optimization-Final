import pandas as pd

# Load the Excel file
file_path = 'real_distances/amazon_delivery_cleaned.csv'  # Replace with your Excel file path
df = pd.read_csv(file_path)

# Extract unique Store and Drop locations
unique_stores = df[['Store_Latitude', 'Store_Longitude']].drop_duplicates().reset_index(drop=True)
unique_drops = df[['Drop_Latitude', 'Drop_Longitude']].drop_duplicates().reset_index(drop=True)

# Add meaningful column names
unique_stores.columns = ['Latitude', 'Longitude']
unique_drops.columns = ['Latitude', 'Longitude']

# Save unique locations to new spreadsheets
unique_stores.to_csv('real_distances/unique_stores.csv', index=False)
unique_drops.to_csv('real_distances/unique_drops.csv', index=False)

print("Unique store and drop locations saved to 'unique_stores.csv' and 'unique_csv.csv'.")
