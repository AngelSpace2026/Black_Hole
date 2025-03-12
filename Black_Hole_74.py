import os
import random
import struct
import paq

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    return b"".join(chunked_data)

def compress_with_paq(data, chunk_size, positions, original_size, bit_size, rand_op, rand_value):
    """Compresses data using PAQ and embeds metadata."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">I", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">I", bit_size) + struct.pack(">I", rand_op) + struct.pack(">I", rand_value)
    compressed_data = paq.compress(metadata + data)
    return compressed_data

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file."""
    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()
        decompressed_data = paq.decompress(compressed_data)

        offset = 0
        original_size = struct.unpack(">I", decompressed_data[offset:offset+4])[0]
        offset += 4
        chunk_size = struct.unpack(">I", decompressed_data[offset:offset+4])[0]
        offset += 4
        num_positions = struct.unpack(">I", decompressed_data[offset:offset+4])[0]
        offset += 4
        positions = struct.unpack(f">{num_positions}I", decompressed_data[offset:offset + num_positions * 4])
        offset += num_positions * 4
        bit_size = struct.unpack(">I", decompressed_data[offset:offset+4])[0]
        offset += 4
        rand_op = struct.unpack(">I", decompressed_data[offset:offset+4])[0]
        offset += 4
        rand_value = struct.unpack(">I", decompressed_data[offset:offset+4])[0]
        offset += 4

        restored_data = decompressed_data[offset:]

        if rand_op == 1:
            restored_data = bytearray([(b - rand_value) % 256 for b in restored_data])
        else:
            restored_data = bytearray([(b + rand_value) % 256 for b in restored_data])

        restored_data = reverse_chunks_at_positions(bytes(restored_data), chunk_size, positions)
        restored_data = restored_data[:original_size]

        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")
    except (FileNotFoundError, paq.PAQError, struct.error) as e:
        print(f"Decompression failed: {e}")

def find_best_chunk_strategy(input_filename, max_iterations=3600):
    """Finds the best chunk size and reversal positions for compression."""
    file_size = os.path.getsize(input_filename)

    try:
        with open(input_filename, 'rb') as infile:
            file_data = infile.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return

    bit_size = len(file_data) * 8  
    bit_size = min(bit_size, 2**63 - 1)  

    best_compression_ratio = float('inf')
    best_chunk_size = 1
    best_positions = []

    for iteration in range(max_iterations):
        chunk_size = random.randint(1, 256)
        max_positions = file_size // chunk_size
        num_positions = random.randint(0, min(max_positions, 64))
        positions = sorted(random.sample(range(max_positions), num_positions)) if num_positions > 0 else []

        reversed_data = reverse_chunks_at_positions(file_data, chunk_size, positions)

        rand_op = random.choice([1, 2])  
        rand_value = random.randint(1, min(2**bit_size - 1, 2**31 - 1))
        if rand_op == 1:
            modified_data = bytearray([(b - rand_value) % 256 for b in reversed_data])
        else:
            modified_data = bytearray([(b + rand_value) % 256 for b in reversed_data])

        compressed_data = compress_with_paq(bytes(modified_data), chunk_size, positions, file_size, bit_size, rand_op, rand_value)
        compression_ratio = len(compressed_data) / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_chunk_size = chunk_size
            best_positions = positions
            print(f"Iteration {iteration+1}: Improved compression: {len(compressed_data)} bytes (chunk size: {chunk_size}, positions: {positions})")

    print(f"\nBest compression achieved after {max_iterations} iterations:")
    print(f"Compression ratio: {best_compression_ratio:.4f}")
    print(f"Chunk size: {best_chunk_size}")
    print(f"Positions: {best_positions}")

    compressed_filename = f"{input_filename}.compressed.bin"
    try:
        with open(compressed_filename, 'wb') as outfile:
            compressed_data = compress_with_paq(reverse_chunks_at_positions(file_data, best_chunk_size, best_positions), best_chunk_size, best_positions, file_size, bit_size, rand_op, rand_value)
            outfile.write(compressed_data)
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
        find_best_chunk_strategy(input_filename)
    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()