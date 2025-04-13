User needdsto manually install the following compilers:
`sudo apt-get update`
`sudo apt-get install libgsl-dev`
`sudo apt-get install texlive-fonts-recommended texlive-fonts-extra`


To run the simulation with a custom .param file, use the following command:​

`make PARAM_FILE=custom.param run`

If no PARAM_FILE is specified, make will use lsf_32.param as defined in the Makefile
