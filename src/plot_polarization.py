import pandas as pd
import matplotlib.pyplot as plt
import argparse

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

        # Calculate Current Density
        df['Current Density (A/cm²)'] = df['FC_A (A)'] / active_area

        # Create the plot
        fig, ax = plt.subplots()
        ax.plot(df['Current Density (A/cm²)'], df['FC_V (V)'], marker='o', linestyle='-')
        ax.set_xlabel("Current Density (A/cm²)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title("Polarization Curve")
        ax.grid(True)

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
    parser = argparse.ArgumentParser(description="Generate a polarization curve from fuel cell data.")
    parser.add_argument(
        '--file', 
        type=str, 
        default='data/V2.5.6-3-2303-18-A.csv', 
        help='Path to the input CSV file.'
    )
    parser.add_argument(
        '--area', 
        type=float, 
        default=100.0, 
        help='Active area of the fuel cell in cm².'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='polarization_curve.png', 
        help='Path to save the output plot image.'
    )
    
    args = parser.parse_args()
    
    plot_polarization_curve(args.file, args.area, args.output)