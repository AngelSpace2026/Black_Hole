import random
import os
import paq
print("Created by Jurijus Pacalovas.")

def compress(data):
    """Compress data using zlib."""
    return paq.compress(data)

def decompress(data):
    """Decompress data using zlib."""
    return paq.decompress(data)

def compress_file_with_prng_size_adjustment(target_size, max_attempts=100, max_random_bytes=100):
    """
    Compresses a file, attempting to adjust size using a PRNG before compression.

    Args:
        target_size: The desired compressed file size in bytes.
        max_attempts: The maximum number of attempts to adjust the size.
        max_random_bytes: The maximum number of random bytes to prepend in each attempt.
    """
    input_filename = input("Enter input filename: ")
    if not os.path.exists(input_filename):
        print("File not found.")
        return

    try:
        with open(input_filename, 'rb') as infile:
            data = infile.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Attempt to adjust size by prepending random data
    best_compressed_data = None
    min_size_difference = float('inf')

    for _ in range(max_attempts):
        random_prefix = os.urandom(random.randint(0, max_random_bytes))
        adjusted_data = random_prefix + data
        compressed_data = compress(adjusted_data)
        size_difference = abs(len(compressed_data) - target_size)

        if size_difference < min_size_difference:
            min_size_difference = size_difference
            best_compressed_data = compressed_data

    output_filename = input_filename + ".b"
    try:
        with open(output_filename, 'wb') as outfile:
            outfile.write(best_compressed_data)
        print(f"File compressed to {output_filename} (size difference: {min_size_difference} bytes)")
    except Exception as e:
        print(f"Error compressing or writing file: {e}")


def extract_file():
    """Extracts a file compressed with zlib."""
    input_filename = input("Enter input filename (.b file): ")
    if not os.path.exists(input_filename):
        print("File not found.")
        return

    output_filename = input_filename.rsplit('.', 1)[0]  # Automatically derive output filename
    try:
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()
        with open(output_filename, 'wb') as outfile:
            outfile.write(decompress(compressed_data))
        print(f"File extracted to {output_filename}")
    except Exception as e:
        print(f"Error extracting or writing file: {e}")


def main():
    print("Select an option:")
    print("1. Compress File (with PRNG size adjustment)")
    print("2. Extract File")
    option = input("Enter option (1 or 2): ")

    if option == '1':
        while True:  # Loop until valid integer input is received
            try:
                target_size = 1000  # You can adjust this as needed
                break  # Exit loop if input is a valid integer
            except ValueError:
                print("Invalid input. Please enter a numerical value for the target size.")
        compress_file_with_prng_size_adjustment(target_size)
    elif option == '2':
        extract_file()
    else:
        print("Invalid option.")

if __name__ == '__main__':
    main()