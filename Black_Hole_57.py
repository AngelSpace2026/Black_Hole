import os
import random
import struct
from pathlib import Path
import zstandard as zstd

# Reverse chunks at specified positions
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Add padding to the last chunk if necessary
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] = chunked_data[-1] + b'\x00' * (chunk_size - len(chunked_data[-1]))

    # Reverse specified chunks and print changes
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            print(f"Reversing chunk at position: {pos}")
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using Zstd with metadata
def compress_with_zstd(reversed_filename, compressed_filename, chunk_size, positions, original_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata: file size (8 bytes), chunk size (4 bytes), number of positions (4 bytes), positions (4 bytes each)
    metadata = struct.pack(">Q", original_size)  # Original file size (8 bytes)
    metadata += struct.pack(">I", chunk_size)  # Chunk size (4 bytes)
    metadata += struct.pack(">I", len(positions))  # Number of positions (4 bytes)
    metadata += struct.pack(f">{len(positions)}I", *positions)  # Store positions (each 4 bytes)

    # Compress the file with metadata
    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

    print(f"✅ Compressed file saved at: {os.path.abspath(compressed_filename)}")

# Decompress and restore data
def decompress_and_restore_zstd(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)

    # Extract metadata
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]  # First 8 bytes: original file size
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]  # Next 4 bytes: chunk size
    num_positions = struct.unpack(">I", decompressed_data[12:16])[0]  # Next 4 bytes: number of positions
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))  # Positions

    # Reconstruct chunks
    chunked_data = decompressed_data[16 + num_positions * 4:]

    total_chunks = len(chunked_data) // chunk_size
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    # Reverse chunks back and print changes
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            print(f"Reversing back chunk at position: {pos}")
            chunked_data[pos] = chunked_data[pos][::-1]

    restored_data = b"".join(chunked_data)[:original_size]  # Trim to original size

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"✅ File extracted to: {os.path.abspath(restored_filename)}")

# Find best chunk strategy for compression
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')

    print("📏 Finding the best chunk strategy...")

    for chunk_size in range(1, min(64, file_size // 2) + 1):
        max_positions = file_size // chunk_size
        if max_positions > 0:
            positions_count = random.randint(1, min(max_positions, 64))
            positions = random.sample(range(max_positions), positions_count)

            reversed_file = "reversed_file.bin"
            reverse_chunks_at_positions(input_filename, reversed_file, chunk_size, positions)

            compressed_file = "compressed_file.bin"
            original_size = os.path.getsize(input_filename)
            compress_with_zstd(reversed_file, compressed_file, chunk_size, positions, original_size)

            compressed_size = os.path.getsize(compressed_file)
            compression_ratio = compressed_size / original_size

            if compression_ratio < best_compression_ratio:
                best_compression_ratio = compression_ratio
                best_chunk_size = chunk_size
                best_positions = positions

    print(f"✅ Best chunk size: {best_chunk_size}, Best positions: {best_positions} (Compression Ratio: {best_compression_ratio})")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")
    
    mode = int(input("Enter mode (1 for compress, 2 for extract): "))
    
    if mode == 1:  # Compression
        input_filename = input("Enter input file name to compress: ")
        find_best_chunk_strategy(input_filename)
        
    elif mode == 2:  # Extraction
        compressed_filename = input("Enter compressed file name to extract: ")
        restored_filename = input("Enter restored file name: ")
        decompress_and_restore_zstd(compressed_filename, restored_filename)

if __name__ == "__main__":
    main()