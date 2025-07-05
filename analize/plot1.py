import json
import argparse

args = argparse.ArgumentParser(description='Plot data from JSON files')
args.add_argument('metrics_file', type=str, help='Path to the metrics JSON file')
args.add_argument('--outfolder', type=str, default='outs', help='Output folder for plots (not used in this script)')
args.add_argument('--override', action='store_true', help='Override existing output folder')

args = args.parse_args()

metrics = None
with open(args.metrics_file, 'r') as f:
    metrics = json.load(f)


print("Simulation on dataset:", metrics['dataset'])
print("Number of rounds:", metrics['num_rounds'])
print("Evaluation frequency:", metrics['eval_every'])
print("Learning rate:", metrics['learning_rate'])
print("Mu value:", metrics['mu'])
print("Number of local epochs:", metrics['num_epochs'])
print("Train Batch size:", metrics['batch_size'])


train_accuracies = metrics['train_accuracies']
accuracies = metrics['accuracies']


# format of bytes_written, bytes_read, computations:
# { [client name : str] : Array[int] (length = num_rounds) }
bytes_written = metrics['bytes_written']
bytes_read = metrics['bytes_read']
computations = metrics['client_computations']

# accuracies is in te format of AOS:
# accuracies [ Array<keys>, Array<groups>, Array<num_samples>, Array<tot_corrects>][] (length = num_rounds + 1)
accuracies = metrics['accuracies'][1:]
assert len(accuracies) == metrics['num_rounds'], "Number of rounds in accuracies does not match num_rounds in metrics"

train_accuracies = metrics['train_accuracies'][1:]
assert len(train_accuracies) == metrics['num_rounds'], "Number of rounds in accuracies does not match num_rounds in metrics"

client_accuracy_map = {}
for idx, client in enumerate(accuracies[0][0]): 
    client_accuracy_map[client] = idx



import pandas as pd

# Create a DataFrame with all clients and their metrics
# Key: round, client
# values: bytes_written, bytes_read, computations (integers)

dtype_mapping = {
    'round': int,
    'client': 'category',
    'bytes_written': int,
    'bytes_read': int,
    'computations': int,
    'test_samples': int,
    'test_corrects': int,
    'train_samples': int,
    'train_corrects': int,
}

full_data = []
for client, rounds_bytes_written in bytes_written.items():
    for rnd, bytes_w in enumerate(rounds_bytes_written):
        acc_id = client_accuracy_map[client]
        full_data.append({
            'round': rnd,
            'client': client,
            'bytes_written': bytes_w,
            'bytes_read': bytes_read[client][rnd],
            'computations': computations[client][rnd],
            'test_samples': accuracies[rnd][2][acc_id],
            'test_corrects': accuracies[rnd][3][acc_id],
            'train_samples': train_accuracies[rnd][2][acc_id],
            'train_corrects': train_accuracies[rnd][3][acc_id],
        })


df = pd.DataFrame(full_data)
df = df.astype(dtype_mapping)


import os
import shutil
from datetime import datetime
outfolder = args.outfolder
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
elif args.override:
    print("Output folder already exists. Overriding...")
    shutil.rmtree(outfolder)
    os.makedirs(outfolder)
else:
    timestamp = datetime.now().strftime("%H_%M_%S")
    outfolder = f"{outfolder}_{timestamp}"
    os.makedirs(outfolder)

print("Saving plots to:", outfolder)

import matplotlib.pyplot as plt

markdown_content = []

markdown_content.append(f"# Simulation Report: {metrics['dataset']}")
markdown_content.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

markdown_content.append("## Simulation Parameters")
markdown_content.append(f"- **Number of rounds**: {metrics['num_rounds']}")
markdown_content.append(f"- **Evaluation frequency**: {metrics['eval_every']}")
markdown_content.append(f"- **Learning rate**: {metrics['learning_rate']}")
markdown_content.append(f"- **Mu value**: {metrics['mu']}")
markdown_content.append(f"- **Number of local epochs**: {metrics['num_epochs']}")
markdown_content.append(f"- **Train Batch size**: {metrics['batch_size']}\n")

markdown_content.append("## Plots\n")

def save_plot(filename, title):
    plt.title(title)
    plt.savefig(os.path.join(outfolder, filename))
    markdown_content.append(f"![{title}]({filename})\n")
    plt.clf()
 
plt.xlabel('Round')
plt.ylabel('Accuracy')
plt.plot(df.groupby('round')['test_corrects'].sum() / df.groupby('round')['test_samples'].sum(), label='Test Accuracy')
save_plot('test_accuracy_per_round.png', 'Test Accuracy per Round')


plt.xlabel('Round')
plt.ylabel('Accuracy')
plt.plot(df.groupby('round')['train_corrects'].sum() / df.groupby('round')['train_samples'].sum(), label='Train Accuracy')
plt.savefig(os.path.join(outfolder, 'train_accuracy_per_round.png'))
save_plot('train_accuracy_per_round.png', 'Train Accuracy per Round')

plt.xlabel('Round')
plt.ylabel('Accuracy')
for client in df['client'].unique():
    client_df = df[df['client'] == client]
    plt.plot(client_df['round'], client_df['test_corrects'] / client_df['test_samples'], label=f'Test Accuracy {client}')
save_plot('test_accuracy_per_round_per_client.png', 'Test Accuracy per Round for Each Client')

plt.xlabel('Round')
plt.ylabel('Accuracy')
for client in df['client'].unique():
    client_df = df[df['client'] == client]
    plt.plot(client_df['round'], client_df['train_corrects'] / client_df['train_samples'], label=f'Train Accuracy {client}')
save_plot('train_accuracy_per_round_per_client.png', 'Train Accuracy per Round for Each Client')

plt.xlabel('Round')
plt.ylabel('Total Computations')
plt.plot(df.groupby('round')['computations'].sum(), label='Total Computations')
plt.savefig(os.path.join(outfolder, 'total_computations_per_round.png'))
save_plot('total_computations_per_round.png', 'Total Computations per Round')

plt.xlabel('Round')
plt.ylabel('Total Bytes Written')
plt.plot(df.groupby('round')['bytes_written'].sum(), label='Total Bytes Written')
plt.savefig(os.path.join(outfolder, 'total_bytes_written_per_round.png'))
save_plot('total_bytes_written_per_round.png', 'Total Bytes Written per Round')

plt.xlabel('Round')
plt.ylabel('Total Bytes Read')
plt.plot(df.groupby('round')['bytes_read'].sum(), label='Total  Bytes Read')
plt.savefig(os.path.join(outfolder, 'total_bytes_read_per_round.png'))
save_plot('total_bytes_read_per_round.png', 'Total Bytes Read per Round')

print("Plots saved successfully in:", outfolder)

# Save the markdown report
markdown_file = os.path.join(outfolder, 'report.md')
with open(markdown_file, 'w') as f:
    f.write('\n'.join(markdown_content))
    
print("Markdown report saved as:", markdown_file)