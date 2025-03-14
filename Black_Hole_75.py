import os
import random
import struct
import time
import paq

def is_prime(n):
    """Checks if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_positions(limit):
    """Returns a list of prime numbers up to 'limit'."""
    return [n for n in range(2, limit) if is_prime(n)]

def delete_one_bit_per_iteration(bits, iteration):
    """Deletes only one bit per iteration at prime-numbered positions."""
    primes = prime_positions(len(bits))
    new_bits = list(bits)
    
    if iteration < len(primes):
        pos = primes[iteration]
        if pos < len(new_bits):
            del new_bits[pos]  # Remove one bit from a prime position
    
    return ''.join(new_bits)

def restore_one_bit_per_iteration(bits, original_bits, iteration):
    """Restores one bit per iteration at prime-numbered positions."""
    primes = prime_positions(len(original_bits))
    restored_bits = list(bits)

    if iteration < len(primes):
        pos = primes[iteration]
        if pos < len(original_bits):
            restored_bits.insert(pos, '0')  # Add back a zero at a prime position
    
    return ''.join(restored_bits)

def reverse_chunks_at_positions(input_data, chunk_size, positions):
    """Reverses specified chunks of byte data."""
    chunked_data = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]
    
    # Add padding if necessary
    padding_needed = (chunk_size - len(chunked_data[-1]) % chunk_size) % chunk_size
    chunked_data[-1] += b'\x00' * padding_needed

    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]
    
    return b"".join(chunked_data)

def compress_with_paq(data, chunk_size, positions, original_bits, iterations):
    """Compresses data using PAQ and embeds metadata."""
    metadata = struct.pack(">I", len(original_bits)) + struct.pack(">I", chunk_size) + \
               struct.pack(">B", len(positions)) + struct.pack(f">{len(positions)}I", *positions) + \
               struct.pack(">I", iterations)  # Store iteration count
    
    compressed_data = paq.compress(metadata + data)
    return compressed_data

def decompress_and_restore_paq(compressed_filename):
    """Decompresses and restores data from a compressed file."""
    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()
        
        decompressed_data = paq.decompress(compressed_data)
        
        # Extract metadata
        original_size = struct.unpack(">I", decompressed_data[:4])[0]
        chunk_size = struct.unpack(">I", decompressed_data[4:8])[0]
        num_positions = struct.unpack(">B", decompressed_data[8:9])[0]
        positions = struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4])
        iterations = struct.unpack(">I", decompressed_data[9 + num_positions * 4:13 + num_positions * 4])[0]  # Retrieve iterations

        print(f"Original file size before iterations: {original_size} bytes.")

        # Prompt user for the file size to extract
        user_size = original_size

        if user_size != original_size:
            print(f"Warning: The provided size ({user_size} bytes) does not match the original size ({original_size} bytes).")
        
        print(f"Restoring with {iterations} iterations...")

        restored_data = reverse_chunks_at_positions(decompressed_data[13 + num_positions * 4:], chunk_size, positions)
        restored_data = restored_data[:user_size]  # Extract according to the user-defined size

        # Restore zeros back per iteration
        original_bits = ''.join(f"{byte:08b}" for byte in decompressed_data[13 + num_positions * 4:])
        for i in range(iterations):
            original_bits = restore_one_bit_per_iteration(original_bits, original_bits, i)

        restored_data = bytes(int(original_bits[i:i+8], 2) for i in range(0, len(original_bits), 8))

        # Ensure restored data matches the original file size
        restored_data = restored_data[:original_size]  # Trim to original size if necessary

        restored_filename = compressed_filename.replace('.compressed.bin', '')
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)
        
        print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")
    
    except (FileNotFoundError, paq.PAQError, struct.error) as e:
        print(f"Decompression failed: {e}")

def find_best_chunk_strategy(input_filename, max_time_seconds, iterations):
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
        chunk_size = random.randint(1, min(256, file_size))
        max_positions = file_size // chunk_size
        num_positions = random.randint(0, min(max_positions, 64))
        positions = sorted(random.sample(range(max_positions), num_positions)) if num_positions > 0 else []

        # Convert to bits
        original_bits = ''.join(f"{byte:08b}" for byte in file_data)

        # Process: Delete only one bit per iteration
        for i in range(iterations):
            original_bits = delete_one_bit_per_iteration(original_bits, i)

        processed_data = bytes(int(original_bits[i:i+8], 2) for i in range(0, len(original_bits), 8))

        reversed_data = reverse_chunks_at_positions(processed_data, chunk_size, positions)
        compressed_data = compress_with_paq(reversed_data, chunk_size, positions, original_bits, iterations)
        
        compression_ratio = len(compressed_data) / file_size
        if compression_ratio < best_compression_ratio:
            best_compression_ratio = compression_ratio
            best_chunk_size = chunk_size
            best_positions = positions
            print(f"Improved compression: {len(compressed_data)} bytes (chunk size: {chunk_size}, positions: {positions})")

    elapsed_time = time.time() - start_time
    print(f"\nBest compression achieved after {iteration} iterations (time limit: {max_time_seconds} seconds):")
    print(f"Compression ratio: {best_compression_ratio:.4f}")
    print(f"Chunk size: {best_chunk_size}")
    print(f"Positions: {best_positions}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    compressed_filename = f"{input_filename}.compressed.bin"
    try:
        with open(compressed_filename, 'wb') as outfile:
            final_data = compress_with_paq(reverse_chunks_at_positions(processed_data, best_chunk_size, best_positions), best_chunk_size, best_positions, original_bits, iterations)
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
        iterations = int(input("Enter number of iterations for bit deletion: "))
        find_best_chunk_strategy(input_filename, max_time_seconds, iterations)
    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()