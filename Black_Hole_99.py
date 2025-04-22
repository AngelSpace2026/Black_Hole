import zlib
from qiskit import QuantumRegister

# Simulated RAM-based quantum memory (for this session only)
quantum_memory = []

# Store bytes in Quantum Registers (simulated only)
def store_in_qubits(data250):
    global quantum_memory
    quantum_memory.clear()
    for i, byte in enumerate(data250):
        qr = QuantumRegister(8, name=f'q{i}_{byte}')
        quantum_memory.append((qr, byte))
    print(f"Stored {len(data250)} bytes in simulated qubits (in memory).")

# Retrieve bytes from simulated qubits
def read_from_qubits():
    if len(quantum_memory) != 250:
        raise ValueError("Qubit memory does not contain 250 bytes.")
    return bytes([byte for (_, byte) in quantum_memory])

# Compress function: store 250 bytes in qubits and compress rest
def compress_data(data):
    if len(data) < 250:
        raise ValueError("Input must be at least 250 bytes.")

    first_250 = data[:250]
    rest = data[250:]

    store_in_qubits(first_250)

    compressed = zlib.compress(rest)
    size_bytes = len(compressed).to_bytes(4, byteorder='big')
    return size_bytes + compressed

# Extract function: decompress and add back 250 bytes from qubits
def extract_data(compressed_data):
    size = int.from_bytes(compressed_data[:4], byteorder='big')
    compressed = compressed_data[4:4+size]
    decompressed = zlib.decompress(compressed)
    restored = read_from_qubits()
    return restored + decompressed

# CLI: Only works in one run
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Compress")
    print("2. Extract (same session)")
    mode = input("Enter 1 or 2: ")

    if mode == "1":
        in_file = input("Enter input file name: ")
        out_file = input("Enter output compressed file name: ")
        with open(in_file, 'rb') as f:
            original_data = f.read()
        result = compress_data(original_data)
        with open(out_file, 'wb') as f:
            f.write(result)
        print(f"Compressed and saved to {out_file}. Keep session running for extraction.")

    elif mode == "2":
        in_file = input("Enter compressed file name: ")
        out_file = input("Enter output restored file name: ")
        with open(in_file, 'rb') as f:
            compressed = f.read()
        result = extract_data(compressed)
        with open(out_file, 'wb') as f:
            f.write(result)
        print(f"Extracted and restored file: {out_file}")
    else:
        print("Invalid choice.")