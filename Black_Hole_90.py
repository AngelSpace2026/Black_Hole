import random
import os
import paq  # Ensure PAQ module is available
from itertools import permutations

# 1. Reverse chunks function
def reverse_chunks(data, chunk_size, positions):
    reversed_data = bytearray(data)
    for pos in positions:
        start = pos * chunk_size
        end = min((pos + 1) * chunk_size, len(data))
        reversed_data[start:end] = reversed_data[start:end][::-1]
    return bytes(reversed_data)

# 2. Apply random bytes to the data
def apply_random_bytes(data, seed):
    random.seed(seed)
    return data + bytearray(random.getrandbits(8) for _ in range(len(data) // 10))

# 3. Subtracting 1 from each byte
def compress_strategy_3(data):
    return bytearray([x - 1 if x > 0 else 255 for x in data])

# 4. Move bits left or right
def function_move(data, direction, num_bits):
    bit_string = ''.join(f'{byte:08b}' for byte in data)
    if direction == 'left':
        bit_string = bit_string[num_bits:] + bit_string[:num_bits]
    else:
        bit_string = bit_string[-num_bits:] + bit_string[:-num_bits]
    return bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))

# 5. Run-length encoding (RLE)
def apply_run_length_encoding(data):
    compressed_data = bytearray()
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        compressed_data.append(data[i])
        compressed_data.append(min(count, 255))
        i += 1
    return bytes(compressed_data)

# 6. Compress data with PAQ
def compress_data(data):
    compressed_data = paq.compress(data)
    last_byte = compressed_data[-1]
    extra_byte = bytes([random.randint(0, 255)])
    compressed_data += extra_byte
    modified_last_byte = bytes([last_byte ^ 0xFF])
    return compressed_data[:-1] + modified_last_byte, last_byte

# 7. Decompress data
def decompress_data(compressed_data, last_byte):
    compressed_data = compressed_data[:-1]
    modified_last_byte = compressed_data[-1]
    compressed_data = compressed_data[:-1] + bytes([modified_last_byte ^ 0xFF])
    return paq.decompress(compressed_data)

# 8. Apply multiple strategies in sequence
def apply_strategies(data, strategies):
    for strategy in strategies:
        data = strategy(data)
    return data

# 9. Find the best compression strategy
def find_best_strategy(data):
    strategies = [reverse_chunks, apply_random_bytes, compress_strategy_3, function_move, apply_run_length_encoding]
    best_compressed_data = None
    best_compression_ratio = float('inf')
    best_strategy = None
    
    for strategy_order in permutations(strategies):
        transformed_data = apply_strategies(data, strategy_order)
        compressed_data = paq.compress(transformed_data)
        compression_ratio = len(compressed_data) / len(data)
        
        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
            best_strategy = strategy_order
    
    return best_compressed_data, best_strategy

# Main processing function
def process_large_file(input_filename, output_filename, mode, attempts=1, iterations=1):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Error: Input file '{input_filename}' not found.")
    
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
    
    if mode == "compress":
        compressed_data, last_byte = compress_data(file_data)
        with open(output_filename, 'wb') as outfile:
            outfile.write(compressed_data)
            outfile.write(bytes([last_byte]))
        print(f"Compression complete. Output saved to: {output_filename}")
    elif mode == "decompress":
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()
        last_byte = compressed_data[-1]
        compressed_data = compressed_data[:-1]
        
        restored_data = decompress_data(compressed_data, last_byte)
        with open(output_filename, 'wb') as outfile:
            outfile.write(restored_data)
        print(f"Decompression complete. Restored file: {output_filename}")

# Main execution
def main():
    mode = input("Enter mode (1 for compress, 2 for decompress): ").strip()
    input_filename = input("Enter input file name: ").strip()
    output_filename = input("Enter output file name: ").strip()
    
    if mode == '1':
        attempts = int(input("Enter the number of attempts: ").strip())
        iterations = int(input("Enter the number of iterations: ").strip())
        process_large_file(input_filename, output_filename, "compress", attempts, iterations)
    elif mode == '2':
        process_large_file(input_filename, output_filename, "decompress")
    else:
        print("Invalid mode selection.")

if __name__ == "__main__":
    main()