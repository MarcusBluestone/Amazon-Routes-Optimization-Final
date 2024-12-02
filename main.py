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

    args = parser.parse_args()
    print(args)
    durations = []
    if not args.real:
            # duration_total = 0
            # for _ in range(3):
            #     start_time = datetime.datetime.now()
                subprocess.run(["python", 'create_data.py', '--size', str(args.size), '--demand_cnt', str(args.N),
                                                            '--M', str(args.M)], check=True)
                subprocess.run(["julia", 'julia_run.jl', str(args.S), str(args.a)], check=True)
                subprocess.run(["python", 'analyze.py'], check=True)
            #     duration_total += (datetime.datetime.now() - start_time).total_seconds()
            # durations.append(duration_total / 3)
            # print(durations[-1])

        
            # with open('durations.pkl', 'wb') as f:
            #     pickle.dump(durations, f)
    else:
        subprocess.run(["julia", 'julia_run.jl', str(args.S), str(args.a), str(args.N)], check=True)
        subprocess.run(["python", 'analyze.py', '--N', str(args.N)], check=True)

