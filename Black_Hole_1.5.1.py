import os
import time
import zstandard as zstd  # Importing Zstd for compression
from pathlib import Path
import struct
from qiskit import QuantumCircuit

# Function to run a quantum computation (without Aer, transpile, or execute)
def quantum_computation_example():
    print("\n🔮 Running a basic quantum computation without Aer, transpile, or execute:")

    # Create a quantum circuit with 2 qubits and 2 classical bits
    circuit = QuantumCircuit(2, 2)
    
    # Apply a Hadamard gate to the first qubit
    circuit.h(0)
    
    # Apply a CNOT gate between the first and second qubits
    circuit.cx(0, 1)
    
    # Measure both qubits
    circuit.measure([0, 1], [0, 1])
    
    # Display the quantum circuit
    print("\nQuantum Circuit:")
    print(circuit)

# Function to reverse data in chunks based on chunk count
def reverse_and_save(input_filename, reversed_filename, chunk_size, num_chunks):
    with open(input_filename, 'rb') as infile, open(reversed_filename, 'wb') as outfile:
        data = infile.read()
        chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Reverse the first `num_chunks` chunks
        for i in range(num_chunks):
            if i < len(chunked_data):
                chunked_data[i] = chunked_data[i][::-1]
        
        outfile.write(b"".join(chunked_data))

# Function to compress and save metadata (chunk size + num_chunks) with Zstd
def compress_reversed_with_zstd(reversed_filename, compressed_filename, chunk_size, num_chunks):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Store metadata (num_chunks) in the first 2 bytes
    metadata = struct.pack(">H", num_chunks)  # Store num_chunks as a 10-bit value in 2 bytes

    # Compress data using Zstd
    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Function to decompress and restore the original file with Zstd
def decompress_and_restore_with_zstd(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    # Decompress the data using Zstd
    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)

    # Read metadata (first 2 bytes for num_chunks)
    num_chunks = struct.unpack(">H", decompressed_data[:2])[0] & 0x03FF  # Mask 10 bits
    reversed_data = decompressed_data[2:]  # Actual reversed data

    # Reconstruct the original file by reversing the first `num_chunks` chunks
    chunk_size = len(reversed_data) // num_chunks  # Approximate chunk size
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
            compress_reversed_with_zstd(reversed_file, compressed_file, chunk_size, num_chunks)

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

# Compression process with nanosecond timing
def process_compression(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size, best_num_chunks = find_best_parameters(input_filename)

    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.b"
    restored_file = f"extract.{Path(input_filename).name}"

    # Start compression timer
    start_compress = time.perf_counter_ns()

    reverse_and_save(input_filename, reversed_file, best_chunk_size, best_num_chunks)
    compress_reversed_with_zstd(reversed_file, compressed_file, best_chunk_size, best_num_chunks)

    # End compression timer
    end_compress = time.perf_counter_ns()
    compression_time_ns = end_compress - start_compress
    print(f"⏳ Compression time: {compression_time_ns} nanoseconds")

    # Start extraction timer
    start_extract = time.perf_counter_ns()

    decompress_and_restore_with_zstd(compressed_file, restored_file)

    # End extraction timer
    end_extract = time.perf_counter_ns()
    extraction_time_ns = end_extract - start_extract
    print(f"⏳ Extraction time: {extraction_time_ns} nanoseconds")

    print(f"✅ Three files remain:\n  1️⃣ Original: '{input_filename}'\n  2️⃣ Best Compressed: '{compressed_file}'\n  3️⃣ Restored: '{restored_file}'")

    os.remove(reversed_file)  # Cleanup temporary file

# Extraction process with nanosecond timing
def process_extraction(input_filename):
    restored_file = f"extract.{Path(input_filename).name.replace('compress.', '').replace('.b', '')}"

    # Start extraction timer
    start_extract = time.perf_counter_ns()

    decompress_and_restore_with_zstd(input_filename, restored_file)

    # End extraction timer
    end_extract = time.perf_counter_ns()
    extraction_time_ns = end_extract - start_extract
    print(f"⏳ Extraction time: {extraction_time_ns} nanoseconds")

    print(f"✅ Extracted file: '{restored_file}'")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")
    
    # Always perform quantum computation (without Aer, transpile, or execute)
    quantum_computation_example()

    # User option for compress or extract
    mode = input("Enter mode (1 for compress, 2 for extract): ").strip()

    if mode == "1":
        input_file = input("Enter input file name to compress: ").strip()
        process_compression(input_file)
    elif mode == "2":
        input_file = input("Enter input file name to extract: ").strip()
        process_extraction(input_file)
    else:
        print("❌ Invalid mode selected. Please choose 1 or 2.")

if __name__ == "__main__":
    main()