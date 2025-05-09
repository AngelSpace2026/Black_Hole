import os
import random
import struct
import paq

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def compress_with_paq(data, chunk_size, positions, original_size, strategy):
    """Compresses data using PAQ and embeds metadata, including the strategy."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">B", strategy)
    return paq.compress(metadata + data)

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file."""
    while not os.path.exists(compressed_filename):
        print(f"Error: File '{compressed_filename}' not found.")
        compressed_filename = input("Enter a valid compressed file name: ")

    try:
        with open(compressed_filename, 'rb') as infile:
            decompressed_data = paq.decompress(infile.read())

        original_size, chunk_size, num_positions = struct.unpack(">IIB", decompressed_data[:9])
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        strategy = struct.unpack(">B", decompressed_data[9 + num_positions * 4:10 + num_positions * 4])[0]

        restored_data = reverse_chunks_at_positions(decompressed_data[10 + num_positions * 4:], chunk_size, positions)
        restored_data = restored_data[:original_size]

        restored_filename = compressed_filename.replace('.compressed.bin', '')
        restored_filename += ''

        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)

        print(f"Decompression complete. Restored file: {restored_filename}")

    except Exception as e:
        print(f"Error during decompression: {e}")

def add_random_bytes(data, num_bytes=4):
    """Adds random 4-byte sequences at random positions."""
    num_insertions = max(1, len(data) // 100)
    for _ in range(num_insertions):
        pos = random.randint(0, max(0, len(data) - num_bytes))
        data = data[:pos] + os.urandom(num_bytes) + data[pos:]
    return data

def find_best_chunk_strategy(input_filename, max_iterations):
    """Finds the best chunk size and reversal positions for compression."""
    while not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' not found.")
        input_filename = input("Enter a valid input file name: ")

    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
        file_size = len(file_data)

    best_compression_ratio = float('inf')
    best_compressed_data = None

    for i in range(max_iterations):
        chunk_size = random.randint(1, min(256, file_size))
        num_positions = random.randint(0, min(file_size // chunk_size, 64))
        positions = sorted(random.sample(range(file_size // chunk_size), num_positions)) if num_positions > 0 else []

        reversed_data_1 = reverse_chunks_at_positions(file_data, chunk_size, positions)
        compressed_data_1 = compress_with_paq(reversed_data_1, chunk_size, positions, file_size, 0)
        compression_ratio_1 = len(compressed_data_1) / file_size

        reversed_data_2 = reverse_chunks_at_positions(file_data, chunk_size, positions)
        modified_data_2 = add_random_bytes(reversed_data_2)
        compressed_data_2 = compress_with_paq(modified_data_2, chunk_size, positions, file_size, 1)
        compression_ratio_2 = len(compressed_data_2) / file_size

        # Keep the best compression ratio (smallest)
        if compression_ratio_1 < compression_ratio_2 and compression_ratio_1 < best_compression_ratio:
            best_compression_ratio = compression_ratio_1
            best_compressed_data = compressed_data_1
        elif compression_ratio_2 < best_compression_ratio:
            best_compression_ratio = compression_ratio_2
            best_compressed_data = compressed_data_2

        # Remove intermediate files after each iteration
        temp_filename_1 = f"{input_filename}_{i}_1.compressed.bin"
        temp_filename_2 = f"{input_filename}_{i}_2.compressed.bin"

        if os.path.exists(temp_filename_1):
            os.remove(temp_filename_1)
        if os.path.exists(temp_filename_2):
            os.remove(temp_filename_2)

    # Save only the best compression result
    best_compressed_filename = f"{input_filename}.compressed.bin"
    with open(best_compressed_filename, 'wb') as outfile:
        outfile.write(best_compressed_data)

    print(f"Best compression result saved as: {best_compressed_filename}")

    return best_compressed_filename

def main():
    print("Created by Jurijus Pacalovas.")

    # Ask the user for the operation (1 = compress, 2 = extract)
    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for extract): "))
            if mode not in [1, 2]:
                print("Error: Please enter 1 for compress or 2 for extract.")
            else:
                break
        except ValueError:
            print("Error: Invalid input. Please enter a number (1 or 2).")

    # If mode is 1 (compress), ask for the file name and run compression
    if mode == 1:
        input_filename = input("Enter input file name to compress (letters and numbers allowed): ")

        # Run the process 7200 times and select the best compression result
        best_compressed_filename = find_best_chunk_strategy(input_filename, 7200)

        # Decompress after selecting the best compression result
        decompress_and_restore_paq(best_compressed_filename)

    # If mode is 2 (extract), ask for the compressed file and run decompression
    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to extract: ")
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()