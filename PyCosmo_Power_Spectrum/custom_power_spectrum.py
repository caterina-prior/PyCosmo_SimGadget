import PyCosmo
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use("pycosmohub")

from Functions.extra_functions import deltanorm
from Functions import pycosmowatermark

from power_spectrum_class import PowerSpectrumClass

import argparse

import os

def main(param_file):
    """
    Main function to run the simulation with the specified parameter file.
    :param param_file: Path to the parameter file
    """
    # Get the relative path to the .param file
    param_file_path = os.path.join("ngenic/parameterfiles", param_file)
    
    # Check if the file exists
    if not os.path.isfile(param_file_path):
        print(f"Error: The file '{param_file_path}' does not exist!")
        return

    # Your simulation code here

    print(f"Using parameter file: {param_file}")

    # Logic to load and process the .param file
    parameters = read_param_file(param_file_path)
    for key, value in parameters.items():
        print(f"{key}: {value}")

# Import variables defined in input_parameters.param
if __name__ == "__main__":
    

    parser = argparse.ArgumentParser(description="Run the simulation with a specified parameter file.")
    parser.add_argument(
        'param_file',
        type=str,
        help="Path to the .param file to be used for the simulation"
    )
    args = parser.parse_args()
    main(args.param_file)

# PyCosmo instance
cosmo = PyCosmo.build()

