import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_frequency_and_average_phase(folder_path):
    frequency_phase_pairs = []  # List to store (frequency, phase_average) tuples

    # Loop through all subfolders
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            # Extract the period from the subfolder name
            period_str = subfolder.split('_')[-1]  # Assumes the format is Phase_Input_1000_{period}
            period_us = float(period_str)  # Convert to float (in microseconds)

            # Calculate frequency (in Hz)
            frequency = 1 / (period_us * 1e-6) if period_us > 0 else 0

            phase_sum = 0
            count = 0

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
                        if not phase.isnull().all():
                            # Sum the second column, ignoring NaN values
                            phase_sum += phase.sum()
                            count += phase.notna().sum()  # Count valid (non-NaN) entries

            # Calculate the average phase if count is greater than zero
            phase_average = phase_sum / count if count > 0 else 0

            # Append the frequency and phase average to the list
            frequency_phase_pairs.append((frequency, phase_average))

    # Sort the list of tuples by frequency (first element of the tuple)
    frequency_phase_pairs.sort(key=lambda x: x[0])

    # Unzip the sorted pairs into two lists
    frequencies, phase_averages = zip(*frequency_phase_pairs) if frequency_phase_pairs else ([], [])

    return frequencies, phase_averages

def plot_results(frequencies, phase_averages):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, phase_averages, marker='x', linestyle='-', markersize=4)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Average Phase Shift (µs)')
    plt.grid()
    plt.savefig('Phase_frequency_PC2.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    folder_path = 'Data/Phase_Shift_vs_Frequency/NEW_Phase_Input_pc2_period=1000'  # Set this to your folder path
    frequencies, phase_averages = calculate_frequency_and_average_phase(folder_path)
    plot_results(frequencies, phase_averages)






