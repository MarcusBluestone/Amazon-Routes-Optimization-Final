import subprocess
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample Python script.")
    parser.add_argument("--N", type=int, required=False, help="Number of Demands")
    parser.add_argument("--size", type=int, required=False, help="Size of the grid")
    parser.add_argument("--S", type=int, required=False, help="Number of trucks")

    args = parser.parse_args()
    print(args)
    subprocess.run(["python", 'create_data.py', '--size', str(args.size), '--demand_cnt', str(args.N)], check=True)
    subprocess.run(["julia", 'julia_run.jl', str(args.S)], check=True)
    subprocess.run(["python", 'analyze.py'], check=True)


    #Checking Feasability of a lot of different situations (note that the objective is commented out)
    # size = 30
    # for N in range(100, 200, 3):
    #     for S in range(1, 5):
    #         print("Info: ", size, N, S)
    #         subprocess.run(["python", 'create_data.py', '--size', str(size), '--demand_cnt', str(N)], check=True)
    #         subprocess.run(["julia", 'julia_run.jl', str(S)], check=True)
    #         subprocess.run(["python", 'analyze.py'], check=True)   


