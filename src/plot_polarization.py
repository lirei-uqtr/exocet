import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_polarization_curve(csv_file, active_area, output_file):
    """
    Generates and saves a polarization curve plot from a CSV file.

    Args:
        csv_file (str): Path to the input CSV file.
        active_area (float): Active area of the fuel cell in cm².
        output_file (str): Path to save the output plot image.
    """
    try:
        df = pd.read_csv(csv_file)
        
        # Clean up column names by stripping whitespace
        df.columns = df.columns.str.strip()

        # Create the plot
        fig, ax = plt.subplots()
        ax.scatter(df['FC_A (A)'], df['FC_V (V)'])
        ax.set_xlabel("Current (A)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title("Polarization Curve")
        ax.grid(True)

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Save the plot
        plt.savefig(output_file)
        print(f"Plot saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except KeyError as e:
        print(f"Error: A required column was not found in the CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define default parameters
    csv_file = 'data/V2.5.6-3-2303-18-A-2.csv'
    active_area = 1
    output_file = 'data/figures/polarization_curve.png'
    
    plot_polarization_curve(csv_file, active_area, output_file)