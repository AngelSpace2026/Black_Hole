import os
import random
import struct
import paq
from itertools import permutations

# ==============================
# Transformation Functions
# ==============================

def reverse_chunks(data, chunk_size, positions):
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def add_random_bytes(data, num_bytes=4):
    num_insertions = max(1, len(data) // 100)
    for _ in range(num_insertions):
        pos = random.randint(0, max(0, len(data) - num_bytes))
        data = data[:pos] + os.urandom(num_bytes) + data[pos:]
    return data

def subtract_bytes(data):
    value = random.randint(1, 2**64-1)
    modified_data = bytes([(byte - value) % 256 for byte in data])
    return struct.pack(">Q", value) + modified_data

def move_bits(data, shift_min=1, shift_max=2**32 - 1):
    modified_data = bytearray()
    for byte in data:
        shift = random.randint(shift_min, shift_max)
        modified_data.append((byte << shift) & 0xFF)
        modified_data.append((byte >> shift) & 0xFF)
    return bytes(modified_data)

# ==============================
# Compression & Decompression
# ==============================

def compress_paq(data, chunk_size, positions, original_size, strategy_index):
    """Compress data with PAQ and store metadata."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">B", strategy_index)  # Store strategy as an index (integer)
    return paq.compress(metadata + data)

def decompress_paq(compressed_filename):
    """Decompress and restore file."""
    with open(compressed_filename, 'rb') as infile:
        decompressed_data = paq.decompress(infile.read())

    original_size, chunk_size, num_positions = struct.unpack(">IIB", decompressed_data[:9])
    positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
    strategy_index = struct.unpack(">B", decompressed_data[9 + num_positions * 4:10 + num_positions * 4])[0]

    # Restore the original data using the stored strategy
    restored_data = reverse_chunks(decompressed_data[10 + num_positions * 4:], chunk_size, positions)
    restored_data = restored_data[:original_size]

    restored_filename = compressed_filename.replace('.compressed.bin', '')
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompression complete. Restored file: {restored_filename}")

# ==============================
# Find Best Compression Strategy
# ==============================

def apply_transformations(data, chunk_size, positions, transformations):
    """Apply the given transformations in order."""
    for transform in transformations:
        if transform == "reverse":
            data = reverse_chunks(data, chunk_size, positions)
        elif transform == "add":
            data = add_random_bytes(data)
        elif transform == "subtract":
            data = subtract_bytes(data)
        elif transform == "move_bits":
            data = move_bits(data)
    return data

def find_best_strategy(input_filename, max_iterations):
    """Find the best compression strategy out of all 24 (4!) possible combinations."""
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
    file_size = len(file_data)

    best_ratio = float('inf')
    best_data = None
    best_strategy_index = None

    all_strategies = list(permutations(["reverse", "add", "subtract", "move_bits"]))

    for _ in range(max_iterations):
        chunk_size = random.randint(1, min(256, file_size))
        num_positions = random.randint(0, min(file_size // chunk_size, 64))
        positions = sorted(random.sample(range(file_size // chunk_size), num_positions)) if num_positions > 0 else []

        for i, strategy in enumerate(all_strategies):
            transformed_data = apply_transformations(file_data, chunk_size, positions, strategy)
            compressed_data = compress_paq(transformed_data, chunk_size, positions, file_size, i)
            compression_ratio = len(compressed_data) / file_size

            if compression_ratio < best_ratio:
                best_ratio = compression_ratio
                best_data = compressed_data
                best_strategy_index = i  # Store strategy as an index

    return best_data, best_ratio, best_strategy_index

# ==============================
# Run Compression
# ==============================

def run_compression(input_filename):
    """Runs 7200 iterations to find the best compression strategy and saves the compressed file."""
    best_data, best_ratio, best_strategy_index = find_best_strategy(input_filename, 24)
    if best_data:
        compressed_filename = f"{input_filename}.compressed.bin"
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(best_data)
        print(f"Best compression saved as: {compressed_filename} (Strategy Index: {best_strategy_index})")
        return compressed_filename
    return None

def main():
    """Main user interaction for compression and extraction."""
    print("Created by Jurijus Pacalovas.")
    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for extract): "))
            if mode not in [1, 2]:
                print("Error: Please enter 1 or 2.")
            else:
                break
        except ValueError:
            print("Error: Invalid input. Enter a number (1 or 2).")

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        compressed_filename = run_compression(input_filename)
        if compressed_filename:
            decompress_paq(compressed_filename)
    elif mode == 2:
        compressed_filename = input("Enter the compressed file name: ")
        decompress_paq(compressed_filename)

if __name__ == "__main__":
    main()
