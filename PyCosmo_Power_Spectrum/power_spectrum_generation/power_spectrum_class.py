import os, sys
import PyCosmo
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Set up relative imports
current_file_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(current_file_path))
sys.path.insert(0, base_dir)

# Import custom modules
from Functions.extra_functions import deltanorm

# Use matplotlib style
plt.style.use("plotting/pycosmohub.mplstyle")

class PowerSpectrumClass:
   
    def __init__(self, parameters):
        """
        Initialize the PowerSpectrumClass with a parameter file.
        
        :param param_file: dictionary containing cosmological parameters
        """
        self.param_dictionary = parameters # Store the parameter as a dictionary
        self.cosmo = PyCosmo.build() # Initialize the PyCosmo object
        
        self.box_size = float(parameters["Box"])  # Get the periodic box size of the simulation
        self.Nsample = int(parameters["Nsample"]) # Get the number of samples in the simulation

        self.z_start = float(parameters["Redshift"]) # Get the starting redshift

        # Calculate and store the appropriate range of k values to use in the simulation 
        self.nyquist = 100 # float((2 * np.pi / self.box_size) * (self.Nsample / 2)) # Calculate the Nyquist frequency
        self.kmin = float(2 * np.pi / self.box_size) # Calculate the minimum k value
        self.k_count = int(self.Nsample)
        self.k_values = np.linspace(self.kmin, self.nyquist, self.k_count)

        # Set the type of linear fitting function
        if parameters["LinearFittingFunction"] == 0:
            self.cosmo.set(pk_type="EH") # Set the linear fitting function to Eisenstein & Hu
        elif parameters["LinearFittingFunction"] == 1:
            self.cosmo.set(pk_type="BBKS") # Set the linear fitting function to BBKS
        else:
            self.cosmo.set(pk_type="boltz")

        # Set the type of non-linear fitting function
        if parameters["NonLinearFittingFunction"] == 0:
            self.cosmo.set(pk_nonlin_type="halofit")
        elif parameters["NonLinearFittingFunction"] == 1:
            self.cosmo.set(pk_nonlin_type="rev_halofit")
        else:
            self.cosmo.set(pk_nonlin_type="mead")

        self.cosmo.set(omega_m=float(parameters["Omega"]), # Set the matter density parameter
                       omega_l=float(parameters["OmegaLambda"]), # Set the dark energy density parameter
                       omega_b=float(parameters["OmegaBaryon"]), # Set the baryon density parameter
                       h=float(parameters["HubbleParam"]), # Set the Hubble parameter
                       pk_norm_type="sigma8", # Set the normalization type to use sigma 8
                       pk_norm=float(parameters["Sigma8"]), # Set the amplitude of the power spectrum
                       )

        self.unitlength_in_cm = parameters["UnitLength_in_cm"] # Get the unit length in cm
        self.unitmass_in_g = parameters["UnitMass_in_g"] # Get the unit mass in g   
        self.unitvelocity_in_cm_per_s = parameters["UnitVelocity_in_cm_per_s"] # Get the unit velocity in cm/s

        self.pk_lin = None # Linear power spectrum not yet initialized
        self.pk_nonlin = None # Non-linear power spectrum not yet initialized
    
    def compute_power_spectra(self):
        """
        Compute the power spectrum using the specified fitting functions."""
        # Compute the linear and non-linear power spectra 
        self.pk_nonlin = self.cosmo.nonlin_pert.powerspec_a_k(1./(1+self.z_start), self.k_values)[:,0]
        print("NONLINEAR POWER SPECTRUM DONE")
        self.pk_lin = self.cosmo.lin_pert.powerspec_a_k(1./(1+self.z_start), self.k_values)[:,0]
 
    def plot_power_spectrum(self):
        """
        Plot the power spectrum.
        """   
        plt.figure(figsize=(15.5, 5.5))
        ax = plt.gca()

        ax.loglog(self.k_values, self.pk_lin, color='dodgerblue', linewidth=2, label='linear')
        ax.loglog(self.k_values, self.pk_nonlin, color='magenta', linewidth=2, label='non-linear')
        ax.set_xlabel(r'$k \ [Mpc^{-1}]$', fontsize=28)
        ax.set_ylabel(r'$P(k) \ [Mpc^{3}]$', fontsize=28)

        x_text = self.k_values[-1]
        y_text = self.pk_nonlin[-1]
        ax.text(x_text, y_text, r'$z = {:.2f}$'.format(self.z_start), fontsize=28, color='black')

        ax.tick_params(axis='both', which='major', labelsize=24)

        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontweight('bold')

        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontweight('bold')

        # Add a text box to the graph displaying the redshift
        textstr = f'Redshift: z = {self.z_start:.2f}'
        props = dict(boxstyle='round', facecolor='white', alpha=0.8)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=18,
            verticalalignment='top', bbox=props)

        plt.legend(loc='best')

        # Ensure the output directory exists
        output_dir = "output_plots"
        os.makedirs(output_dir, exist_ok=True)

        # Save the plot
        output_path = os.path.join(output_dir, f"{self.Nsample}_power_spectrum_plot.png")
        plt.savefig(output_path, bbox_inches='tight')
