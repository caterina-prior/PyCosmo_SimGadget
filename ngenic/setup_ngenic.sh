#!/bin/bash
# Activate N-GenIC virtual environment and load GSL 2.7.1 + FFTW

# Define the virtual environment path
VENV_DIR="$(pwd)/venv_ngenic"

# Set paths
export FFTW_DIR=$HOME/fftw2_mpi
export GSL_DIR=/cluster/project/.../gsl-2.7.1  # or leave unset if not needed here

# Set up library and executable paths
export LD_LIBRARY_PATH=$FFTW_DIR/lib:$GSL_DIR/lib:$LD_LIBRARY_PATH
export PATH=$FFTW_DIR/bin:$PATH

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "[setup_ngenic.sh] Creating N-GenIC virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

echo "[setup_ngenic.sh] N-GenIC environment activated with GSL 2.7.1 and FFTW."
