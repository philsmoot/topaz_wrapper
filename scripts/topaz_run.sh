#!/bin/bash
#! chmod +x run_topaz.sh
#! ./run_topaz.sh params.json

ml anaconda/latest 
conda activate /hpc/projects/group.czii/topaz_wrapper/pytopaz

if [ $# -ne 1 ]; then
    echo "Usage: $0 absolute_path_to_config_file"
    exit 1
fi

# Assign the parameter to a variable
CONFIG_FILE=$1

echo
echo Running Topaz Commands with $CONFIG_FILE
echo

date; step_start_time=`date +%s`

topaz_run --file-path $CONFIG_FILE

echo
echo End Run Topaz Commmands
date; step_end_time=`date +%s`

echo execution time was `expr $step_end_time - $step_start_time` s.

