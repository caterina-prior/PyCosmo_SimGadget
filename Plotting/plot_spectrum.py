import sys
sys.path.append('/psi/home/crazzo_b/libpy')
#print(sys.path)
import numpy as np
import h5py
import matplotlib.animation as animation
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd



folder = "/psi/home/crazzo_b/SimGadget/ngenic/ICs/"
saving_name = "spectrum.png"
spectrum_file = "inputspec_lsf_big.txt"


data = np.loadtxt(folder + spectrum_file, skiprows = 1, usecols = (0,1))
k = data[:,0]
P = data[:,1] / (4*np.pi * k*k*k)

plt.figure()
plt.loglog(k*1000, P, "-o")
plt.xlabel("Wavenumber [h/Mpc]")
plt.ylabel("P(k)")
print(data.shape)
plt.savefig(folder + saving_name)
print("saved at " + folder + saving_name)

