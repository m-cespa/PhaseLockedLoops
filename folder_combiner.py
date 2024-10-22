import pandas as pd
import os
import shutil  # Import shutil for directory deletion

# Get the current working directory
base_dir = os.getcwd()

# Keep track of folders to delete later
folders_to_delete = []

for i in range(0, 600, 100):
    in_folder = f'in_1000_{i}'
    out_folder = f'out_1000_{i}'
    output_folder = f'In_out_1000_{i}'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Add the input and output folders to the list for deletion
    folders_to_delete.append((in_folder, out_folder))

    for j in range(1, 6):  # Assuming there are 5 CSVs in each folder
        in_file = os.path.join(base_dir, in_folder, f'iteration={j}.csv')
        out_file = os.path.join(base_dir, out_folder, f'iteration={j}.csv')

        # Check if files exist before processing
        if not os.path.exists(in_file) or not os.path.exists(out_file):
            print(f"File not found: {in_file} or {out_file}. Skipping...")
            continue

        try:
            # Read the CSV files
            in_df = pd.read_csv(in_file)
            out_df = pd.read_csv(out_file)

            # Create the new DataFrame with the specified columns
            result_df = pd.DataFrame({
                'input1': in_df['V_A'],  # Column 1: V_A from in_df
                'input2': out_df['V_A'],  # Column 2: V_A from out_df
                'output': in_df['V_B']    # Column 3: V_B from in_df
            })

            # Save the new DataFrame to a new CSV
            result_df.to_csv(os.path.join(output_folder, f'result_file_{j}.csv'), index=False)

            print(f"Processed: {in_file} and {out_file} -> {output_folder}/result_file_{j}.csv")
        except Exception as e:
            print(f"Error processing files {in_file} and {out_file}: {e}")

# # Delete the input and output folders after all processing is complete
# for in_folder, out_folder in folders_to_delete:
#     try:
#         shutil.rmtree(in_folder)
#         shutil.rmtree(out_folder)
#         print(f"Deleted folders: {in_folder} and {out_folder}")
#     except Exception as e:
#         print(f"Error deleting folders {in_folder} or {out_folder}: {e}")

print("Processing complete!")
