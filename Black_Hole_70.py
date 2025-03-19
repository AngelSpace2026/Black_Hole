import os
import random
import struct
import paq
import time

def apply_minus_operation(value):
    """Applies a modified minus operation."""
    if value <= 0:
        return value + (2**255 - 1)
    elif value <= (2**24 - 1):
        return value + 3
    else:
        return value + 1

def manage_leading_zeros(input_data):
    """This function processes the input byte data to handle leading zeros and ensures that values within the 1-255 byte range are minimized to a single byte."""
    if not isinstance(input_data, bytes):
        raise ValueError("Input data must be of type 'bytes'")

    stripped_data = input_data.lstrip(b'\x00')
    if not stripped_data:
        stripped_data = b'\x00'

    leading_zeros = 0
    for byte in stripped_data:
        if byte == 0:
            leading_zeros += 8
        else:
            leading_zeros += (8 - len(bin(byte)) + bin(byte).index('1') - 2) if byte != 0 else 0

    print(f"Leading zeros count: {leading_zeros} bits")  # Debug output

    if 1 <= len(stripped_data) <= 255:
        return stripped_data[:1]
    else:
        return stripped_data

def reverse_chunks_in_memory(data, chunk_size, num_reversals, num_sets):
    """Reverses chunks of data in memory."""
    try:
        chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        if len(chunked_data[-1]) < chunk_size:
            chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

        total_chunks = len(chunked_data)
        for _ in range(num_reversals):
            if total_chunks > 1:
                positions = random.sample(range(total_chunks), min(num_sets, total_chunks))
                for pos in positions:
                    chunked_data[pos] = chunked_data[pos][::-1]

        return b"".join(chunked_data)
    except Exception as e:
        print(f"Error in reverse_chunks_in_memory: {e}")
        return None

def compress_with_paq(data, compressed_filename, num_reversals, num_sets, original_size):
    """Compresses data using paq, adds metadata, and saves it."""
    try:
        chunk_size = 1
        metadata = struct.pack(">Q", original_size)
        metadata += struct.pack(">I", chunk_size)
        metadata += struct.pack(">I", num_reversals)
        metadata += struct.pack(">I", num_sets)

        modified_metadata_len = apply_minus_operation(len(metadata))
        metadata = metadata[:modified_metadata_len]

        compressed_data = paq.compress(metadata + data)
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        return True
    except Exception as e:
        print(f"Error in compress_with_paq: {e}")
        return False

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a paq-compressed file."""
    try:
        if not compressed_filename.endswith('.compressed.bin'):
            print(f"Error: Invalid compressed file name: {compressed_filename}")
            return False
        if not os.path.exists(compressed_filename):
            raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()
        decompressed_data = paq.decompress(compressed_data)

        original_size = struct.unpack(">Q", decompressed_data[:8])[0]
        chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]
        num_reversals = struct.unpack(">I", decompressed_data[12:16])[0]
        num_sets = struct.unpack(">I", decompressed_data[16:20])[0]

        restored_data = reverse_chunks_in_memory(decompressed_data[20:], chunk_size, num_reversals, num_sets)
        restored_data = restored_data[:original_size]
        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        print(f"Decompression successful. File saved as: {restored_filename}")
        return True
    except Exception as e:
        print(f"Error in decompress_and_restore_paq: {e}")
        return False

def find_best_chunk_strategy(input_filename, iterations=10000):
    """Finds the best compression strategy within a specified number of iterations."""
    try:
        with open(input_filename, 'rb') as infile:
            original_data = infile.read()
        file_size = len(original_data)
        best_compression_ratio = float('inf')
        best_num_reversals = 0
        best_num_sets = 0
        base_name, _ = os.path.splitext(input_filename)
        compressed_filename = base_name + ".compressed.bin"
        chunk_size = 1

        for iteration in range(1, iterations + 1):
            num_reversals = random.randint(1, 64)
            num_sets = random.randint(1, min(file_size, 64))
            reversed_data = reverse_chunks_in_memory(original_data, chunk_size, num_reversals, num_sets)

            if reversed_data and compress_with_paq(reversed_data, compressed_filename, num_reversals, num_sets, file_size):
                compressed_size = os.path.getsize(compressed_filename)
                compression_ratio = compressed_size / file_size
                if compression_ratio < best_compression_ratio:
                    best_compression_ratio = compression_ratio
                    best_num_reversals = num_reversals
                    best_num_sets = num_sets
                    print(f"Iteration {iteration}: Improved compression: ratio={best_compression_ratio:.4f}, reversals={best_num_reversals}, sets={best_num_sets}")

        print(f"\nBest compression found: ratio={best_compression_ratio:.4f}, reversals={best_num_reversals}, sets={best_num_sets}")
        return True
    except Exception as e:
        print(f"Error in find_best_chunk_strategy: {e}")
        return False

def main():
    """Main function to handle user input and call compression/decompression."""
    print("Created by Jurijus Pacalovas.")
    try:
        mode = int(input("Enter mode (1 for compress, 2 for extract): "))
        if mode == 1:
            input_filename = input("Enter input file name to compress: ")
            if not os.path.exists(input_filename):
                print(f"Error: Input file '{input_filename}' not found.")
                return
            if not find_best_chunk_strategy(input_filename):
                print("Compression failed.")
        elif mode == 2:
            compressed_filename = input("Enter compressed file name to extract (include '.compressed.bin'): ")
            if not os.path.exists(compressed_filename):
                print(f"Error: Compressed file '{compressed_filename}' not found.")
                return
            if not decompress_and_restore_paq(compressed_filename):
                print("Extraction failed.")
        else:
            print("Invalid mode.")
    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
