import os
import random
import struct
import paq

# Reverse chunks at specified positions
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, number_of_positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

    max_position = len(chunked_data)
    positions = [i * (2**31) // max_position for i in range(number_of_positions)]

    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, original_size, times, zero_count):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # FIX: Use 4 bytes (uint32) instead of 1 byte
    metadata = struct.pack(">IIIII", original_size, zero_count, chunk_size, len(positions), times)

    # Position list (each position is 4 bytes)
    metadata += struct.pack(f">{len(positions)}I", *positions)

    compressed_data = paq.compress(metadata + reversed_data)
    compressed_size = len(compressed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

    return compressed_size

# Infinite loop to find the best chunk strategy
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_compression_ratio = float('inf')
    best_compressed_filename = input_filename + ".compressed.bin"
    reversed_filename = f"{input_filename}.reversed.bin"
    previous_size = 10**12

    while True:  # Infinite loop
        times = random.randint(1, 2**24)  # Random times each iteration
        chunk_size = 1  # Set chunk size to always be 1
        max_positions = file_size // chunk_size

        if max_positions > 0:
            positions_count = random.randint(1, min(max_positions, 64))
            positions = [i * (2**31) // file_size for i in range(positions_count)]

            reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions_count)

            # Count trailing zeros in the file
            with open(reversed_filename, 'rb') as f:
                data = f.read()
            zero_count = len(data) - len(data.rstrip(b'\x00'))  # Count trailing zero bytes

            compressed_size = compress_with_paq(reversed_filename, best_compressed_filename, chunk_size, positions, file_size, times, zero_count)

            # Save only if improved
            if compressed_size < previous_size:
                previous_size = compressed_size
                best_compression_ratio = compressed_size / file_size
                print(f"Improved! Times: {times}, Chunk Size: {chunk_size}, Compressed Size: {compressed_size}, Ratio: {best_compression_ratio:.4f}")

# Decompression function
def decompress_and_restore_paq(compressed_filename):
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = paq.decompress(compressed_data)

    if len(decompressed_data) < 20:
        raise ValueError("Decompressed data is too small to contain metadata.")

    # FIX: Read 4-byte values instead of 1 byte
    original_size, zero_count, chunk_size, num_positions, times = struct.unpack(">IIIII", decompressed_data[:20])
    
    metadata_size = 20 + (num_positions * 4)
    if len(decompressed_data) < metadata_size:
        raise ValueError("Decompressed data does not match expected metadata size.")

    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[20:20 + num_positions * 4]))

    chunked_data = decompressed_data[metadata_size:]

    total_chunks = len(chunked_data) // chunk_size
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    restored_data = b"".join(chunked_data)[:original_size]

    # Restore trailing zeros
    restored_data += b'\x00' * zero_count

    restored_filename = compressed_filename.replace('.compressed.bin', '')

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompressed: {restored_filename}, Size: {len(restored_data)}, Zero Count: {zero_count}, Times: {times}")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")

    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for extract): "))
            if mode not in [1, 2]:
                print("Error: Please enter 1 for compress or 2 for extract.")
            else:
                break
        except ValueError:
            print("Error: Invalid input. Please enter a number (1 or 2).")

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