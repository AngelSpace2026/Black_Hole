import os
import random
import struct
import time
import io  # For buffer handling
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
            print(f"Reversing chunk at position: {pos}")
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using PAQ with metadata, and keep in buffer if it's smaller
def compress_with_paq(reversed_filename, chunk_size, positions):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata
    original_size = os.path.getsize(reversed_filename)
    metadata = struct.pack(">Q", original_size)  
    metadata += struct.pack(">I", chunk_size)  
    metadata += struct.pack(">I", len(positions))  
    metadata += struct.pack(f">{len(positions)}I", *positions)  

    # Compress the file
    compressed_data = paq.compress(metadata + reversed_data)

    compressed_size = len(compressed_data)
    print(f"✅ Compressed data size: {compressed_size} bytes")

    # Use BytesIO to hold the compressed data in memory (buffer)
    buffer = io.BytesIO(compressed_data)

    return buffer, compressed_size  # Return the buffer and its size

# Find the best chunk strategy and keep searching infinitely
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_compressed_data = None
    best_compressed_size = float('inf')  # Set it to the largest possible size initially
    best_count = 0  
    previous_compressed_size = None  # To store the previous compressed size

    print("📏 Searching for the best compression strategy...")

    while True:  # Infinite loop for searching compression
        # Set chunk_size as a random value from 1 to 2^28
        chunk_size = random.randint(1, 2**28)  # Random chunk size between 1 and 2^28

        if chunk_size <= 0:
            print("❌ Invalid chunk size. It must be a positive integer.")
            continue

        max_positions = file_size // chunk_size
        if max_positions > 0:
            positions_count = random.randint(1, min(max_positions, 64))
            positions = random.sample(range(max_positions), positions_count)

            reversed_file = "reversed_file.bin"
            reverse_chunks_at_positions(input_filename, reversed_file, chunk_size, positions)

            buffer, compressed_size = compress_with_paq(reversed_file, chunk_size, positions)

            # If this is the first compression or the new compressed size is smaller than the previous saved .bin
            if previous_compressed_size is None or compressed_size < previous_compressed_size:
                # Save the compressed data if it's smaller
                previous_compressed_size = compressed_size  # Update the size of the previously saved .bin file
                with open("compressed_file.bin", 'wb') as outfile:
                    outfile.write(buffer.getvalue())
                print(f"✅ Compressed file saved to: {os.path.abspath('compressed_file.bin')}")
                print(f"✅ New best compression found with size {compressed_size} bytes")
            else:
                # Discard the current attempt if the file is not smaller
                print(f"❌ Compression resulted in a larger file. Discarding attempt.")

            print(f"🔁 Continuing search for better compression...")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")
    
    mode = int(input("Enter mode (1 for compress, 2 for extract): "))
    
    if mode == 1:  
        input_filename = input("Enter input file name to compress: ")
        find_best_chunk_strategy(input_filename)  # Infinite search for best compression
        
    elif mode == 2:  
        compressed_filename = input("Enter compressed file name to extract: ")
        restored_filename = input("Enter restored file name: ")
        decompress_and_restore_paq(compressed_filename, restored_filename)

if __name__ == "__main__":
    main()