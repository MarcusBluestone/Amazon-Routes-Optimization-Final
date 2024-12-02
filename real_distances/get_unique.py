import pandas as pd

# Load the Excel file
# file_path = 'real_distances/amazon_delivery_cleaned.csv'  # Replace with your Excel file path
# df = pd.read_csv(file_path)

# # Extract unique Store and Drop locations
# unique_stores = df[['Store_Latitude', 'Store_Longitude']].drop_duplicates().reset_index(drop=True)
# unique_drops = df[['Drop_Latitude', 'Drop_Longitude']].drop_duplicates().reset_index(drop=True)

# # Add meaningful column names
# unique_stores.columns = ['Latitude', 'Longitude']
# unique_drops.columns = ['Latitude', 'Longitude']

# # Save unique locations to new spreadsheets
# unique_stores.to_csv('real_distances/unique_stores.csv', index=False)
# unique_drops.to_csv('real_distances/unique_drops.csv', index=False)

# print("Unique store and drop locations saved to 'unique_stores.csv' and 'unique_csv.csv'.")

# file_path = 'real_distances/amazon_delivery_cleaned.csv'  # Replace with your CSV file path
# df = pd.read_csv(file_path)

# # Count overlapping rows for the same Store and Drop location
# overlap_counts = df.groupby(['Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude']).size().reset_index(name='Count')

# # Filter to get only overlapping deliveries (more than 1 occurrence)
# overlapping_deliveries = overlap_counts[overlap_counts['Count'] > 1]

# # Save the results to a new CSV file if needed
# # overlapping_deliveries.to_csv('real_distances/overlapping_deliveries.csv', index=False)

# # print("Overlapping deliveries saved to 'real_distances/overlapping_deliveries.csv'.")
# print(overlapping_deliveries)

# Load the CSV file
file_path = 'real_distances/amazon_delivery_cleaned.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Count overlapping rows for the same Store and Drop location
overlap_counts = df.groupby(['Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude']).size().reset_index(name='Count')

# Filter to get only overlapping deliveries (more than 1 occurrence)
overlapping_deliveries = overlap_counts[overlap_counts['Count'] > 1]

# Create a DataFrame with only unique deliveries (removing duplicates)
unique_deliveries = df.drop_duplicates(subset=['Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude'])

# Save the unique deliveries to a new CSV file
unique_deliveries.to_csv('real_distances/unique_deliveries.csv', index=False)

# Calculate total rows
original_row_count = df.shape[0]
unique_row_count = unique_deliveries.shape[0]

# Output the total number of rows
print(f"Total number of rows in the original DataFrame: {original_row_count}")
print(f"Total number of rows in the unique deliveries DataFrame: {unique_row_count}")
print(f"Total duplicates found: {original_row_count - unique_row_count}")


