import pandas as pd
from geopy.distance import geodesic

# Load the unique drops CSV file
drops_file = 'real_distances/unique_drops.csv'  # Replace with your drops file path
drops_df = pd.read_csv(drops_file)

# Initialize an empty DataFrame to store distances
distance_matrix = pd.DataFrame(index=drops_df.index, columns=drops_df.index)
count = 0
# Calculate distances between drop locations
for i, drop_1 in drops_df.iterrows():
    for j, drop_2 in drops_df.iterrows():
        drop_1_coords = (drop_1['Latitude'], drop_1['Longitude'])
        drop_2_coords = (drop_2['Latitude'], drop_2['Longitude'])
        # Calculate geodesic distance
        distance_matrix.loc[i, j] = geodesic(drop_1_coords, drop_2_coords).kilometers

        count += 1
        if count % 50000 == 0:
            print(f"iteration number {count}")

# Add labels to rows and columns
distance_matrix.index = [f"Drop_{idx}" for idx in drops_df.index]
distance_matrix.columns = [f"Drop_{idx}" for idx in drops_df.index]

# Save the distance matrix to a CSV file
distance_matrix.to_csv('real_distances/drop_distance_matrix.csv', index=True)

print("Drop-to-drop distance matrix saved to 'drop_distance_matrix.csv'.")

# file_path = 'real_distances/distance_matrix_store_to_drop.csv'  # Replace with your actual file name

# # Read the CSV into a DataFrame
# distance_matrix = pd.read_csv(file_path, index_col=0)

# # Get the number of rows and columns
# num_rows, num_columns = distance_matrix.shape

# print(f"Number of rows: {num_rows}")
# print(f"Number of columns: {num_columns}")
