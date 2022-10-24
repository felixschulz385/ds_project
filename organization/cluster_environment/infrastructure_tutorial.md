# Working collaboratively on the cluster: An Overview

On the cluster we work by separating domains between our personal directories and the (data) workspace.

The domain separation works as follows:

| Item | Domain |
|---|---|
| GitHub Clone | Personal |
| Data | Workspace |
| Conda environment | Workspace |

The files in the workspace can be accessed under /pfs/work7/workspace/scratch/tu_zxobe27-ds_project

## GitHub

Set up GitHub on the cluster to clone the repository inside your $HOME.

## Data

Data should be saved in /pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data.

## Conda

Use the conda environment available in the workspace. Felix will from time to time update the .yml file that backs up the conda environment.

This can be accomplished by sourcing conda from 

```{.bash}
source /pfs/work7/workspace/scratch/tu_zxobe27-ds_project/conda/bin/activate
```

And then using 

```{.bash}
conda activate ds_project
```
to activate the environment.

Remember to only install packages using conda(-forge) and not pip.

## Running notebooks

It is recommended to request computing power in an interactive session to not misuse the login nodes of the cluster. To this end use 

```{.bash}
salloc --ntasks=1 --partition=single --cpus-per-task=1 --mem-per-cpu=8000 --time=120
```

or, respectively

```{.python}
import os
os.system("salloc --ntasks=1 --partition=single --cpus-per-task=1 --mem-per-cpu=8000 --time=120")
```

Find documentation on the queue details in https://wiki.bwhpc.de/e/BwUniCluster2.0/Slurm.