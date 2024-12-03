import h5py
# import json
import numpy as np
import pandas as pd
import argparse

import networkx as nx
import matplotlib.pyplot as plt


# with open('inputs/info.json', 'r') as f:
#     info_json = json.load(f)
# cand_factories = np.array(info_json['factories'])
# demands = np.array(info_json['demands'])

parser = argparse.ArgumentParser(description="A sample Python script.")
parser.add_argument("--N", type=str, required=True, help="Number of Demands")
args = parser.parse_args()

scale = 1
unique_stores_pd = pd.read_csv('real_distances/unique_stores.csv').applymap(lambda x : scale * x)
demands_pd = pd.read_csv('real_distances/unique_drops.csv').applymap(lambda x : scale * x)

cand_factories = list(zip(unique_stores_pd['Latitude'], unique_stores_pd['Longitude']))
demands = list(zip(demands_pd['Latitude'][:N], demands_pd['Longitude'][:N]))

with h5py.File('results/output.h5', 'r') as f:
    # List all datasets
    print("Datasets in the file:", list(f.keys()))
    factory_indic = f['factories'].__array__() #indicator for each factory
    # x_edges = f['x_edges'].__array__()
    x_edges = np.transpose(np.array(f['x_edges']), axes=(2, 1, 0))
    y_edges = np.transpose(np.array(f['y_edges']), axes=(2, 1, 0))
    z_edges = np.transpose(np.array(f['z_edges']), axes=(2, 1, 0))

S,M,N = y_edges.shape

#color_list = list(mcolors.XKCD_COLORS.keys())
color_list = ['red', 'blue', 'orange', 'green', 'pink', 'black']
# color_num = 0

G = nx.DiGraph()
for i in range(len(cand_factories)):
    color = 'grey'
    if factory_indic[i] == 1:
        color = 'blue'
    G.add_node(str(i) + 'F', color=color, pos=cand_factories[i])

G.add_nodes_from(
    [(str(i) + 'D', {"color": 'red', 'pos': demands[i]}) for i in range(len(demands))]
)

color_num = 0
for truck_num in range(S):
    used_truck = False

    #Factory --> Demand
    idxs = np.where(y_edges[truck_num, :, :])
    idx1_list, idx2_list = idxs #all demand 1's, all demand 2's
    for idx1, idx2 in zip(idx1_list, idx2_list):
        used_truck = True
        G.add_edge((str(idx1) + 'F'), (str(idx2) + 'D'), color = color_list[color_num])

    #Demand --> Demand
    idxs = np.where(x_edges[truck_num, :, :])
    idx1_list, idx2_list = idxs #all demand 1's, all demand 2's
    for idx1, idx2 in zip(idx1_list, idx2_list):
        G.add_edge((str(idx1) + 'D'), (str(idx2) + 'D'), color = color_list[color_num])

    #Demand --> Factory
    idxs = np.where(z_edges[truck_num, :, :])
    idx1_list, idx2_list = idxs #all demand 1's, all demand 2's
    for idx1, idx2 in zip(idx1_list, idx2_list):
        G.add_edge((str(idx1) + 'D'), (str(idx2) + 'F'), color = color_list[color_num])
        
    if used_truck:
        print(truck_num, color_list[color_num])
        color_num = (color_num + 1) % len(color_list)


# print(G.nodes)
# print(G.edges)
node_colors = [G.nodes[node]['color'] for node in G.nodes]
edge_colors = [G.edges[edge]['color'] for edge in G.edges]
pos = nx.get_node_attributes(G, 'pos')  

plt.figure(3,figsize=(100,100)) 

nodes = nx.draw_networkx_nodes(G, pos=pos, node_color=node_colors)
nodes.set_zorder(1)
edges = nx.draw_networkx_edges(G, pos=pos, edge_color=edge_colors, connectionstyle='arc3,rad=0.2', arrows=True)
# labels = nx.draw_networkx_labels(G, pos=pos, font_size=5)

plt.savefig("graph.pdf")
# nx.draw_networkx(G, pos=pos,node_color=node_colors, edge_color=edge_colors,connectionstyle='arc3,rad=0.2', arrows=True, font_size=5)