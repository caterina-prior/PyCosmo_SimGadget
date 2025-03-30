To run the simulation with a custom .param file, use the following command:​

`make PARAM_FILE=custom.param run`

If no PARAM_FILE is specified, make will use lsf_32.param as defined in the Makefile

The following input parameters are not required for the generation of an initial matter power spectrum using PyCosmo: 

* Nmesh: the size of the FFT grid used to compute the displacement field.
* GlassFile: File with unperturbed glass or Cartesian grid
* TileFac: Number of times the glass file is tiled in each dimension
* SphereMode: determines the selection of modes in Fourier space when generating the initial density field
* ShapeGamma: only needed for Efstathiou power spectrum , not avialable in by Pycosmo
* PrimordialIndex: used to tilt the primordial index
* NumFilesWrittenInParallel: not relevant to the generation of the initial power spectrum