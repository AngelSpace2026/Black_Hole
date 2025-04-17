import os
import random
import struct
import paq

# Constants
MAX_POSITIONS = 64

def reverse_chunks(data, chunk_size, positions):
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def apply_calculus(data, calculus_value):
    transformed = bytearray(data)
    for i in range(len(transformed)):
        transformed[i] ^= (calculus_value & 0xFF)
    return bytes(transformed)

def compress_data(data, chunk_size, positions, original_size, calculus_value):
    metadata = struct.pack(">III", original_size, chunk_size, calculus_value)
    num_positions = len(positions)
    # Handle potential overflow of num_positions
    if num_positions > 65535:
        raise ValueError("Too many positions to compress.  Increase MAX_POSITIONS or reduce chunk size.")
    metadata += struct.pack(">H", num_positions)

    packed_positions = struct.pack(f">{num_positions}I", *positions)
    compressed_data = paq.compress(metadata + packed_positions + data)
    return compressed_data

def decompress_data(compressed_data):
    try:
        decompressed_data = paq.decompress(compressed_data)
        original_size, chunk_size, calculus_value = struct.unpack(">III", decompressed_data[:12])
        num_positions = struct.unpack(">H", decompressed_data[12:14])[0]
        positions_start = 14
        positions_end = positions_start + num_positions * 4
        positions = struct.unpack(f">{num_positions}I", decompressed_data[positions_start:positions_end])
        data_start = positions_end
        restored = reverse_chunks(decompressed_data[data_start:], chunk_size, positions)
        restored = apply_calculus(restored, calculus_value)
        return restored[:original_size]
    except (struct.error, zlib.error, ValueError) as e:
        raise Exception(f"Error during decompression: {e}")

def find_best_iteration(input_data, max_iterations, chunk_size):
    best_result = compress_data(input_data, chunk_size, [], len(input_data), 0)
    best_size = len(best_result)
    best_ratio = best_size / len(input_data)
    best_data = best_result

    for i in range(1, max_iterations + 1):
        x = random.randint(7, 17)
        calculus_value = random.randint(1, (2 ** x) - 1)
        num_pos = random.randint(0, min(len(input_data) // chunk_size, MAX_POSITIONS))
        positions = sorted(random.sample(range(len(input_data) // chunk_size), num_pos)) if num_pos > 0 else []

        transformed = apply_calculus(input_data, calculus_value)
        reversed_data = reverse_chunks(transformed, chunk_size, positions)
        compressed = compress_data(reversed_data, chunk_size, positions, len(input_data), calculus_value)

        comp_size = len(compressed)
        if comp_size < best_size:
            best_size = comp_size
            best_data = compressed
            best_ratio = comp_size / len(input_data)
            saved = len(input_data) - comp_size
            print(f"Iteration {i}: Compressed size {comp_size}, Saved {saved} bytes, Ratio: {best_ratio:.5f}")

    print(f"\nFinal best saved {len(input_data) - best_size} bytes, Ratio: {best_ratio:.5f}")
    return best_data, best_ratio

def process_large_file(input_filename, output_filename, mode, attempts=1, iterations=100, fixed_chunk_size=None):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Error: Input file '{input_filename}' not found.")

    with open(input_filename, 'rb') as infile:
        file_data = infile.read()

    if mode == "compress":
        best_compressed_data, best_ratio = find_best_iteration(file_data, iterations, fixed_chunk_size)
        if best_compressed_data:
            with open(output_filename, 'wb') as outfile:
                outfile.write(best_compressed_data)
            print(f"\nBest compression saved to: {output_filename}")
    elif mode == "decompress":
        try:
            restored_data = decompress_data(file_data)
            with open(output_filename, 'wb') as outfile:
                outfile.write(restored_data)
            print(f"Decompression complete. Restored file: {output_filename}")
        except Exception as e:
            print(f"Error during decompression: {e}")

def main():
    print("Created by Jurijus Pacalovas.")
    while True:
        try:
            mode = int(input("Enter mode (1 for compress, 2 for decompress): "))
            if mode in [1, 2]:
                break
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        output_filename = input("Enter output file name (e.g., output.compressed.bin): ")
        while True:
            try:
                n = int(input("Enter a number n (1-5) for a chunk size of 2**(2**n) bytes: "))
                if 1 <= n <= 5:
                    chunk_size = 2**(2**n)
                    print(f"Using chunk size: {chunk_size} bytes")
                    break
                else:
                    print("Please enter a number between 0 and 5.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        while True:
            try:
                attempts = int(input("Enter number of attempts (e.g., 5): "))
                iterations = int(input("Enter number of iterations per attempt (e.g., 100): "))
                if attempts > 0 and iterations > 0:
                    break
                else:
                    print("Please enter positive integers.")
            except ValueError:
                print("Invalid input. Please enter integers.")

        for attempt in range(1, attempts + 1):
            print(f"\n--- Attempt {attempt} ---")
            process_large_file(input_filename, output_filename, "compress", attempts=1, iterations=iterations, fixed_chunk_size=chunk_size)

    elif mode == 2:
        compressed_filename = input("Enter the compressed file name: ")
        output_filename = input("Enter name for the decompressed output: ")
        process_large_file(compressed_filename, output_filename, "decompress")

if __name__ == "__main__":
    main()
