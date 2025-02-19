import os
import zstandard as zstd
from pathlib import Path
import math

# Function to reverse data in multiple ways based on chunk size
def reverse_and_save(input_filename, reversed_filename, chunk_size):
    try:
        with open(input_filename, 'rb') as infile, open(reversed_filename, 'wb') as outfile:
            while chunk := infile.read(chunk_size):
                outfile.write(chunk[::-1])  # Reverse each chunk before writing
        return os.path.getsize(reversed_filename)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Function to compress the reversed file using zstd
def compress_reversed(reversed_filename, compressed_filename):
    try:
        with open(reversed_filename, 'rb') as infile:
            compressed_data = zstd.compress(infile.read())  # Compress reversed file
            with open(compressed_filename, 'wb') as outfile:
                outfile.write(compressed_data)
        return os.path.getsize(compressed_filename)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Function to decompress and restore the original file
def decompress_and_restore(compressed_filename, restored_filename, chunk_size):
    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()

        decompressed_data = zstd.decompress(compressed_data)  # Decompress the data

        # Reverse again in chunks to restore the original order
        restored_data = b"".join([decompressed_data[i:i+chunk_size][::-1] 
                                  for i in range(0, len(decompressed_data), chunk_size)])
        
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        
        return os.path.getsize(restored_filename)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Function to find the best chunk size for compression
def find_best_chunk_size(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1  # Start with minimum chunk size
    best_compression_ratio = float('inf')
    best_compressed_file = None

    print(f"📏 Checking best chunk size from 1 to {file_size} bytes...")

    for chunk_size in range(1, file_size + 1):
        reversed_file = input_filename + ".rev"
        compressed_file = f"compress.{Path(input_filename).name}.b"
        
        reverse_and_save(input_filename, reversed_file, chunk_size)
        compressed_size = compress_reversed(reversed_file, compressed_file)
        
        if compressed_size is not None:
            compression_ratio = compressed_size / file_size  # Lower is better

            if compression_ratio < best_compression_ratio:
                best_compression_ratio = compression_ratio
                best_chunk_size = chunk_size
                best_compressed_file = compressed_file

        os.remove(reversed_file) if os.path.exists(reversed_file) else None
        os.remove(compressed_file) if os.path.exists(compressed_file) else None

    print(f"✅ Best chunk size: {best_chunk_size} bytes (Compression Ratio: {best_compression_ratio:.4f})")
    return best_chunk_size, best_compressed_file

# Function to process compression and leave only three files
def process_compression(input_filename):
    file_size = os.path.getsize(input_filename)
    
    # Find the best chunk size
    best_chunk_size, best_compressed_file = find_best_chunk_size(input_filename)

    # File paths
    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.b"
    restored_file = f"extract.{Path(input_filename).name}"  # Extracted file format
    metadata_file = f"compress.{Path(input_filename).name}.meta"  # Metadata file to store chunk size

    # Process with the best chunk size
    reverse_and_save(input_filename, reversed_file, best_chunk_size)
    compress_reversed(reversed_file, compressed_file)

    # Save metadata about the best chunk size
    with open(metadata_file, "w") as meta:
        meta.write(str(best_chunk_size))

    # Decompress and restore to verify correctness
    decompress_and_restore(compressed_file, restored_file, best_chunk_size)

    # Check file integrity
    original_size = os.path.getsize(input_filename)
    restored_size = os.path.getsize(restored_file)

    print(f"Original file size: {original_size} bytes.")
    print(f"Restored file size: {restored_size} bytes.")

    if original_size == restored_size:
        print("✅ File successfully restored with correct size.")
    else:
        print("❌ Warning: Restored file size does not match the original.")

    # Cleanup: Delete unnecessary temporary files
    os.remove(reversed_file) if os.path.exists(reversed_file) else None
    print(f"✅ Removed temporary file '{reversed_file}'.")

    print(f"✅ Three files are left:\n  1️⃣ Original: '{input_filename}'\n  2️⃣ Best Compressed: '{compressed_file}'\n  3️⃣ Restored: '{restored_file}'")

# Function to extract file
def process_extraction(input_filename):
    try:
        base_name = input_filename.replace("compress.", "").replace(".b", "")
        metadata_file = f"compress.{base_name}.meta"
        
        # Read the best chunk size from metadata file
        with open(metadata_file, "r") as meta:
            best_chunk_size = int(meta.read().strip())

        restored_file = f"extract.{base_name}"
        decompress_and_restore(input_filename, restored_file, best_chunk_size)

        # Remove metadata file after extraction
        os.remove(metadata_file) if os.path.exists(metadata_file) else None
        print(f"✅ Extracted file: '{restored_file}'")

    except FileNotFoundError:
        print("❌ Error: Metadata file not found. Cannot extract properly.")

# Main interactive function
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