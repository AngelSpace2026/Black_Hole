from qiskit import QuantumRegister
import os

# Optional PAQ support
try:
    import paq
    paq_available = True
except ImportError:
    paq_available = False

QUANTUM_FILE = 'quantum_memory.qubits'

def store_in_qubits(data):
    qubit_data = data[:250]
    qubit_bits = len(qubit_data) * 8

    # Simulate quantum register creation
    QuantumRegister(qubit_bits, name='q')
    print(f"Simulated storing first 250 bytes ({qubit_bits} bits) in qubits.")

    # Save qubit data to persistent file
    with open(QUANTUM_FILE, 'wb') as f:
        f.write(qubit_data)

    return data[250:]

def load_qubits():
    if not os.path.exists(QUANTUM_FILE):
        print("Quantum data missing. Cannot extract.")
        return None
    with open(QUANTUM_FILE, 'rb') as f:
        return f.read()

def compress_to_file(input_file, output_file, use_paq=True):
    with open(input_file, 'rb') as f:
        data = f.read()

    if use_paq:
        if not paq_available:
            raise RuntimeError("PAQ module not available.")
        compressed = paq.compress(data)
    else:
        compressed = data

    size_bytes = len(compressed).to_bytes(4, byteorder='big')
    all_data = size_bytes + compressed
    reduced_data = store_in_qubits(all_data)

    with open(output_file, 'wb') as f:
        f.write(reduced_data)

    print(f"Compressed and stored '{output_file}' without first 250 bytes (stored in Qubits).")

def extract_from_file(input_file, output_file, use_paq=True):
    qubit_data = load_qubits()
    if not qubit_data:
        return

    with open(input_file, 'rb') as f:
        file_data = f.read()

    full_data = qubit_data + file_data
    size = int.from_bytes(full_data[:4], byteorder='big')
    compressed = full_data[4:4+size]

    if use_paq:
        if not paq_available:
            raise RuntimeError("PAQ module not available.")
        data = paq.decompress(compressed)
    else:
        data = compressed

    with open(output_file, 'wb') as f:
        f.write(data)

    print(f"Extracted and restored '{output_file}' successfully.")

# CLI
if __name__ == "__main__":
    print("=== Quantum Compression System ===")
    print("1. Compress")
    print("2. Extract")
    mode = input("Choose mode (1 or 2): ").strip()

    use_paq = input("Use PAQ for compression/extraction? (yes/no): ").strip().lower() == 'yes'

    if mode == "1":
        in_file = input("Enter input file name: ")
        out_file = input("Enter output (compressed) file name: ")
        compress_to_file(in_file, out_file, use_paq=use_paq)
    elif mode == "2":
        in_file = input("Enter input (compressed) file name: ")
        out_file = input("Enter output (extracted) file name: ")
        extract_from_file(in_file, out_file, use_paq=use_paq)
    else:
        print("Invalid choice.")