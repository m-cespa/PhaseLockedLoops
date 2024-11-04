import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_period(signal):
    transitions = np.where(np.diff(signal) != 0)[0]
    periods = np.diff(transitions)
    return np.mean(periods) if len(periods) > 0 else np.nan

def calculate_mean_difference(data):
    # Calculate the mean of the absolute differences between the first and second columns
    return np.abs(data.iloc[:, 0] - data.iloc[:, 1]).mean()

main_directory = 'PC2_1k_harmonics_below_period=1000'
output_data = []

for subfolder in os.listdir(main_directory):
    subfolder_path = os.path.join(main_directory, subfolder)
    print(f"Processing subfolder: {subfolder}")  # Log subfolder processing
    
    if os.path.isdir(subfolder_path):
        for file in os.listdir(subfolder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(subfolder_path, file)
                try:
                    data = pd.read_csv(file_path)
                    print(f"  Reading file: {file_path}")  # Log file reading
                    
                    # Calculate mean period of the first column
                    mean_period = calculate_period(data.iloc[:, 0].values)
                    # Calculate mean absolute difference between first and second columns
                    mean_diff = calculate_mean_difference(data)

                    print(f"  Mean Period: {mean_period}, Mean Absolute Difference: {mean_diff}")  # Log calculations

                    if not np.isnan(mean_period) and not np.isnan(mean_diff):
                        output_data.append([mean_period , mean_diff])  # Adjust mean_period for seconds
                    else:
                        print(f"  Skipping due to NaN values in {file_path}")

                except Exception as e:
                    print(f"  Error processing {file_path}: {e}")
                    continue

# Convert output data to DataFrame
output_df = pd.DataFrame(output_data, columns=['Mean Period (s)', 'Mean Absolute Difference'])

# Check if output data is empty
if output_df.empty:
    print("No valid data points were collected for plotting.")
else:
    print("Data points collected for plotting:")
    print(output_df)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(output_df['Mean Period (s)'], output_df['Mean Absolute Difference'], marker='o', linestyle='')
plt.title('Mean Absolute Difference vs Mean Period')
plt.xlabel('Mean Period (s)')
plt.ylabel('Mean Absolute Difference')
plt.grid(True)
# plt.savefig('mean_absolute_difference_vs_mean_period.png')  # Save the plot
plt.show()

