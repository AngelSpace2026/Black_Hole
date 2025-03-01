import os
import random
import struct
import paq

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

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, original_size, first_attempt):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata
    metadata = struct.pack(">Q", original_size)  # Original size
    metadata += struct.pack(">I", chunk_size)  # Chunk size
    metadata += struct.pack(">I", len(positions))  # Number of positions
    metadata += struct.pack(f">{len(positions)}I", *positions)  # Positions list

    # Compress the file
    compressed_data = paq.compress(metadata + reversed_data)

    # Add four bytes (0x00630000) at the beginning of the compressed file
    compressed_data = b'\x00\x63\x00\x00' + compressed_data  # Insert marker bytes

    # Get the current compressed size
    compressed_size = len(compressed_data)

    if first_attempt:
        # First attempt always saves the file
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        first_attempt = False  # No longer the first attempt
        return compressed_size, first_attempt
    elif compressed_size < previous_size:
        # Save only if the new compressed size is smaller
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        previous_size = compressed_size
        return previous_size, first_attempt
    else:
        return previous_size, first_attempt  # Don't overwrite if it's larger

# Decompress and restore data
def decompress_and_restore_paq(compressed_filename):
    # Check if the compressed file exists
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    # Read the compressed data
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    # Extract and verify the first four bytes (should be 0x00630000)
    extracted_bytes = compressed_data[:4]  # First four bytes (marker)
    
    if extracted_bytes != b'\x00\x63\x00\x00':
        print(f"Error: Incorrect marker bytes found: {extracted_bytes.hex()}")
        return

    compressed_data = compressed_data[4:]  # Remove the first 4 bytes

    # Decompress the remaining data
    decompressed_data = paq.decompress(compressed_data)

    # Extract metadata
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]  # Original size
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]  # Chunk size
    num_positions = struct.unpack(">I", decompressed_data[12:16])[0]  # Number of reversed positions
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))  # Reversed positions

    # Reconstruct chunks (data after metadata)
    chunked_data = decompressed_data[16 + num_positions * 4:]

    total_chunks = len(chunked_data) // chunk_size
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    # Reverse chunks back
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    # Combine the chunks
    restored_data = b"".join(chunked_data)

    # Ensure the restored data is exactly the size of the original file
    restored_data = restored_data[:original_size]

    # Automatically generate the restored file name
    restored_filename = compressed_filename.replace('.compressed.bin', '')

    # Write the restored data to the file
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompression completed. File saved as {restored_filename}")

# Find the best chunk strategy and keep searching infinitely
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')
    best_count = 0

    previous_size = 10**12  # Use a very large number to ensure first compression happens
    first_attempt = True  # Track if it's the first attempt

    while True:  # Infinite loop to keep improving
        for chunk_size in range(1, 256):
            max_positions = file_size // chunk_size
            if max_positions > 0:
                positions_count = random.randint(1, min(max_positions, 64))
                positions = random.sample(range(max_positions), positions_count)

                reversed_filename = f"{input_filename}.reversed.bin"
                reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions)

                compressed_filename = f"{input_filename}.compressed.bin"
                compressed_size, first_attempt = compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, file_size, first_attempt)

                if compressed_size < previous_size:
                    # Update the best values when a better compression ratio is found
                    previous_size = compressed_size
                    best_chunk_size = chunk_size
                    best_positions = positions
                    best_compression_ratio = compressed_size / file_size
                    best_count += 1

# Main function
def main():
    print("Created by Jurijus Pacalovas.")

    # Loop to ensure the user only inputs 1 or 2 for mode selection
    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for extract): "))
            if mode not in [1, 2]:
                print("Error: Please enter 1 for compress or 2 for extract.")
            else:
                break  # Exit loop if valid input is provided
        except ValueError:
            print("Error: Invalid input. Please enter a number (1 or 2).")

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        # Check if the input file exists
        if not os.path.exists(input_filename):
            print(f"Error: File {input_filename} not found!")
            return
        find_best_chunk_strategy(input_filename)  # Infinite search

    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"

        # Perform the extraction process
        if not os.path.exists(compressed_filename):
            print(f"Error: Compressed file {compressed_filename} not found!")
            return

        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()