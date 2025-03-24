import os
import random
import struct
import paq

# Constants for clarity
METADATA_HEADER_SIZE = 9  # Size of the metadata header in bytes
MAX_POSITIONS = 64       # Maximum number of chunk positions to reverse

def reverse_chunks(data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def add_random_bytes(data, num_insertions, num_bytes=1):
    """Adds random bytes at random positions."""
    for _ in range(num_insertions):
        pos = random.randint(0, max(0, len(data) - num_bytes))
        data = data[:pos] + os.urandom(num_bytes) + data[pos:]
    return data


def compress_data(data, chunk_size, positions, original_size):
    """Compresses data using PAQ and embeds metadata."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions)
    return paq.compress(metadata + data)

def decompress_data(compressed_data):
    """Decompresses data and extracts metadata."""
    try:
        decompressed_data = paq.decompress(compressed_data)
        original_size, chunk_size, num_positions = struct.unpack(">IIB", decompressed_data[:METADATA_HEADER_SIZE])
        positions = struct.unpack(f">{num_positions}I", decompressed_data[METADATA_HEADER_SIZE:METADATA_HEADER_SIZE + num_positions * 4])
        restored_data = reverse_chunks(decompressed_data[METADATA_HEADER_SIZE + num_positions * 4:], chunk_size, positions)
        return restored_data[:original_size]
    except (struct.error, paq.error) as e:
        raise Exception(f"Error during decompression: {e}") from None


def find_best_iteration(input_data, max_iterations):
    """Finds the best compression within a specified number of iterations using a heuristic."""
    best_compression_ratio = float('inf')
    best_compressed_data = None
    best_chunk_size = 0

    for _ in range(max_iterations):
        # Adaptive chunk size: Start with a medium size, adjust based on previous results
        chunk_size = best_chunk_size or min(128, len(input_data) // 2)  # Default to half the data length

        num_positions = random.randint(0, min(len(input_data) // chunk_size, MAX_POSITIONS))
        positions = sorted(random.sample(range(len(input_data) // chunk_size), num_positions)) if num_positions > 0 else []

        reversed_data = reverse_chunks(input_data, chunk_size, positions)
        compressed_data = compress_data(reversed_data, chunk_size, positions, len(input_data))
        compression_ratio = len(compressed_data) / len(input_data)

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
            best_chunk_size = chunk_size  # Update best chunk size

        # Adjust chunk size based on compression ratio (example heuristic)
        if compression_ratio > 0.8: #If compression is poor, try a different chunk size
            chunk_size = max(1, chunk_size // 2) #Reduce chunk size

    return best_compressed_data, best_compression_ratio


def run_compression(input_filename, num_attempts, iterations_per_attempt):
    """Runs multiple compression attempts and returns the best result."""
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Error: Input file '{input_filename}' not found.")

    with open(input_filename, 'rb') as infile:
        file_data = infile.read()

    best_of_all_compressed_data = None
    best_of_all_ratio = float('inf')

    for i in range(num_attempts):
        print(f"Running compression attempt {i+1}/{num_attempts} with {iterations_per_attempt} iterations...")
        compressed_data, compression_ratio = find_best_iteration(file_data, iterations_per_attempt)
        compressed_size = len(compressed_data)

        print(f"Attempt {i+1} compressed size: {compressed_size} bytes, ratio: {compression_ratio:.4f}")

        if compressed_data and compression_ratio < best_of_all_ratio:
            best_of_all_ratio = compression_ratio
            best_of_all_compressed_data = compressed_data

    return best_of_all_compressed_data, best_of_all_ratio


def decompress_and_restore(compressed_data, output_filename):
    """Decompresses data and saves it to a file."""
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
        num_attempts = 1
        iterations_per_attempt = 300

        try:
            compressed_data, best_ratio = run_compression(input_filename, num_attempts, iterations_per_attempt)
            if compressed_data:
                with open(output_filename, 'wb') as outfile:
                    outfile.write(compressed_data)
                print(f"Best compression saved as: {output_filename}, ratio: {best_ratio:.4f}")
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to decompress: ")
        output_filename = input("Enter the name for the decompressed file: ")

        try:
            with open(compressed_filename, 'rb') as infile:
                compressed_data = infile.read()
                decompress_and_restore(compressed_data, output_filename)
        except FileNotFoundError:
            print(f"Error: File '{compressed_filename}' not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
