#!/bin/bash
# This script formalizes some setup tasks on the cluster

echo "Please choose your desired workflow"
echo "91: Add permission for user to your workspace"
echo "92: Create new conda environment using our template"
read function

if (($function == 91))
then
    echo "Please enter your workspace..."
    read workspace
    echo "Please enter your username..."
    read username
    setfacl -Rm u:$username:rwX,d:u:$username:rwX $(ws_find $workspace)
fi

if (($function == 92))
then
    echo "Please enter the name for the environment..."
    read conda_name
    conda env create --name=$conda_name --file="ds_project/ds_project/organization/cluster_environment/conda_environment.yml"
fi