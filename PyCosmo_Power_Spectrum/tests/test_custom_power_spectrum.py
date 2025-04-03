import unittest
from PyCosmo_Power_Spectrum import power_spectrum_class
from power_spectrum_class import PowerSpectrumClass

import matplotlib.pyplot as plt

class TestPowerSpectrumClass(unittest.TestCase):
    def setUp(self):
        # Example parameters for initializing the PowerSpectrumClass
        self.parameters = {
            "Box": 100.0,
            "Nsample": 64,
            "Redshift": 0.0,
            "Omega": 0.3,
            "OmegaLambda": 0.7,
            "OmegaB": 0.05,
            "HubbleParam": 0.7,
            "Sigma8": 0.8,
            "NonLinearFitingFunction": "halofit",
            "LinearFitingFunction": "eisenstein_hu",
            "UnitLength_in_cm": 3.085677581e24,
            "UnitMass_in_g": 1.989e43,
            "UnitVelocity_in_cm_per_s": 1e5,
        }
        self.ps_class = PowerSpectrumClass(self.parameters)
        self.ps_class.pk_lin = [1, 2, 3]  # Mock linear power spectrum
        self.ps_class.pk_nonlin = [1, 4, 9]  # Mock non-linear power spectrum
        self.ps_class.k_values = [0.1, 0.2, 0.3]  # Mock k values

    def test_plot_power_spectrum(self):
        # Test if the plot_power_spectrum method runs without errors
        try:
            self.ps_class.plot_power_spectrum()
            plt.close('all')  # Close the plot to avoid resource warnings
        except Exception as e:
            self.fail(f"plot_power_spectrum raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()