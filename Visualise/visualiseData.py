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

def plot_error_correction_performance(data, save_dir='plotsTest1'):
    """Create plotsTest11 for error correction performance"""
    # Create directory for plotsTest11 if it doesn't exist
    current_dir = os.path.dirname(__file__)
    workspace_root = os.path.dirname(current_dir)
    save_dir = os.path.join(workspace_root, save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Saving plotsTest1 to: {save_dir}")  # Debug print
    
    # Set style for better visibility
    plt.style.use('default')
    
    # Create figure with 2x2 subplotsTest1
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Error Correction Performance Analysis', fontsize=16)
    
    # Plot 1: Duplicating with BSC
    ax1.plot(data['error_prob'], data['duplicating_error_rate'], 
             marker='o', linestyle='-', linewidth=2, markersize=4)
    ax1.set_title('Duplicating with BSC Channel')
    ax1.set_xlabel('Channel Error Probability')
    ax1.set_ylabel('Error Rate After Correction')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Plot 2: BCH with BSC
    ax2.plot(data['error_prob'], data['bch_error_rate'],
             marker='s', linestyle='-', linewidth=2, markersize=4, color='green')
    ax2.set_title('BCH with BSC Channel')
    ax2.set_xlabel('Channel Error Probability')
    ax2.set_ylabel('Error Rate After Correction')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Plot 3: Duplicating with Gilbert-Eliot
    ax3.plot(data['error_prob'], data['duplicating_error_rate_geliot'],
             marker='o', linestyle='-', linewidth=2, markersize=4, color='purple')
    ax3.set_title('Duplicating with Gilbert-Eliot Channel')
    ax3.set_xlabel('Channel Error Probability')
    ax3.set_ylabel('Error Rate After Correction')
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # Plot 4: BCH with Gilbert-Eliot
    ax4.plot(data['error_prob'], data['bch_error_rate_geliot'],
             marker='s', linestyle='-', linewidth=2, markersize=4, color='orange')
    ax4.set_title('BCH with Gilbert-Eliot Channel')
    ax4.set_xlabel('Channel Error Probability')
    ax4.set_ylabel('Error Rate After Correction')
    ax4.grid(True, linestyle='--', alpha=0.7)
    
    # Add grid and limits to all plotsTest11
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_xlim(0, max(data['error_prob']))
        ax.set_ylim(0, 1)
        ax.set_facecolor('#f8f8f8')  # Light gray background
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'error_correction_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create comparison plot
    plt.figure(figsize=(12, 8))
    plt.plot(data['error_prob'], data['duplicating_error_rate'], 
             marker='o', label='Duplicating (BSC)', linewidth=2, markersize=4)
    plt.plot(data['error_prob'], data['bch_error_rate'],
             marker='s', label='BCH (BSC)', linewidth=2, markersize=4)
    plt.plot(data['error_prob'], data['duplicating_error_rate_geliot'],
             marker='^', label='Duplicating (G-E)', linewidth=2, markersize=4)
    plt.plot(data['error_prob'], data['bch_error_rate_geliot'],
             marker='D', label='BCH (G-E)', linewidth=2, markersize=4)
    
    plt.title('Comparison of All Error Correction Methods')
    plt.xlabel('Channel Error Probability')
    plt.ylabel('Error Rate After Correction')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, max(data['error_prob']))
    plt.ylim(0, 1)
    plt.gca().set_facecolor('#f8f8f8')  # Light gray background
    plt.legend()
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
        print("plotsTest1 have been created successfully in the 'plotsTest1' directory")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run the simulation first to generate results")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
