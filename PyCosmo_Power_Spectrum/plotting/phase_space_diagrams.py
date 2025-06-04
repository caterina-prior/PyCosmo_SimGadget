import sys
import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Add the parent directory to the python path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

def return_integral(dataset, dataset_column, plot_axis, num_bins):
    """
    Calculate the integral of the histogram of a specified column in a dataset and annotate it on the plot axis.
    """

    # Calculate the integral (area under the histogram)
    counts, bins, _ = plot_axis.hist(dataset.iloc[:, dataset_column], bins=num_bins)
    bin_width = bins[1] - bins[0]
    integral = counts.sum() * bin_width

    # Annotate the integral value
    plot_axis.text(
        0.95, 0.95,
        f"Integral: {integral:.2f}",
        transform=plot_axis.transAxes,
        fontsize=12,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7)
    )
    return integral


def plot_phase_space_diagrams(ngenic_results, 
                             pycosmo_results, 
                             num_bins=100):
    
    for column in [0, 1, 2]:
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        column_name = ["x", "y", "z"][column]

        axs[0].hist(ngenic_results.iloc[:, column], bins=num_bins, color='blue')
        axs[0].set_xlabel(rf"${column_name} \ [Mph/h]$", fontsize=14)
        axs[0].set_ylabel(r"Frequency")
        axs[0].set_title(f"N-GenIC {column_name}-coordinates")
        axs[0].grid(True)

        return_integral(ngenic_results, column, axs[0], num_bins)

        axs[1].hist(pycosmo_results.iloc[:, column], bins=num_bins)
        axs[1].set_xlabel(rf"${column_name} \ [Mph/h]$", fontsize=14)
        axs[1].set_ylabel(r"Frequency")
        axs[1].set_title(f"PyCosmo {column_name}-coordinates")
        axs[1].grid(True)

        return_integral(pycosmo_results, column, axs[1], num_bins)

        plt.tight_layout()
        output_dir = Path("./output_plots")
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / f"{column_name}_coords_phase_space.png")
        plt.close(fig)

    for column in [3, 4, 5]:
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        column_name = ["v_x", "v_y", "v_z"][column]

        axs[0].hist(ngenic_results.iloc[:, column], bins=num_bins, color='blue')
        axs[0].set_xlabel(rf"${column_name} \ [cm/s]$", fontsize=14)
        axs[0].set_ylabel(r"Frequency")
        axs[0].set_title(f"N-GenIC {column_name}-values")
        axs[0].grid(True)

        return_integral(ngenic_results, column, axs[0], num_bins)

        axs[1].hist(pycosmo_results.iloc[:, column], bins=num_bins)
        axs[1].set_xlabel(rf"${column_name} \ [cm/h]$", fontsize=14)
        axs[1].set_ylabel(r"Frequency")
        axs[1].set_title(f"PyCosmo {column_name}-values")
        axs[1].grid(True)

        return_integral(pycosmo_results, column, axs[1], num_bins)

        plt.tight_layout()
        output_dir = Path("./output_plots")
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / f"{column_name}_velocities_phase_space.png")
        plt.close(fig)
