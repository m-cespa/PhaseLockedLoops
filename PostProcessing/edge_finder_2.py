import csv
import os
import statistics
import matplotlib.pyplot as plt

def read_csv_column(directory_path, column_index):
    column_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    column_data.append(float(row[column_index]))  # Use float for averaging
    return column_data

def detect_transitions(csv_column):
    transitions = []
    for i in range(1, len(csv_column)):
        prev_value = csv_column[i - 1]
        current_value = csv_column[i]
        if prev_value == 0 and current_value == 1:
            transitions.append((i, 1))  # Transition from 0 to 1
        elif prev_value == 1 and current_value == 0:
            transitions.append((i, -1))  # Transition from 1 to 0
    return transitions

def average_and_sum_transition_diff(transitions, csv_column):
    differences = []
    start_index = None
    
    for row, transition in transitions:
        if transition == 1:  # Up transition
            start_index = row
        elif transition == -1 and start_index is not None:  # Down transition
            differences.append(row - start_index)
            start_index = None
    
    avg_diff = sum(differences) / len(differences) if differences else 0
    return avg_diff

# Main script to analyze folders
base_directory = os.getcwd()  # Get the current working directory
target_directory = os.path.join(base_directory, 'test_vco_period=1000')

# Check if the target directory exists
if not os.path.exists(target_directory):
    print(f"Directory '{target_directory}' does not exist.")
else:
    x_values = []  # For average of the first column
    y_values = []  # For sum of mean up and down

    for folder_name in os.listdir(target_directory):
        folder_path = os.path.join(target_directory, folder_name)
        
        if os.path.isdir(folder_path):  # Check if the item is a directory
            print(f"Processing folder: {folder_path}")
            avg_first_column = None
            sum_mean_diff = 0

            # Collect data from all CSVs in the folder
            csv_first_column_data = []
            csv_second_column_data = []

            for filename in os.listdir(folder_path):
                if filename.endswith('.csv'):
                    file_path = os.path.join(folder_path, filename)

                    # Read first column
                    first_column = read_csv_column(folder_path, 0)
                    csv_first_column_data.extend(first_column)

                    # Read second column for transition analysis
                    second_column = read_csv_column(folder_path, 1)
                    csv_second_column_data.extend(second_column)

                    # Detect transitions and compute mean up and down
                    transitions = detect_transitions(second_column)
                    mean_diff = average_and_sum_transition_diff(transitions, second_column)
                    sum_mean_diff += mean_diff

            # Calculate averages
            if csv_first_column_data:
                avg_first_column = sum(csv_first_column_data) / len(csv_first_column_data)

            if avg_first_column is not None:
                x_values.append(avg_first_column)
                y_values.append(sum_mean_diff)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, color='blue')
    plt.title('Average of First Column vs. Sum of Transition Differences')
    plt.xlabel('Average of First Column')
    plt.ylabel('Sum of Transition Differences')
    plt.grid()
    plt.show()
