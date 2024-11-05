import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calc_period(signal):
    transitions = np.where(np.diff(signal) != 0)[0]
    periods = np.diff(transitions) * 2
    return periods

main_dir = 'test_vco_period=1000'
out = []
time_period = 160e-9  # Time period in seconds

for subfolder in os.listdir(main_dir):
    subfolder_path = os.path.join(main_dir, subfolder)

    if os.path.isdir(subfolder_path) and subfolder.startswith('test_vco_1000_'):
        voltages = []
        periods = []

        for file in os.listdir(subfolder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(subfolder_path, file)
                data = pd.read_csv(file_path)

                voltages.append(data.iloc[:, 0].mean())
                periods.extend(calc_period(data.iloc[:, 1].values))  # Extend to include all periods

        avg_voltage = np.mean(voltages)
        voltage_std_dev = np.std(voltages)  # Calculate standard deviation for voltages
        N = len(periods)

        # Scale periods and calculate average and standard deviation
        scaled_periods = np.array(periods) * time_period
        avg_period = np.mean(scaled_periods)
        std_dev_period = np.std(scaled_periods)

        # Calculate frequency in Hz and convert to MHz
        frequency = (1 / avg_period) / 1e3 if avg_period != 0 else 0  # Convert to MHz
        
        # Apply central limit theorem for error in frequency
        frequency_error = (std_dev_period / (avg_period**2 * np.sqrt(N))) / 1e3 if avg_period != 0 else 0  # Convert to MHz
        
        # Apply central limit theorem for error in voltage
        voltage_error = voltage_std_dev / np.sqrt(len(voltages))  # Standard error for voltage

        out.append((avg_voltage, frequency, frequency_error, voltage_error))

# Separate voltage, frequency, and error data
x, y, y_err, voltage_err = zip(*out)

# Plot with error bars
plt.figure(figsize=(10, 5))
plt.errorbar(x, y, yerr=y_err, fmt='x', capsize=3, markersize=4, label='Measured Frequency')
plt.errorbar(x, y, xerr=voltage_err, fmt='o', capsize=3, markersize=4, label='Voltage Std Error', color='orange', alpha=0.5)

plt.xlabel("Voltage (V)")
plt.ylabel("Frequency (kHz)")  # Label in MHz
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save and show the plot
plt.savefig('VCO_frequency_voltage_with_error.png', dpi=300)
plt.show()



