import os
import zlib

# Class for deleting bits in the data with a limit of total bits to delete
class BitDeleter:
    def __init__(self, max_total_bits=3000):
        self.total_deleted = 0
        self.max_total_bits = max_total_bits

    def delete_bits(self, data, bits_to_delete):
        """Deletes up to 'bits_to_delete' bits from the data, but no more than max_total_bits."""
        if self.total_deleted >= self.max_total_bits:
            return data
        remaining_bits = self.max_total_bits - self.total_deleted
        bits_to_delete = min(bits_to_delete, remaining_bits)
        bytes_to_delete = (bits_to_delete + 7) // 8  # Convert bits to bytes
        self.total_deleted += bits_to_delete
        return data[:-bytes_to_delete] if bytes_to_delete < len(data) else b''

# Basic transformation functions
def reverse_chunk(data):
    """Reverses the data chunk."""
    return data[::-1]

def subtract_1_from_each_byte(data):
    """Subtracts 1 from each byte in the data."""
    return bytes([(b - 1) % 256 for b in data])

def move_bits_left(data):
    """Shifts each byte's bits to the left."""
    return bytes([(b << 1) & 0xFF for b in data])

def move_bits_right(data):
    """Shifts each byte's bits to the right."""
    return bytes([b >> 1 for b in data])

# Placeholder for PAQ compression (you can replace it with actual PAQ compression if needed)
def paq_compress(data):
    """Compresses the data using zlib as a placeholder for PAQ compression."""
    return zlib.compress(data)

def paq_decompress(data):
    """Decompresses the data using zlib as a placeholder for PAQ decompression."""
    return zlib.decompress(data)

# Simulate qubit measurement (0 or 1)
def simulate_qubit_measurement():
    """Simulates a qubit measurement (returns 0 or 1)."""
    return 0 if os.urandom(1)[0] % 2 == 0 else 1

# Function to compress a file using transformations and bit deletion
def compress_file(input_file, output_file, iterations=3000):
    with open(input_file, 'rb') as f:
        original_data = f.read()

    deleter = BitDeleter(max_total_bits=3000)  # Initialize bit deleter
    best_data = original_data
    best_compressed = paq_compress(original_data)  # Initial compression

    for _ in range(iterations):
        data = original_data
        qubit_result = simulate_qubit_measurement()

        if qubit_result == 0:
            # Apply transformations for qubit result 0
            data = reverse_chunk(data)
            data = move_bits_left(data)
            data = deleter.delete_bits(data, 8)  # Delete 8 bits in this iteration
        else:
            # Apply transformations for qubit result 1
            data = subtract_1_from_each_byte(data)
            data = move_bits_right(data)
            data = deleter.delete_bits(data, 16)  # Delete 16 bits in this iteration

        compressed = paq_compress(data)
        if len(compressed) < len(best_compressed):
            best_compressed = compressed
            best_data = data

    with open(output_file, 'wb') as f:
        f.write(best_compressed)
    print("Compression complete. Saved to", output_file)

# Function to decompress a file
def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        compressed_data = f.read()
    data = paq_decompress(compressed_data)

    with open(output_file, 'wb') as f:
        f.write(data)
    print("Decompression complete. Saved to", output_file)

# CLI for user interaction
if __name__ == "__main__":
    choice = input("Choose (1) Compress or (2) Decompress: ")
    input_file = input("Input file name: ")
    output_file = input("Output file name: ")

    if choice == '1':
        compress_file(input_file, output_file)
    elif choice == '2':
        decompress_file(input_file, output_file)
    else:
        print("Invalid choice.")