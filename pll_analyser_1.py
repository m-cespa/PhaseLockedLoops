import csv
import os
import math
import statistics  # For calculating the median

def read_csv_column_from_directory(directory_path, column_index):
    column_data = []

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a CSV file
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            # Open the CSV file
            with open(file_path, 'r') as file:
                reader = csv.reader(file)

                # Skip the header row
                next(reader)

                # Iterate through the remaining rows
                for row in reader:
                    # Append the column value to the list, ensuring it's an integer
                    column_data.append(int(row[column_index]))

    return column_data

def detect_transitions(csv_column):
    transitions = []
    
    # Start checking from the second value since we compare with the previous one
    for i in range(1, len(csv_column)):
        prev_value = csv_column[i - 1]
        current_value = csv_column[i]
        
        if prev_value == 0 and current_value == 1:
            transitions.append((i, 1))  # Transition from 0 to 1
        elif prev_value == 1 and current_value == 0:
            transitions.append((i, -1))  # Transition from 1 to 0

    return transitions

def average_and_sd_transition_diff(transitions, transition_type):
    differences = []
    start_index = None
    
    # Define what to look for based on transition type
    if transition_type == 'up':
        start_transition = 1
        end_transition = -1
    elif transition_type == 'down':
        start_transition = -1
        end_transition = 1
    else:
        raise ValueError("Invalid transition type. Use 'up' or 'down'.")
    
    # Loop through the list of transitions to compute the differences
    for row, transition in transitions:
        if transition == start_transition:
            start_index = row  # Store the row index for the start transition
        elif transition == end_transition and start_index is not None:
            # Compute the difference when the end transition is found
            differences.append(row - start_index)
            start_index = None  # Reset for the next cycle
    
    # If no differences were found, return None
    if not differences:
        return None, None

    # Calculate the median
    median_diff = statistics.median(differences)
    
    # Filter differences to remove points more than 50 from the median
    filtered_differences = [d for d in differences if abs(d - median_diff) <= 50]
    
    # If no filtered differences remain, return None
    if not filtered_differences:
        return None, None

    # Calculate the average of filtered differences
    avg_diff = sum(filtered_differences) / len(filtered_differences)
    
    # Calculate the standard deviation of filtered differences
    variance = sum((x - avg_diff) ** 2 for x in filtered_differences) / len(filtered_differences)
    sd_diff = math.sqrt(variance)
    
    return avg_diff, sd_diff

# Main script to analyze CSV files in all folders in the current directory
base_directory = os.getcwd()  # Get the current working directory

# Arrays to store the means and standard deviations for each folder
means_up = []
sds_up = []
means_down = []
sds_down = []

# Iterate through all items in the base directory
for item in os.listdir(base_directory):
    folder_path = os.path.join(base_directory, item)
    
    if os.path.isdir(folder_path):  # Check if the item is a directory
        print(f"Analyzing folder: {folder_path}")
        
        column_index = 1  # Assuming the data is in the second column (index 1)

        # Read data from all CSV files in the specified directory
        csv_column = read_csv_column_from_directory(folder_path, column_index)

        # Detect transitions in the read column data
        transitions = detect_transitions(csv_column)

        # Calculate average and standard deviation for up transitions
        avg_up_diff, sd_up_diff = average_and_sd_transition_diff(transitions, 'up')
        means_up.append(avg_up_diff)  # Store the average in the means array
        sds_up.append(sd_up_diff)      # Store the standard deviation in the SD array
        

        # Calculate average and standard deviation for down transitions
        avg_down_diff, sd_down_diff = average_and_sd_transition_diff(transitions, 'down')
        means_down.append(avg_down_diff)  # Store the average in the means array
        sds_down.append(sd_down_diff)      # Store the standard deviation in the SD array
        
  

# Final output
print("\nMeans for Up Transitions:", means_up)
print("Standard Deviations for Up Transitions:", sds_up)
print("Means for Down Transitions:", means_down)
print("Standard Deviations for Down Transitions:", sds_down)
