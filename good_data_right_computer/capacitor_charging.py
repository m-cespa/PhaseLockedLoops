import numpy as np
import matplotlib.pyplot as plt

# Load the data (assuming the voltage data is in the second column)
data = np.genfromtxt('inner_capacitor_charging.csv', skip_header=True, delimiter=',')[809:1090, 1]
print(data)
# Calculate the natural logarithm of the data
log_data = np.log(1 -data/2.5)

# Create an array for the row indices
row_indices = np.arange(len(log_data))

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(row_indices, log_data, marker='x', linestyle='', color='b', label='ln(Voltage)')
plt.title('Natural Logarithm of Capacitor Voltage vs. Row Index')
plt.xlabel('Row Index')
plt.ylabel('ln(Voltage)')
plt.legend()
plt.grid()
plt.show()
