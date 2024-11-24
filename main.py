import subprocess
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample Python script.")
    parser.add_argument("--N", type=int, required=True, help="Number of Demands")
    parser.add_argument("--size", type=int, required=True, help="Size of the grid")
    parser.add_argument("--S", type=int, required=True, help="Number of trucks")

    args = parser.parse_args()
    print(args)

    subprocess.run(["python", 'create_data.py', '--size', str(args.size), '--demand_cnt', str(args.N)], check=True)
    subprocess.run(["julia", 'julia_run.jl', str(args.S)], check=True)
    subprocess.run(["python", 'analyze.py'], check=True)

