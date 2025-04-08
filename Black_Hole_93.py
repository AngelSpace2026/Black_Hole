import os
import random
import time
from tqdm import tqdm
import paq  # Placeholder for actual PAQ module

# Helper function to perform a left rotation (reverse left)
def rotate_left(data, positions):
    """Rotate bits of data left by a specified number of positions."""
    return (data << positions) | (data >> (256 - positions))

# Helper function to perform a right rotation (reverse right)
def rotate_right(data, positions):
    """Rotate bits of data right by a specified number of positions."""
    return (data >> positions) | (data << (256 - positions))

# 256-bit Block Reversal Transformations
def reverse_transform_256bit(data):
    """Apply reverse left and right rotations with 256 possible positions on 256-bit blocks."""
    block_size = 32  # 256 bits = 32 bytes
    transformed_data = bytearray()
    metadata = bytearray()

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        block_int = int.from_bytes(block, 'big')  # Convert to integer for bit manipulation
        
        # Store the transformation metadata (reverse left and right rotations)
        reverse_left_pos = random.randint(0, 255)  # Random position for left rotation
        reverse_right_pos = random.randint(0, 255)  # Random position for right rotation
        
        # Perform the transformations
        transformed_left = rotate_left(block_int, reverse_left_pos)
        transformed_right = rotate_right(block_int, reverse_right_pos)
        
        # Convert back to bytes
        left_bytes = transformed_left.to_bytes(block_size, 'big')
        right_bytes = transformed_right.to_bytes(block_size, 'big')

        # Add the transformed data to the result
        transformed_data.extend(left_bytes)
        transformed_data.extend(right_bytes)

        # Add metadata for the transformations
        metadata.extend(reverse_left_pos.to_bytes(1, 'big'))  # 1 byte for reverse left position
        metadata.extend(reverse_right_pos.to_bytes(1, 'big'))  # 1 byte for reverse right position

    return transformed_data, metadata

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
            best_with_transforms = best_compressed
            best_without_transforms = best_compressed

            for j in tqdm(range(iterations), desc=f"Iteration {i + 1}", leave=False):
                # Apply reverse transformations (left and right rotations)
                current_data, _ = reverse_transform_256bit(current_data)  # Apply reverse transformations

                # Compress the transformed data
                compressed_with_transforms = paq.compress(current_data)
                compressed_without_transforms = paq.compress(current_data)

                # Compare the sizes and select the best result
                if len(compressed_with_transforms) < len(best_with_transforms):
                    best_with_transforms = compressed_with_transforms

                if len(compressed_without_transforms) < len(best_without_transforms):
                    best_without_transforms = compressed_without_transforms

                current_data = paq.decompress(best_with_transforms)  # Continue with the best compressed data

            # Choose the better result (with or without transformations)
            if len(best_with_transforms) < len(best_without_transforms):
                best_compressed = best_with_transforms
            else:
                best_compressed = best_without_transforms

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