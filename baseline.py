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

count = 0
# Iterate through each drop location
for _, drop_row in df_drops.iterrows():
    drop_coords = (drop_row["Latitude"], drop_row["Longitude"])
    
    # Calculate the minimum distance to any store
    min_dist = float("inf")  # Start with an infinitely large value
    for _, store_row in df_stores.iterrows():
        store_coords = (store_row["Latitude"], store_row["Longitude"])
        temp_dist = geodesic(store_coords, drop_coords).kilometers
        min_dist = min(min_dist, temp_dist)
    if count % 100 == 0:
        print("Up to count: ", count)
    count += 1
    # Add the minimum distance to the total
    total_dist += min_dist

print("Minimum total distance =", total_dist)
