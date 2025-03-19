import os
import random
import struct
import paq
import time

def reverse_chunks_in_memory(data, chunk_size, positions):
    try:
        chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        if len(chunked_data[-1]) < chunk_size:
            chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

        for pos in positions:
            if 0 <= pos < len(chunked_data):
                chunked_data[pos] = chunked_data[pos][::-1]

        return b"".join(chunked_data)
    except Exception as e:
        print(f"Error in reverse_chunks_in_memory: {e}")
        return None

def compress_with_paq(data, compressed_filename, chunk_size, positions, original_size):
    try:
        metadata = struct.pack(">Q", original_size)
        metadata += struct.pack(">I", chunk_size)
        metadata += struct.pack(">I", len(positions))
        metadata += struct.pack(f">{len(positions)}I", *positions)

        compressed_data = paq.compress(metadata + data)

        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        return True
    except Exception as e:
        print(f"Error in compress_with_paq: {e}")
        return False

def decompress_and_restore_paq(compressed_filename):
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
        num_positions = struct.unpack(">I", decompressed_data[12:16])[0]
        positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))
        chunked_data = decompressed_data[16 + num_positions * 4:]

        total_chunks = len(chunked_data) // chunk_size
        chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

        for pos in positions:
            if 0 <= pos < len(chunked_data):
                chunked_data[pos] = chunked_data[pos][::-1]

        restored_data = b"".join(chunked_data)[:original_size]

        restored_filename = compressed_filename[:-15]

        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        return True
    except Exception as e:
        print(f"Error in decompress_and_restore_paq: {e}")
        return False

def find_best_chunk_strategy(input_filename, timeout_seconds=60):
    try:
        with open(input_filename, 'rb') as infile:
            original_data = infile.read()
        file_size = len(original_data)
        best_chunk_size = 1
        best_positions = []
        best_compression_ratio = float('inf')
        best_compressed_size = float('inf')

        base_name, _ = os.path.splitext(input_filename)
        compressed_filename = base_name + ".compressed.bin"

        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            for chunk_size in range(64, min(513, file_size + 1), 64):
                max_chunks = (file_size + chunk_size - 1) // chunk_size
                max_positions = min(max_chunks, 64)
                if max_positions > 0:
                    positions = random.sample(range(max_chunks), max_positions)
                    reversed_data = reverse_chunks_in_memory(original_data, chunk_size, positions)
                    if reversed_data and compress_with_paq(reversed_data, compressed_filename, chunk_size, positions, file_size):
                        compressed_size = os.path.getsize(compressed_filename)
                        compression_ratio = compressed_size / file_size
                        if compression_ratio < best_compression_ratio:
                            best_compression_ratio = compression_ratio
                            best_chunk_size = chunk_size
                            best_positions = positions
                            best_compressed_size = compressed_size
                            print(f"Improved compression: chunk_size={best_chunk_size}, ratio={best_compression_ratio:.4f}")

        print(f"\nBest compression found: chunk_size={best_chunk_size}, ratio={best_compression_ratio:.4f}, size={best_compressed_size} bytes")
        return True
    except Exception as e:
        print(f"Error in find_best_chunk_strategy: {e}")
        return False

def main():
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
