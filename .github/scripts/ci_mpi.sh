#!/bin/bash
module load gcc/9.2.0
module load openmpi/4.0.5-mlnx-gcc
conda activate devito
# git fetch
# git checkout $1
# git pull
pytest tests/test_subdomains.py
