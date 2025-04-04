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
        self.param_dictionary = parameters # Store the parameter as a dictionary
        self.cosmo = self.build_pycosmo() # Initialize the PyCosmo object
        
        self.box_size = parameters["Box"]  # Get the periodic box size of the simulation
        self.Nsample = parameters["Nsample"] # Get the number of samples in the simulation

        self.z_start = parameters["Redshift"] # Get the starting redshift

        # Calculate and store the appropriate range of k values to use in the simulation 
        self.nyquist = (2 * np.pi / self.box_size) * (self.Nsample / 2) # Calculate the Nyquist frequency
        self.kmin = 2 * np.pi / self.box_size # Calculate the minimum k value
        self.k_values = np.linspace(np.log10(self.kmin), np.log10(self.nyquist), self.Nsample/2) # Store range of k values as a log scale

        self.cosmo.set(omega_m=parameters["Omega"], # Set the matter density parameter
                       omega_lambda=parameters["OmegaLambda"], # Set the dark energy density parameter
                       omega_b=parameters["OmegaB"], # Set the baryon density parameter
                       h=parameters["HubbleParam"], # Set the Hubble parameter
                       sigma_8=parameters["Sigma8"], # Set the amplitude of the power spectrum
                       pk_nonlin_type=parameters["NonLinearFitingFunction"], # Set the non-linear fitting function
                       pk_type=parameters["LinearFitingFunction"], # Set the linear fitting function
                       )

        self.unitlength_in_cm = parameters["UnitLength_in_cm"] # Get the unit length in cm
        self.unitmass_in_g = parameters["UnitMass_in_g"] # Get the unit mass in g   
        self.unitvelocity_in_cm_per_s = parameters["UnitVelocity_in_cm_per_s"] # Get the unit velocity in cm/s

        self.pk_lin = None # Linear power spectrum not yet initialized
        self.pk_nonlin = None # Non-linear power spectrum not yet initialized
    
    @staticmethod
    def compute_power_spectra(self):
        """
        Compute the power spectrum using the specified fitting functions."""
        
        # Calculate the appropriate range of k values to use 
        kmin = 2 * np.pi / self.box_size

        # Compute the linear and non-linear power spectra 
        self.pk_lin = self.cosmo.lin_pert.powerspec_a_k(1./(1+self.z_start), self.k_values)[:,0]
        self.pk_nonlin = self.cosmo.nonlin_pert.powerspec_a_k(1./(1+self.z_start), self.k_values)[:,0]

    def plot_power_spectrum(self):
        """
        Plot the power spectrum.
        """   
        # Create a plot
        plt.figure(figsize=(15.5, 5.5))

        ax = plt.gca()
        ax.loglog(self.k_values, self.pk_lin, color='dodgerblue', linewidth = 2, label = 'linear')
        ax.loglog(self.k_values, self.pk_nonlin, color='magenta', linewidth = 2, label = 'non-linear')
        ax.set_xlabel(r'$k \ [Mpc^{-1}]$', fontsize=28)
        ax.set_ylabel(r'$P(k) \ [Mpc^{3}]$', fontsize=28)
        ax.text(150, 1100, 'z = {:.2f}'.format(self.z_start), fontsize=28, color='black')
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(24) 
            tick.label.set_fontweight('black')
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(24) 
            tick.label.set_fontweight('black')
        plt.legend(loc='best')

        