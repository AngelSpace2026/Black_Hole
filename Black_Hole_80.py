import os
import random
import struct
import time
import paq

# Function to reverse chunks at specific positions
def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

# Function to subtract a random large number
def subtract_large_number(data):
    """Subtracts a large number (1 to 2**64-1) from the data."""
    large_number = random.randint(1, 2**64 - 1)
    modified_data = bytearray(data)
    for i in range(len(modified_data)):
        modified_data[i] = (modified_data[i] - (large_number % 256)) % 256
    return bytes(modified_data)

# Function to move bits randomly
def move_bits_randomly(data):
    """Moves bits left or right randomly."""
    shift = random.randint(1, 2**64 - 1) % 8  # Shifting only within 8 bits
    return bytes(((byte >> shift) | (byte << (8 - shift))) & 0xFF for byte in data)

# Function to compress with PAQ
def compress_with_paq(data, chunk_size, positions, original_size, strategy):
    """Compresses data using PAQ and embeds metadata."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">B", strategy)  
    compressed_data = paq.compress(metadata + data)
    return compressed_data

# Function to decompress
def decompress_and_restore_paq(compressed_filename):
    """Decompresses PAQ-compressed data and restores the original file."""
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()
    
    decompressed_data = paq.decompress(compressed_data)

    if len(decompressed_data) < 9:
        print("Error: Decompressed data is too short.")
        return

    # Extract metadata
    original_size = struct.unpack(">I", decompressed_data[:4])[0]
    chunk_size = struct.unpack(">I", decompressed_data[4:8])[0]
    num_positions = struct.unpack(">B", decompressed_data[8:9])[0]

    offset = 9
    positions = []
    if num_positions > 0:
        positions = list(struct.unpack(f">{num_positions}I", decompressed_data[offset:offset + num_positions * 4]))
        offset += num_positions * 4

    strategy = struct.unpack(">B", decompressed_data[offset:offset + 1])[0]
    offset += 1

    compressed_data_only = decompressed_data[offset:]

    # Reverse the strategy
    if strategy == 1:
        restored_data = reverse_chunks_at_positions(compressed_data_only, chunk_size, positions)
    elif strategy == 2:
        restored_data = reverse_chunks_at_positions(compressed_data_only, chunk_size, positions)
        restored_data = restored_data[:original_size]
    elif strategy == 3:
        restored_data = reverse_chunks_at_positions(compressed_data_only, chunk_size, positions)
        restored_data = subtract_large_number(restored_data)
    elif strategy == 4:
        restored_data = reverse_chunks_at_positions(compressed_data_only, chunk_size, positions)
        restored_data = move_bits_randomly(restored_data)

    # Save the decompressed file
    output_filename = compressed_filename.replace(".compressed.bin", "")
    with open(output_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompression completed. Restored file saved as: {output_filename}")

# Function to find the best compression attempt
def find_best_compression(input_filename, attempts=30, iterations=7200):
    """Finds the best compression attempt among multiple strategies."""
    try:
        with open(input_filename, 'rb') as infile:
            file_data = infile.read()
            file_size = len(file_data)
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        return

    best_compression_ratio = float('inf')
    best_compressed_data = None
    best_strategy = None
    best_attempt = None

    for attempt in range(1, attempts + 1):
        print(f"Running compression attempt {attempt}/{attempts} with {iterations} iterations...")
        chunk_size = random.randint(1, min(256, file_size))
        max_positions = file_size // chunk_size
        num_positions = random.randint(0, min(max_positions, 64))
        positions = sorted(random.sample(range(max_positions), num_positions)) if num_positions > 0 else []

        # Apply different strategies
        if attempt % 4 == 1:
            modified_data = reverse_chunks_at_positions(file_data, chunk_size, positions)  # Strategy 1
        elif attempt % 4 == 2:
            modified_data = reverse_chunks_at_positions(file_data, chunk_size, positions)  # Strategy 2
        elif attempt % 4 == 3:
            modified_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
            modified_data = subtract_large_number(modified_data)  # Strategy 3
        else:
            modified_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
            modified_data = move_bits_randomly(modified_data)  # Strategy 4

        compressed_data = compress_with_paq(modified_data, chunk_size, positions, file_size, attempt % 4)
        compression_ratio = len(compressed_data) / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
            best_strategy = attempt % 4
            best_attempt = attempt

    # Save only the best compressed file
    compressed_filename = f"{input_filename}.compressed.bin"
    with open(compressed_filename, 'wb') as outfile:
        outfile.write(best_compressed_data)

    print(f"\nBest of {attempts} compression saved as: {compressed_filename} (Strategy {best_strategy})")

# Main function
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
        find_best_compression(input_filename)
    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to extract: ")
        decompress_and_restore_paq(compressed_filename)

# Run the program
if __name__ == "__main__":
    main()