#!/bin/bash
# This script serves multiple purposes and guides you through the setup of the work environment on the cluster

echo Please choose your desired workflow
echo "1: request resources and activate conda"
echo "91: Add permission for user to your workspace"
echo "92: Create new conda environment using our template"
read function

if [$function = 1]
then
    
    source $( ws_find ds_project )/conda/etc/profile.d/conda.sh
fi

if [$function = 91]
then
    echo Please enter your workspace...
    read workspace
    echo Please enter your username...
    read username
    setfacl -Rm u:$username:rwX,d:u:$username:rwX $(ws_find $workspace)
fi

if [$function = 92]
then
    echo Please enter the name for the environemtn workspace...
    read conda_name
    conda env create --name=$conda_name --file="ds_project/ds_project/organization/cluster_environment/conda_environment.yml"
fi

setfacl -Rm u:$username:rwX,d:u:$username:rwX $(ws_find $workspa
