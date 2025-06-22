#!/bin/bash

set -e

num_proc=30

micromamba run -n SDSD-phyddle phyddle -c phyddle_config_direct.py --num_proc "$num_proc"
