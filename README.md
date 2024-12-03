# Optimization Final Project (6.C57)

## Clustering Instructions
- Run all cells in cluster.ipynb --> this sets up all the proper data (don't worry, this won't get uploaded to git)
- python main.py --cluster True --S --a 
- Results saved by region in the clusters folder

## Instructions (Main)
- `python main.py` into terminal.
- Arguments:
1. Run on Amazon Dataset: --size --S --a --real True
2. Run on Simulation: --size --S --a --M --N
- Final image ouputted in graph.jpg

## Instruction (Notebooks)
1. Run `create_data.ipynb` to produce the simulation inputs. This will create a Tx, Ty, and Tz csv files, along with `info.json` inside of the `inputs` folder. 
2. Run `julia_run.ipynb`, which takes the input data and runs our model. Results stored in `results/output.h5`
3. Run `analayze.ipynb`, which visualizes the results. 
