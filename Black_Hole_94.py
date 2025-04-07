import os
import time
import struct
from tqdm import tqdm
import paq  # REPLACE with your actual PAQ library

def shift_bits_left(data, positions):
    result = bytearray()
    for byte in data:
        shifted_byte = (byte << positions) % 256
        result.append(shifted_byte)
    return bytes(result)

def exhaustive_hill_climbing_best_shift(block, max_iterations):  
    best_block = bytes(block)
    best_size = len(paq.compress(best_block))
    best_shift = 0

    for iteration in range(max_iterations):
        for shift in range(256):
            shifted_block = shift_bits_left(best_block, shift)
            compressed_size = len(paq.compress(bytes(shifted_block)))
            if compressed_size < best_size:
                best_size = compressed_size
                best_block = shifted_block
                best_shift = shift

    return best_block, best_shift


def compress_data(data):
    original_size = len(data)
    block_size_bytes = 32
    num_blocks = (original_size + block_size_bytes - 1) // block_size_bytes
    best_shifts = bytearray()

    original_data_bytes = bytes(data)
    compressed_original_data = paq.compress(original_data_bytes)

    padded_data = bytearray(data)
    for i in range(0, len(padded_data), block_size_bytes):
        block = padded_data[i:i + block_size_bytes]
        best_block, best_shift = exhaustive_hill_climbing_best_shift(block, max_iterations=1)
        best_shifts.append(best_shift)
        padded_data[i:i + block_size_bytes] = best_block

    compressed_data = struct.pack(">I", original_size) + best_shifts + compressed_original_data

    return compressed_data


def decompress_data(data):
    original_size = struct.unpack(">I", data[:4])[0]
    num_blocks = (original_size + 31) // 32
    best_shifts = data[4:4 + num_blocks]
    compressed_data = data[4 + num_blocks:]
    decompressed_data = paq.decompress(compressed_data)
    return decompressed_data


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
        data = handle_file_io(lambda x: x, in_file)
        if data:
            start_time = time.time()
            compressed_data = compress_data(data)
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
