#!/bin/bash
# This script serves multiple purposes and guides you through the setup of the work environment on the cluster

echo Please choose your desired workflow
echo "1: request resources and activate conda"
echo "91: Add permission for user to your workspace"
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

setfacl -Rm u:$username:rwX,d:u:$username:rwX $(ws_find $workspace)
