import PyCosmo
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use("pycosmohub.mplstyle")

from Functions.extra_functions import deltanorm
from Functions import pycosmowatermark


class PowerSpectrumClass:
   
    def __init__(self, parameters):
        """
        Initialize the PowerSpectrumClass with a parameter file.
        
        :param param_file: dictionary containing cosmological parameters
        """
        
        self.param_dictionary = parameters # Store the parameters
        self.cosmo = self.build_pycosmo() # Initialize the PyCosmo object
        
        self.box_size = parameters["Box"]  # Get the periodic box size of the simulation
        self.Nsample = parameters["Nsample"] # Get the number of samples in the simulation

        self.nyquist = self.calculate_nyquist_k() # Calculate the Nyquist frequency
        self.z_start = parameters["Redshift"] # Get the starting redshift

        self.omega_m = parameters["Omega"] # Get total matter density at z = 0
        self.omega_lambda = parameters["OmegaLambda"] # Get dark energy density at z = 0
        self.omega_b = parameters["OmegaB"] # Get baryon density at z = 0
        self.hubble_param = parameters["HubbleParam"] # Get the Hubble parameter at z = 0
        
        self.sigma_8 = parameters["Sigma8"] # Get the amplitude of the power spectrum normalisation

        self.linear_fit_func = None
        self.non_linear_fit_func = None

        self.unitlength_in_cm = parameters["UnitLength_in_cm"] # Get the unit length in cm
        self.unitmass_in_g = parameters["UnitMass_in_g"] # Get the unit mass in g   
        self.unitvelocity_in_cm_per_s = parameters["UnitVelocity_in_cm_per_s"] # Get the unit velocity in cm/s

    @staticmethod
    def calculate_nyquist_k(self):
        """
        Calculate the Nyquist frequency based on the box size.
        
        :return: Nyquist frequency
        """
        return (2 * np.pi / self.box_size) * (self.Nsample / 2)


    def plot_power_spectrum(self):
        """
        Plot the power spectrum.
        """
        # Example data for demonstration purposes
        k_values = np.linspace(0.001, 1, 100)
        z_values = np.linspace(0, 3, 10)
        
        # Generate power spectrum data
        pk_values = self.generate_power_spectrum(k_values, z_values)
        
        # Create a plot
        plt.figure(figsize=(10, 6))
        for i, z in enumerate(z_values):
            plt.plot(k_values, pk_values[i], label=f'z={z:.2f}')
        
        plt.xlabel('k [h/Mpc]')
        plt.ylabel('P(k) [Mpc/h]^3')
        plt.title('Power Spectrum')
        plt.legend()
        plt.grid()
        plt.show()

        