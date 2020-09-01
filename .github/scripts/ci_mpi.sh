#!/bin/bash
module load gcc/9.2.0
module load openmpi/4.0.5-mlnx-gcc
source ~/d/sw/miniconda3/4.8.2/etc/profile.d/conda.sh
conda activate devito
pytest tests/test_subdomains.py
