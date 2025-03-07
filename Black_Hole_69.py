import os
import random
import struct
import paq

# Apply the minus operation for modifying values
def apply_minus_operation(value):
    if value <= 0:
        return value + (2**255 - 1)  # Wrap around for negative values
    elif value <= (2**24 - 1):
        return value + 3  # Add 3 bytes if value is within the range 0 to (2^24-1)
    else:
        return value + 1  # Add 1 byte for values greater than (2^24 - 1)

# Count leading zeros and save 1 byte for the count
def count_leading_zeros(data):
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 8  # 8 bits for each zero byte
        else:
            leading_zeros += (8 - (byte.bit_length()))  # Count the leading zeros in the byte itself
            break
    return leading_zeros

# Reverse chunks at specified positions
def reverse_chunks(input_filename, reversed_filename, chunk_size, num_reversals, num_sets):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Count leading zeros and store 1 byte to represent them
    leading_zeros = count_leading_zeros(data)
    leading_zeros_byte = struct.pack(">B", leading_zeros)  # Save leading zeros as 1 byte

    # Split data into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))
    total_chunks = len(chunked_data)

    for _ in range(num_reversals):
        if total_chunks > 1:
            positions = [random.randint(0, total_chunks - 1) for _ in range(min(num_sets, total_chunks))]
            for pos in positions:
                chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        # Write leading zeros byte followed by the reversed data
        outfile.write(leading_zeros_byte + b"".join(chunked_data))

# Compress using PAQ
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, num_reversals, num_sets, prev_size, original_size, first_attempt):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    metadata = struct.pack(">I", original_size)  # Changed from >Q to >I (4 bytes for size)
    metadata += struct.pack(">I", chunk_size)
    metadata += struct.pack(">I", num_reversals)
    metadata += struct.pack(">I", num_sets)

    # Apply the minus operation to metadata length
    new_metadata_len = apply_minus_operation(len(metadata))
    metadata = metadata[:new_metadata_len]

    compressed_data = paq.compress(metadata + reversed_data)
    compressed_size = len(compressed_data)

    if first_attempt:
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        return compressed_size, False
    elif compressed_size < prev_size:
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        print(f"Improved compression! Size: {compressed_size} bytes. Ratio: {compressed_size / original_size:.4f}")
        return compressed_size, False
    else:
        return prev_size, False

# Decompress and restore
def decompress_and_restore_paq(compressed_filename):
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = paq.decompress(compressed_data)

    original_size = struct.unpack(">I", decompressed_data[:4])[0]  # Changed from >Q to >I (4 bytes for size)
    chunk_size = struct.unpack(">I", decompressed_data[4:8])[0]
    num_reversals = struct.unpack(">I", decompressed_data[8:12])[0]
    num_sets = struct.unpack(">I", decompressed_data[12:16])[0]

    # Read leading zeros byte
    leading_zeros_byte = decompressed_data[16:17]
    leading_zeros = struct.unpack(">B", leading_zeros_byte)[0]

    chunked_data = decompressed_data[17:]
    chunk_size = min(chunk_size, len(chunked_data))
    total_chunks = max(1, len(chunked_data) // chunk_size)
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    for _ in range(num_reversals):
        if total_chunks > 1:
            positions = [random.randint(0, total_chunks - 1) for _ in range(min(num_sets, total_chunks))]
            for pos in positions:
                chunked_data[pos] = chunked_data[pos][::-1]

    restored_data = b"".join(chunked_data)[:original_size]

    # Restore leading zeros to the beginning of the restored data
    restored_data = b"\x00" * (leading_zeros // 8) + restored_data  # Adding leading zeros back to the data

    restored_filename = compressed_filename.replace('.compressed.bin', '')
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")

# Find best chunk strategy (10,000 iterations)
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_compression_ratio = float('inf')
    prev_size = 10**12
    first_attempt = True

    for iteration in range(1, 10_001):  # Runs exactly 10,000 times
        for chunk_size in range(1, 256):
            max_positions = file_size // chunk_size
            if max_positions > 0:
                num_reversals = random.randint(1, 64)
                num_sets = random.randint(1, min(max_positions, 64))

                reversed_filename = f"{input_filename}.reversed.bin"
                reverse_chunks(input_filename, reversed_filename, chunk_size, num_reversals, num_sets)

                compressed_filename = f"{input_filename}.compressed.bin"
                compressed_size, first_attempt = compress_with_paq(reversed_filename, compressed_filename, chunk_size, num_reversals, num_sets, prev_size, file_size, first_attempt)

                if compressed_size < prev_size:
                    prev_size = compressed_size
                    best_compression_ratio = compressed_size / file_size
                    print(f"Iteration {iteration}: New best compression: {compressed_size} bytes. Ratio: {best_compression_ratio:.4f}")

        if iteration % 1000 == 0:
            print(f"Progress: {iteration}/10,000 iterations completed.")

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