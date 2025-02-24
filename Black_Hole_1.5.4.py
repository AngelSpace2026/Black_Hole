import os
import random
import struct
from pathlib import Path
import zstandard as zstd
from qiskit import QuantumCircuit

# Reverse chunks at specified indices starting from the first byte
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Ensure the chunking starts from byte 1
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Add padding to the last chunk if it's less than the specified chunk size
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] = chunked_data[-1] + b'\x00' * (chunk_size - len(chunked_data[-1]))

    # Reverse chunks at the specified positions, starting from the first chunk
    for pos in positions:
        if 0 <= pos < len(chunked_data):  # Ensure position is within bounds
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Function to generate a random number (simulating quantum-like randomness)
def generate_random_number(num_bits=28):
    # Simulate quantum randomness by generating a random integer within the range of 0 to 2^28
    random_number = random.getrandbits(num_bits)  # Generate random number with 'num_bits' bits
    return random_number % (2**28)  # Ensure the number fits within 28 bits

# Compress using zstd with metadata
def compress_with_zstd(reversed_filename, compressed_filename, chunk_size, positions, original_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack the chunk size (4 bytes), positions, and original file size (8 bytes) into the metadata
    metadata = struct.pack(">Q", original_size)  # Store original file size (8 bytes)
    metadata += struct.pack(">I", chunk_size)  # Store chunk size as 4 bytes (4 bytes)
    metadata += struct.pack(">H", len(positions))  # Store number of positions (2 bytes)
    
    # Pack positions as 28-bit integers, which requires a bit of custom packing
    for pos in positions:
        # Ensure that position fits within 28-bit range
        if pos < 0 or pos >= 2**28:
            raise ValueError(f"Position {pos} is out of bounds for 28-bit encoding (should be 0 to 2^28-1).")
        metadata += struct.pack(">I", pos)  # Pack each position as a 32-bit integer (will mask later)

    # Create a compressor
    cctx = zstd.ZstdCompressor()

    # Compress the file with the metadata
    compressed_data = cctx.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

    # Print the path of the compressed file
    print(f"✅ Compressed file saved at: {os.path.abspath(compressed_filename)}")

# Decompression and restoration using zstd
def decompress_and_restore_zstd(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    # Create a decompressor
    dctx = zstd.ZstdDecompressor()

    # Decompress the data
    decompressed_data = dctx.decompress(compressed_data)

    # Extract metadata
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]  # First 8 bytes for original file size
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]  # Next 4 bytes for chunk size
    num_positions = struct.unpack(">H", decompressed_data[12:14])[0]  # Next 2 bytes for number of positions
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[14:14 + num_positions * 4]))  # Extract positions

    # Reconstruct the chunks
    chunked_data = decompressed_data[14 + num_positions * 4:]

    total_chunks = len(chunked_data) // chunk_size
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    # Reverse the chunks at specified positions
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    restored_data = b"".join(chunked_data)

    # Trim to the original size
    restored_data = restored_data[:original_size]

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"✅ File extracted to: {restored_filename}")

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

            reversed_file = "reversed_file.bin"
            reverse_chunks_at_positions(input_filename, reversed_file, chunk_size, positions)

            # Compress the reversed file
            compressed_file = "compressed_file.bin"
            original_size = os.path.getsize(input_filename)
            compress_with_zstd(reversed_file, compressed_file, chunk_size, positions, original_size)

            # Calculate compression ratio
            compressed_size = os.path.getsize(compressed_file)
            compression_ratio = compressed_size / original_size

            # Track the best compression ratio
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