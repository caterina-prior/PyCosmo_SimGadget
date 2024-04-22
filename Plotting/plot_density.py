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

#folder = "../Results/lcdm_gas"
folder = "/psi/home/crazzo_b/SimGadget/Results/lsf_big"
filetype = "hdf5"
i = 0
if(filetype == "hdf5"):
    f = h5py.File(folder + f"/snapshot_{i:03d}.hdf5", 'r')
    data_all = f['PartType1']
    data = np.asarray(data_all['Coordinates'])
    f.close()
    
elif(filetype == "csv"):
    filename = folder + f"/snapshot{i:03d}.csv"
    data = np.loadtxt(filename, delimiter=',', dtype=float, usecols = (1,2,3))

else:
    print("no known datatype")

 
print(data.shape)

plt.figure()
plt.hist2d(data[:, 0], data[:, 1], bins = 1000)

plt.savefig(folder + "/initial_dens.png")
#ani.save(folder + "/dens_animation_lsf_small.gif", writer = writer)
 


