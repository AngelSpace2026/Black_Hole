import os
import random
import time
from tqdm import tqdm
import paq  # Placeholder for actual PAQ module

# Structured extra move function with added positions and variations
def extra_move(data):
    bit_block_size = 256  # 256 bits = 32 bytes
    byte_block_size = bit_block_size // 8
    result = bytearray()
    positions = []

    # Iterate through the data in blocks
    for i in range(0, len(data), byte_block_size):
        block = data[i:i + byte_block_size]
        if len(block) < byte_block_size:
            result.extend(block)
            continue

        best_block = block
        best_size = len(paq.compress(block))
        modified_flag = 0

        # Random positions for variation (256 variations per block)
        for _ in range(256):  # Randomize 256 possible variations per block
            pos = random.randint(1, 256)  # Random position for each variation
            mod = [(byte + (pos % 256)) % 256 for byte in block]
            mod = move_bits_left(bytes(mod), pos % 8)

            # Save the position (1 byte for position)
            positions.append(pos)

            try_compressed = paq.compress(mod)
            if len(try_compressed) < best_size:
                best_block = mod
                best_size = len(try_compressed)
                modified_flag = 1

        result.extend(best_block)

        # Add 1 byte variation flag after every block (for 1-bit metadata)
        result.append(modified_flag)

    # After all transformations, add the positions as 1 byte metadata (in the required format)
    result.extend(positions)

    # Now compress with PAQ to get the final compressed result
    final_compressed = paq.compress(bytes(result))

    return final_compressed

# Function to shift bits left
def move_bits_left(data, positions):
    return bytes((byte << positions) % 256 for byte in data)

# Compression/Decompression functions
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
            best_with_rle = best_compressed
            best_without_rle = best_compressed

            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                transformed = current_data

                # Apply random transformations and compare the result
                improved_with_rle = extra_move(transformed)
                compressed_with_rle = paq.compress(improved_with_rle)

                improved_without_rle = extra_move(transformed)
                compressed_without_rle = paq.compress(improved_without_rle)

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

# Main function
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