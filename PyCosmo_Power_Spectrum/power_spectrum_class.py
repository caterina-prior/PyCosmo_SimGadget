import PyCosmo
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use("pycosmohub")

from Functions.extra_functions import deltanorm
from Functions import pycosmowatermark

class PowerSpectrumClass:

    def build_pycosmo(self):
        # PyCosmo instance
        cosmo = PyCosmo.build()