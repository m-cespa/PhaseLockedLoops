import os
import pandas as pd
import numpy as np

def calculate_mean_period_of_second_column(folder_path):
    # Loop through all subfolders
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            for file in os.listdir(subfolder_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(subfolder_path, file)
                    
                    # Read the CSV file
                    data = pd.read_csv(file_path, header=None)
                    
                    if data.shape[1] > 1:  # Ensure there is a second column
                        wave = data[1].values  # Get the second column

                        # Interpret 2s as 1s
                        wave = np.where(wave == 2, 1, wave)

                        # Calculate the periods
                        periods = []
                        current_state = wave[0]
                        count = 0

                        for value in wave:
                            if value != current_state:
                                # We have a transition
                                periods.append(count)
                                current_state = value
                                count = 1
                            else:
                                count += 1

                        # Account for the last segment
                        if count > 0:
                            periods.append(count)

                        # Calculate the mean period
                        mean_period = np.mean(periods) if periods else 0
                        print(f"Mean period for {file_path}: {mean_period:.2f} samples")

if __name__ == "__main__":
    folder_path = 'Pc1_closed_loop_output_input,_period=1000'  # Change this to your folder path
    calculate_mean_period_of_second_column(folder_path)














