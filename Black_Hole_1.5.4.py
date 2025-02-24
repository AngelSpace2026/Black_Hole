import os
import zlib
import random
import struct
import zstandard as zstd
from pathlib import Path
# Import Qiskit without Aer and execute
from qiskit import QuantumCircuit  # Just import QuantumCircuit, no Aer or execute

# Reverse chunks at specified indices starting from the first byte
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Ensure the chunking starts from byte 1
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Add padding to the last chunk if it's less than 64 bytes
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] = chunked_data[-1] + b'\x00' * (chunk_size - len(chunked_data[-1]))

    # Reverse chunks at the specified positions, starting from the first chunk
    for pos in positions:
        if 0 <= pos < len(chunked_data):  # Ensure position is within bounds
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using zstd with metadata
def compress_with_zstd(reversed_filename, compressed_filename, chunk_size, positions, original_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack the chunk size, positions, and original file size into the metadata
    metadata = struct.pack(">Q", original_size)  # Store original file size (8 bytes)
    metadata += struct.pack(">H", chunk_size)  # Store chunk size (2 bytes)
    metadata += struct.pack(f">H", len(positions))  # Store number of positions (2 bytes)
    metadata += struct.pack(f">{len(positions)}H", *positions)  # Store positions

    # Compress the file with the metadata using zstd
    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Decompress and restoration using zstd
def decompress_and_restore(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        # Read the entire file at once, including metadata and compressed data
        file_data = infile.read()

    # Create a decompressor object and decompress the file
    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(file_data)

    # Extract metadata and data
    metadata_size = struct.calcsize(">QH H")
    metadata = decompressed_data[:metadata_size]
    data = decompressed_data[metadata_size:]

    # Extract metadata
    original_size, chunk_size, positions_count = struct.unpack(">QH H", metadata)
    positions = struct.unpack(f">{positions_count}H", decompressed_data[metadata_size:metadata_size + 2 * positions_count])

    # Save the decompressed data to file
    with open(restored_filename, 'wb') as outfile:
        outfile.write(data)

    print(f"✅ Decompression successful: {restored_filename}")

# Function to extract file name with extension
def extract_filename_with_extension(filename):
    return Path(filename).name

# Find best chunking strategy based on file size
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')

    # Test different chunk sizes and positions
    print("📏 Finding the best chunk strategy...")

    # Iterate through possible chunk sizes
    for chunk_size in range(1, min(64, file_size // 2) + 1):  # Chunk sizes from 1 to 63
        max_positions = file_size // chunk_size  # Number of possible positions
        if max_positions > 0:
            # Randomly select positions to reverse, but ensure it's within the available range
            positions_count = random.randint(1, min(max_positions, 64))  # Limit to max positions or 64
            positions = random.sample(range(max_positions), positions_count)

            reversed_file = input_filename + ".rev"
            compressed_file = f"compress.{Path(input_filename).name}.zst"

            reverse_chunks_at_positions(input_filename, reversed_file, chunk_size, positions)
            compress_with_zstd(reversed_file, compressed_file, chunk_size, positions, file_size)

            compressed_size = os.path.getsize(compressed_file)
            compression_ratio = compressed_size / file_size

            if compression_ratio < best_compression_ratio:
                best_compression_ratio = compression_ratio
                best_chunk_size = chunk_size
                best_positions = positions

            os.remove(reversed_file)
            os.remove(compressed_file)

    print(f"✅ Best chunk size: {best_chunk_size}, Best positions: {best_positions} (Compression Ratio: {best_compression_ratio:.4f})")

    return best_chunk_size, best_positions

# Process compression
def process_compression(input_filename):
    print(f"🔧 Starting compression for {input_filename}")
    best_chunk_size, best_positions = find_best_chunk_strategy(input_filename)

    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.zst"
    extracted_file_name = f"extract.{Path(input_filename).stem}.{Path(input_filename).suffix}"

    reverse_chunks_at_positions(input_filename, reversed_file, best_chunk_size, best_positions)
    compress_with_zstd(reversed_file, compressed_file, best_chunk_size, best_positions, os.path.getsize(input_filename))
    print(f"✅ File compressed: {compressed_file}")

    decompress_and_restore(compressed_file, extracted_file_name)
    print(f"✅ File extracted to: {extracted_file_name}")

# Main function to run the compression process
if __name__ == "__main__":
    mode = int(input("Enter mode (1 for compress, 2 for extract): "))

    if mode == 1:  # Compress
        input_filename = input("Enter input file name to compress: ")
        process_compression(input_filename)

    elif mode == 2:  # Extract
        input_filename = input("Enter input file name to extract: ")
        restored_filename = f"restored_{Path(input_filename).name}"
        decompress_and_restore(input_filename, restored_filename)
        print(f"✅ File extracted to: {restored_filename}")