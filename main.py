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
    parser.add_argument("--baseline", type=bool, required=False, help="Evaluate the baseline")

    args = parser.parse_args()
    print(args)

    try:
        N = int(args.N)
    except (TypeError, ValueError):
        N = 4356

    if args.cluster and not args.baseline:
        for i in range(12,24):
            directory = f'clusters/{i}'
            print(f"Here in directory {directory}")
            try:
                subprocess.run(["julia", 'julia_run3.jl', str(args.S), str(args.a), directory], check=True)
            except subprocess.CalledProcessError:
                print("Infeasible!")
            else:
                subprocess.run(["python", 'analyze.py', '--i', str(i)])

    elif args.cluster and args.baseline:
        for i in range(0,12):
            directory = f'clusters/{i}'
            print(f"Here in directory baseline {directory}")
            try:
                subprocess.run(["julia", 'julia_run4.jl', str(args.a), directory], check=True)
            except subprocess.CalledProcessError:
                print("Infeasible!")
            # else: # I didn't want to overwrite the regular files with this so need to change the directory or file names
            #     subprocess.run(["python", 'analyze.py', '--i', str(i)])

    else:
        durations = []
        if not args.real:
            subprocess.run(["python", 'create_data.py', '--size', str(args.size), '--demand_cnt', str(N),
                                                        '--M', str(args.M)], check=True)
            subprocess.run(["julia", 'julia_run2.jl', str(args.S), str(args.a)], check=True)
            subprocess.run(["python", 'analyze.py'], check=True)
        else:
            subprocess.run(["julia", 'julia_run2.jl', str(args.S), str(args.a), str(N)], check=True)
            subprocess.run(["python", 'analyze.py', '--N', str(N)], check=True)

