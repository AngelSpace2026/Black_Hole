import os
import random
import struct
import paq

# Constants
METADATA_HEADER_SIZE = 13  # 9 bytes + 4 bytes (calculus value)
MAX_POSITIONS = 64
ATTEMPTS = 1
ITERATIONS_PER_ATTEMPT = 10000

def reverse_chunks(data, chunk_size, positions):
    """Reverses chunks at specified positions."""
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def apply_calculus_transformation(data, transform_value):
    """Applies a reversible transformation."""
    transformed_data = bytearray()
    for byte in data:
        transformed_data.append((byte ^ transform_value) % 256)  # XOR transformation
    return bytes(transformed_data)

def compress_data(data):
    """Finds the best compression over multiple iterations."""
    original_size = len(data)
    if original_size < 2**7:
        raise ValueError("Error: File is too small for compression.")

    best_compressed = None
    best_ratio = float('inf')

    for attempt in range(ATTEMPTS):
        print(f"Compression attempt {attempt + 1}/{ATTEMPTS}")

        for iteration in range(ITERATIONS_PER_ATTEMPT):
            chunk_size = random.randint(2**7, min(2**17 - 1, original_size))
            num_positions = random.randint(1, min(len(data) // chunk_size, MAX_POSITIONS))
            positions = sorted(random.sample(range(len(data) // chunk_size), num_positions))
            transform_value = random.randint(1, 2**15 - 1)

            reversed_data = reverse_chunks(data, chunk_size, positions)
            transformed_data = apply_calculus_transformation(reversed_data, transform_value)

            metadata = struct.pack(">IIB", original_size, chunk_size, num_positions) + \
                       struct.pack(f">{num_positions}I", *positions) + \
                       struct.pack(">I", transform_value)

            compressed = paq.compress(metadata + transformed_data)
            compression_ratio = len(compressed) / original_size

            if compression_ratio < best_ratio:
                best_ratio = compression_ratio
                best_compressed = compressed

            #print(f"Iteration {iteration + 1}/{ITERATIONS_PER_ATTEMPT} - Ratio: {compression_ratio:.4f}")

    return best_compressed

def decompress_data(compressed_data):
    """Decompresses and restores the original data."""
    try:
        decompressed_data = paq.decompress(compressed_data)

        original_size, chunk_size, num_positions = struct.unpack(">IIB", decompressed_data[:9])
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        transform_value = struct.unpack(">I", decompressed_data[9 + num_positions * 4:13 + num_positions * 4])[0]

        reversed_data = apply_calculus_transformation(decompressed_data[13 + num_positions * 4:], transform_value)
        restored_data = reverse_chunks(reversed_data, chunk_size, positions)

        return restored_data[:original_size]
    except (struct.error, Exception) as e:
        raise Exception(f"Error during decompression: {e}")

def main():
    print("Created by Jurijus Pacalovas.")

    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for decompress): "))
            if mode not in [1, 2]:
                print("Error: Enter 1 for compress or 2 for decompress.")
            else:
                break
        except ValueError:
            print("Error: Enter a number (1 or 2).")

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        output_filename = input("Enter output file name (e.g., output.compressed.bin): ")

        try:
            with open(input_filename, 'rb') as infile:
                file_data = infile.read()
            
            compressed_data = compress_data(file_data)
            if compressed_data:
                with open(output_filename, 'wb') as outfile:
                    outfile.write(compressed_data)
                print(f"Best compression saved as: {output_filename}")
            else:
                print("Compression failed. No valid compression found.")
        except FileNotFoundError:
            print(f"Error: File '{input_filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif mode == 2:
        compressed_filename = input("Enter compressed file name: ")
        output_filename = input("Enter decompressed file name: ")

        try:
            with open(compressed_filename, 'rb') as infile:
                compressed_data = infile.read()
            
            decompressed_data = decompress_data(compressed_data)
            with open(output_filename, 'wb') as outfile:
                outfile.write(decompressed_data)

            print(f"Decompression complete. Restored as: {output_filename}")
        except FileNotFoundError:
            print(f"Error: File '{compressed_filename}' not found.")
        except Exception as e:
            print(f"Error during decompression: {e}")

if __name__ == "__main__":
    main()