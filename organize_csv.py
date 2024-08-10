import pandas as pd
import os

# Ensure an experiment number is passed as an argument
if len(sys.argv) < 2:
    print("Usage: python script.py <experiment_number>")
    sys.exit(1)

# Get experiment number from command-line arguments
x = sys.argv[1]
root_dir = '/home/locolinux2/FETS2024/final_metrics_LesionWise'
input_csv = os.path.join(root_dir, f'{x}_lesionwise_results.csv')
df = pd.read_csv(input_csv)

# Initialize an empty list to store the rows of the new DataFrame
rows = []

# Group by 'labels' column to iterate over each unique case
grouped = df.groupby('labels')

# Loop through each group and extract the data for WT, TC, and ET
for name, group in grouped:
    # Create a dictionary to store the merged data
    merged_data = {
        'Label': name,
        'LesionWise_DSC_WT': None,
        'LesionWise_DSC_TC': None,
        'LesionWise_DSC_ET': None,
        'LesionWise_HD95_WT': None,
        'LesionWise_HD95_TC': None,
        'LesionWise_HD95_ET': None
    }
    
    # Loop through each row in the group
    for _, row in group.iterrows():
        if row['Labels'] == 'WT':
            merged_data['LesionWise_DSC_WT'] = row['LesionWise_Score_Dice']
            merged_data['LesionWise_HD95_WT'] = row['LesionWise_Score_HD95']
        elif row['Labels'] == 'TC':
            merged_data['LesionWise_DSC_TC'] = row['LesionWise_Score_Dice']
            merged_data['LesionWise_HD95_TC'] = row['LesionWise_Score_HD95']
        elif row['Labels'] == 'ET':
            merged_data['LesionWise_DSC_ET'] = row['LesionWise_Score_Dice']
            merged_data['LesionWise_HD95_ET'] = row['LesionWise_Score_HD95']
    
    # Append the merged data to the list
    rows.append(merged_data)

# Create a new DataFrame from the list of merged data
new_df = pd.DataFrame(rows)

# Calculate mean and standard deviation for each column
mean_row = new_df.mean()
std_row = new_df.std()

# Add the 'Label' for the mean and std rows
mean_row['Label'] = 'mean'
std_row['Label'] = 'std'

# Append mean and std rows to the DataFrame
new_df = new_df.append([mean_row, std_row], ignore_index=True)

# Save the new DataFrame to a CSV file
output_csv = os.path.join(root_dir, f'{x}_rearranged_lesionwise_results.csv')
new_df.to_csv(output_csv, index=False)

print(f"Rearranged CSV with mean and std saved to {output_csv}")
