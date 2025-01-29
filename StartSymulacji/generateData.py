import random
import os

def generate_binary_data(rows, filename="dane2.txt"):
    """
    Generate a specified number of rows with 8-bit binary strings and save to a file.

    :param rows: Number of rows to generate.
    :param filename: Name of the file to save the data.
    :return: None
    """
    # Ensure the file is created in the StartSymulacji directory
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(file_path, "w") as file:
        for _ in range(rows):
            # Generate 8-bit binary string
            binary_string = ''.join(random.choice('01') for _ in range(5))
            file.write(binary_string + "\n")

if __name__ == "__main__":
    # Generate 5000 rows of test data by default
    rows = 1000
    generate_binary_data(rows)
    print(f"Generated {rows} rows of test data in dane2.txt")
