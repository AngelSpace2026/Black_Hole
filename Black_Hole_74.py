import os
import random
import struct
import paq
import time
import sys

def manage_leading_zeros(input_data):
    """Strips leading zeros from byte data."""
    if not isinstance(input_data, bytes):
        raise ValueError("Input data must be bytes.")
    stripped_data = input_data.lstrip(b'\x00')
    return stripped_data or b'\x00'

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    padding_needed = (chunk_size - len(chunked_data[-1]) % chunk_size) % chunk_size
    chunked_data[-1] += b'\x00' * padding_needed
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def compress_with_paq(data, chunk_size, positions, original_size):
    """Compresses data using PAQ and embeds metadata."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">I", len(positions)) + struct.pack(f">{len(positions)}I", *positions)
    compressed_data = paq.compress(metadata + data)
    return compressed_data

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file."""
    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()
        decompressed_data = paq.decompress(compressed_data)
        original_size = struct.unpack(">I", decompressed_data[:4])[0]
        chunk_size = struct.unpack(">I", decompressed_data[4:8])[0]
        num_positions = struct.unpack(">I", decompressed_data[8:12])[0]
        positions = struct.unpack(f">{num_positions}I", decompressed_data[12:12 + num_positions * 4])
        restored_data = reverse_chunks_at_positions(decompressed_data[12 + num_positions * 4:], chunk_size, positions)
        restored_data = restored_data[:original_size]
        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")
    except (FileNotFoundError, paq.PAQError, struct.error) as e:
        print(f"Decompression failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during decompression: {e}")


def find_best_chunk_strategy(input_filename, max_consecutive_no_improvements=360000, max_time_seconds=360000, max_iterations=1000001):
    """Finds the best chunk size and reversal positions for compression."""
    try:
        with open(input_filename, 'rb') as infile:
            file_data = infile.read()
            file_size = len(file_data)
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return None  # Return None to indicate failure

    best_compression_ratio = float('inf')
    best_chunk_size = 1
    best_positions = []
    consecutive_no_improvements = 0
    start_time = time.time()

    for iteration in range(max_iterations):
            chunk_size = int(random.uniform(1, min(1024, file_size)))  # Wider chunk size range
            max_positions = file_size // chunk_size
            num_positions = int(random.uniform(0, min(max_positions, 128)))  # More positions allowed
            positions = sorted(random.sample(range(max_positions), num_positions)) if num_positions > 0 else []

            try:
                reversed_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
                compressed_data = compress_with_paq(reversed_data, chunk_size, positions, file_size)
                compression_ratio = len(compressed_data) / file_size

                if compression_ratio < best_compression_ratio:
                    best_compression_ratio = compression_ratio
                    best_chunk_size = chunk_size
                    best_positions = positions
                    consecutive_no_improvements = 0
                    print(f"Improved compression: Ratio: {compression_ratio:.4f}, Size: {len(compressed_data)} bytes") # Only print ratio and size
                else:
                    consecutive_no_improvements += 1
            except Exception as e:
                print(f"Error during iteration {iteration}: {e}")  # Catch errors during iteration.


            if time.time() - start_time > max_time_seconds:
                print("\nTime limit reached.")
                break
            if consecutive_no_improvements >= max_consecutive_no_improvements:
                print(f"\nNo improvement for {max_consecutive_no_improvements} iterations.")
                break

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nBest compression achieved after {iteration + 1} iterations (time limit: {max_time_seconds} seconds, no improvement for {max_consecutive_no_improvements} consecutive iterations):")
    print(f"Compression ratio: {best_compression_ratio:.4f}")
    print(f"Chunk size: {best_chunk_size}")
    print(f"Positions: {best_positions}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    compressed_filename = f"{input_filename}.compressed.bin"
    try:
        with open(compressed_filename, 'wb') as outfile:
            compressed_data = compress_with_paq(reverse_chunks_at_positions(file_data, best_chunk_size, best_positions), best_chunk_size, best_positions, file_size)
            outfile.write(compressed_data)
        print(f"Compressed file saved as {compressed_filename}")
    except Exception as e:
        print(f"Error writing compressed file: {e}")
    return (best_compression_ratio, best_chunk_size, best_positions)


def main():
    print("Created by Jurijus Pacalovas (Improved by Bard).")
    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for extract): "))
            if mode not in [1, 2]:
                print("Error: Please enter 1 for compress or 2 for extract.")
            else:
                break
        except ValueError:
            print("Error: Invalid input. Please enter a number (1 or 2).")

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        find_best_chunk_strategy(input_filename)
    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()
