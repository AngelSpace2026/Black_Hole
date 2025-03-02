import os
import random
import struct
import paq

# Reverse chunks at specified positions
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, num_positions):
    with open(input_filename, 'rb') as infile, open(reversed_filename, 'wb') as outfile:
        file_size = os.path.getsize(input_filename)
        total_chunks = (file_size + chunk_size - 1) // chunk_size  # Ensure all chunks are counted

        # Generate spaced positions for reversal
        positions = random.sample(range(total_chunks), min(num_positions, total_chunks))

        for i in range(total_chunks):
            chunk = infile.read(chunk_size)
            if i in positions:
                chunk = chunk[::-1]  # Reverse chunk
            outfile.write(chunk)

    return positions

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, original_size, first_attempt):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata
    metadata = struct.pack(">Q", original_size)  # Store original file size
    metadata += struct.pack(">I", chunk_size)  # Chunk size
    metadata += struct.pack(">I", len(positions))  # Number of positions
    metadata += struct.pack(f">{len(positions)}I", *positions)  # Store reversed positions

    # Compress with PAQ
    compressed_data = paq.compress(metadata + reversed_data)
    compressed_size = len(compressed_data)

    if first_attempt or compressed_size < previous_size:
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        print(f"New best compression: {compressed_size} bytes (ratio: {compressed_size/original_size:.4f})")
        return compressed_size, False  # Update previous size, disable first_attempt
    return previous_size, first_attempt  # Keep old file if compression is worse

# Decompress and restore data
def decompress_and_restore_paq(compressed_filename):
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = paq.decompress(compressed_data)

    # Extract metadata
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]
    num_positions = struct.unpack(">I", decompressed_data[12:16])[0]
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))

    # Restore original chunks
    chunked_data = decompressed_data[16 + num_positions * 4:]
    total_chunks = (len(chunked_data) + chunk_size - 1) // chunk_size
    restored_chunks = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    for pos in positions:
        if 0 <= pos < len(restored_chunks):
            restored_chunks[pos] = restored_chunks[pos][::-1]

    restored_data = b"".join(restored_chunks)[:original_size]

    restored_filename = compressed_filename.replace('.compressed.bin', '')
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompression complete. Restored file: {restored_filename}")

# Find the best chunk strategy and keep searching infinitely
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    previous_size = float('inf')
    first_attempt = True

    while True:  # Infinite loop to keep improving
        chunk_size = random.randint(1, min(file_size, 2**31))
        max_positions = file_size // chunk_size
        num_positions = random.randint(1, min(64, max_positions)) if max_positions > 0 else 1

        reversed_filename = f"{input_filename}.reversed.bin"
        positions = reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, num_positions)

        compressed_filename = f"{input_filename}.compressed.bin"
        previous_size, first_attempt = compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, file_size, first_attempt)

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
        find_best_chunk_strategy(input_filename)  # Infinite search

    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"

        if not os.path.exists(compressed_filename):
            print(f"Error: Compressed file {compressed_filename} not found!")
            return

        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()