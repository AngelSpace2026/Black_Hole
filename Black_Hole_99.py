from qiskit import QuantumRegister
import paq
import random

# Function to simulate storing data in qubits
def store_in_qubits(data):
    bit_length = len(data) * 8
    chunks = (bit_length // 2000) + (1 if bit_length % 2000 != 0 else 0)
    
    qubits = []
    for i in range(chunks):
        chunk_size = min(2000, bit_length - i * 2000)
        qubits.append(QuantumRegister(chunk_size, name=f'q{i}'))

    print(f"Simulated storing data in {len(qubits)} quantum registers.")
    return qubits

# Compress with optional use of PAQ
def compress_to_file(input_file, output_file, use_paq=True):
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())

    if len(data) > 250:
        indices_to_remove = sorted(random.sample(range(len(data)), 250), reverse=True)
        for idx in indices_to_remove:
            del data[idx]
    else:
        print("Warning: File too small to remove 250 bytes.")
        data = bytearray()

    compressed = paq.compress(bytes(data)) if use_paq else data
    size_bytes = len(compressed).to_bytes(4, byteorder='big')
    final_data = size_bytes + compressed

    store_in_qubits(final_data)

    with open(output_file, 'wb') as f:
        f.write(final_data)

    print("Compression complete. Stored in file:", output_file)

# Extract with optional use of PAQ
def extract_from_file(input_file, output_file, use_paq=True):
    with open(input_file, 'rb') as f:
        stored_data = f.read()

    size = int.from_bytes(stored_data[:4], byteorder='big')
    compressed = stored_data[4:4+size]

    data = paq.decompress(compressed) if use_paq else compressed

    with open(output_file, 'wb') as f:
        f.write(data)

    print("Extraction complete. Output file:", output_file)

# CLI
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Compress")
    print("2. Extract")
    mode = input("Enter 1 or 2: ")

    print("Use PAQ compression? (y/n):")
    use_paq = input().strip().lower() == "y"

    if mode == "1":
        in_file = input("Enter input file name: ")
        out_file = input("Enter output (compressed) file name: ")
        compress_to_file(in_file, out_file, use_paq)
    elif mode == "2":
        in_file = input("Enter input (compressed) file name: ")
        out_file = input("Enter output (extracted) file name: ")
        extract_from_file(in_file, out_file, use_paq)
    else:
        print("Invalid choice.")