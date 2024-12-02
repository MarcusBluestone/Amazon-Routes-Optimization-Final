import random
import numpy as np
import pandas as pd
import json

import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("--size", type=str, required=True, help="Grid Size")
parser.add_argument("--demand_cnt", type=str, required=True, help="# Demand")
parser.add_argument("--M", type=str, required=False, help="Number of Candidate Factories")

args = parser.parse_args()

size = int(args.size) #40
demand_cnt = int(args.demand_cnt) #100
factory_cnt = int(args.M)

def get_time(loc1, loc2):
    return abs(loc1[0]  - loc2[0]) + abs(loc1[1]  - loc2[1])

def get_data(size):
    demand_locations = set()

    while len(demand_locations) < demand_cnt:
        rand_row, rand_col = random.choice(range(size)), random.choice(range(size))
        demand_locations.add((rand_row, rand_col))
    
    candidate_facilties = set()
    while len(candidate_facilties) < factory_cnt:
        rand_row, rand_col = random.choice(range(size)), random.choice(range(size))
        candidate_facilties.add((rand_row, rand_col))
        if (rand_row, rand_col) not in demand_locations:
            candidate_facilties.add((rand_row, rand_col))

    demand_locations = list(demand_locations)
    candidate_facilties = list(candidate_facilties)

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