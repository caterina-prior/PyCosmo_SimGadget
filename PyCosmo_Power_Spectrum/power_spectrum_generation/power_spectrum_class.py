import os, sys
import PyCosmo
import numpy as np
import matplotlib.pyplot as plt

# Set up relative imports
current_file_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(current_file_path))
sys.path.insert(0, base_dir)  # Adds base_dir to Python path

# Use matplotlib style
style_path = os.path.join(base_dir, "pycosmo_plotting", "pycosmohub.mplstyle")
plt.style.use(style_path)

class PowerSpectrumClass:
   
    def __init__(self, parameters):
        """
        Initialize the PowerSpectrumClass with a parameter file.
        
        :param param_file: dictionary containing cosmological parameters
        """
        self.param_dictionary = parameters # Store the parameter as a dictionary
        self.cosmo = PyCosmo.build() # Initialize the PyCosmo object
        
        self.box_size = float(parameters["Box"])  # Box size in Mpc/h
        self.Nsample = int(parameters["Nsample"]) # Get the number of samples in the simulation

        self.z_start = float(parameters["Redshift"]) # Get the starting redshift

        # Calculate and store the appropriate range of k values to use in the simulation
        self.k_count = int(self.Nsample)**3 # Number of k values to sample

        self.unitlength_in_cm = float(parameters["UnitLength_in_cm"]) # Get the unit length in cm
        self.unitmass_in_g = float(parameters["UnitMass_in_g"]) # Get the unit mass in g   
        self.unitvelocity_in_cm_per_s = float(parameters["UnitVelocity_in_cm_per_s"]) # Get the unit velocity in cm/s

        self.kmin = 2 * np.pi / (1000.0 * (3.085678e24 / self.unitlength_in_cm)) # Minimum k value in Mpc/h
        self.nyquist = self.box_size * 2 * np.pi / (0.001 * (3.085678e24 / self.unitlength_in_cm)) # Nyquist frequency in Mpc/h

        # Ensure kmin and nyquist are valid to avoid invalid values in k_values        
        if self.kmin <= 0 or self.nyquist <= 0:
            raise ValueError("Invalid kmin or nyquist values. Ensure Box and Nsample are positive.")
        
        self.k_values = np.linspace(np.log10(self.kmin), np.log10(self.nyquist), self.k_count)

        print(f"Using k values from {self.kmin:.2e} to {self.nyquist:.2e} with {self.k_count} samples")
    
        # Set the type of linear fitting function
        if int(parameters["LinearFittingFunction"]) == 0:
            print("Using Eisenstein & Hu linear fitting function")
            self.cosmo.set(pk_type="EH") # Set the linear fitting function to Eisenstein & Hu
        elif int(parameters["LinearFittingFunction"]) == 1:
            print("Using Bardeen, Bond, Kaiser & Szalay linear fitting function")
            self.cosmo.set(pk_type="BBKS") # Set the linear fitting function to BBKS
        else:
            print("Using Boltzmann linear fitting function")
            self.cosmo.set(pk_type="boltz")

        # Set the type of non-linear fitting function
        if int(parameters["NonLinearFittingFunction"]) == 0:
            print("Using Halofit non-linear fitting function")
            self.cosmo.set(pk_nonlin_type="halofit")
        elif int(parameters["NonLinearFittingFunction"]) == 1:
            print("Using Takahashi non-linear fitting function")
            self.cosmo.set(pk_nonlin_type="rev_halofit")
        else:
            print("Using Mead non-linear fitting function")
            self.cosmo.set(pk_nonlin_type="mead")

        self.cosmo.set(omega_m=float(parameters["Omega"]), # Set the matter density parameter
                       omega_l=float(parameters["OmegaLambda"]), # Set the dark energy density parameter
                       omega_b=float(parameters["OmegaBaryon"]), # Set the baryon density parameter
                       h=float(parameters["HubbleParam"]), # Set the Hubble parameter
                       pk_norm_type="sigma8", # Set the normalization type to use sigma 8
                       pk_norm= float(parameters["Sigma8"]), # Set the amplitude of the power spectrum
                       )

        self.pk_lin = None # Linear power spectrum not yet initialized
        self.pk_nonlin = None # Non-linear power spectrum not yet initialized
    
    def compute_power_spectra(self):
        """
        Compute the power spectrum using the specified fitting functions."""
        assert np.all(np.isfinite(self.k_values)), "k_values must be finite"

        a = 1. / (1 + self.z_start)

        print(f"Computing power spectra at redshift z={self.z_start} (a={a})")

        if self.cosmo.lin_pert is not None:
            print("Calling linear power spectrum...")
            try:
                result = self.cosmo.lin_pert.powerspec_a_k(a, 10**(self.k_values))
                print("Returned from linear power spectrum")
                self.pk_lin = result[:, 0]
            except Exception as e:
                print(f"Error in linear powerspec: {e}")
                raise
        else:
            print("WARNING: Linear power spectrum is not available at this redshift or model. Skipping.")
            self.pk_lin = None

        if self.cosmo.nonlin_pert is not None:
            print("Calling non-linear power spectrum...")
            try:
                result = self.cosmo.nonlin_pert.powerspec_a_k(a, 10**(self.k_values))
                print("Returned from non-linear power spectrum")
                self.pk_nonlin = result[:, 0]
                print("NONLINEAR POWER SPECTRUM DONE")
            except Exception as e:
                print(f"Error in non-linear powerspec: {e}")
                raise
        else:
            print("WARNING: Non-linear power spectrum is not available at this redshift or model. Skipping.")
            self.pk_nonlin = None
        
    def plot_power_spectrum(self):
        """
        Plot the power spectrum.
        """   
        plt.figure(figsize=(15.5, 5.5))
        ax = plt.gca()

        if self.pk_lin is not None:
            ax.plot(self.k_values, np.log10(self.pk_lin), color='dodgerblue', linewidth=2, label='linear')
        
        if self.pk_nonlin is not None:
            ax.plot(self.k_values, np.log10(self.pk_nonlin), color='magenta', linewidth=2, label='non-linear')
        
        if self.pk_lin is None and self.pk_nonlin is None:
            raise ValueError("No power spectrum data available. Run compute_power_spectra() first.")

        ax.set_xlabel(r'$k \ [Mpc^{-1}]$', fontsize=28)
        ax.set_ylabel(r'$P(k) \ [Mpc^{3}]$', fontsize=28)
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

        print(f"Power spectrum plot saved in: {output_path}")

    def save_power_spectrum_for_ngenic(self, output_path=f"outputted_power_spectrum/input_spectrum.txt"):
        """
        Save the linear power spectrum in N-GenIC-compatible format:
        - Space-separated ASCII file
        - No header
        - Units: k in h/Mpc, P(k) in (Mpc/h)^3
        """
        if self.pk_lin is None:
            raise ValueError("Linear power spectrum not computed. Run compute_power_spectra() first.")

        output_path=f"outputted_power_spectrum/{self.Nsample}_input_spectrum.txt"

        k_h_Mpc = 10**(self.k_values) 

        # Calculate the dimensionless power spectrum
        delta_squared = 4 * np.pi * (k_h_Mpc)**3 * (self.pk_lin)

        log_k = np.log10(k_h_Mpc)

        log_delta_sqrd = np.log10(delta_squared)
        
        data = np.column_stack((log_k, log_delta_sqrd))
        np.savetxt(output_path, data, fmt="%.8e", delimiter=" ")

        print(f"Power spectrum saved in N-GenIC format to: {output_path}")