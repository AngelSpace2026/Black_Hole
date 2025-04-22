from qiskit import QuantumRegister
import zlib

# Function to simulate storing data in qubits (chunked if too large)
def store_in_qubits(data):
    data = data[250:]  # Delete the first 250 bytes
    bit_length = len(data) * 8

    chunks = (bit_length // 2000) + (1 if bit_length % 2000 != 0 else 0)
    
    qubits = []
    for i in range(chunks):
        chunk_size = min(2000, (len(data) - i * 250) * 8)
        qubits.append(QuantumRegister(chunk_size, name=f'q{i}'))

    print(f"Simulated storing data in {len(qubits)} quantum registers.")
    return qubits

# Write compressed file (no 4-byte header)
def compress_to_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    compressed = zlib.compress(data)
    
    store_in_qubits(compressed)  # Simulate storing in qubits

    with open(output_file, 'wb') as f:
        f.write(compressed)

    print("Compression complete. Stored in file:", output_file)

# Read compressed file (no 4-byte header)
def extract_from_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        compressed = f.read()

    data = zlib.decompress(compressed)

    with open(output_file, 'wb') as f:
        f.write(data)

    print("Extraction complete. Output file:", output_file)

# CLI
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Compress")
    print("2. Extract")
    mode = input("Enter 1 or 2: ")

    if mode == "1":
        in_file = input("Enter input file name: ")
        out_file = input("Enter output (compressed) file name: ")
        compress_to_file(in_file, out_file)
    elif mode == "2":
        in_file = input("Enter input (compressed) file name: ")
        out_file = input("Enter output (extracted) file name: ")
        extract_from_file(in_file, out_file)
    else:
        print("Invalid choice.")
