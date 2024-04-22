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

n_max = 13
dt = (64)**(1/n_max)
folder = "/psi/home/crazzo_b/IPPL/ippl/build_serial/alpine/data/lsf_small"
#folder = "/psi/home/crazzo_b/SimGadget/Results/lsf_small"
saving_name = "/dens_animation_2.gif"
filetype = "csv"
#Data = np.array([[]])
stack = []
time = np.zeros(n_max)

if(filetype == "hdf5"):
    time[0] = 1./64
    for i in range(0,n_max):
        f = h5py.File(folder + f"/snapshot_{i:03d}.hdf5", 'r')
        data_all = f['PartType1']
        data = np.asarray(data_all['Coordinates'])
        if (i>0):
            time[i] = np.sqrt(2) * time[i-1]
        f.close()
        
        #Data = np.hstack((Data, data))
        stack.append(data)
    Data = np.stack(stack, axis = 0)
elif(filetype == "csv"):
    for i in range(0,n_max):

        filename = folder + f"/snapshot_{i:03d}.csv"
        data = np.loadtxt(filename, delimiter=',', dtype=float, usecols = (1,2,3))
        time[i] = np.loadtxt(filename, delimiter=',', dtype=float, usecols = 10, max_rows = 1)
        stack.append(data)
    Data = np.stack(stack, axis = 0)
else:
    print("no known datatype")

 
print(Data.shape)


class Plotting:

    def __init__(self, fig, ax, data):
        self.fig = fig
        self.ax = ax
        self.data = data

    def animate(self, n):
        self.ax.clear()
        self.ax.hist2d(self.data[n, :, 0], self.data[n, :, 1], bins = 500, cmap = 'magma')
        self.ax.set_title(f"a = {round(time[n], 4)}, z = {round(1/time[n],4)}")

fig, ax = plt.subplots()

picture = Plotting(fig, ax, Data)
ani = animation.FuncAnimation(fig, picture.animate, frames = n_max, interval = 500)
writer = animation.PillowWriter(fps = 1)
ani.save(folder + saving_name, writer = writer)
print("saved " + folder + saving_name)
 


