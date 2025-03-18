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

def add_random_bytes(data, num_bytes=4):
    """Adds random 4-byte sequences at random positions."""
    num_insertions = max(1, len(data) // 100)
    for _ in range(num_insertions):
        pos = random.randint(0, max(0, len(data) - num_bytes))
        data = data[:pos] + os.urandom(num_bytes) + data[pos:]
    return data

def subtract_and_move_bits(data, shift_min=1, shift_max=7):
    """Subtracts a random value and moves bits."""
    modified_data = bytearray()
    for byte in data:
        sub_value = random.randint(1, 255)
        new_byte = (byte - sub_value) % 256  
        shift_amount = random.randint(shift_min, shift_max)
        shifted_byte = ((new_byte << shift_amount) | (new_byte >> (8 - shift_amount))) & 0xFF  
        modified_data.append(shifted_byte)
    return bytes(modified_data)

def move_bits_randomly(data, shift_min=1, shift_max=7):
    """Moves bits randomly without increasing file size."""
    modified_data = bytearray()
    for byte in data:
        shift_amount = random.randint(shift_min, shift_max)
        shifted_byte = ((byte << shift_amount) | (byte >> (8 - shift_amount))) & 0xFF  
        modified_data.append(shifted_byte)
    return bytes(modified_data)

def compress_with_paq(data, chunk_size, positions, original_size, strategy):
    """Compresses data using PAQ and embeds metadata."""
    metadata = struct.pack(">I", original_size) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">B", strategy)  
    return paq.compress(metadata + data)

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file."""
    try:
        with open(compressed_filename, 'rb') as infile:
            decompressed_data = paq.decompress(infile.read())

        original_size, chunk_size, num_positions = struct.unpack(">IIB", decompressed_data[:9])
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        strategy = struct.unpack(">B", decompressed_data[9 + num_positions * 4:10 + num_positions * 4])[0]

        restored_data = decompressed_data[10 + num_positions * 4:]

        # Reverse the transformations based on strategy
        if strategy == 1:  
            restored_data = reverse_chunks_at_positions(restored_data, chunk_size, positions)
        elif strategy == 2:  
            restored_data = reverse_chunks_at_positions(restored_data, chunk_size, positions)
            restored_data = add_random_bytes(restored_data)
        elif strategy == 3:  
            restored_data = subtract_and_move_bits(restored_data)
        elif strategy == 4:  
            restored_data = move_bits_randomly(restored_data)

        restored_data = restored_data[:original_size]

        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)

        print(f"Decompression complete. Restored file: {restored_filename}")
    except Exception as e:
        print(f"Error during decompression: {e}")

def find_best_iteration(input_filename, max_iterations):
    """Finds the best compression strategy within the given iterations."""
    with open(input_filename, 'rb') as infile:
        file_data = infile.read()
        file_size = len(file_data)

    best_compression_ratio = float('inf')
    best_compressed_data = None
    best_strategy = None

    for iteration in range(max_iterations):
        chunk_size = random.randint(1, min(256, file_size))
        num_positions = random.randint(0, min(file_size // chunk_size, 64))
        positions = sorted(random.sample(range(file_size // chunk_size), num_positions)) if num_positions > 0 else []

        strategy = (iteration % 24) + 1  

        if strategy == 1:
            transformed_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
        elif strategy == 2:
            transformed_data = reverse_chunks_at_positions(file_data, chunk_size, positions)
            transformed_data = add_random_bytes(transformed_data)
        elif strategy == 3:
            transformed_data = subtract_and_move_bits(file_data)
        elif strategy == 4:
            transformed_data = move_bits_randomly(file_data)

        compressed_data = compress_with_paq(transformed_data, chunk_size, positions, file_size, strategy)
        compression_ratio = len(compressed_data) / file_size

        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_compressed_data = compressed_data
            best_strategy = strategy

    return best_compressed_data, best_compression_ratio, best_strategy

def run_compression(input_filename, L):
    """Runs compression, skipping .bin and .txt files, and files smaller than 2KB."""
    if input_filename.lower().endswith((".bin", ".txt")):
        print(f"Skipping compression for {input_filename} (Unsupported file type).")
        return None

    if os.path.getsize(input_filename) < 2048:  
        print(f"Skipping compression for {input_filename} (File size is less than 2KB).")
        return None

    iterations_map = {
        1: 300,
        2: 1000,
        3: 3600,
        4: 7200,
        5: 6 * 7200,
        6: 9 * 7200,
        7: 12 * 7200,
        8: 15 * 7200,
        9: 18 * 7200
    }
    
    max_iterations = iterations_map.get(L, 7200)

    best_of_30_compressed_data = None
    best_of_30_ratio = float('inf')
    best_of_30_strategy = None

    for i in range(30):
        print(f"Running compression attempt {i+1}/30 with {max_iterations} iterations...")
        compressed_data, compression_ratio, strategy = find_best_iteration(input_filename, max_iterations)

        if compressed_data and compression_ratio < best_of_30_ratio:
            best_of_30_ratio = compression_ratio
            best_of_30_compressed_data = compressed_data
            best_of_30_strategy = strategy

        temp_filename = f"{input_filename}_attempt_{i}.compressed.bin"
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    final_compressed_filename = f"{input_filename}.compressed.bin"
    with open(final_compressed_filename, 'wb') as outfile:
        outfile.write(best_of_30_compressed_data)

    print(f"Best of 30 compression saved as: {final_compressed_filename} (Strategy {best_of_30_strategy})")
    return final_compressed_filename

def main():
    print("Created by Jurijus Pacalovas.")

    mode = int(input("Enter mode (1 for compress, 2 for extract): "))

    if mode == 1:
        
        while True:
            try:
                L = int(input("Enter Level of compress (1 to 9): "))
                if L not in range(1, 10):
                    print("Error: Please enter a value for L between 1 and 9.")
                else:
                    break
            except ValueError:
                print("Error: Invalid input. Please enter a number between 1 and 9.")        
        
        input_filename = input("Enter input file name to compress: ")
        best_compressed_filename = run_compression(input_filename, L)
        if best_compressed_filename:
            decompress_and_restore_paq(best_compressed_filename)

    elif mode == 2:
        compressed_filename = input("Enter the compressed file name to extract: ")
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()