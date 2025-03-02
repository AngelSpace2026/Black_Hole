import os
import random
import struct
import paq
import math

# Generate root whole numbers (1-64)
def generate_root_numbers():
    return [i for i in range(1, 65) if math.sqrt(i).is_integer()]

# Reverse chunks at random positions with spacing
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, number_of_positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

    max_position = len(chunked_data)
    positions = sorted(random.sample(range(max_position), min(number_of_positions, max_position)))

    for pos in positions:
        chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

    return positions

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, original_size, first_attempt):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    metadata = struct.pack(">Q", original_size)  
    metadata += struct.pack(">I", chunk_size)
    metadata += struct.pack(">I", len(positions))
    metadata += struct.pack(f">{len(positions)}I", *positions)

    compressed_data = paq.compress(metadata + reversed_data)
    compressed_size = len(compressed_data)

    if first_attempt or compressed_size < previous_size:
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        previous_size = compressed_size
        print(f"New best compression: {compressed_size} bytes (chunk size {chunk_size}, {len(positions)} positions)")

    return previous_size, False

# Decompress and restore data
def decompress_and_restore_paq(compressed_filename):
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = paq.decompress(compressed_data)

    original_size = struct.unpack(">Q", decompressed_data[:8])[0]
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]
    num_positions = struct.unpack(">I", decompressed_data[12:16])[0]
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))

    chunked_data = decompressed_data[16 + num_positions * 4:]
    total_chunks = len(chunked_data) // chunk_size
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    for pos in positions:
        chunked_data[pos] = chunked_data[pos][::-1]

    restored_data = b"".join(chunked_data)[:original_size]
    restored_filename = compressed_filename.replace('.compressed.bin', '')

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompressed successfully. Restored file: {restored_filename}")

# Infinite search for best compression
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    previous_size = float('inf')
    first_attempt = True
    root_numbers = generate_root_numbers()

    while True:
        chunk_size = random.choice(root_numbers)
        max_positions = file_size // chunk_size
        number_of_positions = random.randint(1, min(max_positions, 64))

        reversed_filename = f"{input_filename}.reversed.bin"
        positions = reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, number_of_positions)

        compressed_filename = f"{input_filename}.compressed.bin"
        previous_size, first_attempt = compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, file_size, first_attempt)

# Main function
def main():
    print("Created by Jurijus Pacalovas.")

    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for extract): "))
            if mode in [1, 2]:
                break
            print("Error: Please enter 1 for compress or 2 for extract.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        if not os.path.exists(input_filename):
            print(f"Error: File {input_filename} not found!")
            return
        find_best_chunk_strategy(input_filename)

    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"

        if not os.path.exists(compressed_filename):
            print(f"Error: Compressed file {compressed_filename} not found!")
            return

        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()