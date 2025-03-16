import os
import random
import struct
import time
import paq  # Ensure PAQ is available

SPECIAL_MARKER = b'\xE7'  # Special marker for encoding/decoding

def encode_three_to_one(data):
    """Encodes every three-bit sequence into a single bit equivalent."""
    binary_data = ''.join(format(byte, '08b') for byte in data)  # Convert to binary
    encoded_bits = ''.join(binary_data[i] for i in range(0, len(binary_data), 3))  # Take every 3rd bit
    return bytearray(int(encoded_bits[i:i+8], 2) for i in range(0, len(encoded_bits), 8))

def decode_one_to_three(data, original_length):
    """Decodes single-bit compressed form back into three-bit sequences."""
    binary_data = ''.join(format(byte, '08b') for byte in data)  # Convert to binary
    expanded_bits = ''.join(bit * 3 for bit in binary_data)  # Expand back to three-bit
    expanded_bits = expanded_bits[:original_length * 8]  # Trim excess
    return bytearray(int(expanded_bits[i:i+8], 2) for i in range(0, len(expanded_bits), 8))

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specific chunks in the byte data."""
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    
    return b"".join(chunked_data)

def compress_with_paq(data, chunk_size, positions, original_size):
    """Compresses data using PAQ and embeds metadata."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions)
    
    compressed_data = paq.compress(metadata + data)
    return compressed_data

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file."""
    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()
        
        decompressed_data = paq.decompress(compressed_data)
        
        original_size = struct.unpack(">I", decompressed_data[:4])[0]
        chunk_size = struct.unpack(">I", decompressed_data[4:8])[0]
        num_positions = struct.unpack(">B", decompressed_data[8:9])[0]
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        
        restored_data = reverse_chunks_at_positions(decompressed_data[9 + num_positions * 4:], chunk_size, positions)
        restored_data = decode_one_to_three(restored_data, original_size)  # Restore original bits
        restored_data = restored_data[:original_size]
        
        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        
        print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")
    
    except (FileNotFoundError, paq.PAQError, struct.error) as e:
        print(f"Decompression failed: {e}")

def find_best_chunk_strategy(input_filename, max_time_seconds):
    """Finds the best chunk size and reversal positions for compression."""
    try:
        with open(input_filename, 'rb') as infile:
            file_data = infile.read()
        
        file_size = len(file_data)
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return
    
    best_compression_ratio = float('inf')
    best_chunk_size = 1
    best_positions = []
    
    start_time = time.time()
    iteration = 0
    
    while time.time() - start_time < max_time_seconds:
        iteration += 1
        chunk_size = random.randint(1, min(256, file_size))  # Cap chunk size to file size
        max_positions = file_size // chunk_size
        num_positions = random.randint(0, min(max_positions, 64))  # Limit number of positions
        positions = sorted(random.sample(range(max_positions), num_positions)) if num_positions > 0 else []

        # Encode 3-bit to 1-bit
        encoded_data = encode_three_to_one(file_data)

        # Reverse chunks
        reversed_data = reverse_chunks_at_positions(encoded_data, chunk_size, positions)

        compressed_data = compress_with_paq(reversed_data, chunk_size, positions, file_size)
        compression_ratio = len(compressed_data) / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_chunk_size = chunk_size
            best_positions = positions
            print(f"Improved compression: {len(compressed_data)} bytes (compression ratio: {compression_ratio:.4f})")

    elapsed_time = time.time() - start_time
    print(f"\nBest compression achieved after {iteration} iterations (time limit: {max_time_seconds} seconds):")
    print(f"Compression ratio: {best_compression_ratio:.4f}")
    print(f"Chunk size: {best_chunk_size}")
    print(f"Positions: {best_positions}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    compressed_filename = f"{input_filename}.compressed.bin"
    try:
        with open(compressed_filename, 'wb') as outfile:
            final_data = compress_with_paq(reverse_chunks_at_positions(encode_three_to_one(file_data), best_chunk_size, best_positions), best_chunk_size, best_positions, file_size)
            outfile.write(final_data)
        print(f"Compressed file saved as {compressed_filename}")
    except Exception as e:
        print(f"Error writing compressed file: {e}")

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
        max_time_seconds = int(input("Enter maximum time limit for compression (in seconds): "))
        find_best_chunk_strategy(input_filename, max_time_seconds)
    
    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()