import pandas as pd
import glob
import os

def check_ranges():
    # Use the same default files as in plot_polarization.py to verify specific behavior,
    # but also check all files to see the broader context if needed.
    # For now, let's grab all CSVs in data/ as implied by "each csv files".
    csv_files = glob.glob('data/*.csv')
    csv_files.sort()
    
    print(f"{'File':<40} | {'Min Current (A)':<15} | {'Max Current (A)':<15} | {'Row Count':<10}")
    print("-" * 90)
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            # Strip whitespace from columns as done in plot_polarization.py
            df.columns = df.columns.str.strip()
            
            if 'FC_A (A)' in df.columns:
                # Coerce to numeric, turning errors like 'XX.X' into NaN
                df['FC_A (A)'] = pd.to_numeric(df['FC_A (A)'], errors='coerce')
                
                min_current = df['FC_A (A)'].min()
                max_current = df['FC_A (A)'].max()
                count = len(df)
                
                # Check for NaNs which indicate bad data was dropped/converted
                nan_count = df['FC_A (A)'].isna().sum()
                
                print(f"{os.path.basename(csv_file):<40} | {min_current:<15.4f} | {max_current:<15.4f} | {count:<10} (NaNs: {nan_count})")
            else:
                print(f"{os.path.basename(csv_file):<40} | {'N/A':<15} | {'N/A':<15} | {'0':<10} (Column not found)")
        except Exception as e:
            print(f"{os.path.basename(csv_file):<40} | Error: {e}")

if __name__ == "__main__":
    check_ranges()