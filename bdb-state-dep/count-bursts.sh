#!/bin/bash

set -e

micromamba run -n SDSD-phyddle python sim_bdb.py --sample-burst-counts > burst-counts.tsv
