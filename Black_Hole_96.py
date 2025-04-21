import zlib
from qiskit import QuantumRegister

# Simulate storing in qubits
def store_in_qubits(data):
    bit_length = len(data) * 8
    if bit_length > 3000:
        raise ValueError("Data too large to store in 3000 qubits.")
    qubits = QuantumRegister(bit_length, name='q')
    print(f"Simulated storing {bit_length} bits in {len(qubits)} qubits.")
    return qubits

# Append compressed data with 4-byte size header to end of file
def compress_append_to_file(input_file):
    with open(input_file, 'rb') as f:
        original_data = f.read()

    compressed = zlib.compress(original_data)
    size_bytes = len(compressed).to_bytes(4, byteorder='big')
    append_data = size_bytes + compressed

    store_in_qubits(append_data)

    with open(input_file, 'ab') as f:
        f.write(append_data)

    print(f"Compressed data appended to end of: {input_file}")

# Extract and remove compressed data from the end
def extract_from_end(input_file, output_file):
    with open(input_file, 'rb') as f:
        full_data = f.read()

    if len(full_data) < 4:
        raise ValueError("File too small for valid extraction.")

    size_bytes = full_data[-(4):]
    compressed_size = int.from_bytes(size_bytes, byteorder='big')
    total_append_size = compressed_size + 4

    if len(full_data) < total_append_size:
        raise ValueError("Not enough data for stated compressed size.")

    compressed_data = full_data[-total_append_size + 4:-4]
    decompressed_data = zlib.decompress(compressed_data)

    # Save decompressed data
    with open(output_file, 'wb') as f:
        f.write(decompressed_data)

    # Remove the appended data from original file
    new_data = full_data[:-total_append_size]
    with open(input_file, 'wb') as f:
        f.write(new_data)

    print(f"Extraction complete. Original file restored, output saved to: {output_file}")

# CLI
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Compress (append to file)")
    print("2. Extract and restore")
    mode = input("Enter 1 or 2: ")

    if mode == "1":
        in_file = input("Enter file name to compress and append to: ")
        compress_append_to_file(in_file)
    elif mode == "2":
        in_file = input("Enter file name to extract from: ")
        out_file = input("Enter output file name for decompressed data: ")
        extract_from_end(in_file, out_file)
    else:
        print("Invalid choice.")