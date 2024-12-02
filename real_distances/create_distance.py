from geopy.distance import geodesic
import pandas as pd



def calculate_distance(row):
    store_coords = (row['Store_Latitude'], row['Store_Longitude'])
    drop_coords = (row['Drop_Latitude'], row['Drop_Longitude'])
    # Calculate the distance in kilometers
    return geodesic(store_coords, drop_coords).kilometers


if __name__ == "__main__":
    file_path = 'real_distances/unique_deliveries.csv'  # Replace with your Excel file path
    df = pd.read_csv(file_path)

    distances_df = pd.DataFrame({
        'Distance_km': df.apply(calculate_distance, axis=1)
    })
    distances_df.to_csv('real_distances/distances_only_unique.csv', index=False)
    print("Distances saved to 'distances_only.csv'.")

    # file_drops = 'real_distances/unique_drops.csv'
    # file_stores = "real_distances/unique_stores.csv"

    # df_drops = pd.read_csv(file_drops)
    # df_stores = pd.read_csv(file_stores)
    
    # distance_matrix = pd.DataFrame(index=df_stores.index, columns=df_drops.index)
    # count = 0
    # for drop_idx, drop_row in df_drops.iterrows():
    #     for store_idx, store_row in df_stores.iterrows():
    #         store_coords = (store_row['Latitude'], store_row['Longitude'])
    #         drop_coords = (drop_row['Latitude'], drop_row['Longitude'])
    #         distance = geodesic(store_coords, drop_coords).kilometers
    #         distance_matrix.loc[store_idx, drop_idx] = distance

    #         count += 1
    #         if count % 50000 == 0:
    #             print(f"iteration number {count}")

    # # Add labels to rows and columns
    # distance_matrix.index = [f"Store_{i}" for i in df_stores.index]
    # distance_matrix.columns = [f"Drop_{j}" for j in df_drops.index]

    # # Save the distance matrix to a CSV file
    # distance_matrix.to_csv('real_distances/distance_matrix_store_to_drop.csv', index=True)

    # print("Distance matrix saved to 'distance_matrix.csv'.")

    # existing_matrix_file = 'real_distances/distance_matrix_store_to_drop.csv'  # Replace with your file path
    # distance_matrix = pd.read_csv(existing_matrix_file, index_col=0)  # Load with the first column as index

    # # Transpose the matrix to flip rows and columns
    # flipped_matrix = distance_matrix.T

    # # Save the transposed matrix to a new CSV file
    # flipped_matrix.to_csv('real_distances/drop_to_store_distance_matrix.csv', index=True)

    # print("Drop-to-store distance matrix saved to 'drop_to_store_distance_matrix.csv'.")






# # Define two points (latitude, longitude)
# coords_1 = (40.748817, -73.985428)  # New York (Empire State Building)
# coords_2 = (34.052235, -118.243683)  # Los Angeles

# # Calculate the geodesic distance (in kilometers)
# distance_km = geodesic(coords_1, coords_2).kilometers
# print(f"Distance: {distance_km} km")