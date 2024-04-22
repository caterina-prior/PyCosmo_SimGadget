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

folder1 = "/psi/home/crazzo_b/IPPL/ippl/build_serial/alpine/data/lsf_small"
folder2 = "/psi/home/crazzo_b/SimGadget/Results/lsf_small"

i = 3
a0 = 1./64
a = a0 * (np.sqrt(2))**i
print("a = ", a)
saving_name = f"hist_{i}.png"


fig_pos, ax_pos = plt.subplots()
fig_vel, ax_vel = plt.subplots()
fig_acc, ax_acc = plt.subplots()

# Gadget hdf5 file
f = h5py.File(folder2 + f"/snapshot_{i:03d}.hdf5", 'r')
data_all = f['PartType1']
pos = np.asarray(data_all['Coordinates'])
vel = np.asarray(data_all['Velocities']) / np.sqrt(a)
acc = np.asarray(data_all['Acceleration']) 
t = np.asarray(data_all['TimeStep']) 
print(t)
V = np.linalg.norm(vel, axis = 1)
A = np.linalg.norm(acc, axis = 1)
print("Gadget")
f.close()
print(pos.shape)

print("Position")
print("mean pos: ", np.mean(pos[:,0]), np.mean(pos[:,1]), np.mean(pos[:,2]))
print("var pos: ", np.std(pos[:,0]), np.std(pos[:,1]), np.std(pos[:,2]))

print("Velocity")
print("mean velocity: ", np.mean(V))
print("vel dist. ", np.std(V))

print("Acceleration")
print("mean acc: ", np.mean(A))
print("acc dist. ", np.std(A))
print("------------------------")

ax_pos.hist(pos[:,0], bins = 100, alpha = 0.5, label = "gadget", density = True)
ax_vel.hist(V, bins = 100, alpha = 0.5, label = "gadget", density = True)
ax_acc.hist(A, bins = 100, alpha = 0.5, label = "gadget", density = True)


# IPPL csv file
filename = folder1 + f"/snapshot_{i:03d}.csv"
data = np.loadtxt(filename, delimiter=',', dtype=float, usecols = (1,2,3,4,5,6, 7, 8, 9))
pos = data[:,0:3]
vel = data[:,3:6] / (a*a)
acc = data[:,6:9]
V = np.linalg.norm(vel, axis = 1)
A = np.linalg.norm(acc, axis = 1)
print("IPPL")
print(pos.shape)

print("Position")
print("mean pos: ", np.mean(pos[:,0]), np.mean(pos[:,1]), np.mean(pos[:,2]))
print("var pos: ", np.std(pos[:,0]), np.std(pos[:,1]), np.std(pos[:,2]))

print("Velocity")
print("mean velocity: ", np.mean(V))
print("vel dist. ", np.std(V))

print("Acceleration")
print("mean acc: ", np.mean(A))
print("acc dist. ", np.std(A))

ax_pos.hist(pos[:,0], bins = 100, alpha = 0.5, label = "ippl", density = True)
ax_vel.hist(V, bins = 100, alpha = 0.5, label = "ippl", density = True)
ax_acc.hist(A, bins = 100, alpha = 0.5, label = "ippl", density = True)
ax_pos.set_xlabel("comoving pos [kpc/h]")
ax_pos.set_ylabel("number of particles")
ax_vel.set_xlabel("vel [km/s]")
ax_vel.set_ylabel("number of particles")
ax_acc.set_xlabel("acc [h km^2/s^2/kpc]")
ax_acc.set_ylabel("number of particles")
ax_pos.legend()
ax_vel.legend()
ax_acc.legend()

fig_pos.savefig(folder2 + "/pos" + saving_name)
fig_vel.savefig(folder2 +  "/vel" + saving_name)
fig_acc.savefig(folder2 +  "/acc" + saving_name)
print("saved " + folder2 + "/vel" + saving_name)




