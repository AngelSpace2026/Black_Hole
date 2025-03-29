import os
import random
import struct
import paq

# Constants
MAX_POSITIONS = 64  # Maximum number of chunk positions to reverse

def reverse_chunks(data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def apply_calculus(data, calculus_value):
    """Applies bitwise transformations to each byte."""
    transformed_data = bytearray(data)
    for i in range(len(transformed_data)):
        transformed_data[i] ^= (calculus_value & 0xFF)  # XOR with last 8 bits
    return bytes(transformed_data)

def compress_data(data, chunk_size, positions, original_size, calculus_value):
    """Compresses data using PAQ and embeds metadata."""
    # Adding 7 items for packing (original_size, chunk_size, calculus_value, num_positions, positions)
    metadata = struct.pack(">III", original_size, chunk_size, calculus_value) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions)
    return paq.compress(metadata + data)

def decompress_data(compressed_data):
    """Decompresses data and extracts metadata."""
    try:
        decompressed_data = paq.decompress(compressed_data)
        original_size, chunk_size, calculus_value = struct.unpack(">III", decompressed_data[:12])
        num_positions = struct.unpack(">B", decompressed_data[12:13])[0]
        positions = struct.unpack(f">{num_positions}I", decompressed_data[13:13 + num_positions * 4])

        restored_data = reverse_chunks(decompressed_data[13 + num_positions * 4:], chunk_size, positions)
        restored_data = apply_calculus(restored_data, calculus_value)  # Reverse calculus
        return restored_data[:original_size]

    except (struct.error, paq.error) as e:
        raise Exception(f"Error during decompression: {e}") from None

def find_best_iteration(input_data, max_iterations):
    """Finds the best compression within a specified number of iterations using a heuristic."""
    best_compression_ratio = float('inf')
    best_compressed_data = None

    for _ in range(max_iterations):
        chunk_size = random.randint(2**7, 2**17 - 1)  # Random chunk size in the range 2⁷ to 2¹⁷
        x = random.randint(7, 17)  # Randomly choose x between 7 and 17
        calculus_value = random.randint(1, (2**x) - 1)  # Random value from 1 to (2ˣ - 1)
        
        num_positions = random.randint(0, min(len(input_data) // chunk_size, MAX_POSITIONS))
        positions = sorted(random.sample(range(len(input_data) // chunk_size), num_positions)) if num_positions > 0 else []

        transformed_data = apply_calculus(input_data, calculus_value)
        reversed_data = reverse_chunks(transformed_data, chunk_size, positions)
        compressed_data = compress_data(reversed_data, chunk_size, positions, len(input_data), calculus_value)

        compression_ratio = len(compressed_data) / len(input_data)

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data

    return best_compressed_data, best_compression_ratio

def process_large_file(input_filename, output_filename, mode, attempts=1, iterations=100):
    """Handles large files in chunks and applies compression or decompression."""
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Error: Input file '{input_filename}' not found.")

    with open(input_filename, 'rb') as infile:
        file_data = infile.read()

    if mode == "compress":
        best_compressed_data, best_ratio = find_best_iteration(file_data, iterations)
        if best_compressed_data:
            with open(output_filename, 'wb') as outfile:
                outfile.write(best_compressed_data)
            print(f"Best compression saved as: {output_filename}, ratio: {best_ratio:.4f}")

    elif mode == "decompress":
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()
        try:
            restored_data = decompress_data(compressed_data)
            with open(output_filename, 'wb') as outfile:
                outfile.write(restored_data)
            print(f"Decompression complete. Restored file: {output_filename}")
        except Exception as e:
            print(f"Error during decompression: {e}")

def main():
    print("Created by Jurijus Pacalovas.")

    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for decompress): "))
            if mode not in [1, 2]:
                print("Error: Please enter 1 for compress or 2 for decompress.")
            else:
                break
        except ValueError:
            print("Error: Invalid input. Please enter a number (1 or 2).")

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        output_filename = input("Enter output file name (e.g., output.compressed.bin): ")
        
        # Ask for number of attempts and iterations
        while True:
            try:
                attempts = int(input("Enter the number of attempts (e.g., 5): "))
                iterations = int(input("Enter the number of iterations (e.g., 100): "))
                if attempts <= 0 or iterations <= 0:
                    print("Please enter positive integers for both attempts and iterations.")
                else:
                    break
            except ValueError:
                print("Error: Please enter valid numbers for attempts and iterations.")
        
        process_large_file(input_filename, output_filename, "compress", attempts=attempts, iterations=iterations)

    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to decompress: ")
        output_filename = input("Enter the name for the decompressed file: ")
        process_large_file(compressed_filename, output_filename, "decompress")

if __name__ == "__main__":
    main()