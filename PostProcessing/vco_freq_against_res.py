import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os

# Directory where the CSV files are located
directory_path = 'Resistor_Calibration'  # Folder with the CSV files
file_pattern = os.path.join(directory_path, 'resistor_calib_*.csv')

# Lists to store resistance values and average periods
resistances = []
average_periods = []

# Function to calculate the average period of square waves
def calculate_average_period(signal, timestep_ns=160):
    # Find rising edges (where signal transitions from 0 to 1)
    rising_edges = np.where(np.diff(signal.astype(int)) == 1)[0]
    # Calculate periods between successive rising edges
    periods = np.diff(rising_edges) * timestep_ns  # Convert indices to time in nanoseconds
    if len(periods) > 0:
        return np.mean(periods)  # Average period
    else:
        return 0  # If no edges are found

# Iterate over all matching CSV files
for file_name in glob.glob(file_pattern):
    # Extract resistance value from filename
    match = re.search(r'resistor_calib_(\d+)', file_name)
    if match:
        resistance_value = int(match.group(1))
        resistances.append(resistance_value)

        # Determine the timestep based on resistance values
        if resistance_value in [1000000, 1500000, 2200000, 3300000, 4700000, 6800000]:
            timestep_ns = 1000  # 1 microsecond in nanoseconds
        else:
            timestep_ns = 160  # 160 nanoseconds

        # Load the CSV file, skipping the first row
        data = pd.read_csv(file_name, header=None, skiprows=1)
        signal = data[0].values  # Assuming the signal is in the first column

        # Calculate average period
        avg_period = calculate_average_period(signal, timestep_ns=timestep_ns)
        average_periods.append(avg_period)

# Convert resistances to logarithmic scale
resistances = np.log(resistances)
# average_periods = np.log(average_periods)

# Plotting the average periods against the logarithm of resistances
plt.figure(figsize=(10, 6))
plt.plot(resistances, average_periods, marker='x', linestyle='', color='b', markersize=4)
plt.title('period vs log(R)')
plt.xlabel('log(R) (Ohms)')
plt.ylabel('t (ns)')
plt.grid(True)
plt.savefig('Log_Resistance.png', dpi=300)
plt.show()





