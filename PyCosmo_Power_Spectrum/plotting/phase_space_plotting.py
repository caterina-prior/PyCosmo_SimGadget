import numpy as np
import matplotlib.pyplot as plt

# Load data from file
data = np.loadtxt('PyCosmo_Power_Spectrum/outputted_power_spectrum/output_power_spectrum_ngenic.txt')

# Assuming columns: k, vx
k = data[:, 0]
vx = data[:, 1]

# Phase-space plot: k vs vx
plt.figure(figsize=(8, 6))
plt.scatter(k, vx, marker='o', color='b')
plt.xscale('log')
plt.xlabel(r'$k$ [$h/\mathrm{Mpc}$]')
plt.ylabel(r'$v$ [velocity units]')
plt.title('Phase-Space Diagram: Velocity vs Wavenumber')
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.tight_layout()
plt.savefig("PyCosmo_Power_Spectrum/output_plots/PyCosmo_spectrum_phase_space_velocities.png")