import subprocess
import argparse
# import datetime
# import pickle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample Python script.")
    parser.add_argument("--N", type=int, required=False, help="Number of Demands")
    parser.add_argument("--size", type=int, required=False, help="Size of the grid")
    parser.add_argument("--S", type=int, required=False, help="Number of trucks")
    parser.add_argument("--M", type=int, required=False, help="Number of Candidate Factories")
    parser.add_argument("--a", type=float, required=False, help="Alpha Value")
    parser.add_argument("--real", type=bool, required=False, help="Run on Amazon Dataset?")
    parser.add_argument("--cluster", type=bool, required=False, help="Run on Amazon Dataset?")


    args = parser.parse_args()
    print(args)

    try:
        N = int(args.N)
    except (TypeError, ValueError):
        N = 4356

    if args.cluster:
        for i in range(24):
            directory = f'clusters/{i}'
            print(f"Here in directory {directory}")
            try:
                subprocess.run(["julia", 'julia_run3.jl', str(args.S), str(args.a), directory], check=True)
            except subprocess.CalledProcessError:
                print("Infeasible!")

    durations = []
    if not args.real:
        subprocess.run(["python", 'create_data.py', '--size', str(args.size), '--demand_cnt', str(N),
                                                    '--M', str(args.M)], check=True)
        subprocess.run(["julia", 'julia_run2.jl', str(args.S), str(args.a)], check=True)
        subprocess.run(["python", 'analyze.py'], check=True)
    else:
        subprocess.run(["julia", 'julia_run2.jl', str(args.S), str(args.a), str(N)], check=True)
        subprocess.run(["python", 'analyze.py', '--N', str(N)], check=True)

