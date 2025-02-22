import os
import time
import zstandard as zstd  # Importing Zstd for compression
import struct
from pathlib import Path
from qiskit import QuantumCircuit
import random

# Function to run a quantum computation (without Aer, transpile, or execute)
def quantum_computation_example():
    print("\n🔮 Running a basic quantum computation without Aer, transpile, or execute:")
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    print("\nQuantum Circuit:")
    print(circuit)

# Function to reverse specific chunks and record metadata
def reverse_chunks_and_save(input_filename, reversed_filename, chunk_size, num_chunks, iterations):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    file_size = len(chunked_data)

    # Store the indices of reversed chunks for each iteration
    reversed_metadata = []

    for _ in range(iterations):
        # Select `num_chunks` random indices (ensuring they are unique)
        indices = sorted(random.sample(range(file_size), min(num_chunks, file_size)))
        reversed_metadata.append(indices)

        # Reverse only selected chunks
        for i in indices:
            chunked_data[i] = chunked_data[i][::-1]

    # Save reversed data
    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

    return reversed_metadata

# Function to compress reversed data with metadata using Zstd
def compress_with_zstd(reversed_filename, compressed_filename, chunk_size, reversed_metadata):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Store metadata: chunk size + reversed chunk indices (2 bytes per index)
    metadata = struct.pack(">H", chunk_size)  # Store chunk size (2 bytes)
    for iteration in reversed_metadata:
        metadata += struct.pack(f">{len(iteration)}H", *iteration)

    # Compress data using Zstd
    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Function to decompress and restore the original file
def decompress_and_restore(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    # Decompress using Zstd
    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)

    # Read metadata
    chunk_size = struct.unpack(">H", decompressed_data[:2])[0]  # Read chunk size
    metadata_offset = 2
    chunked_data = decompressed_data[metadata_offset:]

    # Determine number of chunks
    file_size = len(chunked_data)
    total_chunks = file_size // chunk_size

    # Read reversed indices (last to first for restoration)
    reversed_metadata = []
    while metadata_offset < len(decompressed_data):
        num_entries = (len(decompressed_data) - metadata_offset) // 2  # 2 bytes per index
        indices = list(struct.unpack(f">{num_entries}H", decompressed_data[metadata_offset:metadata_offset + num_entries * 2]))
        reversed_metadata.insert(0, indices)  # Reverse the order for restoration
        metadata_offset += num_entries * 2

    # Restore the original data by reversing in reverse order
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]
    for indices in reversed_metadata:
        for i in indices:
            chunked_data[i] = chunked_data[i][::-1]

    restored_data = b"".join(chunked_data)

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

# Function to determine the best chunk size and number of reversed chunks
def find_best_parameters(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_num_chunks = 1
    best_iterations = 1
    best_compression_ratio = float('inf')

    print(f"📏 Finding the best parameters (chunk size, reversed chunks, and iterations)...")

    for chunk_size in range(1, file_size + 1):
        for num_chunks in range(2, min(file_size, 1024)):  # Min 2 chunks up to 1024
            for iterations in range(2, min(file_size, 1024)):  # Min 2 iterations up to 1024
                reversed_file = input_filename + ".rev"
                compressed_file = f"compress.{Path(input_filename).name}.b"

                reversed_metadata = reverse_chunks_and_save(input_filename, reversed_file, chunk_size, num_chunks, iterations)
                compress_with_zstd(reversed_file, compressed_file, chunk_size, reversed_metadata)

                compressed_size = os.path.getsize(compressed_file)
                compression_ratio = compressed_size / file_size

                if compression_ratio < best_compression_ratio:
                    best_compression_ratio = compression_ratio
                    best_chunk_size = chunk_size
                    best_num_chunks = num_chunks
                    best_iterations = iterations

                os.remove(reversed_file)
                os.remove(compressed_file)

    print(f"✅ Best chunk size: {best_chunk_size}, best reversed chunks: {best_num_chunks}, best iterations: {best_iterations} (Compression Ratio: {best_compression_ratio:.4f})")
    return best_chunk_size, best_num_chunks, best_iterations

# Compression process with nanosecond timing
def process_compression(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size, best_num_chunks, best_iterations = find_best_parameters(input_filename)

    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.b"
    restored_file = f"extract.{Path(input_filename).name}"

    start_compress = time.perf_counter_ns()

    reversed_metadata = reverse_chunks_and_save(input_filename, reversed_file, best_chunk_size, best_num_chunks, best_iterations)
    compress_with_zstd(reversed_file, compressed_file, best_chunk_size, reversed_metadata)

    end_compress = time.perf_counter_ns()
    print(f"⏳ Compression time: {end_compress - start_compress} nanoseconds")

    start_extract = time.perf_counter_ns()
    decompress_and_restore(compressed_file, restored_file)
    end_extract = time.perf_counter_ns()
    print(f"⏳ Extraction time: {end_extract - start_extract} nanoseconds")

# Extraction process with nanosecond timing
def process_extraction(input_filename):
    restored_file = f"extract.{Path(input_filename).name.replace('compress.', '').replace('.b', '')}"
    start_extract = time.perf_counter_ns()
    decompress_and_restore(input_filename, restored_file)
    end_extract = time.perf_counter_ns()
    print(f"✅ Extracted file: '{restored_file}' in {end_extract - start_extract} nanoseconds")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")
    quantum_computation_example()
    mode = input("Enter mode (1 for compress, 2 for extract): ").strip()
    if mode == "1":
        process_compression(input("Enter input file name to compress: ").strip())
    elif mode == "2":
        process_extraction(input("Enter input file name to extract: ").strip())

if __name__ == "__main__":
    main()