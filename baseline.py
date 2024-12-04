import numpy as np
import pandas as pd
from geopy.distance import geodesic

# Load the data
df_stores = pd.read_csv("real_distances/unique_stores.csv")
df_drops = pd.read_csv("real_distances/unique_drops.csv")

# Ensure columns "Latitude" and "Longitude" exist in both dataframes
if not {"Latitude", "Longitude"}.issubset(df_stores.columns) or not {"Latitude", "Longitude"}.issubset(df_drops.columns):
    raise ValueError("Both CSV files must have 'Latitude' and 'Longitude' columns.")

# Initialize total distance
total_dist = 0
unique_closest_stores = set()
max_min_dist = 0
count = 0
# Iterate through each drop location
for _, drop_row in df_drops.iterrows():
    drop_coords = (drop_row["Latitude"], drop_row["Longitude"])
    
    # Calculate the minimum distance to any store
    min_dist = float("inf")  # Start with an infinitely large value
    closest_store = None
    for _, store_row in df_stores.iterrows():
        store_coords = (store_row["Latitude"], store_row["Longitude"])
        temp_dist = geodesic(store_coords, drop_coords).kilometers
        if temp_dist < min_dist:
            min_dist = temp_dist
            closest_store = store_row["Latitude"], store_row["Longitude"]
        # min_dist = min(min_dist, temp_dist)
    if closest_store:
        unique_closest_stores.add(closest_store)
    if count % 100 == 0:
        print("Up to count: ", count)
    count += 1
    # Add the minimum distance to the total
    total_dist += min_dist
    max_min_dist = max(max_min_dist, min_dist)

print("Minimum total distance =", total_dist)
print("Number of unique stores that were the closest to a drop =", len(unique_closest_stores))
print("Longest wait time: ", max_min_dist)

