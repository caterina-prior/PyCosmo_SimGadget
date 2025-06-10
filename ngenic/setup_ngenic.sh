#!/bin/bash
# Activate N-GenIC virtual environment and load GSL 2.7.1 + FFTW

# Define the virtual environment path
VENV_DIR="$(pwd)/venv_ngenic"

# User can override the base gsl dir for N-GenIC
if [ -n "$GSL_BASE_NGENIC" ]; then
  export GSL_DIR="$GSL_BASE_NGENIC/lib"
# Otherwise, try to find gsl 2.7.1 folder on cluster (using wildcard)
elif GSL_BASE_NGENIC=$(echo /cluster/project/.../gsl-2.7.1*/lib 2>/dev/null | head -n1); then
  export GSL_DIR="$GSL_BASE_NGENIC"
# Fallback to a common local install path if exists
elif [ -d "$HOME/gsl-2.7.1/lib" ]; then
  export GSL_DIR="$HOME/gsl-2.7.1/lib"
else
  echo "ERROR: Could not locate GSL 2.7.1 library directory. Please set GSL_BASE_NGENIC environment variable."
  return 1  # Exit script if sourced
fi


# Set paths
export FFTW_DIR=$HOME/fftw2_mpi

# Set up library and executable paths
export LD_LIBRARY_PATH=$FFTW_DIR/lib:$GSL_DIR/$LD_LIBRARY_PATH
export PATH=$FFTW_DIR/bin:$PATH

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "[setup_ngenic.sh] Creating N-GenIC virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

echo "[setup_ngenic.sh] N-GenIC environment activated with GSL 2.7.1 and FFTW."
