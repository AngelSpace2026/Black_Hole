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

def shift_block_left(data, shift_value):
    shift_value = shift_value % len(data)
    return data[shift_value:] + data[:shift_value]

def shift_block_right(data, shift_value):
    shift_value = shift_value % len(data)
    return data[-shift_value:] + data[:-shift_value]

def random_minus_64bit(data):
    block_size = 8  # 64-bit = 8 bytes
    transformed_data = bytearray()
    metadata = bytearray()

    random_value = random.randint(1, 2**64 - 1)

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        transformed_block = bytes([(byte - (random_value % 256)) % 256 for byte in block])
        transformed_data.extend(transformed_block)
        metadata.extend(random_value.to_bytes(8, 'big'))

    return transformed_data, metadata

# RLE with 2-byte count (up to 65536)

def rle_encode_2byte(data):
    if not data:
        return data
    encoded_data = bytearray()
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1] and count < 65535:
            count += 1
        else:
            encoded_data.extend([data[i - 1]])
            encoded_data.extend(count.to_bytes(2, 'big'))
            count = 1
    encoded_data.extend([data[-1]])
    encoded_data.extend(count.to_bytes(2, 'big'))
    return bytes(encoded_data)

# Apply random transformations + always RLE

def apply_random_transformations(data, num_transforms=10):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True),
        (random_minus_64bit, False)
    ]
    marker = 0
    transformed_data = data

    for i in range(num_transforms):
        transform, needs_paq = random.choice(transforms)
        try:
            if needs_paq:
                paq = random.randint(1, 8) if transform != reverse_chunk else random.randint(1, len(data))
                transformed_data = transform(transformed_data, paq)
            else:
                if transform == random_minus_64bit:
                    transformed_data, _ = transform(transformed_data)
                else:
                    transformed_data = transform(transformed_data)
            marker |= (1 << (i % 8))
        except Exception as e:
            print(f"Error applying transformation: {e}")

    # Always apply RLE
    transformed_data = rle_encode_2byte(transformed_data)
    return transformed_data, marker

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

# Compression with Iterations

def compress_with_iterations(data, attempts, iterations):
    best_compressed = paq.compress(data)
    best_size = len(best_compressed)

    for i in tqdm(range(attempts), desc="Compression Attempts"):
        try:
            current_data = data
            best_this_attempt = best_compressed

            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                transformed, marker = apply_random_transformations(current_data)
                compressed = paq.compress(transformed)

                if len(compressed) < len(best_this_attempt):
                    best_this_attempt = compressed

                current_data = paq.decompress(best_this_attempt)

            if len(best_this_attempt) < best_size:
                best_compressed = best_this_attempt
                best_size = len(best_this_attempt)

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
