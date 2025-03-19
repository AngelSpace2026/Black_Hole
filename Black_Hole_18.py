import os
import math
import time
import zstandard as zstd
from pathlib import Path
from qiskit import QuantumCircuit

# Function to reverse chunks of data and save
def reverse_and_save(input_filename, reversed_filename, chunk_size):
    try:
        with open(input_filename, 'rb') as infile, open(reversed_filename, 'wb') as outfile:
            while chunk := infile.read(chunk_size):
                outfile.write(chunk[::-1])  # Reverse the chunk before writing
        return os.path.getsize(reversed_filename)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Function to compress the reversed file using zstd
def compress_reversed(reversed_filename, compressed_filename):
    try:
        with open(reversed_filename, 'rb') as infile:
            compressed_data = zstd.compress(infile.read())  # Compress entire reversed file
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

# Function to simulate a quantum circuit with X+1 qubits
def quantum_compress(file_size):
    X = math.floor(math.log2(file_size)) if file_size > 0 else 1
    num_qubits = X + 1  # X+1 rule

    print(f"🔬 Quantum Simulation: Using {num_qubits} qubits (X = {X}, X+1 rule applied)")
    
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))  # Apply Hadamard gate to each qubit
    for qubit in range(num_qubits - 1):  
        qc.cx(qubit, qubit + 1)  # Apply CNOT for entanglement
    
    print(f"✅ Quantum Circuit with {num_qubits} qubits created.")

# Main function to process compression
def check_extract_save_num_check_and_chunk(input_filename):
    file_size = os.path.getsize(input_filename)

    # File paths
    reversed_file = input_filename + ".rev"
    compressed_file = f"{input_filename}.b"
    restored_file = f"extract.{Path(input_filename).name}"

    # Start compression timer
    start_compress = time.perf_counter_ns()

    # Process compression
    reverse_and_save(input_filename, reversed_file, file_size)
    compress_reversed(reversed_file, compressed_file)

    # End compression timer
    end_compress = time.perf_counter_ns()
    compression_time_ns = end_compress - start_compress
    print(f"⏳ Compression time: {compression_time_ns} nanoseconds")

    # Start extraction timer
    start_extract = time.perf_counter_ns()

    decompress_and_restore(compressed_file, restored_file, file_size)

    # End extraction timer
    end_extract = time.perf_counter_ns()
    extraction_time_ns = end_extract - start_extract
    print(f"⏳ Extraction time: {extraction_time_ns} nanoseconds")

    # Check file integrity
    original_size = os.path.getsize(input_filename)
    restored_size = os.path.getsize(restored_file)

    print(f"Original file size: {original_size} bytes.")
    print(f"Restored file size: {restored_size} bytes.")

    if original_size == restored_size:
        print("✅ File successfully restored with correct size.")
    else:
        print("❌ Warning: Restored file size does not match the original.")

    # Cleanup temporary files
    os.remove(reversed_file) if os.path.exists(reversed_file) else None
    print(f"✅ Removed temporary file '{reversed_file}'.")

    print(f"✅ Three files are left:\n  1️⃣ Original: '{input_filename}'\n  2️⃣ Compressed: '{compressed_file}'\n  3️⃣ Restored: '{restored_file}'")

# Main interactive function
def main():
    print("Created by Jurijus Pacalovas.")
    
    mode = input("Enter mode (compress/extract): ").strip().lower()
    input_file = input("Enter input file name: ").strip()

    if mode == "compress":
        check_extract_save_num_check_and_chunk(input_file)
        quantum_compress(os.path.getsize(input_file))

    elif mode == "extract":
        restored_file = f"extract.{Path(input_file).stem}"

        # Start extraction timer
        start_extract = time.perf_counter_ns()

        decompress_and_restore(input_file, restored_file, os.path.getsize(restored_file))

        # End extraction timer
        end_extract = time.perf_counter_ns()
        extraction_time_ns = end_extract - start_extract
        print(f"⏳ Extraction time: {extraction_time_ns} nanoseconds")

        quantum_compress(os.path.getsize(restored_file))

    else:
        print("❌ Invalid mode selected.")

if __name__ == "__main__":
    main()