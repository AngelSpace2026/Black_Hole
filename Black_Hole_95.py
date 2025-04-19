import random
import time
from qiskit import QuantumCircuit
from tqdm import tqdm

# --- Quantum Random Bytes Mock (without Aer or execute) ---
def quantum_random_bytes_mock(num_bits=2000):
    # Generate random bits as a classical substitute
    return bytes([random.getrandbits(8) for _ in range((num_bits + 7) // 8)])

# --- Reversible Transformation Functions ---
def reverse_chunk(data, chunk_size): return data[::-1]

def add_random_noise(data, noise_level=10):
    return bytes([byte ^ random.randint(0, noise_level) for byte in data])

def subtract_1_from_each_byte(data):
    return bytes([(byte - 1) % 256 for byte in data])

def move_bits_left(data, n):
    n = n % 8
    return bytes([(byte << n & 0xFF) | (byte >> (8 - n)) & 0xFF for byte in data])

def move_bits_right(data, n):
    n = n % 8
    return bytes([(byte >> n & 0xFF) | (byte << (8 - n)) & 0xFF for byte in data])

def quantum_minus_blocks(data, block_size_bits=64):
    block_size = block_size_bits // 8
    if block_size == 0:
        raise ValueError("Block size cannot be 0 bytes")
    transformed_data = bytearray()
    metadata = bytearray()
    qr_bytes = quantum_random_bytes_mock(2000)  # Mocked quantum bytes
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        if len(block) < block_size:
            block += bytes(block_size - len(block))
        transformed_block = bytes([(b - qr_bytes[j % len(qr_bytes)]) % 256 for j, b in enumerate(block)])
        transformed_data.extend(transformed_block)
        metadata.extend(qr_bytes)
    return bytes(transformed_data), bytes(metadata)

def xor_with_binary_pattern(data):
    patterns = [0b01, 0b10, 0b001, 0b100, 0b0001, 0b1000]
    block_size = 8
    transformed = bytearray()
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size:
            block += bytes(block_size - len(block))
        pattern = random.choice(patterns)
        pattern_bytes = (pattern.to_bytes(1, 'big') * block_size)[:block_size]
        xor_block = bytes([b ^ pattern_bytes[j] for j, b in enumerate(block)])
        transformed.extend(xor_block)
    return bytes(transformed)

def add_block_size_64(data):
    transformed_data = bytearray()
    block_size = 64
    i = 0
    while i < len(data):
        block = data[i:i + block_size]
        if len(block) < block_size:
            block += bytes(block_size - len(block))
        transformed_data.extend((block_size).to_bytes(2, 'big'))
        transformed_data.extend(block)
        i += block_size
    return bytes(transformed_data)

def rle_encode_1byte(data):
    if not data:
        return data
    encoded_data = bytearray()
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1] and count < 255:
            count += 1
        else:
            encoded_data.extend([data[i - 1]])
            encoded_data.extend([count])
            count = 1
    encoded_data.extend([data[-1]])
    encoded_data.extend([count])
    return bytes(encoded_data)

# --- Placeholder for PAQ compression using reverse for now ---
class zlib_wrapper:
    @staticmethod
    def compress(data): return data[::-1]
    @staticmethod
    def decompress(data): return data[::-1]

def apply_random_transformations(data, num_transforms=10):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True),
        (quantum_minus_blocks, False),
        (xor_with_binary_pattern, False)
    ]
    marker = 0
    transformed_data = data
    for i in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        try:
            if transform == quantum_minus_blocks:
                transformed_data, _ = transform(transformed_data, block_size_bits=64)
            elif needs_param:
                param = random.randint(1, 7)
                transformed_data = transform(transformed_data, param)
            else:
                transformed_data = transform(transformed_data)
            marker |= (1 << (i % 8))
        except Exception as e:
            print(f"Error applying {transform.__name__}: {e}")
    if len(transformed_data) < 1024:
        transformed_data = rle_encode_1byte(transformed_data)
    transformed_data = add_block_size_64(transformed_data)
    return transformed_data, marker

def compress_data(data):
    try:
        return zlib_wrapper.compress(data)
    except Exception as e:
        print(f"Compression error: {e}")
        return data

def decompress_data(data):
    try:
        return zlib_wrapper.decompress(data)
    except Exception as e:
        print(f"Decompression error: {e}")
        return data

def compress_with_iterations(data, attempts, iterations):
    best_compressed = compress_data(data)
    best_size = len(best_compressed)
    for i in tqdm(range(attempts), desc="Attempts"):
        try:
            current_data = data
            best_this_attempt = best_compressed
            for j in tqdm(range(iterations), desc=f"Iter {i + 1}", leave=False):
                transformed, marker = apply_random_transformations(current_data)
                compressed = compress_data(transformed)
                if len(compressed) < len(best_this_attempt):
                    best_this_attempt = compressed
                current_data = decompress_data(best_this_attempt)
            if len(best_this_attempt) < best_size:
                best_compressed = best_this_attempt
                best_size = len(best_this_attempt)
        except Exception as e:
            print(f"Iteration {i + 1} error: {e}")
    return best_compressed

def handle_file_io(func, file_name, data=None):
    try:
        if data is None:
            with open(file_name, 'rb') as f:
                return func(f.read())
        else:
            with open(file_name, 'wb') as f:
                f.write(data)
            return True
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"I/O error: {e}")
    return None

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Enter a positive integer.")
        except ValueError:
            print("Invalid input.")

def main():
    choice = input("Choose (1: Compress, 2: Extract): ")
    in_file = input("Input file: ")
    out_file = input("Output file: ")
    if choice == '1':
        attempts = get_positive_integer("Compression attempts: ")
        iterations = get_positive_integer("Iterations per attempt: ")
        data = handle_file_io(lambda x: x, in_file)
        if data:
            start = time.time()
            compressed_data = compress_with_iterations(data, attempts, iterations)
            end = time.time()
            handle_file_io(lambda x: x, out_file, compressed_data)
            print(f"Compressed to {out_file} in {end - start:.2f} seconds")
    elif choice == '2':
        data = handle_file_io(decompress_data, in_file)
        if data:
            handle_file_io(lambda x: x, out_file, data)
            print(f"Extracted to {out_file}")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()