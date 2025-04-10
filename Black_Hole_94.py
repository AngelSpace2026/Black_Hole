import os
import random
import time
import zlib
import paq  # PAQ compression module (ensure it's working)
from tqdm import tqdm

# Compression using zlib (placeholder for PAQ)
class zlib_wrapper:
    @staticmethod
    def compress(data):
        return paq.compress(data)

    @staticmethod
    def decompress(data):
        return paq.decompress(data)

# Reversible Transformation Functions
def reverse_chunk(data, chunk_size):
    return data[::-1]

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

# Function for PAQ compression check on various bit shifts and sizes
def apply_paq_compression(data, block_sizes=[2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]):
    best_compressed = None
    best_size = float('inf')
    
    for block_size_bits in block_sizes:
        block_size = block_size_bits // 8
        if block_size == 0:
            continue  # Skip if the block size is 0 (should not happen, but good for safety)
        
        for shift in range(1, block_size_bits + 1):  # Shift sizes from 1 to block_size_bits
            # Process data in chunks
            chunked_data = [data[i:i + block_size] for i in range(0, len(data), block_size)]
            processed_data = b""

            for chunk in chunked_data:
                # Move bits and apply shift
                shifted_chunk = move_bits_left(chunk, shift)
                processed_data += shifted_chunk

            # Now compress the transformed chunk with PAQ
            compressed = paq.compress(processed_data)
            if len(compressed) < best_size:
                best_compressed = compressed
                best_size = len(compressed)

        # Now also apply doubling to 2^32 for large blocks (1024 bits)
        if block_size_bits == 1024:
            for shift in range(1, 33):  # Apply shift up to 2^32 for 1024-bit block
                shifted_data = move_bits_left(data, shift)
                compressed = paq.compress(shifted_data)
                if len(compressed) < best_size:
                    best_compressed = compressed
                    best_size = len(compressed)

    return best_compressed

# Apply random transformations + always RLE
def apply_random_transformations(data, num_transforms=10):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True),
    ]
    transformed_data = data
    for _ in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        try:
            if needs_param:
                param = random.randint(1, 7)
                transformed_data = transform(transformed_data, param)
            else:
                transformed_data = transform(transformed_data)
        except Exception as e:
            print(f"Error applying transformation {transform.__name__}: {e}")
    return transformed_data

# Compression function with PAQ compression
def compress_with_paq(data):
    best_compressed = apply_paq_compression(data)
    return best_compressed

# Iterative compression logic
def compress_with_iterations(data, attempts, iterations):
    best_compressed = zlib_wrapper.compress(data)
    best_size = len(best_compressed)

    for i in tqdm(range(attempts), desc="Compression Attempts"):
        try:
            current_data = data
            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                transformed_data = apply_random_transformations(current_data)
                # Apply PAQ compression
                compressed = compress_with_paq(transformed_data)
                if len(compressed) < len(best_compressed):
                    best_compressed = compressed
                current_data = zlib_wrapper.decompress(best_compressed)
            if len(best_compressed) < best_size:
                best_size = len(best_compressed)
        except Exception as e:
            print(f"Error during iteration {i + 1}: {e}")
    return best_compressed

# File I/O
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
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"Error during file I/O: {e}")
    return None

# User input
def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Main driver
def main():
    choice = input("Choose (1: Compress, 2: Extract): ")
    in_file = input("Input file: ")
    out_file = input("Output file: ")

    if choice == '1':
        attempts = get_positive_integer("Enter number of compression attempts: ")
        iterations = get_positive_integer("Enter number of iterations per attempt: ")
        data = handle_file_io(lambda x: x, in_file)
        if data:
            start_time = time.time()
            compressed_data = compress_with_iterations(data, attempts, iterations)
            end_time = time.time()
            handle_file_io(lambda x: x, out_file, compressed_data)
            print(f"Compressed to {out_file} in {end_time - start_time:.2f} seconds")
    elif choice == '2':
        data = handle_file_io(zlib_wrapper.decompress, in_file)
        if data:
            handle_file_io(lambda x: x, out_file, data)
            print(f"Extracted to {out_file}")
        else:
            print("Invalid choice. Please enter 1 for compression or 2 for extraction.")

if __name__ == "__main__":
    main()