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

def format_error_rate(error_prob):
    """Format error rate for display, handling both small and regular numbers"""
    if error_prob < 0.0001:  # For very small numbers, use full decimal format
        return f"{error_prob*100:.6f}%"  # Will show as 0.0001% for 10^-6
    else:  # For regular numbers, use decimal format
        return f"{error_prob*100:.1f}".rstrip('0').rstrip('.') + "%"

def create_method_comparison(bch_data, duplicating_data, channel_name, error_prob, save_dir):
    """Create side-by-side comparison of BCH and Duplicating methods for a given channel and error rate"""
    plt.figure(figsize=(15, 8))
    
    # Define all possible error counts (0-4)
    all_error_counts = list(range(5))
    
    # Initialize frequency arrays for both methods
    bch_freqs = [0] * 5
    dup_freqs = [0] * 5
    
    # Process BCH data
    for col in bch_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            if count < 5:  # Only consider errors 0-4
                bch_freqs[count] = bch_data[col]
    
    # Process Duplicating data
    for col in duplicating_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            if count < 5:  # Only consider errors 0-4
                dup_freqs[count] = duplicating_data[col]
    
    # Convert to percentages
    total_bch = sum(bch_freqs)
    total_dup = sum(dup_freqs)
    bch_percent = [f/total_bch * 100 if total_bch > 0 else 0 for f in bch_freqs]
    dup_percent = [f/total_dup * 100 if total_dup > 0 else 0 for f in dup_freqs]
    
    # Set up bar positions
    x = np.arange(len(all_error_counts))
    width = 0.35
    
    # Create figure with adjusted size for legend
    fig = plt.gcf()
    fig.set_size_inches(15, 8)
    
    # Create bars
    plt.bar(x - width/2, bch_percent, width, label='Kod BCH', color='#2ca02c', alpha=0.7)
    plt.bar(x + width/2, dup_percent, width, label='Kod Powtórzeniowy', color='#d62728', alpha=0.7)
    
    # Add value labels on top of bars
    for i in range(len(all_error_counts)):
        if bch_percent[i] >= 0.1:  # Show values ≥ 0.1%
            plt.text(i - width/2, bch_percent[i], f'{bch_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=14)
        if dup_percent[i] >= 0.1:  # Show values ≥ 0.1%
            plt.text(i + width/2, dup_percent[i], f'{dup_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=14)
    
    # Format error rate for title and filename
    error_rate_str = format_error_rate(error_prob)
    
    # Customize plot
    plt.title(f'Porównanie Metod - {channel_name}\nPrawdopodobieństwo Błędu Kanału: {error_rate_str}', 
             fontsize=20, pad=20)
    plt.xlabel('Liczba Błędów w Wiadomości', fontsize=16)
    plt.ylabel('Procent Wiadomości (%)', fontsize=16)
    plt.xticks(x, all_error_counts, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set y-axis to go from 0 to 100%
    plt.ylim(0, 100)
    
    # Calculate statistics
    bch_mean = sum(count * freq for count, freq in zip(all_error_counts, bch_freqs)) / total_bch if total_bch > 0 else 0
    dup_mean = sum(count * freq for count, freq in zip(all_error_counts, dup_freqs)) / total_dup if total_dup > 0 else 0
    
    # Calculate max errors (highest error count with non-zero frequency)
    bch_max = max((i for i, f in enumerate(bch_freqs) if f > 0), default=0)
    dup_max = max((i for i, f in enumerate(dup_freqs) if f > 0), default=0)
    
    # Create statistics text
    stats_text = (
        f'Statystyki Kodu BCH:\n'
        f'Średnia Liczba Błędów: {bch_mean:.3f}\n'
        f'Maksymalna Liczba Błędów: {bch_max}\n'
        f'Liczba Wiadomości: {int(total_bch)}\n\n'
        f'Statystyki Kodu Powtórzeniowego:\n'
        f'Średnia Liczba Błędów: {dup_mean:.3f}\n'
        f'Maksymalna Liczba Błędów: {dup_max}\n'
        f'Liczba Wiadomości: {int(total_dup)}'
    )
    
    # Add legend in the bottom right corner
    plt.legend(loc='center right', fontsize=14)
    
    # Position the stats box in the upper right corner of the plot
    plt.text(0.98, 0.95, stats_text,
            transform=plt.gca().transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'),
            fontsize=14)
    
    # Adjust layout to prevent text cutoff
    plt.tight_layout()
    
    # Save plot with consistent filename format
    if error_prob < 0.0001:
        filename = os.path.join(save_dir, 
                           f'method_comparison_{channel_name.lower().replace(" ", "_")}_{error_prob*100:.6f}'.replace('.', '_') + 'percent.png')
    else:
        filename = os.path.join(save_dir, 
                           f'method_comparison_{channel_name.lower().replace(" ", "_")}_{error_prob*100:.1f}'.rstrip('0').rstrip('.') + 'percent.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created method comparison plot for {channel_name} at {error_rate_str} error rate")

def plot_method_comparisons(files, save_dir='finalplots'):
    """Create visualizations comparing BCH and Duplicating methods"""
    # Create directory for finalplots if it doesn't exist
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    # Set style
    plt.style.use('default')
    
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
    
    # Define the error probabilities we want to visualize
    target_error_probs = [0.000001] + [0.005 + i * 0.005 for i in range(10)]  # 10^-6 and 0.5% to 5% in 0.5% steps
    
    # Get unique error probabilities from the data and filter for our target values
    error_probs = sorted(channel_data['BSC']['bch']['error_prob'].unique())
    error_probs = [prob for prob in error_probs if float(prob) in target_error_probs]
    
    # Create method comparisons for each channel and error rate
    for channel_name, data in channel_data.items():
        for error_prob_str in error_probs:
            # Convert string to float for comparison
            error_prob = float(error_prob_str)
            
            # Get rows for this error probability
            bch_row = data['bch'][data['bch']['error_prob'] == error_prob_str].iloc[0]
            dup_row = data['duplicating'][data['duplicating']['error_prob'] == error_prob_str].iloc[0]
            
            # Create comparison plot
            create_method_comparison(bch_row, dup_row, channel_name, error_prob, save_dir)

if __name__ == "__main__":
    try:
        # Find latest distribution files
        dist_files = find_latest_distributions()
        print(f"Found {len(dist_files)} distribution files")
        
        # Create visualizations
        plot_method_comparisons(dist_files)
        print("finalplots have been created successfully in the 'finalplots' directory")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run the simulation first to generate results")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc() 