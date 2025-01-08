from ObslugaDanych.OdczytajDane import OdczytDanych
from StartSymulacji import SymulacjaDlaPowielania
from StartSymulacji import SymulacjaDlaBCH
from StartSymulacji import SymulacjaBCHGEliot
from StartSymulacji import SymulacjaDlaPowielaniaGEliot
from config import BCH_K
import csv
from datetime import datetime
import os
import multiprocessing as mp
from tqdm import tqdm
from collections import defaultdict

def count_errors_in_sequence(original, decoded):
    """Count number of errors in a single sequence"""
    if len(original) != len(decoded):
        raise ValueError(f"Length mismatch: original={len(original)}, decoded={len(decoded)}")
    return sum(1 for i in range(len(original)) if original[i] != decoded[i])

def prepare_data_for_bch(data):
    """
    Prepare data for BCH encoding by splitting into chunks of size BCH_K.
    If the last chunk is incomplete, it's padded with zeros.
    """
    chunks = []
    for i in range(0, len(data), BCH_K):
        chunk = data[i:i + BCH_K]
        # Pad last chunk with zeros if needed
        if len(chunk) < BCH_K:
            chunk = chunk + [0] * (BCH_K - len(chunk))
        chunks.append(chunk)
    return chunks

def run_simulation(params):
    """
    Run a single simulation with given parameters.
    params is a tuple of (error_prob, repetitions, input_file)
    """
    error_prob, repetitions, input_file = params
    
    # Make input_file path relative to this script's location
    input_file = os.path.join(os.path.dirname(__file__), input_file)
    
    odczyt = OdczytDanych(input_file)
    total_bits = 0
    incorrect_bits_powielanie = 0
    incorrect_bits_bch = 0
    incorrect_bits_powielanie_ge = 0
    incorrect_bits_bch_ge = 0
    ilosc_danych = 0
    
    # Track error count distributions
    error_dist_powielanie = defaultdict(int)
    error_dist_bch = defaultdict(int)
    error_dist_powielanie_ge = defaultdict(int)
    error_dist_bch_ge = defaultdict(int)

    dane_bin = odczyt.odczytaj_dane()

    for dane_wejsciowe in dane_bin:
        ilosc_danych += 1
        total_bits += len(dane_wejsciowe)
        
        # powielanie BSC
        bledy_powielanie, dane_po_powielaniu, dane_po_bsc_powielanie, dane_zakodowane_powielanie = SymulacjaDlaPowielania.SymulujPowielanie(
            dane_wejsciowe, 
            error_prob=error_prob, 
            repetitions=repetitions
        )
        errors = count_errors_in_sequence(dane_wejsciowe, dane_po_powielaniu)
        error_dist_powielanie[errors] += 1
        incorrect_bits_powielanie += errors

        # BCH BSC - process data in 5-bit chunks
        total_bch_errors = 0
        decoded_bch_data = []
        bch_chunks = prepare_data_for_bch(dane_wejsciowe)
        
        for chunk in bch_chunks:
            bledy_BCH, dane_po_bch, dane_po_bsc_bch, dane_zakodowane_bch = SymulacjaDlaBCH.SymulujBCH(
                chunk,
                error_prob=error_prob
            )
            total_bch_errors += bledy_BCH
            decoded_bch_data.extend(dane_po_bch[:len(chunk)])  # Only take the actual data length, not padding
        
        # Trim decoded data to original length
        decoded_bch_data = decoded_bch_data[:len(dane_wejsciowe)]
        errors = count_errors_in_sequence(dane_wejsciowe, decoded_bch_data)
        error_dist_bch[errors] += 1
        incorrect_bits_bch += errors

        # powielanie Gilbert-Eliot
        bledy_powielanie_ge, dane_po_powielaniu_ge, dane_po_ge_powielanie = SymulacjaDlaPowielaniaGEliot.SymulujPowielanieGEliot(
            dane_wejsciowe,
            error_prob=error_prob,
            repetitions=repetitions
        )
        errors = count_errors_in_sequence(dane_wejsciowe, dane_po_powielaniu_ge)
        error_dist_powielanie_ge[errors] += 1
        incorrect_bits_powielanie_ge += errors

        # BCH Gilbert-Eliot - process data in 5-bit chunks
        total_bch_ge_errors = 0
        decoded_bch_ge_data = []
        
        for chunk in bch_chunks:
            bledy_BCH_ge, dane_po_bch_ge, dane_po_ge_bch = SymulacjaBCHGEliot.SymulujBCHEliot(
                chunk,
                error_prob=error_prob
            )
            total_bch_ge_errors += bledy_BCH_ge
            decoded_bch_ge_data.extend(dane_po_bch_ge[:len(chunk)])  # Only take the actual data length, not padding
            
        # Trim decoded data to original length
        decoded_bch_ge_data = decoded_bch_ge_data[:len(dane_wejsciowe)]
        errors = count_errors_in_sequence(dane_wejsciowe, decoded_bch_ge_data)
        error_dist_bch_ge[errors] += 1
        incorrect_bits_bch_ge += errors

    return {
        'error_prob': error_prob,
        'repetitions': repetitions,
        'total_bits': total_bits,
        'incorrect_bits_powielanie': incorrect_bits_powielanie,
        'incorrect_bits_bch': incorrect_bits_bch,
        'incorrect_bits_powielanie_ge': incorrect_bits_powielanie_ge,
        'incorrect_bits_bch_ge': incorrect_bits_bch_ge,
        'duplicating_error_rate': incorrect_bits_powielanie/total_bits,
        'bch_error_rate': incorrect_bits_bch/total_bits,
        'duplicating_error_rate_geliot': incorrect_bits_powielanie_ge/total_bits,
        'bch_error_rate_geliot': incorrect_bits_bch_ge/total_bits,
        'error_dist_powielanie': dict(error_dist_powielanie),
        'error_dist_bch': dict(error_dist_bch),
        'error_dist_powielanie_ge': dict(error_dist_powielanie_ge),
        'error_dist_bch_ge': dict(error_dist_bch_ge)
    }

