import os
import random
import struct
import time
import paq

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specified chunks of byte data while ensuring proper chunk handling."""
    if not input_data:
        return input_data

    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    
    return b"".join(chunked_data)

def add_random_bytes(data, num_bytes=4):
    """Adds random bytes while ensuring the buffer size remains valid."""
    if len(data) < num_bytes:
        return data

    num_insertions = max(1, len(data) // 100)
    for _ in range(num_insertions):
        pos = random.randint(0, len(data) - num_bytes)
        data = data[:pos] + os.urandom(num_bytes) + data[pos:]
    
    return data

def subtract_large_number(data):
    """Subtracts a large random number (1 to 2**64 - 1) safely from byte data."""
    if not data:
        return data

    large_number = random.randint(1, 2**64 - 1)

    try:
        data_as_int = int.from_bytes(data, byteorder="big", signed=False)
        if data_as_int < large_number:
            return data  # Avoid underflow errors

        new_data_as_int = data_as_int - large_number
        byte_length = max((new_data_as_int.bit_length() + 7) // 8, 1)
        new_data = new_data_as_int.to_bytes(byte_length, byteorder="big")
    except (OverflowError, ValueError):
        return data  # Return original if an error occurs

    return new_data

def compress_with_paq(data, chunk_size, positions, original_size, strategy):
    """Compresses data using PAQ and embeds metadata, ensuring buffer safety."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">B", strategy)  # Add strategy info

    return paq.compress(metadata + data)

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file safely."""
    try:
        with open(compressed_filename, 'rb') as infile:
            decompressed_data = paq.decompress(infile.read())

        original_size, chunk_size, num_positions = struct.unpack(">IIB", decompressed_data[:9])
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        strategy = struct.unpack(">B", decompressed_data[9 + num_positions * 4:10 + num_positions * 4])[0]

        restored_data = reverse_chunks_at_positions(decompressed_data[10 + num_positions * 4:], chunk_size, positions)
        restored_data = restored_data[:original_size]

        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)

        print(f"Decompression complete. Restored file: {restored_filename}")
    except Exception as e:
        print(f"Error during decompression: {e}")

def find_best_iteration(input_filename, max_iterations):
    """Finds the best compression strategy within a single attempt (7200 iterations)."""
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
        file_size = len(file_data)

    best_compression_ratio = float('inf')
    best_compressed_data = None
    best_strategy = None

    for iteration in range(max_iterations):
        chunk_size = random.randint(1, min(256, file_size))
        num_positions = random.randint(0, min(file_size // chunk_size, 64))
        positions = sorted(random.sample(range(file_size // chunk_size), num_positions)) if num_positions > 0 else []

        # Choose strategy based on iteration number
        if iteration % 3 == 0:  # Strategy 1: Reverse chunks
            transformed_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
            compressed_data = compress_with_paq(transformed_data, chunk_size, positions, file_size, 1)

        elif iteration % 3 == 1:  # Strategy 2: Reverse + add random bytes
            transformed_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
            transformed_data = add_random_bytes(transformed_data)
            compressed_data = compress_with_paq(transformed_data, chunk_size, positions, file_size, 2)

        else:  # Strategy 3: Reverse + subtract large number
            transformed_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
            transformed_data = subtract_large_number(transformed_data)
            compressed_data = compress_with_paq(transformed_data, chunk_size, positions, file_size, 3)

        compression_ratio = len(compressed_data) / file_size

        # Choose the best strategy in this iteration
        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
            best_strategy = (iteration % 3) + 1

    return best_compressed_data, best_compression_ratio, best_strategy

def run_compression(input_filename):
    """Runs 30 attempts, each with 7200 iterations, and picks the best overall result."""
    best_of_30_compressed_data = None
    best_of_30_ratio = float('inf')
    best_of_30_strategy = None

    for i in range(30):
        print(f"Running compression attempt {i+1}/30 with 7200 iterations...")
        compressed_data, compression_ratio, strategy = find_best_iteration(input_filename, 7200)

        if compressed_data and compression_ratio < best_of_30_ratio:
            best_of_30_ratio = compression_ratio
            best_of_30_compressed_data = compressed_data
            best_of_30_strategy = strategy

        # Remove intermediate files
        temp_filename = f"{input_filename}_attempt_{i}.compressed.bin"
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    # Save the best compression result
    final_compressed_filename = f"{input_filename}.compressed.bin"
    with open(final_compressed_filename, 'wb') as outfile:
        outfile.write(best_of_30_compressed_data)

    print(f"Best of 30 compression saved as: {final_compressed_filename} (Strategy {best_of_30_strategy})")
    return final_compressed_filename

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

        # Run 30 compression attempts, each with 7200 iterations
        best_compressed_filename = run_compression(input_filename)

        # Decompress the best compression result
        decompress_and_restore_paq(best_compressed_filename)

    elif mode == 2:
        compressed_filename = input("Enter the full name of the compressed file to extract: ")
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()