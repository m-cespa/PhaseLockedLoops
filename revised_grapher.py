import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def read_csv_data(file_path):
    """Reads the voltage and logic data from the CSV file."""
    voltage = []
    logic_data = []
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            voltage.append(float(row[0]))  # First column is voltage
            logic_data.append(int(row[1]))  # Second column is logic data (0 or 1)
    
    return voltage, logic_data

def calculate_mean_time_period(logic_data):
    """Calculates the mean time period of the square wave from the logic data."""
    transitions = []
    
    for i in range(1, len(logic_data)):
        if logic_data[i] != logic_data[i - 1]:
            transitions.append(i)

    if len(transitions) < 2:
        return 0

    periods = []
    for i in range(1, len(transitions)):
        periods.append(transitions[i] - transitions[i - 1])

    mean_period = 2 * sum(periods) / len(periods) if periods else 0
    return mean_period

# Main script to analyze folders
base_directory = os.getcwd()
target_directory = os.path.join(base_directory, 'test_vco_period=1000')

voltages = []
avg_time_periods = []

for folder_name in os.listdir(target_directory):
    folder_path = os.path.join(target_directory, folder_name)
    
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_path}")

        time_periods = []

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                temp_volt = []
                file_path = os.path.join(folder_path, file_name)

                voltage_data, logic_data = read_csv_data(file_path)
                if voltage_data:
                    voltage_value = np.mean(voltage_data)
                    time_period = calculate_mean_time_period(logic_data)

                    if time_period > 0:  # Check for valid period
                        temp_volt.append(voltage_value)
                        time_periods.append(time_period)

        if time_periods:
            avg_time_period = sum(time_periods) / len(time_periods)
            avg_time_periods.append(avg_time_period)
            voltages.append(np.mean(temp_volt))

# Debugging prints
print(f"Voltages: {voltages}")
print(f"Average Time Periods: {avg_time_periods}")
print(f"Length of Voltages: {len(voltages)}")
print(f"Length of Average Time Periods: {len(avg_time_periods)}")

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(voltages, avg_time_periods, color='blue')
plt.title('Average Time Period vs. Input Voltage')
plt.xlabel('Input Voltage (V)')
plt.ylabel('Average Time Period (samples)')
plt.grid()
plt.show()

