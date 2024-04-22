import sys
sys.path.append('/psi/home/crazzo_b/libpy')
#print(sys.path)
import numpy as np
import h5py
import matplotlib.animation as animation
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


# Example usage:
#folder = "../Results/ippl/"
#filename = folder + "Positions.csv"
folder = "/psi/home/crazzo_b/IPPL/ippl/build_serial/alpine/data/"
filename = folder + "snapshot000.csv"
data = np.loadtxt(filename, delimiter=',', dtype=float)

plt.figure()
plt.hist(data[:,1], bins = 100, histtype = 'step')
plt.savefig(folder + "histogram_pos.png")
#print(data.shape)