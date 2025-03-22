import os
import random
import struct
import paq

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def flip_2bit_pairs(data):
    modified_data = bytearray(data)
    for i in range(0, len(modified_data) * 8, 2):
        byte_index = i // 8
        bit_position = i % 8
        if byte_index < len(modified_data):
            byte = modified_data[byte_index]
            bit_pair = (byte >> (6 - bit_position)) & 0b11
            flipped_pair = bit_pair ^ 0b11
            modified_data[byte_index] = (byte & ~(0b11 << (6 - bit_position))) | (flipped_pair << (6 - bit_position))
    return bytes(modified_data)

def compress_with_paq(data, chunk_size, positions, original_size):
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions)
    return paq.compress(metadata + data)

def decompress_with_paq(compressed_data):
    decompressed_data = paq.decompress(compressed_data)
    original_size = struct.unpack(">I", decompressed_data[:4])[0]
    chunk_size = struct.unpack(">I", decompressed_data[4:8])[0]
    num_positions = struct.unpack(">B", decompressed_data[8:9])[0]
    positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + (num_positions * 4)])

    modified_data = decompressed_data[9 + (num_positions * 4):]
    modified_data = flip_2bit_pairs(modified_data)
    original_data = reverse_chunks_at_positions(modified_data, chunk_size, positions)

    return original_data[:original_size]

def find_best_iteration(input_filename, max_iterations):
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
        file_size = len(file_data)

    best_compression_ratio = float('inf')
    best_compressed_data = None

    for _ in range(max_iterations):
        chunk_size = random.randint(1, min(256, file_size))
        num_positions = random.randint(0, min(file_size // chunk_size, 64))
        positions = sorted(random.sample(range(file_size // chunk_size), num_positions)) if num_positions > 0 else []

        modified_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
        modified_data = flip_2bit_pairs(modified_data)

        compressed_data = compress_with_paq(modified_data, chunk_size, positions, file_size)
        compression_ratio = len(compressed_data) / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data

    return best_compressed_data, best_compression_ratio

def run_compression(input_filename):
    best_compressed_data = None
    best_ratio = float('inf')

    for i in range(1, 9):  
        print(f"Running compression attempt {i} with 300 iterations...")
        compressed_data, compression_ratio = find_best_iteration(input_filename, 300)

        if compressed_data and compression_ratio < best_ratio:
            best_ratio = compression_ratio
            best_compressed_data = compressed_data

    final_compressed_filename = f"{input_filename}.compressed.bin"
    with open(final_compressed_filename, 'wb') as outfile:
        outfile.write(best_compressed_data)

    print(f"Best compression saved as: {final_compressed_filename}")

def run_extraction(input_filename):
    with open(input_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = decompress_with_paq(compressed_data)
    original_filename = input_filename.replace(".compressed.bin", "")

    with open(original_filename, 'wb') as outfile:
        outfile.write(decompressed_data)

    print(f"File successfully extracted: {original_filename}")

def main():
    print("Created by Jurijus Pacalovas.")
    choice = input("Choose an option:\n1 - Compress\n2 - Extract\n> ")

    if choice == "1":
        input_filename = input("Enter input file name to compress: ")
        run_compression(input_filename)

    elif choice == "2":
        input_filename = input("Enter compressed file name to extract: ")
        run_extraction(input_filename)

    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()