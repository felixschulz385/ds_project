# Working collaboratively on the cluster: An Overview

On the cluster I suggest we work separating domains between our personal directories and the workspace.

The domain separation works as follows:

| Item | Domain |
|---|---|
| GitHub Clone | Personal |
| Data | Workspace |
| Conda environment | Workspace |

The files in the workspace can be accessed under /pfs/work7/workspace/scratch/tu_zxobe27-ds_project

## Data

Data should be saved in /pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data.

## GitHub

I set up GitHub on the cluster to clone the repository inside my $HOME.

## Conda

I uses a conda environment available in the workspace. Its biggest plus is that all packages and dependencies can easily be installed and updated. If using conda, remember to only install packages using conda(-forge) and not pip.

conda works by sourcing it from 

```{.bash}
source /pfs/work7/workspace/scratch/tu_zxobe27-ds_project/conda/bin/activate
conda activate ds_project
```

pandoc infrastructure_tutorial.md -o infrastructure_tutorial.html --citeproc --biblio=.pandoc/literature.bib --csl=.pandoc/apa.csl --template=.pandoc/template.html --css=.pandoc/template.css --toc

## Running notebooks

There are two good ways to work with notebooks on the cluster.

1. JupyterHub: https://uc2-jupyter.scc.kit.edu/jhub/hub/spawn (not yet working with conda)
2. code-server: This hosts a VS Code session in the cloud that can be accessed through an SSH tunnel (super cool, but takes 2-3 minutes to set up for each session)

To start with set a password on the cluster. This step has to be done only once.

```{.bash}
nano ~/.config
```

There are two steps to getting the vscode-server running. Every time you need to work with notebooks on the cluster, get resources and start the server by executing the following commands **on the cluster**:

```{.bash}
salloc --ntasks=1 --partition=single --cpus-per-task=1 --mem-per-cpu=8000 --time=120
module load devel/code-server
code-server --bind-addr 0.0.0.0:8081 --auth password /home/tu/tu_tu/tu_zxobe27/ds_project/ds_project/organization/cluster_environment/ds_project.code-workspace
```

Keep this window running. 

You might need different hardware. It is defined in the `salloc`-call. Find documentation on the queue details in https://wiki.bwhpc.de/e/BwUniCluster2.0/Slurm.

The cluster will assign you a node (as in: *Nodes uc2n414 are ready for job*). Use the ID of that node and create a tunnel to the cluster on **your local command line**:

```{.bash}
ssh -L 8081:<computeNodeID>:8081 <userID>@hk.scc.kit.edu
```

Then you can access the server from http://127.0.0.1:8081 on your **local web browser**.

More on the VScode server on https://www.nhr.kit.edu/userdocs/horeka/debugging_codeserver/.

