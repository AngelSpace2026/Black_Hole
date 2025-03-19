import os
import random
import struct
import paq
import time

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def subtract_random_value(data):
    value = random.randint(1, 2**64 - 1)
    modified_data = bytes((byte - (value % 256)) % 256 for byte in data)
    return modified_data, value  

def move_bits_randomly(data):
    shift_amount = random.randint(1, 31)
    modified_data = bytearray()
    for byte in data:
        modified_data.append((byte << shift_amount) & 0xFF)
        modified_data.append((byte >> shift_amount) & 0xFF)
    return bytes(modified_data), shift_amount

def apply_all_transformations(data, chunk_size, positions):
    data = reverse_chunks_at_positions(data, chunk_size, positions)
    data, sub_value = subtract_random_value(data)
    data, shift_value = move_bits_randomly(data)
    return data, sub_value, shift_value

def compress_with_paq(data, metadata):
    return paq.compress(metadata + data)

def decompress_and_restore_paq(compressed_filename):
    try:
        with open(compressed_filename, 'rb') as infile:
            decompressed_data = paq.decompress(infile.read())

        if len(decompressed_data) < 19:
            print("Error: Insufficient metadata in decompressed file.")
            return

        metadata_size = struct.calcsize(">IIBQH")
        metadata = decompressed_data[:metadata_size]
        original_size, chunk_size, num_positions, sub_value, shift_value = struct.unpack(">IIBQH", metadata)

        if len(decompressed_data) < metadata_size + num_positions * 4:
            print("Error: Not enough bytes to read positions.")
            return
        
        positions = struct.unpack(f">{num_positions}I", decompressed_data[metadata_size:metadata_size + num_positions * 4])
        restored_data = decompressed_data[metadata_size + num_positions * 4:]

        restored_data = bytearray(restored_data)
        
        for i in range(0, len(restored_data), 2):
            restored_data[i] = (restored_data[i] >> shift_value) & 0xFF
            if i+1 < len(restored_data):
                restored_data[i+1] = (restored_data[i+1] << shift_value) & 0xFF

        restored_data = bytes((byte + (sub_value % 256)) % 256 for byte in restored_data)
        restored_data = reverse_chunks_at_positions(restored_data, chunk_size, positions)
        
        restored_data = restored_data[:original_size]

        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        print(f"Decompression complete. Restored file: {restored_filename}")
    except Exception as e:
        print(f"Error during decompression: {e}")

def find_best_iteration(input_filename, max_iterations):
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
    file_size = len(file_data)

    best_compression_ratio = float('inf')
    best_compressed_data = None
    best_strategy = None

    for iteration in range(max_iterations):
        chunk_size = random.randint(1, min(256, file_size))
        num_positions = random.randint(0, min(file_size // chunk_size, 64))
        positions = sorted(random.sample(range(file_size // chunk_size), num_positions)) if num_positions > 0 else []

        transformed_data, sub_value, shift_value = apply_all_transformations(file_data, chunk_size, positions)

        metadata = struct.pack(">IIBQH", file_size, chunk_size, len(positions), sub_value, shift_value) + \
                   struct.pack(f">{len(positions)}I", *positions)

        compressed_data = compress_with_paq(transformed_data, metadata)
        compression_ratio = len(compressed_data) / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
            best_strategy = 2  # Strategy for this iteration, 2 means we used all transformations

    return best_compressed_data, best_compression_ratio, best_strategy

def run_compression(input_filename, max_attempts, max_iterations):
    best_of_30_compressed_data = None
    best_of_30_ratio = float('inf')
    best_of_30_strategy = None

    for attempt in range(max_attempts):
        print(f"Running attempt {attempt+1} of {max_attempts} with {max_iterations} iterations...")
        compressed_data, compression_ratio, strategy = find_best_iteration(input_filename, max_iterations)

        if compressed_data and compression_ratio < best_of_30_ratio:
            best_of_30_ratio = compression_ratio
            best_of_30_compressed_data = compressed_data
            best_of_30_strategy = strategy

    final_compressed_filename = f"{input_filename}.compressed.bin"
    with open(final_compressed_filename, 'wb') as outfile:
        outfile.write(best_of_30_compressed_data)

    print(f"Best of 30 compression saved as: {final_compressed_filename} (Strategy {best_of_30_strategy})")

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
        compressed_filename = run_compression(input_filename, max_attempts=1, max_iterations=24)
        decompress_and_restore_paq(compressed_filename)
    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to extract: ")
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()