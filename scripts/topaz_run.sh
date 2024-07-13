#!/bin/bash
#! chmod +x run_topaz.sh
#! ./run_topaz.sh name_of_dataset

# next lines is for Bruno enivronment
# module load cudnn/8.9.7.29_cuda12 cuda/12.0.0_525.60.13
# ml anaconda/latest; 
# conda activate /hpc/projects/group.czii/phil.smoot/phil_topaz_wrapper/pyTopaz/

if [ $# -ne 1 ]; then
    echo "Usage: $0 config_file"
    exit 1
fi

# Assign the parameter to a variable
CONFIG_FILE=$1

echo
echo Running Topaz Commands with $CONFIG_FILE
echo

date; step_start_time=`date +%s`

python3 topaz_run.py $CONFIG_FILE

echo
echo End Run Topaz Commmands
date; step_end_time=`date +%s`

echo execution time was `expr $step_end_time - $step_start_time` s.

