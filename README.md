# Optimization Final Project (6.C57)
## Instructions (Main)
- `python main.py` into terminal.
- Arguments:
1. Run on Amazon Dataset: --size --S --a --real True
2. Run on Simulation: --size --S --a --M --N
3. Run w/ Clustering: --cluster True --S --a
- Final image ouputted in graph.jpg

## Instruction (Notebooks)
1. Run `create_data.ipynb` to produce the simulation inputs. This will create a Tx, Ty, and Tz csv files, along with `info.json` inside of the `inputs` folder. 
2. Run `julia_run.ipynb`, which takes the input data and runs our model. Results stored in `results/output.h5`
3. Run `analayze.ipynb`, which visualizes the results. 
