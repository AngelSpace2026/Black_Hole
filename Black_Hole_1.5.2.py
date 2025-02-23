import os
import time
import zstandard as zstd  # Import Zstd for compression
import struct
from pathlib import Path
import random
import qiskit
from qiskit import QuantumCircuit

# Reverse chunks at specified positions
def reverse_chunks(input_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    if chunk_size <= 0 or len(data) < chunk_size:
        raise ValueError("Chunk size must be positive and less than file size.")
    
    # Split the data into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Reverse the chunks at the specified positions
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
        else:
            print(f"⚠️ Invalid position {pos} (out of range), skipping this position.")
    
    return chunked_data

# Quantum reverse function (simulating the behavior without Aer and execute)
def quantum_reverse(input_filename, chunk_size, qubits):
    # Simulate the quantum operation on chunk indices using Qiskit
    # Create quantum circuit with qubits
    qc = QuantumCircuit(qubits)
    qc.h(range(qubits))  # Apply Hadamard gate to all qubits (superposition)
    
    # Classical simulation of quantum behavior: just randomly reverse positions
    reverse_positions = random.sample(range(len(input_filename) // chunk_size), qubits)  # Use random positions based on qubits

    # Reverse chunks at the quantum-derived positions
    return reverse_chunks(input_filename, chunk_size, reverse_positions)

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

# Finding the best chunk strategy
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')

    print(f"📏 Finding the best chunk strategy...")

    for chunk_size in range(1, file_size + 1):
        positions = random.sample(range(file_size // chunk_size), random.randint(1, file_size // chunk_size))

        if chunk_size <= 0 or len(positions) == 0:
            print("⚠️ Invalid chunk size or positions, skipping this iteration.")
            continue

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

    # Quantum reverse step: This replaces the regular reverse with the quantum reverse
    qubits = best_chunk_size + 1  # Use X + 1 qubits for quantum simulation
    reversed_data = quantum_reverse(input_filename, best_chunk_size, qubits)
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