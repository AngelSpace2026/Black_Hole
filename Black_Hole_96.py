from qiskit import QuantumRegister
import paq

# Function to simulate storing data in qubits (chunked if too large)
def store_in_qubits(data):
    bit_length = len(data) * 8  # Convert data length to bits
    
    # Calculate how many chunks of 2000 qubits (2000 bits) are needed
    chunks = (bit_length // 2000) + (1 if bit_length % 2000 != 0 else 0)
    
    qubits = []
    for _ in range(chunks):
        qubits.append(QuantumRegister(min(2000, len(data) * 8), name='q'))
        data = data[2000:]  # Slice off the chunk

    print(f"Simulated storing data in {len(qubits)} quantum registers.")
    return qubits

# Write compressed file with 4-byte size header
def compress_to_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    compressed = paq.compress(data)
    size_bytes = len(compressed).to_bytes(4, byteorder='big')  # 4-byte header for size
    final_data = size_bytes + compressed

    store_in_qubits(final_data)  # Simulate storing in qubits

    with open(output_file, 'wb') as f:
        f.write(final_data)

    print("Compression complete. Stored in file:", output_file)

# Read compressed file with 4-byte header and extract
def extract_from_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        stored_data = f.read()

    size = int.from_bytes(stored_data[:4], byteorder='big')
    compressed = stored_data[4:4+size]

    data = paq.decompress(compressed)

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