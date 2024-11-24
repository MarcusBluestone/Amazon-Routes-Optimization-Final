import subprocess


if __name__ == "__main__":
    subprocess.run(["python", 'create_data.py'], check=True)
    subprocess.run(["julia", 'julia_run.jl'], check=True)
    subprocess.run(["python", 'analyze.py'], check=True)

