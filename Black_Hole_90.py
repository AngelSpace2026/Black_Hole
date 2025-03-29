import random
import os
import paq  # Ensure you have a PAQ Python wrapper or library

def reverse_chunks(data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    reversed_data = bytearray(data)
    for pos in positions:
        start = pos * chunk_size
        end = min((pos + 1) * chunk_size, len(data))
        reversed_data[start:end] = reversed_data[start:end][::-1]
    return bytes(reversed_data)

def apply_calculus(data, num_bytes):
    """Adds random bytes to the data."""
    return data + bytearray(random.getrandbits(8) for _ in range(num_bytes))

def subtract_one(data):
    """Subtracts 1 from each byte."""
    return bytearray([x - 1 if x > 0 else 0 for x in data])

def function_move(data, direction, num_bits):
    """Moves bits left or right in the data."""
    bit_string = ''.join(f'{byte:08b}' for byte in data)
    if direction == 'left':
        bit_string = bit_string[num_bits:] + bit_string[:num_bits]
    else:
        bit_string = bit_string[-num_bits:] + bit_string[:-num_bits]
    return bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))

def compress_strategy_1(data, chunk_size, positions):
    return reverse_chunks(data, chunk_size, positions)

def compress_strategy_2(data, chunk_size, positions):
    return apply_calculus(data, random.randint(1, 255))

def compress_strategy_3(data, chunk_size, positions):
    return subtract_one(data)

def compress_strategy_4(data, chunk_size, positions):
    direction = random.choice(["left", "right"])
    num_bits = random.randint(1, 8)
    return function_move(data, direction, num_bits)

def compress_strategy_5(data, chunk_size, positions):
    return compress_zeros(data)

def compress_strategy_6(data, chunk_size, positions):
    return compress_repeated_bytes(data)

def compress_strategy_7(data, chunk_size, positions):
    chunk_size = random.randint(2**7, 2**28 - 1)
    return reverse_chunks(data, chunk_size, positions)

def compress_strategy_8(data, chunk_size, positions):
    return apply_run_length_encoding(data)

def compress_zeros(data):
    return bytearray([b if b != 0 else 1 for b in data])

def compress_repeated_bytes(data):
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

def apply_run_length_encoding(data):
    return compress_repeated_bytes(data)

def find_best_strategy(data, chunk_size, positions):
    strategies = [compress_strategy_1, compress_strategy_2, compress_strategy_3, compress_strategy_4,
                  compress_strategy_5, compress_strategy_6, compress_strategy_7, compress_strategy_8]
    best_compressed_data = None
    best_ratio = float('inf')
    for strategy in strategies:
        compressed_data = strategy(data, chunk_size, positions)
        compressed_size = len(compressed_data)
        compression_ratio = compressed_size / len(data)
        if compression_ratio < best_ratio:
            best_ratio = compression_ratio
            best_compressed_data = compressed_data
    return best_compressed_data

def compress_data(data):
    return paq.compress(bytes(data))

def decompress_data(compressed_data):
    return paq.decompress(compressed_data)

def process_large_file(input_filename, output_filename, mode, attempts=1, iterations=100):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Error: Input file '{input_filename}' not found.")
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
    if mode == "compress":
        for _ in range(attempts):
            chunk_size = random.randint(2**7, 2**17 - 1)
            max_positions = len(file_data) // chunk_size
            num_positions = random.randint(0, max_positions)
            positions = sorted(random.sample(range(max_positions), num_positions))
            best_compressed_data = find_best_strategy(file_data, chunk_size, positions)
            compressed_data = compress_data(best_compressed_data)
        with open(output_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        print(f"Best compression saved as: {output_filename}")
    elif mode == "decompress":
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()
        restored_data = decompress_data(compressed_data)
        with open(output_filename, 'wb') as outfile:
            outfile.write(restored_data)
        print(f"Decompression complete. Restored file: {output_filename}")

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

if __name__ == "__main__":
    main()