#!/bin/bash
# Activate PyCosmo virtual environment and load GSL 2.8

# GSL 2.8 absolute path (modify if needed)
export GSL_DIR=/cluster/software/stacks/2024-06/spack/opt/spack/linux-ubuntu22.04-x86_64_v3/gcc-12.2.0/gsl-2.8-*/lib
export LD_LIBRARY_PATH=$GSL_DIR:$LD_LIBRARY_PATH

# Activate virtual environment
source venv/bin/activate

echo "[setup_pycosmo.sh] PyCosmo environment activated with GSL 2.8."
