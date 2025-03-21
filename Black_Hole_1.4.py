import os
import time
import zstandard as zstd
from pathlib import Path
import math
from qiskit import QuantumCircuit

# Function to reverse data in chunks
def reverse_and_save(input_filename, reversed_filename, chunk_size):
    with open(input_filename, 'rb') as infile, open(reversed_filename, 'wb') as outfile:
        while chunk := infile.read(chunk_size):
            outfile.write(chunk[::-1])  # Reverse each chunk before writing

# Function to compress and embed chunk size
def compress_reversed(reversed_filename, compressed_filename, chunk_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()
    
    # Embed the chunk size at the beginning (4 bytes, big-endian)
    chunk_size_bytes = chunk_size.to_bytes(4, 'big')
    compressed_data = zstd.compress(chunk_size_bytes + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Function to decompress and restore the original file
def decompress_and_restore(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = zstd.decompress(compressed_data)
    
    # Extract the first 4 bytes to get the chunk size
    chunk_size = int.from_bytes(decompressed_data[:4], 'big')
    reversed_data = decompressed_data[4:]  # The actual reversed data
    
    # Reverse chunks again to restore original order
    restored_data = b"".join(
        [reversed_data[i:i+chunk_size][::-1] for i in range(0, len(reversed_data), chunk_size)]
    )

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

# Function to determine the best chunk size
def find_best_chunk_size(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_compression_ratio = float('inf')

    print(f"📏 Checking best chunk size from 1 to {file_size} bytes...")

    for chunk_size in range(1, file_size + 1):
        reversed_file = input_filename + ".rev"
        compressed_file = f"compress.{Path(input_filename).name}.b"
        
        reverse_and_save(input_filename, reversed_file, chunk_size)
        compress_reversed(reversed_file, compressed_file, chunk_size)

        compressed_size = os.path.getsize(compressed_file)
        compression_ratio = compressed_size / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_chunk_size = chunk_size

        os.remove(reversed_file)
        os.remove(compressed_file)

    print(f"✅ Best chunk size: {best_chunk_size} bytes (Compression Ratio: {best_compression_ratio:.4f})")
    return best_chunk_size

# Quantum circuit simulation
def quantum_compression_simulation(file_size):
    num_qubits = math.ceil(math.log2(file_size)) + 1  # X+1 qubits
    qc = QuantumCircuit(num_qubits)

    qc.h(range(num_qubits))  # Superposition
    for qubit in range(num_qubits - 1):
        qc.cx(qubit, qubit + 1)  # Entanglement

    print(f"⚛️ Quantum Circuit Created with {num_qubits} qubits (for simulation).")

# Compression process
def process_compression(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = find_best_chunk_size(input_filename)

    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.b"
    restored_file = f"extract.{Path(input_filename).name}"

    # Start compression timer
    start_compress = time.perf_counter_ns()

    reverse_and_save(input_filename, reversed_file, best_chunk_size)
    compress_reversed(reversed_file, compressed_file, best_chunk_size)

    # End compression timer
    end_compress = time.perf_counter_ns()
    compression_time_ns = end_compress - start_compress
    print(f"⏳ Compression time: {compression_time_ns} nanoseconds")

    # Start extraction timer
    start_extract = time.perf_counter_ns()

    decompress_and_restore(compressed_file, restored_file)

    # End extraction timer
    end_extract = time.perf_counter_ns()
    extraction_time_ns = end_extract - start_extract
    print(f"⏳ Extraction time: {extraction_time_ns} nanoseconds")

    quantum_compression_simulation(file_size)

    print(f"✅ Three files remain:\n  1️⃣ Original: '{input_filename}'\n  2️⃣ Best Compressed: '{compressed_file}'\n  3️⃣ Restored: '{restored_file}'")

    os.remove(reversed_file)  # Cleanup temporary file

# Extraction process
def process_extraction(input_filename):
    restored_file = f"extract.{Path(input_filename).name.replace('compress.', '').replace('.b', '')}"

    # Start extraction timer
    start_extract = time.perf_counter_ns()

    decompress_and_restore(input_filename, restored_file)

    # End extraction timer
    end_extract = time.perf_counter_ns()
    extraction_time_ns = end_extract - start_extract
    print(f"⏳ Extraction time: {extraction_time_ns} nanoseconds")

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