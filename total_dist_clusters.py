import h5py
import numpy as np
import pandas as pd

overall_total = 0
all_stores_array = []
tot_facs = 0
for i in range(12, 24):
    # Directory where the .h5 file is saved
    directory = f"clusters/{i}"

    Tx = pd.read_csv(f"{directory}/demand_distance.csv").iloc[:, 1:].to_numpy()  # N x N
    Ty = pd.read_csv(f"{directory}/store_demand_distance.csv").iloc[:, 1:].to_numpy()  # M x N
    Tz = pd.read_csv(f"{directory}/demand_store_distance.csv").iloc[:, 1:].to_numpy()  # N x M
    stores = pd.read_csv(f"{directory}/stores.csv").iloc[:, 1:].to_numpy() 
    
    print("Tx shape:", Tx.shape)
    print("Ty shape:", Ty.shape)
    print("Tz shape:", Tz.shape)
    
    # Load the data from the .h5 file
    with h5py.File(f"{directory}/output.h5", "r") as f:
        factories = np.array(f["factories"])  # Load factories matrix
        x_edges = np.array(f["x_edges"])      # Load x_edges matrix
        y_edges = np.array(f["y_edges"])      # Load y_edges matrix
        z_edges = np.array(f["z_edges"])      # Load z_edges matrix

    tot_facs += np.sum(factories)
    facs = stores[factories == 1]
    # print("facs here ", facs)
    # print(factories)
    all_stores_array.append(facs)
    
    print("X shape:", x_edges.shape)
    print("Y shape:", y_edges.shape)
    print("Z shape:", z_edges.shape)
    print("Factories Shape: ", factories.shape[0])
    # print(np.sum(factories))
    # print(factories)
    # Perform the calculations
    # Example: Assuming the same shape as the distance matrix
    # total_distance = (
    #     np.sum(x_edges * Tx) +
    #     np.sum(y_edges * Ty) +
    #     np.sum(z_edges * Tz)
    # )

    # Expand dimensions of the distance matrices
    Tx_expanded = np.expand_dims(Tx, axis=-1)  # Shape: (220, 220, 1)
    Ty_expanded = np.expand_dims(Ty, axis=-1)  # Shape: (220, 220, 1)
    Tz_expanded = np.expand_dims(Tz, axis=-1)  # Shape: (220, 220, 1)

    Y_transposed = np.transpose(y_edges, axes=(1, 0, 2))  # Shape: (20, 220, 4)
    Z_transposed = np.transpose(z_edges, axes=(1, 0, 2))  # Shape: (220, 20, 4)

    # Perform element-wise multiplication
    x_weighted = x_edges * Tx_expanded  # Shape: (220, 220, 4)
    y_weighted = Y_transposed * Ty_expanded  # Shape: (220, 220, 4)
    z_weighted = Z_transposed * Tz_expanded  # Shape: (220, 220, 4)

    # Sum over the last axis to get the total distance for each
    total_distance_x = np.sum(x_weighted)
    total_distance_y = np.sum(y_weighted)
    total_distance_z = np.sum(z_weighted)

    # Total combined distance
    total_distance = total_distance_x + total_distance_y + total_distance_z
    overall_total += total_distance
    print(f"Total distance for cluster {i}:", total_distance)
print(f"Total together: {overall_total}")


combined_coordinates = np.vstack(all_stores_array)
print("Total non-unique stoes = ", combined_coordinates.shape[0])
unique_coordinates = np.unique(combined_coordinates, axis=0)
# Get the number of unique coordinates
num_unique_coordinates = unique_coordinates.shape[0]
print("Number of unique stoes = ", num_unique_coordinates)

objective_val = tot_facs * 3 + 4*12 + .01 * overall_total
print("Final Objective Value = ", objective_val)

# Load the CSV file
file_path = "real_distances/distances_only.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Sum the 'Distance_km' column
tot_amaz = data['Distance_km'].sum()

print("Total Distance Amazon (km):", tot_amaz)

file_path2 = "real_distances/distances_only_unique.csv"  # Replace with your file path
data2 = pd.read_csv(file_path2)

# Sum the 'Distance_km' column
tot_amaz2 = data2['Distance_km'].sum()

print("Total Distance Amazon Unique (km):", tot_amaz2)
