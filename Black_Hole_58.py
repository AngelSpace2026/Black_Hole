import os
import random
import struct
import paq  # Ensure this module exists or replace it with an external PAQ8PX call

# Reverse chunks at specified positions
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Reverse specified chunks
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    # Write reversed data back
    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, original_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata (original file size, chunk size, and reversed positions)
    metadata = struct.pack(">Q", original_size)  # Store original size
    metadata += struct.pack(">I", chunk_size)  # Chunk size (unsigned int)
    metadata += struct.pack(">I", len(positions))  # Number of positions
    metadata += struct.pack(f">{len(positions)}I", *positions)  # Positions

    # Compress using PAQ
    compressed_data = paq.compress(metadata + reversed_data)

    compressed_size = len(compressed_data)

    # Handle compression results
    if compressed_size < previous_size:
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        return compressed_size  # Update previous size to smaller one
    elif compressed_size >= previous_size:
        return previous_size  # Keep previous size without saving

# Decompress and restore data
def decompress_and_restore_paq(compressed_filename, restored_filename):
    if not os.path.exists(compressed_filename):
        print(f"Error: Incorrect file path '{compressed_filename}'.")
        return

    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()

        # Decompress data
        decompressed_data = paq.decompress(compressed_data)

        # Check if metadata exists
        if len(decompressed_data) < 16:
            print("Error: Incorrect file for extraction.")
            return

        # Extract metadata
        original_size = struct.unpack(">Q", decompressed_data[:8])[0]
        chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]
        num_positions = struct.unpack(">I", decompressed_data[12:16])[0]

        if len(decompressed_data) < (16 + num_positions * 4):
            print("Error: Incorrect file for extraction.")
            return

        positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))

        # Extract chunked data
        chunked_data = decompressed_data[16 + num_positions * 4:]
        total_chunks = len(chunked_data) // chunk_size
        chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

        # Reverse chunks back
        for pos in positions:
            if 0 <= pos < len(chunked_data):
                chunked_data[pos] = chunked_data[pos][::-1]

        # Reconstruct file
        restored_data = b"".join(chunked_data)[:original_size]  # Ensure exact size

        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)

    except Exception:
        print("Error: Incorrect file for extraction.")

# Find the best chunk strategy (runs infinitely)
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    previous_size = 10**12  # Large number for initial comparison
    first_attempt = True  # Track first iteration

    while True:  # Infinite loop
        chunk_size = random.randint(1, 256)  # Random chunk size
        max_positions = file_size // chunk_size
        if max_positions > 0:
            positions_count = random.randint(1, min(max_positions, 64))
            positions = random.sample(range(max_positions), positions_count)

            reversed_file = "reversed_file.bin"
            reverse_chunks_at_positions(input_filename, reversed_file, chunk_size, positions)

            compressed_file = "compressed_file.bin"
            compressed_size = compress_with_paq(reversed_file, compressed_file, chunk_size, positions, previous_size, file_size)

            if first_attempt:
                # Save first compression attempt regardless of size
                previous_size = compressed_size
                first_attempt = False
            elif compressed_size < previous_size:
                # Save only if it's smaller
                previous_size = compressed_size
            elif compressed_size >= previous_size:
                # If bigger or equal, do nothing (keep previous best)
                pass

# Main function
def main():
    print("Created by Jurijus Pacalovas.")

    mode = input("Enter mode (1 for compress, 2 for extract): ")

    if mode == "1":
        input_filename = input("Enter input file name to compress: ")

        # Check if the file exists before proceeding
        if not os.path.exists(input_filename):
            print(f"Error: File '{input_filename}' not found.")
            return

        find_best_chunk_strategy(input_filename)  # Infinite loop runs here
        
    elif mode == "2":
        compressed_filename = input("Enter compressed file name to extract: ")
        restored_filename = input("Enter restored file name: ")

        if not os.path.exists(compressed_filename):
            print(f"Error: Incorrect file path '{compressed_filename}'.")
            return

        decompress_and_restore_paq(compressed_filename, restored_filename)

if __name__ == "__main__":
    main()