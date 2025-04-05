import os
import random
import time
import paq  # Replace with real PAQ module if needed
from tqdm import tqdm  # For progress bar


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
        count = int.from_bytes(data[i + 1:i + 3], 'big')
        decoded.extend([byte] * count)
        i += 3
    return bytes(decoded)


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


def apply_random_transformations(data, num_transforms=5):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True)
    ]
    for _ in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        if needs_param:
            param = random.randint(1, 8) if transform != reverse_chunk else random.randint(1, len(data))
            try:
                data = transform(data, param)
            except Exception as e:
                print(f"Error applying transformation: {e}")
        else:
            try:
                data = transform(data)
            except Exception as e:
                print(f"Error applying transformation: {e}")
    return data


def compress_data(data):
    try:
        return paq.compress(data)
    except Exception as e:
        print(f"Error during compression: {e}")
        return data


def decompress_data(data):
    try:
        return paq.decompress(data)
    except Exception as e:
        print(f"Error during decompression: {e}")
        return data


def extra_move(data):
    chunk_size = 4096
    best_data = bytearray()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        best_chunk = chunk
        best_score = len(compress_data(chunk))

        for _ in range(16):  # 16 variations
            transformed = bytearray(chunk)
            for j in range(len(transformed)):
                transformed[j] = (transformed[j] + random.randint(0, 255)) % 256
                if random.choice([True, False]):
                    shift = random.randint(1, 7)
                    transformed[j] = ((transformed[j] << shift) | (transformed[j] >> (8 - shift))) & 0xFF
                else:
                    shift = random.randint(1, 7)
                    transformed[j] = ((transformed[j] >> shift) | (transformed[j] << (8 - shift))) & 0xFF

            comp_size = len(compress_data(transformed))
            if comp_size < best_score:
                best_score = comp_size
                best_chunk = transformed

        best_data += best_chunk
    return bytes(best_data)


def compress_with_iterations(data, attempts, iterations):
    best_compressed = compress_data(data)
    best_size = len(best_compressed)

    for i in tqdm(range(attempts), desc="Compression Attempts"):
        try:
            current_data = data
            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                current_data = apply_random_transformations(current_data)
                current_data = extra_move(current_data)
                rle_encoded = rle_encode(current_data)
                compressed_data = compress_data(rle_encoded)
                if len(compressed_data) < best_size:
                    best_compressed = compressed_data
                    best_size = len(compressed_data)
                current_data = rle_decode(decompress_data(compressed_data))
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
        return None
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