import random
import numpy as np
import pandas as pd
import json


size = 20 #40
demand_cnt = 75#100

def get_time(loc1, loc2):
    return abs(loc1[0]  - loc2[0]) + abs(loc1[1]  - loc2[1])

def get_data(size):
    grid = np.zeros((size, size))
    demand_locations = set()

    while len(demand_locations) < demand_cnt:
        rand_row, rand_col = random.choice(range(size)), random.choice(range(size))
        demand_locations.add((rand_row, rand_col))
        grid[rand_row, rand_col] = 1
    
    candidate_facilties = []
    for i in range(size):
        for j in range(size):
            if grid[i,j] == 0:
                candidate_facilties.append((i,j))

    demand_locations = list(demand_locations)

    Tx = np.zeros((demand_cnt, demand_cnt))
    for j1 in range(demand_cnt):
        for j2 in range(demand_cnt):
            Tx[j1, j2] = get_time(demand_locations[j1], demand_locations[j2])

    Ty = np.zeros((len(candidate_facilties), demand_cnt))
    for i in range(len(candidate_facilties)):
        for j in range(demand_cnt):
            Ty[i, j] = get_time(candidate_facilties[i], demand_locations[j])

    Tz = np.zeros((demand_cnt, len(candidate_facilties)))
    for i in range(demand_cnt):
        for j in range(len(candidate_facilties)):
            Tz[i, j] = get_time(demand_locations[i], candidate_facilties[j])

    #Locations
    with open('inputs/info.json', 'w') as f:
        json.dump({"factories": candidate_facilties, "demands": demand_locations}, f)
    return Tx, Ty, Tz

Tx, Ty, Tz = get_data(size)

pd.DataFrame(Tx).to_csv('inputs/Tx.csv', index=True)
pd.DataFrame(Ty).to_csv('inputs/Ty.csv', index=True)
pd.DataFrame(Tz).to_csv('inputs/Tz.csv', index=True)