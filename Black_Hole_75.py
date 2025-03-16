import os
import random
import struct
import time
import paq

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

def compress_with_paq(data, chunk_size, positions, original_size, strategy):
    """Compresses data using PAQ and embeds metadata, including the strategy."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">B", strategy)  # Add strategy bit to metadata
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
        num_positions = struct.unpack(">B", decompressed_data[8:9])[0]
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        strategy = struct.unpack(">B", decompressed_data[9 + num_positions * 4: 9 + num_positions * 4 + 1])[0]  # Extract strategy bit
        restored_data = reverse_chunks_at_positions(decompressed_data[9 + num_positions * 4 + 1:], chunk_size, positions)
        restored_data = restored_data[:original_size]
        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")
    except FileNotFoundError:
        print(f"Error: File not found: {compressed_filename}")
    except Exception as e:  # Catch any other exceptions
        print(f"Decompression failed: {e}")


def add_random_bytes(data, num_bytes=4):
    """Adds random 4-byte sequences at random positions."""
    num_insertions = max(1, len(data) // 100)
    for _ in range(num_insertions):
        pos = random.randint(0, max(0, len(data) - num_bytes))
        data = data[:pos] + os.urandom(num_bytes) + data[pos:]
    return data

def find_best_chunk_strategy(input_filename, max_time_seconds):
    """Finds the best chunk size and reversal positions for compression, automatically choosing the best strategy."""
    try:
        with open(input_filename, 'rb') as infile:
            file_data = infile.read()
            file_size = len(file_data)
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return

    best_compression_ratio = float('inf')
    best_chunk_size = 1
    best_positions = []
    best_strategy = None
    start_time = time.time()

    iteration = 0
    while time.time() - start_time < max_time_seconds:
        iteration += 1
        chunk_size = random.randint(1, min(256, file_size))
        max_positions = file_size // chunk_size
        num_positions = random.randint(0, min(max_positions, 64))
        positions = sorted(random.sample(range(max_positions), num_positions)) if num_positions > 0 else []

        # Strategy 1: Basic reversal
        reversed_data_1 = reverse_chunks_at_positions(file_data, chunk_size, positions)
        compressed_data_1 = compress_with_paq(reversed_data_1, chunk_size, positions, file_size, 0)  # strategy 0
        compression_ratio_1 = len(compressed_data_1) / file_size

        # Strategy 2: Reversal + random bytes
        reversed_data_2 = reverse_chunks_at_positions(file_data, chunk_size, positions)
        modified_data_2 = add_random_bytes(reversed_data_2)
        compressed_data_2 = compress_with_paq(modified_data_2, chunk_size, positions, file_size, 1)  # strategy 1
        compression_ratio_2 = len(compressed_data_2) / file_size

        # Choose the better strategy automatically
        if compression_ratio_1 < compression_ratio_2 and compression_ratio_1 < best_compression_ratio:
            best_compression_ratio = compression_ratio_1
            best_chunk_size = chunk_size
            best_positions = positions
            best_strategy = 0
            print(f"Improved compression (Strategy 1): {len(compressed_data_1)} bytes (ratio: {compression_ratio_1:.4f})")
        elif compression_ratio_2 < best_compression_ratio:
            best_compression_ratio = compression_ratio_2
            best_chunk_size = chunk_size
            best_positions = positions
            best_strategy = 1
            print(f"Improved compression (Strategy 2): {len(compressed_data_2)} bytes (ratio: {compression_ratio_2:.4f})")

    print(f"\nBest compression achieved after {iteration} iterations (time limit: {max_time_seconds} seconds):")
    print(f"Strategy: {best_strategy}")
    print(f"Compression ratio: {best_compression_ratio:.4f}")
    print(f"Chunk size: {best_chunk_size}")
    print(f"Positions: {best_positions}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")

    compressed_filename = f"{input_filename}.compressed.bin"
    try:
        with open(compressed_filename, 'wb') as outfile:
            if best_strategy == 0:
                compressed_data = compress_with_paq(reverse_chunks_at_positions(file_data, best_chunk_size, best_positions), best_chunk_size, best_positions, file_size, 0)
            else:
                compressed_data = compress_with_paq(add_random_bytes(reverse_chunks_at_positions(file_data, best_chunk_size, best_positions)), best_chunk_size, best_positions, file_size, 1)
            outfile.write(compressed_data)
        print(f"Compressed file saved as {compressed_filename}")
    except Exception as e:
        print(f"Error writing compressed file: {e}")

def main():
    print("Created by Jurijus Pacalovas.")

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
        max_time_seconds = int(input("Enter maximum time limit for compression (in seconds): "))
        find_best_chunk_strategy(input_filename, max_time_seconds)
    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to extract: ")
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()