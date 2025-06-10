#!/bin/bash
# Activate PyCosmo virtual environment and load GSL 2.8

# Define the virtual environment path (relative to this script's location)
VENV_DIR="$(pwd)/venv"

# GSL 2.8 absolute path (modify if needed)
export GSL_DIR=/cluster/software/stacks/2024-06/spack/opt/spack/linux-ubuntu22.04-x86_64_v3/gcc-12.2.0/gsl-2.8-*/lib

# Export library paths
export LD_LIBRARY_PATH=$GSL_DIR:$LD_LIBRARY_PATH

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "[setup_pycosmo.sh] Creating PyCosmo virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

echo "[setup_pycosmo.sh] PyCosmo environment activated with GSL 2.8."
