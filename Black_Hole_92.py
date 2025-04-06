import os
import random
import time
from tqdm import tqdm
import paq  # Placeholder for actual PAQ module

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

# Identify all-zero or all-one blocks

def find_zero_and_one_blocks(data, block_size=256):
    blocks = []
    i = 0
    while i < len(data):
        block = data[i:i + block_size]
        
        if all(byte == 0 for byte in block):  # All zeros
            blocks.append(("zero", block))
        elif all(byte == 255 for byte in block):  # All ones
            blocks.append(("one", block))
        i += block_size
    return blocks

# Apply transformations to all-zero and all-one blocks

def transform_zero_and_one_blocks(blocks):
    transformed_data = bytearray()

    for block_type, block in blocks:
        if block_type == "zero":
            transformed_data.extend(move_bits_left(block, 1))  # Apply left shift to all-zero block
            transformed_data.append(1)  # Mark the block as modified
        elif block_type == "one":
            transformed_data.extend(move_bits_right(block, 1))  # Apply right shift to all-one block
            transformed_data.append(1)  # Mark the block as modified
        else:
            transformed_data.extend(block)
            transformed_data.append(0)  # Mark the block as unchanged
    
    return bytes(transformed_data)

# Compression/Decompression

def compress_data(data):
    try:
        return paq.compress(data)
    except Exception as e:
        print(f"Error during PAQ compression: {e}")
    return data

def decompress_data(data):
    try:
        return paq.decompress(data)
    except Exception as e:
        print(f"Error during PAQ decompression: {e}")
    return data

# ------------------- Compression with Iterations -------------------

def compress_with_iterations(data, attempts, iterations):
    best_compressed = paq.compress(data)
    best_size = len(best_compressed)

    for i in tqdm(range(attempts), desc="Compression Attempts"):
        try:
            current_data = data
            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                blocks = find_zero_and_one_blocks(current_data)  # Find all-zero and all-one blocks
                transformed_data = transform_zero_and_one_blocks(blocks)  # Transform those blocks
                compressed = paq.compress(transformed_data)  # Compress the transformed data

                # Compare with the best compressed result
                if len(compressed) < best_size:
                    best_compressed = compressed
                    best_size = len(compressed)

                current_data = paq.decompress(best_compressed)  # Continue with the best compressed data

        except Exception as e:
            print(f"Error during iteration {i + 1}: {e}")

    return best_compressed

# File I/O handler

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
        return None
    except Exception as e:
        print(f"Error during file I/O: {e}")
        return None

# Get positive integer input

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

# Main

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
        data = handle_file_io(decompress_data, in_file)
        if data:
            handle_file_io(lambda x: x, out_file, data)
            print(f"Extracted to {out_file}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()