import os
import random
import time
from tqdm import tqdm
import paq  # Placeholder for actual PAQ module

# ------------------- Reversible Transformation Functions -------------------

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

# ------------------- Run-Length Encoding (RLE) -------------------

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

# ------------------- Random Transformations -------------------

def apply_random_transformations(data, num_transforms=10):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True),
        (rle_encode, False)
    ]
    marker = 0
    transformed_data = data
    rle_applied = False

    for i in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        try:
            if needs_param:
                param = random.randint(1, 8) if transform != reverse_chunk else random.randint(1, len(data))
                transformed_data = transform(transformed_data, param)
            else:
                transformed_data = transform(transformed_data)
                if transform == rle_encode:
                    rle_applied = True
            marker |= (1 << (i % 4))
        except Exception as e:
            print(f"Error applying transformation: {e}")
            return transformed_data, marker, rle_applied

    return transformed_data, marker, rle_applied

# ------------------- Structured Extra Move -------------------

def extra_move(data):
    bit_block_size = 256  # 256 bits = 32 bytes
    byte_block_size = bit_block_size // 8
    result = bytearray()

    for i in range(0, len(data), byte_block_size):
        block = data[i:i + byte_block_size]
        if len(block) < byte_block_size:
            result.extend(block)
            continue

        best_block = block
        best_size = len(paq.compress(block))
        modified_flag = 0

        block_len = len(block)
        levels = block_len // byte_block_size
        variation_count = 256 ** levels

        # Safety cap to limit time complexity
        if variation_count > 10_000_000:
            variation_count = 1000

        for b in range(variation_count):
            try:
                mod = [(byte + (b % 256)) % 256 for byte in block]
                mod = move_bits_left(bytes(mod), b % 8)
                try_compressed = paq.compress(mod)
                if len(try_compressed) < best_size:
                    best_block = mod
                    best_size = len(try_compressed)
                    modified_flag = 1
            except Exception as e:
                print(f"Variation {b} error: {e}")
                continue

        result.extend(best_block)
        result.append(modified_flag)  # Store 1-bit flag as byte

    return bytes(result)

# ------------------- PAQ Compression Wrapper -------------------

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
                transformed, marker, rle_applied = apply_random_transformations(current_data)
                improved = extra_move(transformed)
                compressed_data = paq.compress(improved)

                if len(compressed_data) < best_size:
                    best_compressed = compressed_data
                    best_size = len(compressed_data)

                current_data = paq.decompress(compressed_data)

            if rle_applied:
                best_compressed += b'\x01'  # Simple 1-bit RLE flag

        except Exception as e:
            print(f"Error during iteration {i + 1}: {e}")

    return best_compressed

# ------------------- File I/O Handler -------------------

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

# ------------------- Get Integer Input -------------------

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

# ------------------- Main Function -------------------

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