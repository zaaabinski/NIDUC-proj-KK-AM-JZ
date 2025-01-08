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

def create_channel_comparison(bsc_data, ge_data, method_name, error_prob, save_dir):
    """Create side-by-side comparison of BSC and G-E channels for a given method and error rate"""
    plt.figure(figsize=(15, 8))
    
    # Get error counts and frequencies for both channels
    error_counts_bsc = []
    freqs_bsc = []
    error_counts_ge = []
    freqs_ge = []
    
    # Process BSC data
    for col in bsc_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            freq = bsc_data[col]
            if freq > 0:
                error_counts_bsc.append(count)
                freqs_bsc.append(freq)
    
    # Process G-E data
    for col in ge_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            freq = ge_data[col]
            if freq > 0:
                error_counts_ge.append(count)
                freqs_ge.append(freq)
    
    # Get union of error counts
    all_error_counts = sorted(list(set(error_counts_bsc + error_counts_ge)))
    
    # Prepare data for plotting
    bsc_freqs = []
    ge_freqs = []
    for count in all_error_counts:
        if count in error_counts_bsc:
            idx = error_counts_bsc.index(count)
            bsc_freqs.append(freqs_bsc[idx])
        else:
            bsc_freqs.append(0)
            
        if count in error_counts_ge:
            idx = error_counts_ge.index(count)
            ge_freqs.append(freqs_ge[idx])
        else:
            ge_freqs.append(0)
    
    # Convert to percentages
    total_bsc = sum(bsc_freqs)
    total_ge = sum(ge_freqs)
    bsc_percent = [f/total_bsc * 100 for f in bsc_freqs]
    ge_percent = [f/total_ge * 100 for f in ge_freqs]
    
    # Set up bar positions
    x = np.arange(len(all_error_counts))
    width = 0.35
    
    # Create bars
    plt.bar(x - width/2, bsc_percent, width, label='BSC Channel', color='#1f77b4', alpha=0.7)
    plt.bar(x + width/2, ge_percent, width, label='Gilbert-Eliot Channel', color='#ff7f0e', alpha=0.7)
    
    # Add value labels on top of bars
    for i in range(len(all_error_counts)):
        if bsc_percent[i] >= 1:
            plt.text(i - width/2, bsc_percent[i], f'{bsc_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=10)
        if ge_percent[i] >= 1:
            plt.text(i + width/2, ge_percent[i], f'{ge_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=10)
    
    # Customize plot
    plt.title(f'Channel Comparison - {method_name}\nChannel Error Rate: {error_prob:.1%}', 
             fontsize=14, pad=20)
    plt.xlabel('Number of Errors in Message', fontsize=12)
    plt.ylabel('Percentage of Messages (%)', fontsize=12)
    plt.xticks(x, all_error_counts)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # Add statistics
    bsc_mean = sum(count * freq for count, freq in zip(all_error_counts, bsc_freqs)) / total_bsc
    ge_mean = sum(count * freq for count, freq in zip(all_error_counts, ge_freqs)) / total_ge
    
    stats_text = (
        f'BSC Statistics:\n'
        f'Mean Errors: {bsc_mean:.2f}\n'
        f'Max Errors: {all_error_counts[bsc_percent.index(max(bsc_percent))]}\n'
        f'Total Messages: {total_bsc}\n\n'
        f'G-E Statistics:\n'
        f'Mean Errors: {ge_mean:.2f}\n'
        f'Max Errors: {all_error_counts[ge_percent.index(max(ge_percent))]}\n'
        f'Total Messages: {total_ge}'
    )
    
    plt.text(0.98, 0.98, stats_text,
            transform=plt.gca().transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            fontsize=10)
    
    # Save plot
    filename = os.path.join(save_dir, 
                           f'channel_comparison_{method_name.lower().replace(" ", "_")}_{int(error_prob*100)}percent.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created channel comparison plot for {method_name} at {error_prob:.1%} error rate")

def plot_error_distributions(files, save_dir='plotsTest2Test12'):
    """Create visualizations of error distributions"""
    # Create directory for plotsTest2Test12 if it doesn't exist
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    # Set style
    plt.style.use('default')
    
    # Plot settings
    error_probs_to_show = [0.01, 0.05, 0.1, 0.2, 0.3]  # 1%, 5%, 10%, 20%, 30%
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Distinct colors for each probability
    
    # Group files by method
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
    method_data = {}
    for method in ['Duplicating', 'BCH']:
        if method in bsc_files and method in ge_files:
            bsc_df = pd.read_csv(bsc_files[method])
            ge_df = pd.read_csv(ge_files[method])
            method_data[method] = {'bsc': bsc_df, 'ge': ge_df}
    
    # Create channel comparisons for each method and error rate
    for method, data in method_data.items():
        for error_prob in error_probs_to_show:
            # Find closest error probability in BSC data
            bsc_prob = data['bsc']['error_prob'].iloc[
                (data['bsc']['error_prob'] - error_prob).abs().argsort()[:1]].values[0]
            bsc_row = data['bsc'][data['bsc']['error_prob'] == bsc_prob].iloc[0]
            
            # Find closest error probability in G-E data
            ge_prob = data['ge']['error_prob'].iloc[
                (data['ge']['error_prob'] - error_prob).abs().argsort()[:1]].values[0]
            ge_row = data['ge'][data['ge']['error_prob'] == ge_prob].iloc[0]
            
            # Create comparison plot
            create_channel_comparison(bsc_row, ge_row, method, error_prob, save_dir)

if __name__ == "__main__":
    try:
        # Find latest distribution files
        dist_files = find_latest_distributions()
        print(f"Found {len(dist_files)} distribution files")
        
        # Create visualizations
        plot_error_distributions(dist_files)
        print("plotsTest2Test1 have been created successfully in the 'plotsTest2Test12' directory")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run the simulation first to generate results")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc() 