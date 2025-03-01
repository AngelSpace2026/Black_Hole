import os
import random
import struct

# Reverse chunks at specified positions
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Add padding if needed
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

    # Reverse specified chunks
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using zlib (default compression level)
def compress_with_zlib(reversed_filename, compressed_filename, chunk_size, positions, previous_size, original_size, first_attempt):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Compress the data using zlib (default level 6)
    compressed_data = reversed_data

    # Pack metadata (original_size, chunk_size, and positions)
    metadata = struct.pack(">Q", original_size)  # Original size
    metadata += struct.pack(">I", chunk_size)    # Chunk size
    metadata += struct.pack(">I", len(positions)) # Number of positions
    metadata += struct.pack(f">{len(positions)}I", *positions) # Positions

    # Combine metadata and compressed data
    full_compressed_data = metadata + compressed_data

    # Get the current compressed size
    compressed_size = len(full_compressed_data)

    if first_attempt:
        # For the first attempt, overwrite the file
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(full_compressed_data)
        first_attempt = False
        return compressed_size, first_attempt
    elif compressed_size < previous_size:
        # Save the smaller compressed file and print improvement
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(full_compressed_data)
        previous_size = compressed_size
        #print(f"Improved compression with chunk size {chunk_size}, {len(positions)} positions, compressed size {compressed_size}")
        return previous_size, first_attempt
    else:
        return previous_size, first_attempt

# Decompress and restore data using zlib
def decompress_and_restore_zlib(compressed_filename):
    # Check if the compressed file exists
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    # Extract metadata
    original_size = struct.unpack(">Q", compressed_data[:8])[0]
    chunk_size = struct.unpack(">I", compressed_data[8:12])[0]
    num_positions = struct.unpack(">I", compressed_data[12:16])[0]
    positions = list(struct.unpack(f">{num_positions}I", compressed_data[16:16 + num_positions * 4]))

    # Reconstruct data (after metadata)
    data = compressed_data[16 + num_positions * 4:]

    # Decompress the data using zlib
    decompressed_data = data

    # Reverse chunks back (applying the inverse of the chunk reversal)
    chunked_data = [decompressed_data[i:i + chunk_size] for i in range(0, len(decompressed_data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    # Combine the chunks
    restored_data = b"".join(chunked_data)

    # Ensure the restored file matches the original file size
    restored_data = restored_data[:original_size]

    # Write the restored data to a new file
    restored_filename = compressed_filename.replace('.compressed.bin', '')
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    # Ensure the restored file is saved without the .jpg extension
    final_restored_filename = restored_filename.replace('.restored', '')  # Remove the .restored part, keeping original name
    os.rename(restored_filename, final_restored_filename)

    print(f"Restored data written to {final_restored_filename}")

# Find the best chunk strategy and keep searching
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')
    best_count = 0

    previous_size = 10**12  # Large number to ensure first compression
    first_attempt = True

    while True:
        for exp in range(31):  # Iterate over powers of 2 up to 2^31
            chunk_size = 2 ** exp
            if chunk_size > file_size:
                break

            max_positions = file_size // chunk_size
            if max_positions > 0:
                positions_count = random.randint(1, min(max_positions, 64))
                positions = random.sample(range(max_positions), positions_count)

                reversed_filename = f"{input_filename}.reversed.bin"
                reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions)

                compressed_filename = f"{input_filename}.compressed.bin"
                compressed_size, first_attempt = compress_with_zlib(reversed_filename, compressed_filename, chunk_size, positions, previous_size, file_size, first_attempt)

                if compressed_size < previous_size:
                    previous_size = compressed_size
                    best_chunk_size = chunk_size
                    best_positions = positions
                    best_compression_ratio = compressed_size / file_size
                    best_count += 1

                    print(f"Improved compression with chunk size {chunk_size} and {len(positions)} reversed positions. Compression ratio: {best_compression_ratio:.4f}")

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
        if not os.path.exists(input_filename):
            print(f"Error: File {input_filename} not found!")
            return
        find_best_chunk_strategy(input_filename)  # Infinite search

    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"
        if not os.path.exists(compressed_filename):
            print(f"Error: Compressed file {compressed_filename} not found!")
            return
        decompress_and_restore_zlib(compressed_filename)

if __name__ == "__main__":
    main()