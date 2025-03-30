import random
import os
import paq  # Ensure PAQ module is available

# 1. Reverse chunks function
def reverse_chunks(data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    reversed_data = bytearray(data)
    for pos in positions:
        start = pos * chunk_size
        end = min((pos + 1) * chunk_size, len(data))
        reversed_data[start:end] = reversed_data[start:end][::-1]
    return bytes(reversed_data)

# 2. Apply random bytes to the data
def apply_random_bytes(data, num_bytes):
    """Adds random bytes to the data."""
    return data + bytearray(random.getrandbits(8) for _ in range(num_bytes))

# 3. Compress strategy 3 (subtracting 1 from each byte)
def compress_strategy_3(data):
    """Subtracts 1 from each byte in the data."""
    return bytearray([x - 1 if x > 0 else 0 for x in data])  # Ensure no byte is less than 0

# 4. Function to move bits left or right in the data
def function_move(data, direction, num_bits):
    """Moves bits left or right in the data."""
    bit_string = ''.join(f'{byte:08b}' for byte in data)
    if direction == 'left':
        bit_string = bit_string[num_bits:] + bit_string[:num_bits]
    else:
        bit_string = bit_string[-num_bits:] + bit_string[:-num_bits]
    return bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))

# 5. Apply run-length encoding for repeated sequences
def apply_run_length_encoding(data):
    """A simple run-length encoding (RLE) for repeated sequences of bytes."""
    compressed_data = bytearray()
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        compressed_data.append(data[i])
        compressed_data.append(count)
        i += 1
    return bytes(compressed_data)

# 6. Compress data with PAQ
def compress_data(data):
    """Compresses the data using PAQ compression, adds one byte, and changes the last byte."""
    compressed_data = paq.compress(data)  # Using PAQ compression instead of zlib
    last_byte = compressed_data[-1]
    extra_byte = bytes([random.randint(0, 255)])  # Add random byte
    compressed_data += extra_byte
    modified_last_byte = bytes([last_byte ^ 0xFF])  # Modify last byte using XOR
    compressed_data = compressed_data[:-1] + modified_last_byte
    return compressed_data, last_byte  # Return modified data and last byte

# 7. Decompress data with byte restoration
def decompress_data(compressed_data, last_byte):
    """Restores the last byte and decompresses the data."""
    compressed_data = compressed_data[:-1]  # Remove the extra byte
    modified_last_byte = compressed_data[-1]
    compressed_data = compressed_data[:-1] + bytes([modified_last_byte ^ 0xFF])  # Restore the last byte
    return paq.decompress(compressed_data)  # Using PAQ decompression

# 8. Strategy 7: Compress length of bits (0-2^28) for zeros, and add last byte from the original file
def strategy_7(data, last_byte_from_file):
    """Compresses long sequences of zeros and adds the last byte from the original file."""
    bit_string = ''.join(f'{byte:08b}' for byte in data)
    compressed_data = bit_string.replace('0', '')  # Removing zeros to compress zero sequences
    compressed_data = bytearray(int(compressed_data[i:i + 8], 2) for i in range(0, len(compressed_data), 8))
    compressed_data.append(last_byte_from_file)  # Add the last byte from the original file
    return bytes(compressed_data)

# 9. Strategy 8: Compress repeated sequences longer than 4 bytes
def strategy_8(data):
    """Compress sequences of more than 4 bytes that repeat."""
    i = 0
    compressed_data = bytearray()
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i:i+4] == data[i+1:i+5]:  # Checking for 4-byte sequences
            i += 4
            count += 1
        if count > 1:
            compressed_data.append(count)
            compressed_data.extend(data[i:i+4])
        else:
            compressed_data.append(data[i])
        i += 1
    return bytes(compressed_data)

# 10. Find the best compression strategy by applying various strategies
def find_best_strategy(data):
    """Find the best compression strategy by applying all strategies."""
    strategies = [reverse_chunks, apply_random_bytes, compress_strategy_3, function_move, apply_run_length_encoding, strategy_7, strategy_8]
    best_compressed_data = None
    best_compression_ratio = float('inf')
    for strategy in strategies:
        # We randomly choose chunk size and positions for testing
        chunk_size = random.randint(1, 256)
        positions = sorted(random.sample(range(len(data) // chunk_size), random.randint(0, len(data) // chunk_size)))
        transformed_data = strategy(data, chunk_size, positions)
        compressed_data = paq.compress(transformed_data)  # Using PAQ compression
        compression_ratio = len(compressed_data) / len(data)
        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
    return best_compressed_data, best_compression_ratio

# 11. Process large files for compression and decompression
def process_large_file(input_filename, output_filename, mode, attempts=1, iterations=100):
    """Handles large files in chunks and applies compression or decompression."""
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Error: Input file '{input_filename}' not found.")
    
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()

    if mode == "compress":
        compressed_data, last_byte = compress_data(file_data)
        with open(output_filename, 'wb') as outfile:
            outfile.write(compressed_data)
            outfile.write(bytes([last_byte]))  # Store the last byte for decompression
        print(f"Compression complete. Output saved to: {output_filename}")
        return last_byte  # Return the last byte for decompression use
    elif mode == "decompress":
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()
        
        # The last byte is stored as the last byte in the file
        last_byte = compressed_data[-1]
        compressed_data = compressed_data[:-1]  # Remove the last byte

        try:
            restored_data = decompress_data(compressed_data, last_byte)
            with open(output_filename, 'wb') as outfile:
                outfile.write(restored_data)
            print(f"Decompression complete. Restored file: {output_filename}")
        except Exception as e:
            print(f"Error during decompression: {e}")

# Main program to execute based on user input
def main():
    mode = input("Enter mode (1 for compress, 2 for decompress): ").strip()
    input_filename = input("Enter input file name: ").strip()
    output_filename = input("Enter output file name: ").strip()

    if mode == '1':  # Compression mode
        attempts = int(input("Enter the number of attempts (e.g., 5): ").strip())
        iterations = int(input("Enter the number of iterations (e.g., 100): ").strip())
        try:
            process_large_file(input_filename, output_filename, "compress", attempts, iterations)
        except Exception as e:
            print(f"Error: {e}")
    elif mode == '2':  # Decompression mode
        try:
            process_large_file(input_filename, output_filename, "decompress")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()