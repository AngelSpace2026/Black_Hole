import os
import paq
import random
import time
from tqdm import tqdm  # For progress bar

# RLE Encoding and Decoding
def rle_encode(data):
    if not data:
        return b""
    encoded = []
    count = 1
    prev_byte = data[0]
    for i in range(1, len(data)):
        if data[i] == prev_byte:
            count += 1
        else:
            encoded.append((prev_byte, count))
            prev_byte = data[i]
            count = 1
    encoded.append((prev_byte, count))
    result = b""
    for byte, count in encoded:
        result += byte.to_bytes(1, 'big') + count.to_bytes(2, 'big')
    return result

def rle_decode(data):
    decoded = []
    i = 0
    while i < len(data):
        byte = data[i]
        count = int.from_bytes(data[i+1:i+3], 'big')
        decoded.extend([byte] * count)
        i += 3
    return bytes(decoded)

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

# Apply random transformations to the data
def apply_random_transformations(data, num_transforms=10):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True)
    ]
    marker = 0  # 4-bit marker for tracking transformations
    transformed_data = data
    
    for i in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        if needs_param:
            param = random.randint(1, 8) if transform != reverse_chunk else random.randint(1, len(data))
            try:
                transformed_data = transform(transformed_data, param)
                marker |= (1 << (i % 4))  # Set 4-bit marker based on applied transformation
            except Exception as e:
                print(f"Error applying transformation: {e}")
                return transformed_data, marker
        else:
            try:
                transformed_data = transform(transformed_data)
                marker |= (1 << (i % 4))  # Set 4-bit marker based on applied transformation
            except Exception as e:
                print(f"Error applying transformation: {e}")
                return transformed_data, marker

    return transformed_data, marker  # Return the transformed data and the marker

# Extra move function with 256-bit variations
def extra_move(data):
    """Apply 256 variations every 256 bits, add a byte and move bits to find the best variant."""
    block_size = 256
    best_data = data
    best_size = len(paq.compress(data))
    result = bytearray()

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        best_block = block
        best_block_size = best_size

        for b in range(256):  # 256 variations
            modified = bytes([(byte + b) % 256 for byte in block])
            modified = move_bits_left(modified, b % 8)
            try_compressed = paq.compress(modified)
            if len(try_compressed) < best_block_size:
                best_block = modified
                best_block_size = len(try_compressed)

        result.extend(best_block)

    # Add 1-bit flag for modified block (0 if unmodified, 1 if modified)
    result.append(1 if best_data != result else 0)
    return bytes(result)

# Compression and Decompression using PAQ
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

# Compress with iterations and random transformations
def compress_with_iterations(data, attempts, iterations):
    best_compressed = paq.compress(data)
    best_size = len(best_compressed)

    for i in tqdm(range(attempts), desc="Compression Attempts"):
        try:
            current_data = data
            for j in tqdm(range(iterations), desc=f"Iteration {i+1}", leave=False):
                rle_encoded = rle_encode(current_data)
                transformed, marker = apply_random_transformations(rle_encoded)
                improved = extra_move(transformed)
                compressed_data = paq.compress(improved)

                if len(compressed_data) < best_size:
                    best_compressed = compressed_data
                    best_size = len(compressed_data)

                # Prepare next round
                current_data = rle_decode(paq.decompress(compressed_data))
        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")

    return best_compressed

# File input/output handler
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

# Main Function to Run the Program
def main():
    choice = input("Choose (1: Compress, 2: Extract): ")
    in_file, out_file = input("Input file: "), input("Output file: ")

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