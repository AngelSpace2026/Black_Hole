import os
import random
import struct
import time
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

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, original_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata
    metadata = struct.pack(">Q", original_size)  
    metadata += struct.pack(">I", chunk_size)  
    metadata += struct.pack(">I", len(positions))  
    metadata += struct.pack(f">{len(positions)}I", *positions)  

    # Compress the file
    compressed_data = paq.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

    compressed_size = os.path.getsize(compressed_filename)
    print(f"✅ Compressed file size: {compressed_size} bytes")
    return compressed_size

# Decompress and restore data
def decompress_and_restore_paq(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    # Decompress the data
    decompressed_data = paq.decompress(compressed_data)

    # Extract metadata
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]  # Original size from metadata
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
            print(f"Reversing back chunk at position: {pos}")
            chunked_data[pos] = chunked_data[pos][::-1]

    # Combine the chunks
    restored_data = b"".join(chunked_data)

    # Ensure the restored data is exactly the original size
    restored_data = restored_data[:original_size]

    # Write the restored data to the file
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"✅ File extracted to: {os.path.abspath(restored_filename)} with size {len(restored_data)} bytes")

# Find the best chunk strategy and keep searching infinitely
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')
    best_count = 0  

    print("📏 Searching for the best compression strategy (Infinite Mode)...")

    while True:  # Infinite loop to keep improving
        for chunk_size in range(1, 256):
            max_positions = file_size // chunk_size
            if max_positions > 0:
                positions_count = random.randint(1, min(max_positions, 64))
                positions = random.sample(range(max_positions), positions_count)

                reversed_file = "reversed_file.bin"
                reverse_chunks_at_positions(input_filename, reversed_file, chunk_size, positions)

                compressed_file = "compressed_file.bin"
                original_size = os.path.getsize(input_filename)
                compressed_size = compress_with_paq(reversed_file, compressed_file, chunk_size, positions, original_size)

                compression_ratio = compressed_size / original_size

                if compression_ratio < best_compression_ratio:
                    best_compression_ratio = compression_ratio
                    best_chunk_size = chunk_size
                    best_positions = positions
                    best_count += 1  # Count how many times a new best is found

                    if best_count == 1:
                        print("⏳ First best compression found. Sleeping for 5 seconds...")
                        time.sleep(5)
                    else:
                        print(f"⏳ Found the best compression for the {best_count}th time! Sleeping for 30 seconds...")
                        time.sleep(30)

                print(f"✅ Best compression so far: {best_compression_ratio} (Chunk size: {best_chunk_size}, Positions: {best_positions})")
                print(f"🔁 Continuing search for better compression...")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")
    
    mode = int(input("Enter mode (1 for compress, 2 for extract): "))
    
    if mode == 1:  
        input_filename = input("Enter input file name to compress: ")
        find_best_chunk_strategy(input_filename)  # Infinite search
        
    elif mode == 2:  
        compressed_filename = input("Enter compressed file name to extract: ")
        restored_filename = input("Enter restored file name: ")
        decompress_and_restore_paq(compressed_filename, restored_filename)

if __name__ == "__main__":
    main()