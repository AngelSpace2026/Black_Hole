from qiskit import QuantumRegister, QuantumCircuit
import zlib

# -------- Transformations --------
def reverse_data(data):
    return data[::-1]

def subtract_one(data):
    return bytes((b - 1) % 256 for b in data)

def shift_left(data):
    return bytes((b << 1) & 0xFF for b in data)

def shift_right(data):
    return bytes((b >> 1) for b in data)

def delete_bits(data, max_bits):
    bytes_to_delete = min(len(data), max_bits // 8)
    return data[:-bytes_to_delete] if bytes_to_delete > 0 else data

# -------- Compression --------
def compress_mode(input_file, output_file, iterations=3000):
    with open(input_file, 'rb') as f:
        original_data = f.read()

    # Simulate 3000 Qubits
    quantum_register = QuantumRegister(3000, "q")
    quantum_circuit = QuantumCircuit(quantum_register)

    data = original_data
    iterations = min(iterations, 3000)

    for _ in range(iterations):
        data = reverse_data(data)
        data = subtract_one(data)
        data = shift_left(data)
        data = shift_right(data)
        data = delete_bits(data, max_bits=8)  # 1 Qubit = delete up to 8 bits

    compressed = zlib.compress(data)
    with open(output_file, 'wb') as f:
        f.write(compressed)

    print("Compression complete. Saved to", output_file)

# -------- Extraction --------
def extract_mode(input_file, output_file):
    with open(input_file, 'rb') as f:
        compressed = f.read()

    try:
        data = zlib.decompress(compressed)
        with open(output_file, 'wb') as f:
            f.write(data)
        print("Extraction complete. Saved to", output_file)
    except Exception as e:
        print("Decompression failed:", e)

# -------- CLI --------
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Compress")
    print("2. Extract")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        input_file = input("Input file name: ")
        output_file = input("Output compressed file name: ")
        iterations = int(input("Number of iterations (max 3000): "))
        compress_mode(input_file, output_file, iterations)
    elif choice == "2":
        input_file = input("Input compressed file name: ")
        output_file = input("Output extracted file name: ")
        extract_mode(input_file, output_file)
    else:
        print("Invalid choice.")