import argparse


parser = argparse.ArgumentParser(description='Analyze and summarize all metrics')
parser.add_argument('folder', type=str, help='Path to the folder containing metrics JSON files')
args = parser.parse_args()

# list all folders in folder

import os

if not os.path.exists(args.folder):
    print(f"Folder {args.folder} does not exist.")
    exit(1)

folders = [f for f in os.listdir(args.folder) if os.path.isdir(os.path.join(args.folder, f))]
if not folders:
    print(f"No subfolders found in {args.folder}.")
    exit(1)

print(f"Found {len(folders)} subfolders in {args.folder}.")

import subprocess

if not os.path.exists('all'):
    os.makedirs('all')

# run the plot1.py script for each folder
for folder in folders:
    folder_path = os.path.join(args.folder, folder)
    # find **_metrics.json in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    if not files:
        print(f"No metrics.json found in {folder_path}. Skipping.")
        continue

    for metrics_file in files:
        # remove metrics_ prefix if it exists and .json suffix
        metric_name = metrics_file.replace('metrics_', '').replace('.json', '')
        print(f"Processing {metrics_file} in folder {folder}...")

        # create sub subfolder for the metric
        metric_folder = os.path.join('all', folder, metric_name)
        if not os.path.exists(metric_folder):
            os.makedirs(metric_folder)

        command = [
            'python', 'plot1.py',
            os.path.join(folder_path, metrics_file),
            '--outfolder', metric_folder,
            '--override'
        ]

        # Execute the command
        subprocess.run(command, check=True)
    

print(f"Processed {len(folders)} subfolders and generated plots in 'all' folder.")
    

