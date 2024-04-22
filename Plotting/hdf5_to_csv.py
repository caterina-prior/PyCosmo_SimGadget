import sys
sys.path.append('/psi/home/crazzo_b/libpy')
#print(sys.path)
import numpy as np
import h5py

folder = "../Results/lsf_small"

f = h5py.File(folder + "/snapshot_000.hdf5", 'r')
print(f['Header'])
data_all = f['PartType1'] # [u'Acceleration', u'Coordinates', u'ParticleIDs', u'Potential', u'Velocities']
print(data_all.keys())
Data = []

DataID = np.asarray([data_all['ParticleIDs']]).T
DataR = np.asarray(data_all['Coordinates'])
DataV = np.asarray(data_all['Velocities'])
data = np.concatenate((DataID, DataR, DataV), axis = 1)

f.close()

print("reading in done")
print("data size ", len(DataID[:,0]))
np.savetxt(folder + "/Data.csv", data, delimiter= ", ")

'''
import matplotlib.animation as animation
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.figure()
plt.plot(DataID)
plt.savefig(folder + "/ID.png")

plt.figure()
plt.plot(DataR[:,0], label = "x")
plt.plot(DataR[:,1], label = "y")
plt.plot(DataID[:,0], DataR[:,0], label = "x id")
plt.legend()
plt.savefig(folder + "/Pos.png")


plt.figure()
plt.hist(DataR[:,0], label = "x", histtype='step', bins = 100)
plt.hist(DataR[:,1], label = "y", histtype='step', bins = 100)
plt.hist(DataR[:,2], label = "z", histtype='step', bins = 100)
plt.legend()
plt.savefig(folder + "/PosHist.png")


#plt.figure()
#plt.plot(DataID)
#plt.savefig(folder + "/Vel.png")


'''



