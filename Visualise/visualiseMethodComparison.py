import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import numpy as np

def find_latest_distributions():
    """Find the most recent error distribution files"""
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    if not os.path.exists(results_dir):
        raise FileNotFoundError("Results directory not found")
    
    # Find all distribution files
    files = glob.glob(os.path.join(results_dir, 'error_distribution_*.csv'))
    if not files:
        raise FileNotFoundError("No error distribution files found")
    
    # Group files by timestamp
    timestamps = set()
    for f in files:
        # Extract timestamp from filename
        ts = f.split('_')[-1].replace('.csv', '')
        timestamps.add(ts)
    
    latest_ts = max(timestamps)
    latest_files = [f for f in files if latest_ts in f]
    
    return latest_files

def create_method_comparison(bch_data, duplicating_data, channel_name, error_prob, save_dir):
    """Create side-by-side comparison of BCH and Duplicating methods for a given channel and error rate"""
    plt.figure(figsize=(15, 8))
    
    # Get error counts and frequencies for both methods
    error_counts_bch = []
    freqs_bch = []
    error_counts_dup = []
    freqs_dup = []
    
    # Process BCH data
    for col in bch_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            freq = bch_data[col]
            if freq > 0:
                error_counts_bch.append(count)
                freqs_bch.append(freq)
    
    # Process Duplicating data
    for col in duplicating_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            freq = duplicating_data[col]
            if freq > 0:
                error_counts_dup.append(count)
                freqs_dup.append(freq)
    
    # Get union of error counts
    all_error_counts = sorted(list(set(error_counts_bch + error_counts_dup)))
    
    # Prepare data for plotting
    bch_freqs = []
    dup_freqs = []
    for count in all_error_counts:
        if count in error_counts_bch:
            idx = error_counts_bch.index(count)
            bch_freqs.append(freqs_bch[idx])
        else:
            bch_freqs.append(0)
            
        if count in error_counts_dup:
            idx = error_counts_dup.index(count)
            dup_freqs.append(freqs_dup[idx])
        else:
            dup_freqs.append(0)
    
    # Convert to percentages
    total_bch = sum(bch_freqs)
    total_dup = sum(dup_freqs)
    bch_percent = [f/total_bch * 100 for f in bch_freqs]
    dup_percent = [f/total_dup * 100 for f in dup_freqs]
    
    # Set up bar positions
    x = np.arange(len(all_error_counts))
    width = 0.35
    
    # Create bars
    plt.bar(x - width/2, bch_percent, width, label='BCH', color='#2ca02c', alpha=0.7)
    plt.bar(x + width/2, dup_percent, width, label='Duplicating', color='#d62728', alpha=0.7)
    
    # Add value labels on top of bars
    for i in range(len(all_error_counts)):
        if bch_percent[i] >= 1:
            plt.text(i - width/2, bch_percent[i], f'{bch_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=10)
        if dup_percent[i] >= 1:
            plt.text(i + width/2, dup_percent[i], f'{dup_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=10)
    
    # Customize plot
    plt.title(f'Method Comparison - {channel_name}\nChannel Error Rate: {error_prob:.1%}', 
             fontsize=14, pad=20)
    plt.xlabel('Number of Errors in Message', fontsize=12)
    plt.ylabel('Percentage of Messages (%)', fontsize=12)
    plt.xticks(x, all_error_counts)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # Add statistics
    bch_mean = sum(count * freq for count, freq in zip(all_error_counts, bch_freqs)) / total_bch
    dup_mean = sum(count * freq for count, freq in zip(all_error_counts, dup_freqs)) / total_dup
    
    stats_text = (
        f'BCH Statistics:\n'
        f'Mean Errors: {bch_mean:.2f}\n'
        f'Max Errors: {all_error_counts[bch_percent.index(max(bch_percent))]}\n'
        f'Total Messages: {total_bch}\n\n'
        f'Duplicating Statistics:\n'
        f'Mean Errors: {dup_mean:.2f}\n'
        f'Max Errors: {all_error_counts[dup_percent.index(max(dup_percent))]}\n'
        f'Total Messages: {total_dup}'
    )
    
    plt.text(0.98, 0.98, stats_text,
            transform=plt.gca().transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            fontsize=10)
    
    # Save plot
    filename = os.path.join(save_dir, 
                           f'method_comparison_{channel_name.lower().replace(" ", "_")}_{int(error_prob*100)}percent.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created method comparison plot for {channel_name} at {error_prob:.1%} error rate")

def plot_method_comparisons(files, save_dir='plotsTest3Test133'):
    """Create visualizations comparing BCH and Duplicating methods"""
    # Create directory for plotsTest3Test1331 if it doesn't exist
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    # Set style
    plt.style.use('default')
    
    # Plot settings
    error_probs_to_show = [0.01, 0.05, 0.1, 0.2, 0.3]  # 1%, 5%, 10%, 20%, 30%
    
    # Group files by method and channel
    bsc_files = {}
    ge_files = {}
    
    for file in files:
        if 'powielanie_ge' in file:
            ge_files['Duplicating'] = file
        elif 'bch_ge' in file:
            ge_files['BCH'] = file
        elif 'powielanie' in file:
            bsc_files['Duplicating'] = file
        elif 'bch' in file:
            bsc_files['BCH'] = file
    
    # Read data for each method
    channel_data = {
        'BSC': {'bch': pd.read_csv(bsc_files['BCH']),
                'duplicating': pd.read_csv(bsc_files['Duplicating'])},
        'Gilbert-Eliot': {'bch': pd.read_csv(ge_files['BCH']),
                         'duplicating': pd.read_csv(ge_files['Duplicating'])}
    }
    
    # Create method comparisons for each channel and error rate
    for channel_name, data in channel_data.items():
        for error_prob in error_probs_to_show:
            # Find closest error probability in BCH data
            bch_prob = data['bch']['error_prob'].iloc[
                (data['bch']['error_prob'] - error_prob).abs().argsort()[:1]].values[0]
            bch_row = data['bch'][data['bch']['error_prob'] == bch_prob].iloc[0]
            
            # Find closest error probability in Duplicating data
            dup_prob = data['duplicating']['error_prob'].iloc[
                (data['duplicating']['error_prob'] - error_prob).abs().argsort()[:1]].values[0]
            dup_row = data['duplicating'][data['duplicating']['error_prob'] == dup_prob].iloc[0]
            
            # Create comparison plot
            create_method_comparison(bch_row, dup_row, channel_name, error_prob, save_dir)

if __name__ == "__main__":
    try:
        # Find latest distribution files
        dist_files = find_latest_distributions()
        print(f"Found {len(dist_files)} distribution files")
        
        # Create visualizations
        plot_method_comparisons(dist_files)
        print("plotsTest3Test133 have been created successfully in the 'plotsTest3Test133' directory")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run the simulation first to generate results")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc() 