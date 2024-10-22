import pandas as pd
import matplotlib.pyplot as plt
import os

# Get the current working directory
base_dir = os.getcwd()

# Find the only CSV file in the directory
csv_files = [f for f in os.listdir(base_dir) if f.endswith('.csv')]
if len(csv_files) != 1:
    raise FileNotFoundError("There should be exactly one CSV file in the directory.")

# Read the CSV file
csv_file = csv_files[0]
data = pd.read_csv(csv_file)

# Limit to the first 500 rows
data_subset = data.head(500)

# Create plots
plt.figure(figsize=(14, 6))

# Plot for the first two columns
plt.subplot(1, 2, 1)
plt.plot(data_subset.index, data_subset.iloc[:, 0], label=data.columns[0], marker='o')
plt.plot(data_subset.index, data_subset.iloc[:, 1], label=data.columns[1], marker='o')
plt.title('First Two Columns vs Row Index (First 500 Points)')
plt.xlabel('Row Index')
plt.ylabel('Values')
plt.legend()
plt.grid()

# Plot for the third column
plt.subplot(1, 2, 2)
plt.plot(data_subset.index, data_subset.iloc[:, 2], label=data.columns[2], color='orange', marker='o')
plt.title('Third Column vs Row Index (First 500 Points)')
plt.xlabel('Row Index')
plt.ylabel('Values')
plt.legend()
plt.grid()

# Show the plots
plt.tight_layout()
plt.savefig('plots.png')  # Optional: Save the plot as a PNG file
plt.show()
