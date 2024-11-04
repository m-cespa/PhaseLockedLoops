import numpy as np

# # Load the CSV files
# comp_df = np.genfromtxt('rising_falling_out_comp.csv', delimiter=',', skip_header=True, dtype=int)
# sig_df = np.genfromtxt('rising_falling_out_sig.csv', delimiter=',', skip_header=True, dtype=int)

# # Extract the relevant columns
# out_data = comp_df[:, 0]
# comp = comp_df[:, 1]
# sig = sig_df[:, 1]

# # Stack the data as columns and create a merged array
# merged = np.column_stack((out_data, comp, sig))

# # Save the merged array to a new CSV file
# np.savetxt('Rising_Falling_PC2.csv', merged, delimiter=',', header='OUT,COMP,SIG', comments='', fmt='%s')

# print("Files merged successfully and saved as 'merged_output.csv'.")

import matplotlib.pyplot as plt

# Load the CSV file
data = np.genfromtxt('Rising_Falling_PC2.csv', delimiter=',', skip_header=True)

# Extract columns (limited to the first 500 rows)
out = data[:500, 0]
comp = data[:500, 1]
sig = data[:500, 2]
indices = np.arange(out.shape[0])

# Create and save the first plot for COMP and SIG
plt.figure(figsize=(12, 6))
plt.plot(indices, comp, label='COMP', color='orange', linewidth=1)
plt.plot(indices, sig, label='SIG', color='green', linewidth=1)
plt.title('SIG & COMP Signals')
plt.xlabel('Timestamps (41micro_s)')
plt.ylabel('Logic Signal')
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.savefig('COMP_SIG_Rising_Falling.png', dpi=300)
plt.close()  # Close the figure to avoid overlap

# Create and save the second plot for OUT
plt.figure(figsize=(12, 6))
plt.plot(indices, out, label='OUT', color='blue', linewidth=1)
plt.title('OUTPUT SIgnal')
plt.xlabel('Timestamps (41micro_s)')
plt.ylabel('3 Level Signal')
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.savefig('OUT_Rising_Falling.png', dpi=300)
plt.close()  # Close the figure to avoid overlap

print("Plots saved as 'COMP_SIG_Rising_Falling.png' and 'OUT_Rising_Falling.png'.")





