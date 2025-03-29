import random
import os
import paq  # Assuming you have a PAQ Python wrapper or interface

# Define chunk reversal function
def reverse_chunks(data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    reversed_data = bytearray(data)
    for pos in positions:
        start = pos * chunk_size
        end = min((pos + 1) * chunk_size, len(data))
        reversed_data[start:end] = reversed_data[start:end][::-1]
    return bytes(reversed_data)  # Convert back to bytes before returning

# Apply a random transformation
def apply_calculus(data, num_bytes):
    """Adds random bytes to the data."""
    return data + bytearray(random.getrandbits(8) for _ in range(num_bytes))

# Strategy for subtracting 1 from each byte
def compress_strategy_3(data, chunk_size, positions):
    """Subtracts 1 from each byte in the data."""
    return bytearray([x - 1 if x > 0 else 0 for x in data])  # Ensure no byte is less than 0

# Function to move bits left or right
def function_move(data, direction, num_bits):
    """Moves bits left or right in the data."""
    bit_string = ''.join(f'{byte:08b}' for byte in data)
    if direction == 'left':
        bit_string = bit_string[num_bits:] + bit_string[:num_bits]
    else:
        bit_string = bit_string[-num_bits:] + bit_string[:-num_bits]
    return bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))

# Run-length encoding for repeated sequences
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

# Compression strategies
def compress_strategy_1(data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    return reverse_chunks(data, chunk_size, positions)

def compress_strategy_2(data, chunk_size, positions):
    """Adds random bytes to the data."""
    return apply_calculus(data, random.randint(1, 255))

def compress_strategy_4(data, chunk_size, positions):
    """Moves bits left or right in the data."""
    direction = random.choice(["left", "right"])
    num_bits = random.randint(1, 8)
    return function_move(data, direction=direction, num_bits=num_bits)

def compress_strategy_5(data, chunk_size, positions):
    """Compress sequences of zeros (length 1 to 28)."""
    return compress_zeros(data)

def compress_strategy_6(data, chunk_size, positions):
    """Compress sequences of more than 4 repeated bytes."""
    return compress_repeated_bytes(data)

def compress_strategy_7(data, chunk_size, positions):
    """Apply additional random chunk size and transformations."""
    chunk_size = random.randint(2**7, 2**17 - 1)  # Random chunk size in the range 2⁷ to 2¹⁷
    positions = sorted(random.sample(range(len(data) // chunk_size), random.randint(0, len(data) // chunk_size)))
    return reverse_chunks(data, chunk_size, positions)

def compress_strategy_8(data, chunk_size, positions):
    """Apply extra compression heuristics (example: entropy reduction or custom RLE)."""
    return apply_run_length_encoding(data)

# Placeholder function for compressing zeros
def compress_zeros(data):
    """A function to compress sequences of zeros in the data."""
    # Example: Replace long sequences of zeros with a marker byte (e.g., 0x00) followed by length
    compressed_data = bytearray()
    zero_count = 0
    for byte in data:
        if byte == 0:
            zero_count += 1
        else:
            if zero_count > 0:
                compressed_data.append(0)  # Marker for zeros
                compressed_data.append(zero_count)  # Store the length of the zero sequence
                zero_count = 0
            compressed_data.append(byte)
    if zero_count > 0:
        compressed_data.append(0)
        compressed_data.append(zero_count)
    return bytes(compressed_data)

# Function to compress repeated byte sequences
def compress_repeated_bytes(data):
    """A function to compress repeated byte sequences in the data."""
    compressed_data = bytearray()
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        compressed_data.append(data[i])  # Append the byte
        compressed_data.append(count)  # Append the count of repetitions
        i += 1
    return bytes(compressed_data)

# Function to find best compression strategy
def find_best_strategy(data, chunk_size, positions):
    """Find the best compression strategy by applying all strategies."""
    strategies = [compress_strategy_1, compress_strategy_2, compress_strategy_3, compress_strategy_4, compress_strategy_5, compress_strategy_6, compress_strategy_7, compress_strategy_8]
    
    best_compressed_data = None
    best_compression_ratio = float('inf')
    
    for strategy in strategies:
        transformed_data = strategy(data, chunk_size, positions)
        compressed_data = compress_data(transformed_data, chunk_size, positions, len(data), random.randint(1, 255))
        compression_ratio = len(compressed_data) / len(data)
        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
    
    return best_compressed_data, best_compression_ratio

# Function to find best iteration
def find_best_iteration(input_data, max_iterations):
    """Finds the best compression by iterating through multiple random transformations."""
    best_compressed_data = None
    best_compression_ratio = float('inf')

    for _ in range(max_iterations):
        chunk_size = random.randint(2**7, 2**17 - 1)  # Random chunk size
        max_positions = len(input_data) // chunk_size
        num_positions = random.randint(0, max_positions)
        positions = sorted(random.sample(range(max_positions), num_positions))

        compressed_data, compression_ratio = find_best_strategy(input_data, chunk_size, positions)
        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data

    return best_compressed_data, best_compression_ratio

# Function to process large files
def process_large_file(input_filename, output_filename, mode, attempts=1, iterations=100):
    """Handles large files in chunks and applies compression or decompression."""
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Error: Input file '{input_filename}' not found.")
    
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
    
    if mode == "compress":
        best_compressed_data, best_ratio = find_best_iteration(file_data, iterations)
        if best_compressed_data:
            with open(output_filename, 'wb') as outfile:
                outfile.write(best_compressed_data)
            print(f"Best compression saved as: {output_filename}, ratio: {best_ratio:.4f}")
    
    elif mode == "decompress":
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()
        
        try:
            restored_data = decompress_data(compressed_data)
            with open(output_filename, 'wb') as outfile:
                outfile.write(restored_data)
            print(f"Decompression complete. Restored file: {output_filename}")
        except Exception as e:
            print(f"Error during decompression: {e}")

# PAQ compression function
def compress_data(data, chunk_size, positions, data_size, random_value):
    """Compress data using PAQ."""
    try:
        # Convert data from bytearray to bytes for PAQ
        compressed_data = paq.compress(bytes(data))
        return compressed_data
    except Exception as e:
        print(f"Error during PAQ compression: {e}")
        return data

# PAQ decompression function
def decompress_data(compressed_data):
    """Decompress data using PAQ."""
    try:
        # Decompress using PAQ library (assumed paq.decompress method exists)
        restored_data = paq.decompress(compressed_data)
        return restored_data
    except Exception as e:
        print(f"Error during PAQ decompression: {e}")
        return compressed_data

# Main program
def main():
    mode = input("Enter mode (1 for compress, 2 for decompress): ").strip()
    input_filename = input("Enter input file name to compress: ").strip()
    output_filename = input("Enter output file name (e.g., output.compressed.bin): ").strip()

    if mode == '1':
        attempts = int(input("Enter the number of attempts (e.g., 5): ").strip())
        iterations = int(input("Enter the number of iterations (e.g., 100): ").strip())
        try:
            process_large_file(input_filename, output_filename, "compress", attempts, iterations)
        except Exception as e:
            print(f"Error: {e}")
    elif mode == '2':
        try:
            process_large_file(input_filename, output_filename, "decompress")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()