import os
import paq
from pathlib import Path
import struct

# Function to reverse data in chunks based on chunk count
def reverse_and_save(input_filename, reversed_filename, chunk_size, num_chunks):
    #print(f"🔄 Reversing with {num_chunks} chunks, chunk size: {chunk_size} bytes")
    with open(input_filename, 'rb') as infile, open(reversed_filename, 'wb') as outfile:
        data = infile.read()
        chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Reverse the first `num_chunks` chunks
        for i in range(num_chunks):
            if i < len(chunked_data):
                chunked_data[i] = chunked_data[i][::-1]
        
        outfile.write(b"".join(chunked_data))

# Function to compress and save metadata (chunk size + num_chunks)
def compress_reversed(reversed_filename, compressed_filename, chunk_size, num_chunks):
    #print(f"📦 Compressing with chunk size {chunk_size} bytes and {num_chunks} reversed chunks")
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Store metadata (chunk size and num_chunks) in the first 8 bytes (4 bytes each)
    metadata = struct.pack(">II", chunk_size, num_chunks)
    compressed_data = paq.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Function to decompress and restore the original file
def decompress_and_restore(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = paq.decompress(compressed_data)

    # Read metadata (first 8 bytes)
    chunk_size, num_chunks = struct.unpack(">II", decompressed_data[:8])
    #print(f"🔄 Restoring with chunk size: {chunk_size}, reversed chunks: {num_chunks}")

    reversed_data = decompressed_data[8:]  # Actual reversed data

    # Reconstruct the original file by reversing the first `num_chunks` chunks
    chunked_data = [reversed_data[i:i + chunk_size] for i in range(0, len(reversed_data), chunk_size)]
    for i in range(num_chunks):
        if i < len(chunked_data):
            chunked_data[i] = chunked_data[i][::-1]

    restored_data = b"".join(chunked_data)

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

# Function to determine the best chunk size and number of reversed chunks
def find_best_parameters(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_num_chunks = 1
    best_compression_ratio = float('inf')

    print(f"📏 Finding the best parameters (chunk size and reversed chunks)...")

    for chunk_size in range(1, file_size + 1):
        for num_chunks in range(1, file_size // chunk_size + 1):
            reversed_file = input_filename + ".rev"
            compressed_file = f"compress.{Path(input_filename).name}.b"

            reverse_and_save(input_filename, reversed_file, chunk_size, num_chunks)
            compress_reversed(reversed_file, compressed_file, chunk_size, num_chunks)

            compressed_size = os.path.getsize(compressed_file)
            compression_ratio = compressed_size / file_size

            if compression_ratio < best_compression_ratio:
                best_compression_ratio = compression_ratio
                best_chunk_size = chunk_size
                best_num_chunks = num_chunks

            os.remove(reversed_file)
            os.remove(compressed_file)

    print(f"✅ Best chunk size: {best_chunk_size}, best reversed chunks: {best_num_chunks} (Compression Ratio: {best_compression_ratio:.4f})")
    return best_chunk_size, best_num_chunks

# Compression process
def process_compression(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size, best_num_chunks = find_best_parameters(input_filename)

    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.b"
    restored_file = f"extract.{Path(input_filename).name}"

    reverse_and_save(input_filename, reversed_file, best_chunk_size, best_num_chunks)
    compress_reversed(reversed_file, compressed_file, best_chunk_size, best_num_chunks)
    decompress_and_restore(compressed_file, restored_file)

    print(f"✅ Three files remain:\n  1️⃣ Original: '{input_filename}'\n  2️⃣ Best Compressed: '{compressed_file}'\n  3️⃣ Restored: '{restored_file}'")

    os.remove(reversed_file)  # Cleanup temporary file

# Extraction process
def process_extraction(input_filename):
    restored_file = f"extract.{Path(input_filename).name.replace('compress.', '').replace('.b', '')}"
    decompress_and_restore(input_filename, restored_file)
    print(f"✅ Extracted file: '{restored_file}'")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")
    
    mode = input("Enter mode (compress/extract): ").strip().lower()
    input_file = input("Enter input file name: ").strip()

    if mode == "compress":
        process_compression(input_file)
    elif mode == "extract":
        process_extraction(input_file)
    else:
        print("❌ Invalid mode selected.")

if __name__ == "__main__":
    main()