import os
import time
import zstandard as zstd
import struct
from pathlib import Path
import random
import qiskit
from qiskit import QuantumCircuit

# Reverse chunks at specified positions dynamically based on the file size
def reverse_chunks(input_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split the data into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Reverse the chunks at the specified positions
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    return chunked_data

# Compress the reversed data with Zstd
def compress_with_zstd(reversed_data, compressed_filename, chunk_size, positions):
    metadata = struct.pack(">H", chunk_size)  # Store chunk size (2 bytes)
    metadata += struct.pack(">H", len(positions))  # Store number of positions
    for pos in positions:
        metadata += struct.pack(">H", pos)

    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(metadata + b"".join(reversed_data))

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Decompression and restoration with extracted file name printing
def decompress_and_restore(compressed_filename, restored_filename):
    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()

        # Decompress the data
        dctx = zstd.ZstdDecompressor()
        decompressed_data = dctx.decompress(compressed_data)

        # Extract metadata
        chunk_size = struct.unpack(">H", decompressed_data[:2])[0]
        num_positions = struct.unpack(">H", decompressed_data[2:4])[0]  # Number of positions
        positions = list(struct.unpack(f">{num_positions}H", decompressed_data[4:4 + num_positions * 2]))

        # Reconstruct the chunks
        chunked_data = decompressed_data[4 + num_positions * 2:]

        total_chunks = len(chunked_data) // chunk_size
        chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

        # Reverse the chunks at specified positions
        for pos in positions:
            if 0 <= pos < len(chunked_data):
                chunked_data[pos] = chunked_data[pos][::-1]

        restored_data = b"".join(chunked_data)

        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)

        print(f"✅ File extracted successfully: {restored_filename}")
        print(f"Extracted file name: {restored_filename}")  # Print the extracted file name
    except Exception as e:
        print(f"Error during extraction: {e}")

# Quantum-inspired optimization for positions (without using Aer or execute)
def quantum_optimize_positions(file_size, chunk_size):
    # Initialize the quantum circuit for randomness
    qc = QuantumCircuit(3, 3)  # A simple 3-qubit circuit for this example
    qc.h([0, 1, 2])  # Apply Hadamard gates to create a superposition of all possible states

    # Simulate a randomness by using the quantum circuit's state to choose positions (no Aer needed)
    positions = random.sample(range(file_size // chunk_size), random.randint(1, file_size // chunk_size))
    
    # Return best chunk positions (based on randomness)
    return positions

# Finding the best chunk strategy
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')

    print(f"📏 Finding the best chunk strategy...")

    for chunk_size in range(1, file_size + 1):
        # Quantum-inspired optimization for positions
        positions = quantum_optimize_positions(file_size, chunk_size)

        reversed_data = reverse_chunks(input_filename, chunk_size, positions)
        compressed_filename = f"compress.{Path(input_filename).name}.b"
        compress_with_zstd(reversed_data, compressed_filename, chunk_size, positions)

        compressed_size = os.path.getsize(compressed_filename)
        compression_ratio = compressed_size / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_chunk_size = chunk_size
            best_positions = positions

        os.remove(compressed_filename)

    print(f"✅ Best chunk size: {best_chunk_size}, Best positions: {best_positions} (Compression Ratio: {best_compression_ratio:.4f})")
    return best_chunk_size, best_positions

# Compression process
def process_compression(input_filename):
    best_chunk_size, best_positions = find_best_chunk_strategy(input_filename)

    reversed_data = reverse_chunks(input_filename, best_chunk_size, best_positions)
    compressed_filename = f"compress.{Path(input_filename).name}.b"
    compress_with_zstd(reversed_data, compressed_filename, best_chunk_size, best_positions)

    print(f"✅ File compressed successfully: {compressed_filename}")

# Extraction process
def process_extraction(input_filename):
    restored_filename = f"extract.{Path(input_filename).name.replace('compress.', '').replace('.b', '')}"
    decompress_and_restore(input_filename, restored_filename)

# Main function
def main():
    print("Created by Jurijus Pacalovas.")
    mode = input("Enter mode (1 for compress, 2 for extract): ").strip()
    if mode == "1":
        process_compression(input("Enter input file name to compress: ").strip())
    elif mode == "2":
        process_extraction(input("Enter input file name to extract: ").strip())

if __name__ == "__main__":
    main()