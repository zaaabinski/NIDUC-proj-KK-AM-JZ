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
        return f"{error_prob*100:.4f}%"  # Will show as 0.0001% for 10^-6
    else:  # For regular numbers, use decimal format
        return f"{error_prob*100:.1f}".rstrip('0').rstrip('.') + "%"

def create_channel_comparison(bsc_data, ge_data, method_name, error_prob, save_dir):
    """Create side-by-side comparison of BSC and G-E channels for a given method and error rate"""
    plt.figure(figsize=(15, 8))
    
    # Define all possible error counts (0-4)
    all_error_counts = list(range(5))
    
    # Initialize frequency arrays for both channels
    bsc_freqs = [0] * 5
    ge_freqs = [0] * 5
    
    # Process BSC data
    for col in bsc_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            if count < 5:  # Only consider errors 0-4
                bsc_freqs[count] = bsc_data[col]
    
    # Process G-E data
    for col in ge_data.index:
        if col.startswith('errors_'):
            count = int(col.replace('errors_', ''))
            if count < 5:  # Only consider errors 0-4
                ge_freqs[count] = ge_data[col]
    
    # Convert to percentages
    total_bsc = sum(bsc_freqs)
    total_ge = sum(ge_freqs)
    bsc_percent = [f/total_bsc * 100 if total_bsc > 0 else 0 for f in bsc_freqs]
    ge_percent = [f/total_ge * 100 if total_ge > 0 else 0 for f in ge_freqs]
    
    # Set up bar positions
    x = np.arange(len(all_error_counts))
    width = 0.35
    
    # Create figure with adjusted size for legend
    fig = plt.gcf()
    fig.set_size_inches(15, 8)
    
    # Create bars
    plt.bar(x - width/2, bsc_percent, width, label='Kanał BSC', color='#1f77b4', alpha=0.7)
    plt.bar(x + width/2, ge_percent, width, label='Kanał Gilberta-Elliotta', color='#ff7f0e', alpha=0.7)
    
    # Add value labels on top of bars
    for i in range(len(all_error_counts)):
        if bsc_percent[i] >= 0.1:  # Show values ≥ 0.1%
            plt.text(i - width/2, bsc_percent[i], f'{bsc_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=14)
        if ge_percent[i] >= 0.1:  # Show values ≥ 0.1%
            plt.text(i + width/2, ge_percent[i], f'{ge_percent[i]:.1f}%', 
                    ha='center', va='bottom', fontsize=14)
    
    # Format error rate for title and filename
    error_rate_str = format_error_rate(error_prob)
    
    # Customize plot
    method_display_name = 'Kod BCH' if method_name == 'BCH' else 'Kod Powtórzeniowy'
    plt.title(f'Porównanie Kanałów - {method_display_name}\nPrawdopodobieństwo Błędu Kanału: {error_rate_str}', 
             fontsize=20, pad=20)
    plt.xlabel('Liczba Błędów w Wiadomości', fontsize=16)
    plt.ylabel('Procent Wiadomości (%)', fontsize=16)
    plt.xticks(x, all_error_counts, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set y-axis to go from 0 to 100%
    plt.ylim(0, 100)
    
    # Calculate statistics
    bsc_mean = sum(count * freq for count, freq in zip(all_error_counts, bsc_freqs)) / total_bsc if total_bsc > 0 else 0
    ge_mean = sum(count * freq for count, freq in zip(all_error_counts, ge_freqs)) / total_ge if total_ge > 0 else 0
    
    # Calculate max errors (highest error count with non-zero frequency)
    bsc_max = max((i for i, f in enumerate(bsc_freqs) if f > 0), default=0)
    ge_max = max((i for i, f in enumerate(ge_freqs) if f > 0), default=0)
    
    # Create statistics text
    stats_text = (
        f'Statystyki Kanału BSC:\n'
        f'Średnia Liczba Błędów: {bsc_mean:.3f}\n'
        f'Maksymalna Liczba Błędów: {bsc_max}\n'
        f'Liczba Wiadomości: {int(total_bsc)}\n\n'
        f'Statystyki Kanału Gilberta-Elliotta:\n'
        f'Średnia Liczba Błędów: {ge_mean:.3f}\n'
        f'Maksymalna Liczba Błędów: {ge_max}\n'
        f'Liczba Wiadomości: {int(total_ge)}'
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
                           f'channel_comparison_{method_name.lower().replace(" ", "_")}_{error_prob*100:.6f}'.replace('.', '_') + 'percent.png')
    else:
        filename = os.path.join(save_dir, 
                           f'channel_comparison_{method_name.lower().replace(" ", "_")}_{error_prob*100:.1f}'.rstrip('0').rstrip('.') + 'percent.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created channel comparison plot for {method_display_name} at {error_rate_str} error rate")

def plot_error_distributions(files, save_dir='finalplots'):
    """Create visualizations of error distributions"""
    # Create directory for finalplots if it doesn't exist
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    # Set style
    plt.style.use('default')
    
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
    
    # Define the error probabilities we want to visualize
    target_error_probs = [0.000001] + [0.005 + i * 0.005 for i in range(10)]  # 10^-6 and 0.5% to 5% in 0.5% steps
    
    # Get unique error probabilities from the data and filter for our target values
    error_probs = sorted(method_data['BCH']['bsc']['error_prob'].unique())
    error_probs = [prob for prob in error_probs if float(prob) in target_error_probs]
    
    # Create channel comparisons for each method and error rate
    for method, data in method_data.items():
        for error_prob_str in error_probs:
            # Convert string to float for comparison
            error_prob = float(error_prob_str)
            
            # Get rows for this error probability
            bsc_row = data['bsc'][data['bsc']['error_prob'] == error_prob_str].iloc[0]
            ge_row = data['ge'][data['ge']['error_prob'] == error_prob_str].iloc[0]
            
            # Create comparison plot
            create_channel_comparison(bsc_row, ge_row, method, error_prob, save_dir)

if __name__ == "__main__":
    try:
        # Find latest distribution files
        dist_files = find_latest_distributions()
        print(f"Found {len(dist_files)} distribution files")
        
        # Create visualizations
        plot_error_distributions(dist_files)
        print("finalplots have been created successfully in the 'finalplots' directory")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run the simulation first to generate results")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc() 