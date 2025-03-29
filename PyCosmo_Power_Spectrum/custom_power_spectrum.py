import PyCosmo
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use("pycosmohub")

from Functions.extra_functions import deltanorm
from Functions import pycosmowatermark

from power_spectrum_class import PowerSpectrumClass

# Import variables defined in input_parameters.param
if __name__ == "__main__":
    param_file_path = "ngenic/parameterfiles/lsf_16.param"
    parameters = read_param_file(param_file_path)
    for key, value in parameters.items():
        print(f"{key}: {value}")

# PyCosmo instance
cosmo = PyCosmo.build()

