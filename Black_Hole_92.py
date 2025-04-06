import os
import random
import time
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

# Decompression Function (PAQ placeholder)
def decompress_data(data):
    try:
        return paq.decompress(data)  # Placeholder for PAQ decompression
    except Exception as e:
        print(f"Error during PAQ decompression: {e}")
        return data  # Return original data in case of error

# Apply random transformations (optimized for performance)
def apply_random_transformations(data, num_transforms=3):  # Limit transformations
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True)
    ]
    transformed_data = data
    for i in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        try:
            if needs_param:
                param = random.randint(1, 8) if transform != reverse_chunk else random.randint(1, len(data))
                transformed_data = transform(transformed_data, param)
            else:
                transformed_data = transform(transformed_data)
        except Exception as e:
            print(f"Error applying transformation: {e}")
    return transformed_data

# Efficient Compression with PAQ
def compress_with_paq(data):
    try:
        return paq.compress(data)  # Placeholder for PAQ compression
    except Exception as e:
        print(f"Error during PAQ compression: {e}")
        return data  # Return original data in case of error

# Compression with Iterations (optimized)
def compress_with_iterations(data, attempts, iterations):
    best_compressed = compress_with_paq(data)
    best_size = len(best_compressed)

    for i in range(attempts):
        try:
            current_data = data
            for j in range(iterations):
                transformed = apply_random_transformations(current_data)
                compressed = compress_with_paq(transformed)

                if len(compressed) < best_size:
                    best_compressed = compressed
                    best_size = len(compressed)
                current_data = paq.decompress(best_compressed)  # Decompress to continue with best result
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