import os
import random
import time
import paq  # Assumed to be a working PAQ wrapper module
from tqdm import tqdm

class zlib_wrapper:
    @staticmethod
    def compress(data):
        return paq.compress(data)

    @staticmethod
    def decompress(data):
        return paq.decompress(data)

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

def random_minus_blocks(data, block_size_bits=64):
    block_sizes = [2**i for i in range(1, 33)]
    if block_size_bits not in block_sizes:
        raise ValueError("Invalid block size.")
    block_size = block_size_bits // 8
    if block_size == 0:
        raise ValueError("Block size cannot be 0 bytes")

    transformed_data = bytearray()
    metadata = bytearray()
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        if len(block) < block_size:
            block += bytes(block_size - len(block))
        random_value = random.randint(1, 2 ** block_size_bits - 1)
        rand_bytes = random_value.to_bytes(block_size, byteorder='big')
        transformed_block = bytes([(b - rand_bytes[j % block_size]) % 256 for j, b in enumerate(block)])
        transformed_data.extend(transformed_block)
        metadata.extend(rand_bytes)
    return bytes(transformed_data), bytes(metadata)

def rle_encode_1byte(data):
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

def add_block_size_64(data):
    transformed_data = bytearray()
    block_size = 64
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        if len(block) < block_size:
            block += bytes(block_size - len(block))
        transformed_data.extend((block_size).to_bytes(2, 'big'))
        transformed_data.extend(block)
    return bytes(transformed_data)

def apply_random_transformations(data, num_transforms=10):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True),
        (random_minus_blocks, False)
    ]
    marker = 0
    transformed_data = data
    for i in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        try:
            if transform == random_minus_blocks:
                bits = random.choice([2**i for i in range(1, 33)])
                transformed_data, _ = transform(transformed_data, block_size_bits=bits)
            elif needs_param:
                param = random.randint(1, 7)
                transformed_data = transform(transformed_data, param)
            else:
                transformed_data = transform(transformed_data)
            marker |= (1 << (i % 8))
        except Exception as e:
            print(f"Error applying transformation {transform.__name__}: {e}")

    if len(transformed_data) < 1024:
        transformed_data = rle_encode_1byte(transformed_data)

    transformed_data = add_block_size_64(transformed_data)
    return transformed_data, marker

def extra_move(data):
    bit_block_size = 256
    byte_block_size = bit_block_size // 8
    result = bytearray()
    metadata = bytearray()

    for i in range(0, len(data), byte_block_size):
        block = data[i:i + byte_block_size]
        if len(block) < byte_block_size:
            result.extend(block)
            continue

        best_block = block
        best_compressed = paq.compress(block)
        best_size = len(best_compressed)
        best_shift = 0

        for shift in range(256):
            shifted = move_bits_left(block, shift % 8)
            compressed = paq.compress(shifted)
            if len(compressed) < best_size:
                best_block = shifted
                best_compressed = compressed
                best_size = len(compressed)
                best_shift = shift

        zeros = sum(bin(byte).count('0') - 1 for byte in best_block)
        ones = sum(bin(byte).count('1') for byte in best_block)
        result.extend(best_block)
        metadata.extend([zeros & 0xFF, ones & 0xFF, best_shift & 0xFF])

    return bytes(result), bytes(metadata)

def compress_data(data):
    try:
        return zlib_wrapper.compress(data)
    except Exception as e:
        print(f"Error during zlib compression: {e}")
    return data

def decompress_data(data):
    try:
        return zlib_wrapper.decompress(data)
    except Exception as e:
        print(f"Error during zlib decompression: {e}")
    return data

def compress_with_iterations(data, attempts, iterations):
    best_compressed = zlib_wrapper.compress(data)
    best_size = len(best_compressed)

    for i in tqdm(range(attempts), desc="Compression Attempts"):
        try:
            current_data = data
            best_this_attempt = best_compressed
            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                transformed, marker = apply_random_transformations(current_data)
                transformed, _ = extra_move(transformed)
                compressed = zlib_wrapper.compress(transformed)
                if len(compressed) < len(best_this_attempt):
                    best_this_attempt = compressed
                current_data = zlib_wrapper.decompress(best_this_attempt)
            if len(best_this_attempt) < best_size:
                best_compressed = best_this_attempt
                best_size = len(best_this_attempt)
        except Exception as e:
            print(f"Error during iteration {i + 1}: {e}")
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
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"Error during file I/O: {e}")
    return None

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