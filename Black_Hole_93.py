import os
import random
import time
from tqdm import tqdm
import paq  # Placeholder for actual PAQ module

# Reversible Transformation Functions

# Random Subtraction Function for 256-bit blocks (subtract random value between 1 and 2**256 - 1)
def random_subtract_256bit(data):
    """Subtract a random value from each 256-bit block and add metadata for the subtraction."""
    block_size = 32  # 256 bits = 32 bytes
    transformed_data = bytearray()
    metadata = bytearray()

    # Generate a random subtraction value for each 256-bit block
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        random_value = random.randint(1, 2**256 - 1)

        # Subtract the random value from each byte of the 256-bit block
        transformed_block = bytes([(byte - (random_value % 256)) % 256 for byte in block])
        transformed_data.extend(transformed_block)

        # Add metadata: 32 bytes indicating the random value used
        metadata.extend(random_value.to_bytes(32, 'big'))

    return transformed_data, metadata

# Reversing function for chunk transformations
def reverse_chunk(data, chunk_size):
    return data[::-1]

# Adding random noise
def add_random_noise(data, noise_level=10):
    return bytes([byte ^ random.randint(0, noise_level) for byte in data])

# Subtract 1 from each byte
def subtract_1_from_each_byte(data):
    return bytes([(byte - 1) % 256 for byte in data])

# Move bits left (1-8 bits)
def move_bits_left(data, n):
    n = n % 8
    return bytes([(byte << n & 0xFF) | (byte >> (8 - n)) & 0xFF for byte in data])

# Move bits right (1-8 bits)
def move_bits_right(data, n):
    n = n % 8
    return bytes([(byte >> n & 0xFF) | (byte << (8 - n)) & 0xFF for byte in data])

# Run-Length Encoding (RLE)
def rle_encode(data):
    if not data:
        return data
    encoded_data = bytearray()
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1] and count < 255:
            count += 1
        else:
            encoded_data.extend([data[i - 1], count])
            count = 1
    encoded_data.extend([data[-1], count])
    return bytes(encoded_data)

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
            best_with_rle = best_compressed
            best_without_rle = best_compressed

            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                # Apply transformations and compression
                current_data, _ = random_subtract_256bit(current_data)  # Apply random subtraction transformation
                current_data = reverse_chunk(current_data, 64)  # Apply chunk reversal
                current_data = add_random_noise(current_data)  # Add random noise
                current_data = subtract_1_from_each_byte(current_data)  # Subtract 1 from each byte
                current_data = move_bits_left(current_data, random.randint(1, 8))  # Move bits left
                current_data = move_bits_right(current_data, random.randint(1, 8))  # Move bits right

                # Apply RLE compression to the transformed data
                current_data = rle_encode(current_data)

                # Compress the transformed data with RLE applied
                compressed_with_rle = paq.compress(current_data)
                compressed_without_rle = paq.compress(current_data)

                # Compare the sizes with and without RLE and select the best
                if len(compressed_with_rle) < len(best_with_rle):
                    best_with_rle = compressed_with_rle

                if len(compressed_without_rle) < len(best_without_rle):
                    best_without_rle = compressed_without_rle

                current_data = paq.decompress(best_with_rle)  # Continue with the best compressed data

            # Choose the better result (with or without RLE)
            if len(best_with_rle) < len(best_without_rle):
                best_compressed = best_with_rle
            else:
                best_compressed = best_without_rle

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