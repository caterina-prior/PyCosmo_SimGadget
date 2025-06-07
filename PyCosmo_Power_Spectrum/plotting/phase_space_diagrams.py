import sys
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Add the parent directory to the python path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

def return_integral(series, ax, num_bins):
    """
    Calculate the integral of the histogram of a specified column in a dataset and annotate it on the plot axis.
    """
    # Calculate the integral (area under the histogram)
    counts, bins, _ = ax.hist(series, bins=num_bins)
    bin_width = bins[1] - bins[0]
    integral = counts.sum() * bin_width

    # Annotate the integral value
    ax.text(
        0.95, 0.95,
        f"Integral: {integral:.2f}",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7)
    )
    return integral

def plot_comparison_histograms(ngenic_results, pycosmo_results, column_name, units, titles, filename, num_bins=100):
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    for i, (data, ax, title) in enumerate(zip([ngenic_results, pycosmo_results], axs, titles)):
        ax.hist(data, bins=num_bins, color='blue' if i == 0 else None)
        ax.set_xlabel(rf"${column_name} \ [{units[i]}]$", fontsize=14)
        ax.set_ylabel("Frequency")
        ax.set_title(title)
        ax.grid(True)
        return_integral(pd.DataFrame(data), ax, num_bins)

    plt.tight_layout()
    output_dir = Path("./output_plots")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / filename)
    plt.close(fig)

def plot_phase_space_diagrams(ngenic_results, pycosmo_results, num_bins=100):
    coord_labels = ['x', 'y', 'z']
    vel_labels = ['v_x', 'v_y', 'v_z']

    for i, column_name in enumerate(coord_labels):
        plot_comparison_histograms(
            ngenic_results[column_name],
            pycosmo_results[column_name],
            column_name,
            units=['Mph/h', 'Mph/h'],
            titles=[f"N-GenIC {column_name}-coordinates", f"PyCosmo {column_name}-coordinates"],
            filename=f"{column_name}_coords_phase_space.png",
            num_bins=num_bins
        )

    for i, column_name in enumerate(vel_labels, start=3):
        plot_comparison_histograms(
            ngenic_results[column_name],
            pycosmo_results[column_name],
            column_name,
            units=['cm/s', 'cm/h'],
            titles=[f"N-GenIC {column_name}-values", f"PyCosmo {column_name}-values"],
            filename=f"{column_name}_velocities_phase_space.png",
            num_bins=num_bins
        )

def main(particle_number):
    input_dir = Path("./initial_conditions")
    ngenic_path = input_dir / f"lsf_{particle_number}.csv"
    pycosmo_path = input_dir / f"lsf_pycosmo_{particle_number}.csv"

    if not ngenic_path.exists() or not pycosmo_path.exists():
        raise FileNotFoundError(f"Expected files not found: {ngenic_path}, {pycosmo_path}")

    columns = ["x", "y", "z", "v_x", "v_y", "v_z"]
    ngenic_data = pd.read_csv(ngenic_path, header=None, names=columns)
    pycosmo_data = pd.read_csv(pycosmo_path, header=None, names=columns)
    plot_phase_space_diagrams(ngenic_data, pycosmo_data)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the simulation with a specified number of particles.")
    
    parser.add_argument(
        'particle_number',
        type=str,
        help="The number of particles in the simulation to be graphed"
    )
    
    args = parser.parse_args()

    main(args.particle_number)
