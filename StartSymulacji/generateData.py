import random

def generate_binary_data(rows, filename="dane2.txt"):
    """
    Generate a specified number of rows with 8-bit binary strings and save to a file.

    :param rows: Number of rows to generate.
    :param filename: Name of the file to save the data.
    :return: None
    """
    with open(filename, "w") as file:
        for _ in range(rows):
            binary_string = ''.join(random.choice('01') for _ in range(8))
            file.write(binary_string + "\n")

if __name__ == "__main__":
    try:
        num_rows = int(input("Enter the number of rows to generate: "))
        if num_rows > 0:
            generate_binary_data(num_rows)
            print(f"Data successfully saved to dane.txt.")
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
