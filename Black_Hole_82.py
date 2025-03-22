import os
import random
import struct
import time
import paq

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def flip_2bit_pairs(data):
    """Flips 2-bit pairs in the byte data."""
    modified_data = bytearray(data)
    for i in range(0, len(modified_data) * 8, 2):  # Process in 2-bit steps
        byte_index = i // 8
        bit_position = i % 8

        if byte_index < len(modified_data):
            byte = modified_data[byte_index]

            # Extract the 2-bit pair
            bit_pair = (byte >> (6 - bit_position)) & 0b11

            # Flip the 2-bit pair
            flipped_pair = bit_pair ^ 0b11  # Invert both bits

            # Update the byte
            modified_data[byte_index] = (byte & ~(0b11 << (6 - bit_position))) | (flipped_pair << (6 - bit_position))

    return bytes(modified_data)

def compress_with_paq(data, chunk_size, positions, original_size, strategy):
    """Compresses data using PAQ and embeds metadata, including the strategy."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">B", strategy)
    return paq.compress(metadata + data)

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file."""
    if not os.path.exists(compressed_filename):
        print(f"Error: File '{compressed_filename}' not found.")
        return

    try:
        with open(compressed_filename, 'rb') as infile:
            decompressed_data = paq.decompress(infile.read())

        original_size, chunk_size, num_positions = struct.unpack(">IIB", decompressed_data[:9])
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        strategy = struct.unpack(">B", decompressed_data[9 + num_positions * 4:10 + num_positions * 4])[0]

        restored_data = reverse_chunks_at_positions(decompressed_data[10 + num_positions * 4:], chunk_size, positions)
        restored_data = flip_2bit_pairs(restored_data)  # Restore the flipped 2-bit pairs
        restored_data = restored_data[:original_size]

        restored_filename = compressed_filename.replace('.compressed.bin', '')

        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)

        print(f"Decompression complete. Restored file: {restored_filename}")

    except Exception as e:
        print(f"Error during decompression: {e}")

def find_best_iteration(input_filename, max_iterations):
    """Finds the best compression within a single attempt."""
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
        file_size = len(file_data)

    best_compression_ratio = float('inf')
    best_compressed_data = None

    for _ in range(max_iterations):
        chunk_size = random.randint(1, min(256, file_size))
        num_positions = random.randint(0, min(file_size // chunk_size, 64))
        positions = sorted(random.sample(range(file_size // chunk_size), num_positions)) if num_positions > 0 else []

        modified_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
        modified_data = flip_2bit_pairs(modified_data)  # Apply 2-bit flipping

        compressed_data = compress_with_paq(modified_data, chunk_size, positions, file_size, 0)
        compression_ratio = len(compressed_data) / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data

    return best_compressed_data, best_compression_ratio

def run_compression(input_filename):
    """Runs 4 attempts, each with 300 iterations, and keeps only the best compression result."""
    best_of_4_compressed_data = None
    best_of_4_ratio = float('inf')

    for i in range(4):
        print(f"Running compression attempt {i+1}/4 with 300 iterations...")
        compressed_data, compression_ratio = find_best_iteration(input_filename, 300)

        if compressed_data and compression_ratio < best_of_4_ratio:
            best_of_4_ratio = compression_ratio
            best_of_4_compressed_data = compressed_data

    # Save the best compression result
    final_compressed_filename = f"{input_filename}.compressed.bin"
    with open(final_compressed_filename, 'wb') as outfile:
        outfile.write(best_of_4_compressed_data)

    print(f"Best compression saved as: {final_compressed_filename}")
    return final_compressed_filename

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

        # Run 4 compression attempts, each with 300 iterations
        best_compressed_filename = run_compression(input_filename)

        # Decompress the best compression result
        decompress_and_restore_paq(best_compressed_filename)

    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to extract: ")
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()