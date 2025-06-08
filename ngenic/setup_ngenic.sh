#!/bin/bash

export FFTW_DIR=$HOME/fftw2_mpi
export GSL_DIR=/cluster/project/.../gsl-2.7.1  # or leave unset if not needed here

export LD_LIBRARY_PATH=$FFTW_DIR/lib:$LD_LIBRARY_PATH
export PATH=$FFTW_DIR/bin:$PATH

echo "N-GenIC environment loaded (FFTW from $FFTW_DIR)"

