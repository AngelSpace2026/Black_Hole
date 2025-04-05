import os
import paq
import random
import time
from tqdm import tqdm

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

# Map transformations to 3-bit IDs
TRANSFORMATIONS = {
    0: (reverse_chunk, True),
    1: (add_random_noise, True),
    2: (subtract_1_from_each_byte, False),
    3: (move_bits_left, True),
    4: (move_bits_right, True)
}

def apply_random_transformations(data, num_transforms=5):
    markers = []
    for _ in range(num_transforms):
        transform_id = random.choice(list(TRANSFORMATIONS.keys()))
        transform, needs_param = TRANSFORMATIONS[transform_id]
        try:
            if needs_param:
                param = random.randint(1, 8) if transform != reverse_chunk else random.randint(1, len(data))
                data = transform(data, param)
            else:
                data = transform(data)
            markers.append(transform_id)
        except Exception as e:
            print(f"Error applying transformation {transform_id}: {e}")
            continue
    return data, markers

def pack_3bit_markers(markers):
    bits = ''.join(format(m, '03b') for m in markers)
    # Pad to full bytes
    bits += '0' * ((8 - len(bits) % 8) % 8)
    return int(bits, 2).to_bytes(len(bits) // 8, 'big')

def unpack_3bit_markers(data, num_markers):
    bits = bin(int.from_bytes(data, 'big'))[2:].zfill(len(data) * 8)
    return [int(bits[i:i+3], 2) for i in range(0, num_markers * 3, 3)]

def extra_move(data):
    block_size = 256
    best_data = data
    best_size = len(paq.compress(data))
    result = bytearray()
    flag_bits = []

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        best_block = block
        best_block_size = best_size
        best_flag = 0

        for b in range(256):
            modified = bytes([(byte + b) % 256 for byte in block])
            modified = move_bits_left(modified, b % 8)
            try_compressed = paq.compress(modified)
            if len(try_compressed) < best_block_size:
                best_block = modified
                best_block_size = len(try_compressed)
                best_flag = b  # Store which variation was best

        result.extend(best_block)
        flag_bits.append(best_flag % 2)  # Store 1-bit flag

    # Pack flags into bytes
    flags_binary = ''.join(str(bit) for bit in flag_bits)
    flags_binary += '0' * ((8 - len(flags_binary) % 8) % 8)
    flag_bytes = int(flags_binary, 2).to_bytes(len(flags_binary) // 8, 'big')
    return bytes(result) + flag_bytes

def compress_with_iterations(data, attempts, iterations):
    best_compressed = paq.compress(data)
    best_size = len(best_compressed)

    for i in tqdm(range(attempts), desc="Compression Attempts"):
        try:
            current_data = data
            all_markers = []
            for j in tqdm(range(iterations), desc=f"Iteration {i+1}", leave=False):
                rle_encoded = rle_encode(current_data)
                transformed, markers = apply_random_transformations(rle_encoded)
                all_markers.extend(markers)
                improved = extra_move(transformed)
                compressed_data = paq.compress(improved)

                if len(compressed_data) < best_size:
                    best_compressed = compressed_data
                    best_size = len(compressed_data)

                current_data = rle_decode(paq.decompress(compressed_data))

            marker_data = pack_3bit_markers(all_markers)
            best_compressed += marker_data  # append markers at the end

        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")

    return best_compressed

def decompress_data(data):
    try:
        return paq.decompress(data)
    except Exception as e:
        print(f"Error during PAQ decompression: {e}")
        return data

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