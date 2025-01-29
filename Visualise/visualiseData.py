import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

def find_latest_results():
    """Find the most recent simulation results file"""
    # Look in the results directory relative to the workspace root
    current_dir = os.path.dirname(__file__)
    workspace_root = os.path.dirname(current_dir)  # Go up one level to workspace root
    results_dir = os.path.join(workspace_root, 'results')
    
    print(f"Looking for results in: {results_dir}")  # Debug print
    
    if not os.path.exists(results_dir):
        # Try to find results in the current directory
        results_dir = os.getcwd()
        print(f"Results directory not found, trying current directory: {results_dir}")
    
    # Look for CSV files with simulation results
    files = glob.glob(os.path.join(results_dir, 'simulation_results_*.csv'))
    if not files:
        # Try looking in the current directory
        files = glob.glob('simulation_results_*.csv')
        
    if not files:
        raise FileNotFoundError(f"No simulation results files found in {results_dir} or current directory")
    
    latest_file = max(files)
    print(f"Found results file: {latest_file}")
    return latest_file

def format_error_rate(error_prob):
    """Format error rate for display, handling both small and regular numbers"""
    if error_prob < 0.0001:  # For very small numbers, use full decimal format
        return f"{error_prob*100:.6f}%"  # Will show as 0.0001% for 10^-6
    else:  # For regular numbers, use decimal format
        return f"{error_prob*100:.1f}".rstrip('0').rstrip('.') + "%"

def plot_error_correction_performance(data, save_dir='finalplots'):
    """Create finalplots for error correction performance"""
    # Create directory for finalplots if it doesn't exist
    current_dir = os.path.dirname(__file__)
    workspace_root = os.path.dirname(current_dir)
    save_dir = os.path.join(workspace_root, save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Saving finalplots to: {save_dir}")  # Debug print
    
    # Set style for better visibility
    plt.style.use('default')
    
    # Ensure all required error probabilities are present
    required_error_probs = [0.000001] + [0.005 + i * 0.005 for i in range(10)]  # 10^-6 and 0.5% to 5% in 0.5% steps
    
    # Check if we have all required error probabilities (with floating point tolerance)
    def is_close(a, b, rel_tol=1e-9):
        return abs(a - b) <= rel_tol
    
    # Check if each required probability exists in data (with tolerance)
    missing_probs = []
    for req_prob in required_error_probs:
        if not any(is_close(req_prob, actual_prob) for actual_prob in data['error_prob'].values):
            missing_probs.append(req_prob)
    
    if missing_probs:
        print(f"Warning: Missing error probabilities: {[format_error_rate(p) for p in missing_probs]}")
        print("\nAvailable probabilities:")
        for p in sorted(data['error_prob'].values):
            print(f"{p:.6f} ({format_error_rate(p)})")
    
    # Create figure with 2x2 finalplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Analiza Skuteczności Korekcji Błędów', fontsize=22, y=0.95)
    
    # Plot 1: Duplicating with BSC
    ax1.plot(data['error_prob'], data['duplicating_error_rate'], 
             marker='o', linestyle='-', linewidth=2, markersize=4, label='Kod Powtórzeniowy')
    ax1.set_title('Kanał BSC', fontsize=20)
    ax1.set_xlabel('Prawdopodobieństwo Błędu Kanału', fontsize=16)
    ax1.set_ylabel('Współczynnik Błędów Po Korekcji', fontsize=16)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Plot 2: BCH with BSC
    ax2.plot(data['error_prob'], data['bch_error_rate'],
             marker='s', linestyle='-', linewidth=2, markersize=4, color='green', label='Kod BCH')
    ax2.set_title('Kanał BSC', fontsize=20)
    ax2.set_xlabel('Prawdopodobieństwo Błędu Kanału', fontsize=16)
    ax2.set_ylabel('Współczynnik Błędów Po Korekcji', fontsize=16)
    ax2.tick_params(axis='both', which='major', labelsize=14)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Plot 3: Duplicating with Gilbert-Eliot
    ax3.plot(data['error_prob'], data['duplicating_error_rate_geliot'],
             marker='o', linestyle='-', linewidth=2, markersize=4, color='purple', label='Kod Powtórzeniowy')
    ax3.set_title('Kanał Gilberta-Elliotta', fontsize=20)
    ax3.set_xlabel('Prawdopodobieństwo Błędu Kanału', fontsize=16)
    ax3.set_ylabel('Współczynnik Błędów Po Korekcji', fontsize=16)
    ax3.tick_params(axis='both', which='major', labelsize=14)
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # Plot 4: BCH with Gilbert-Eliot
    ax4.plot(data['error_prob'], data['bch_error_rate_geliot'],
             marker='s', linestyle='-', linewidth=2, markersize=4, color='orange', label='Kod BCH')
    ax4.set_title('Kanał Gilberta-Elliotta', fontsize=20)
    ax4.set_xlabel('Prawdopodobieństwo Błędu Kanału', fontsize=16)
    ax4.set_ylabel('Współczynnik Błędów Po Korekcji', fontsize=16)
    ax4.tick_params(axis='both', which='major', labelsize=14)
    ax4.grid(True, linestyle='--', alpha=0.7)
    
    # Add grid and limits to all finalplots
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_xlim(0, max(data['error_prob']))
        ax.set_ylim(0, max(data['error_prob']) * 1.1)  # Scale y-axis to match input error rate
        ax.set_facecolor('#f8f8f8')  # Light gray background
        ax.legend(loc='upper left', fontsize=14)  # Place legends in upper left to avoid overlap
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'error_correction_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create combined comparison plot
    plt.figure(figsize=(12, 8))
    plt.plot(data['error_prob'], data['duplicating_error_rate'], 
             marker='o', label='Kod Powtórzeniowy (BSC)', linewidth=2, markersize=4)
    plt.plot(data['error_prob'], data['bch_error_rate'],
             marker='s', label='Kod BCH (BSC)', linewidth=2, markersize=4)
    plt.plot(data['error_prob'], data['duplicating_error_rate_geliot'],
             marker='^', label='Kod Powtórzeniowy (G-E)', linewidth=2, markersize=4)
    plt.plot(data['error_prob'], data['bch_error_rate_geliot'],
             marker='D', label='Kod BCH (G-E)', linewidth=2, markersize=4)
    
    plt.title('Porównanie wszystkich metod korekcji błędów', fontsize=20)
    plt.xlabel('Prawdopodobieństwo Błędu Kanału', fontsize=16)
    plt.ylabel('Współczynnik Błędów Po Korekcji', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0.05, 0)  # Reversed x-axis from 0.05 to 0
    plt.ylim(0, max(data['error_prob']) * 1.1)  # Scale y-axis to match input error rate
    plt.gca().set_facecolor('#f8f8f8')  # Light gray background
    plt.legend(loc='upper left', fontsize=14)  # Place legend in upper left
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'error_correction_comparison_combined.png'), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    try:
        # Read the latest results file
        latest_file = find_latest_results()
        print(f"Reading results from: {latest_file}")
        data = pd.read_csv(latest_file)
        
        # Create visualizations
        plot_error_correction_performance(data)
        print("finalplots have been created successfully in the 'finalplots' directory")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run the simulation first to generate results")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
