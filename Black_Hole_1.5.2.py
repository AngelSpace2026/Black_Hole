import os
import time
import zstandard as zstd  # Import Zstd for compression
import struct
from pathlib import Path
from qiskit import QuantumCircuit
import random

# Quantum computation example
def quantum_computation_example():
    print("\n🔮 Running a basic quantum computation without Aer, transpile, or execute:")
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    print("\nQuantum Circuit:")
    print(circuit)

# Reverse chunks at multiple stages with different chunk selections
def multi_reverse_chunks(input_filename, reversed_filename, chunk_size, iterations):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    file_size = len(chunked_data)

    # Store indices of reversed chunks for each iteration
    reversed_metadata = []

    for _ in range(iterations):
        num_chunks_to_reverse = random.randint(2, file_size)  # Varies each iteration
        indices = sorted(random.sample(range(file_size), num_chunks_to_reverse))
        reversed_metadata.append(indices)

        # Reverse selected chunks
        for i in indices:
            chunked_data[i] = chunked_data[i][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

    return reversed_metadata

# Compress using Zstd with metadata
def compress_with_zstd(reversed_filename, compressed_filename, chunk_size, reversed_metadata):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    metadata = struct.pack(">H", chunk_size)  # Store chunk size (2 bytes)
    for iteration in reversed_metadata:
        metadata += struct.pack(f">{len(iteration)}H", *iteration)

    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Decompression and restoration
def decompress_and_restore(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)

    chunk_size = struct.unpack(">H", decompressed_data[:2])[0]
    metadata_offset = 2
    chunked_data = decompressed_data[metadata_offset:]

    file_size = len(chunked_data)
    total_chunks = file_size // chunk_size

    reversed_metadata = []
    while metadata_offset < len(decompressed_data):
        num_entries = (len(decompressed_data) - metadata_offset) // 2
        indices = list(struct.unpack(f">{num_entries}H", decompressed_data[metadata_offset:metadata_offset + num_entries * 2]))
        reversed_metadata.insert(0, indices)
        metadata_offset += num_entries * 2

    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]
    for indices in reversed_metadata:
        for i in indices:
            chunked_data[i] = chunked_data[i][::-1]

    restored_data = b"".join(chunked_data)

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

# Finding the best chunk size and reversal strategy
def find_best_parameters(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_iterations = 1
    best_compression_ratio = float('inf')

    print(f"📏 Finding the best parameters (chunk size and iterations)...")

    for chunk_size in range(1, file_size + 1):
        for iterations in range(2, min(file_size, 1024)):
            reversed_file = input_filename + ".rev"
            compressed_file = f"compress.{Path(input_filename).name}.b"

            reversed_metadata = multi_reverse_chunks(input_filename, reversed_file, chunk_size, iterations)
            compress_with_zstd(reversed_file, compressed_file, chunk_size, reversed_metadata)

            compressed_size = os.path.getsize(compressed_file)
            compression_ratio = compressed_size / file_size

            if compression_ratio < best_compression_ratio:
                best_compression_ratio = compression_ratio
                best_chunk_size = chunk_size
                best_iterations = iterations

            os.remove(reversed_file)
            os.remove(compressed_file)

    print(f"✅ Best chunk size: {best_chunk_size}, best iterations: {best_iterations} (Compression Ratio: {best_compression_ratio:.4f})")
    return best_chunk_size, best_iterations

# Compression process with nanosecond timing
def process_compression(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size, best_iterations = find_best_parameters(input_filename)

    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.b"
    restored_file = f"extract.{Path(input_filename).name}"

    start_compress = time.perf_counter_ns()
    reversed_metadata = multi_reverse_chunks(input_filename, reversed_file, best_chunk_size, best_iterations)
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