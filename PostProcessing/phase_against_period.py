import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_frequency_and_average_phase(folder_path):
    frequency_phase_pairs = []  # List to store (frequency, phase_average, phase_std_dev) tuples

    # Loop through all subfolders
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            # Extract the period from the subfolder name
            period_str = subfolder.split('_')[-1]  # Assumes the format is Phase_Input_1000_{period}
            period_us = float(period_str)  # Convert to float (in microseconds)

            # Calculate frequency (in Hz)
            frequency = 1 / (period_us * 1e-6) if period_us > 0 else 0

            phase_values = []  # Store all phase values for this frequency

            # Read the CSV files for the three iterations
            for i in range(1, 4):
                file_name = f'iteration={i}.csv'
                file_path = os.path.join(subfolder_path, file_name)
                
                if os.path.exists(file_path):
                    data = pd.read_csv(file_path, header=None)

                    if data.shape[1] > 1:  # Ensure there are two columns
                        # Convert the second column to numeric, coercing errors
                        phase = pd.to_numeric(data[1], errors='coerce')

                        # Check for NaN values and handle them
                        phase_values.extend(phase.dropna().tolist())  # Add valid (non-NaN) entries

            # Calculate average phase and standard deviation if there are valid entries
            if phase_values:
                phase_average = np.mean(phase_values)
                phase_error = (np.std(phase_values) + 1) / np.sqrt(len(phase_values))
            else:
                phase_average = 0
                phase_std_dev = 0

            # Append the frequency, phase average, and phase std dev to the list
            frequency_phase_pairs.append((frequency, phase_average, phase_error))

    # Sort the list of tuples by frequency (first element of the tuple)
    frequency_phase_pairs.sort(key=lambda x: x[0])

    # Unzip the sorted pairs into three lists
    frequencies, phase_averages, phase_errors = zip(*frequency_phase_pairs) if frequency_phase_pairs else ([], [], [])

    return frequencies, phase_averages, phase_errors

def plot_results(frequencies, phase_averages, phase_errors):
    plt.figure(figsize=(10, 6))
    plt.errorbar(frequencies, phase_averages, yerr=phase_errors, fmt='x', capsize=3, markersize=3, label=r"$\text{error} = \frac{\sigma_{\phi}}{\sqrt{N}}$")
    plt.plot(frequencies, phase_averages, linestyle='-', alpha=0.6)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Average Phase Shift (µs)')
    plt.grid()
    plt.legend()
    plt.savefig('Phase_frequency_PC1_errors.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    folder_path = 'Data/Phase_Shift_vs_Frequency/Phase_Input_pc1'  # Set this to your folder path
    frequencies, phase_averages, phase_std_devs = calculate_frequency_and_average_phase(folder_path)
    plot_results(frequencies, phase_averages, phase_std_devs)