def run_error_rate_analysis(min_error=0.01, max_error=0.3, step=0.01, repetitions=3, input_file="dane2.txt"):
    """Run analysis for different error rates with specified intervals using multiple processes"""
    error_probs = [round(x * step, 3) for x in range(int(min_error/step), int(max_error/step) + 1)]
    
    # Prepare parameters for parallel processing
    params = [(prob, repetitions, input_file) for prob in error_probs]
    
    # Get the number of CPU cores (leave one core free for system)
    num_processes = max(1, mp.cpu_count() - 1)
    print(f"Running simulations using {num_processes} processes...")
    
    # Create a pool of processes
    with mp.Pool(processes=num_processes) as pool:
        # Run simulations in parallel with progress bar
        results = list(tqdm(
            pool.imap(run_simulation, params),
            total=len(params),
            desc="Simulating",
            unit="error_prob"
        ))
    
    # Sort results by error probability to maintain order
    results.sort(key=lambda x: x['error_prob'])
    return results

def save_error_distributions(results, results_dir, timestamp):
    """Save error count distributions to separate CSV files"""
    methods = [
        ('powielanie', 'Duplicating BSC'),
        ('bch', 'BCH BSC'),
        ('powielanie_ge', 'Duplicating G-E'),
        ('bch_ge', 'BCH G-E')
    ]
    
    for method_key, method_name in methods:
        dist_filename = os.path.join(results_dir, f"error_distribution_{method_key}_{timestamp}.csv")
        
        # Get all possible error counts across all error probabilities
        all_error_counts = set()
        for result in results:
            all_error_counts.update(result[f'error_dist_{method_key}'].keys())
        
        error_counts = sorted(all_error_counts)
        
        with open(dist_filename, 'w', newline='') as csvfile:
            fieldnames = ['error_prob'] + [f'errors_{count}' for count in error_counts]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row = {'error_prob': result['error_prob']}
                dist = result[f'error_dist_{method_key}']
                for count in error_counts:
                    row[f'errors_{count}'] = dist.get(count, 0)
                writer.writerow(row)
        
        print(f"Error distribution for {method_name} saved to {dist_filename}")

if __name__ == "__main__":
    try:
        # Install tqdm if not already installed
        import importlib
        if importlib.util.find_spec("tqdm") is None:
            import subprocess
            subprocess.check_call(["pip", "install", "tqdm"])
            
        # Create timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get the workspace root directory (one level up from this script)
        workspace_root = os.path.dirname(os.path.dirname(__file__))
        
        # Create results directory in workspace root
        results_dir = os.path.join(workspace_root, 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        print(f"Results will be saved to: {results_dir}")
        
        # Run simulation
        results = run_error_rate_analysis(
            min_error=0.01,  # 0.5%
            max_error=0.3,    # 50%
            step=0.01,       # 0.5% intervals
            repetitions=3
        )
        
        # Save main results to CSV
        csv_filename = os.path.join(results_dir, f"simulation_results_{timestamp}.csv")
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['error_prob', 'repetitions', 'total_bits',
                         'incorrect_bits_powielanie', 'incorrect_bits_bch',
                         'incorrect_bits_powielanie_ge', 'incorrect_bits_bch_ge',
                         'duplicating_error_rate', 'bch_error_rate',
                         'duplicating_error_rate_geliot', 'bch_error_rate_geliot']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                # Create a copy without the distribution data
                result_copy = {k: v for k, v in result.items() if k not in 
                             ['error_dist_powielanie', 'error_dist_bch', 
                              'error_dist_powielanie_ge', 'error_dist_bch_ge']}
                writer.writerow(result_copy)
        
        print(f"\nMain results have been saved to {csv_filename}")
        
        # Save error distributions
        save_error_distributions(results, results_dir, timestamp)
        
        # Print summary of key points
        print("\nKey Points Summary:")
        print("-" * 100)
        print("Error Prob | BSC Channel                      | Gilbert-Eliot Channel")
        print("          | Duplicating | BCH     | Diff     | Duplicating | BCH     | Diff")
        print("-" * 100)
        
        # Print only some strategic points
        strategic_points = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
        for result in results:
            if round(result['error_prob'], 2) in strategic_points:
                bsc_diff = result['bch_error_rate'] - result['duplicating_error_rate']
                ge_diff = result['bch_error_rate_geliot'] - result['duplicating_error_rate_geliot']
                print(f"{result['error_prob']:^10.2f} | "
                      f"{result['duplicating_error_rate']:^10.4f} | "
                      f"{result['bch_error_rate']:^7.4f} | "
                      f"{bsc_diff:^8.4f} | "
                      f"{result['duplicating_error_rate_geliot']:^10.4f} | "
                      f"{result['bch_error_rate_geliot']:^7.4f} | "
                      f"{ge_diff:^8.4f}")
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user. Partial results may have been saved.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        raise


