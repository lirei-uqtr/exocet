import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from matplotlib.ticker import MaxNLocator

def plot_polarization_curve(csv_files, active_area, output_file):
    """
    Generates and saves a polarization curve plot from one or more CSV files.

    Args:
        csv_files (list of str): Paths to the input CSV files.
        active_area (float): Active area of the fuel cell in cm².
        output_file (str): Path to save the output plot image.
    """
    try:
        all_data = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            df.columns = df.columns.str.strip()
            
            # Convert columns to numeric, coercing errors to NaN
            if 'FC_A (A)' in df.columns:
                df['FC_A (A)'] = pd.to_numeric(df['FC_A (A)'], errors='coerce')
            if 'FC_V (V)' in df.columns:
                df['FC_V (V)'] = pd.to_numeric(df['FC_V (V)'], errors='coerce')
            
            # Drop rows with NaNs in the plotting columns
            df.dropna(subset=['FC_A (A)', 'FC_V (V)'], inplace=True)

            # Filter outliers: voltages < 40
            df = df[df['FC_V (V)'] >= 40]
            
            if not df.empty:
                df['source'] = os.path.basename(csv_file)
                all_data.append(df)
        
        if not all_data:
            print("No valid data found in any CSV file.")
            return

        combined_df = pd.concat(all_data, ignore_index=True)

        fig, ax = plt.subplots()

        # Sort sources to maintain consistent plot order
        sources = sorted(combined_df['source'].unique())
        for source in sources:
            group = combined_df[combined_df['source'] == source]
            ax.scatter(group['FC_A (A)'], group['FC_V (V)'], label=source)

        ax.set_xlabel("Current (A)")
        ax.set_ylabel("Voltage (V)")
        ax.set_ylim(40, 90)
        ax.set_title("Polarization Curve")
        ax.grid(True)
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Save the plot
        plt.savefig(output_file)
        print(f"Plot saved to {output_file}")

    except FileNotFoundError as e:
        print(f"Error: The file {e.filename} was not found.")
    except KeyError as e:
        print(f"Error: A required column was not found in the CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def plot_time_series(csv_file, output_file):
    """
    Generates and saves a time series plot of Current and Voltage from a CSV file.
    """
    try:
        print(f"Processing time series for {csv_file}...")
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip()
        
        # Parse Date-Time. Format example: 11/18/25-15:39:29
        if 'Date-Time' in df.columns:
            df['Date-Time'] = pd.to_datetime(df['Date-Time'], format='%m/%d/%y-%H:%M:%S', errors='coerce')
        else:
            print("Error: 'Date-Time' column not found.")
            return

        # Clean numeric columns
        for col in ['FC_A (A)', 'FC_V (V)']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with NaNs in critical columns
        df.dropna(subset=['Date-Time', 'FC_A (A)', 'FC_V (V)'], inplace=True)

        # Filter outliers: voltages < 40
        df = df[df['FC_V (V)'] >= 40]
        
        if df.empty:
            print("No valid data found after cleaning.")
            return

        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Current (A)', color=color)
        ax1.plot(df['Date-Time'], df['FC_A (A)'], color=color, label='Current')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:red'
        ax2.set_ylabel('Voltage (V)', color=color)
        ax2.plot(df['Date-Time'], df['FC_V (V)'], color=color, label='Voltage')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title(f"Current and Voltage vs Time\n{os.path.basename(csv_file)}")
        fig.tight_layout()
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        plt.savefig(output_file)
        print(f"Time series plot saved to {output_file}")

    except Exception as e:
        print(f"An error occurred in plot_time_series: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Set to True to plot all CSV files in the 'data' directory,
    # or False to plot only the files specified in the 'default_csv_files' list.
    plot_all_files = False
    # --- End Configuration ---

    default_csv_files = [
        'data\V2.5.6-3-2302-17-A-7.csv',
        'data/V2.5.6-3-2303-18-A-2.csv',
        'data/V2.5.6-3-2302-17-A-8.csv',
        'data/V2.5.6-3-2302-17-A-9.csv'
    ]

    if plot_all_files:
        csv_files = glob.glob('data/*.csv')
    else:
        csv_files = default_csv_files

    active_area = 1
    output_file = 'data/figures/polarization_curve.png'
    
    plot_polarization_curve(csv_files, active_area, output_file)

    # Plot time series for specific file
    time_series_file = 'data/V2.5.6-3-2302-17-A-8.csv'
    time_series_output = 'data/figures/current_voltage_time.png'
    if os.path.exists(time_series_file):
        plot_time_series(time_series_file, time_series_output)
    else:
        print(f"File for time series not found: {time_series_file}")