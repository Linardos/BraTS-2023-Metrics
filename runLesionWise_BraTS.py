import os
import sys
import pandas as pd
from tqdm import tqdm
from metrics import get_LesionWiseResults

# Ensure an experiment number is passed as an argument
if len(sys.argv) < 2:
    print("Usage: python script.py <experiment_number>")
    sys.exit(1)

# Get experiment number from command-line arguments
x = sys.argv[1]

# Define directories
GT_dir = "/home/locolinux2/datasets/RSNA_ASNR_MICCAI_BraTS2021_TestingGT"
PRED_dir = f'/home/locolinux2/.local/workspace/checkpoint/experiment_{x}/model_outputs'
output_dir = "/home/locolinux2/FETS2024/final_metrics_LesionWise"
output_file = os.path.join(output_dir, f'{x}_lesionwise_results.csv')

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load existing results if they exist
if os.path.exists(output_file):
    final_df = pd.read_csv(output_file)
else:
    final_df = pd.DataFrame()

# Iterate over each file in the prediction directory with tqdm progress bar
for pred_file in tqdm(os.listdir(PRED_dir), desc="Processing files"):
    pred_file_path = os.path.join(PRED_dir, pred_file)
    
    # Get the corresponding ground truth file
    gt_file = os.path.join(GT_dir, pred_file)

    # Check if this file has already been processed
    if not final_df.empty and pred_file in final_df['labels'].values:
        print(f"Skipping {pred_file}, already processed.")
        continue

    # Compute lesion-wise results
    results_df = get_LesionWiseResults(pred_file_path, gt_file, challenge_name='BraTS-GLI')

    # Add the filename to the results
    results_df['labels'] = pred_file

    # Append the results to the final DataFrame
    final_df = pd.concat([final_df, results_df])

    # Save the updated results to the CSV file
    final_df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
