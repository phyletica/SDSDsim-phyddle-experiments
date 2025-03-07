#!/bin/bash

set -e

num_proc=30


if [ -n "$(command -v conda)" ]
then
    eval "$(conda shell.bash hook)"
    conda activate SDSD-phyddle
fi

phyddle -c phyddle_config.py --num_proc "$num_proc"
