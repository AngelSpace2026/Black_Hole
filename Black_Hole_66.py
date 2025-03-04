import os
import random
import struct
import paq

# Reverse chunks at specified positions with spacing
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, number_of_positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]  

    if len(chunked_data[-1]) < chunk_size:  
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))  

    max_position = len(chunked_data)  
    positions = [i * (2**31) // max_position for i in range(number_of_positions)]  

    for pos in positions:  
        if 0 <= pos < len(chunked_data):  
            chunked_data[pos] = chunked_data[pos][::-1]  

    with open(reversed_filename, 'wb') as outfile:  
        outfile.write(b"".join(chunked_data))

# Compress using PAQ with metadata including "times" (3-byte storage)
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, original_size, times):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    metadata = struct.pack(">Q", original_size)  
    metadata += struct.pack(">I", chunk_size)  
    metadata += struct.pack(">I", len(positions))  
    metadata += struct.pack(f">{len(positions)}I", *positions)  

    # Store "times" in 3 bytes
    metadata += times.to_bytes(3, 'big')  

    compressed_data = paq.compress(metadata + reversed_data)  
    compressed_size = len(compressed_data)

    with open(compressed_filename, 'wb') as outfile:  
        outfile.write(compressed_data)  

    return compressed_size

# Find best chunk strategy for given "times" value
def find_best_chunk_strategy(input_filename, times):
    file_size = os.path.getsize(input_filename)
    best_compression_ratio = float('inf')
    best_compressed_filename = input_filename + ".compressed.bin"
    reversed_filename = f"{input_filename}.reversed.bin"
    previous_size = 10**12  
    best_times = times  # Track best times value

    for chunk_size in range(1, file_size // times + 1):  
        max_positions = file_size // chunk_size  
        if max_positions > 0:  
            positions_count = random.randint(1, min(max_positions, 64))  
            positions = [i * (2**31) // file_size for i in range(positions_count)]  

            reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions_count)  
            compressed_size = compress_with_paq(reversed_filename, best_compressed_filename, chunk_size, positions, file_size, times)  

            # Keep track of the best compression ratio
            if compressed_size < previous_size:
                previous_size = compressed_size
                best_compression_ratio = compressed_size / file_size
                best_times = times
                print(f"Times: {times}, Chunk Size: {chunk_size}, Compressed Size: {compressed_size}, Ratio: {best_compression_ratio:.4f}")

    # Clean up intermediate files after processing
    os.remove(reversed_filename)

    return best_compressed_filename

# Decompress and restore original file
def decompress_and_restore_paq(compressed_filename):
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    with open(compressed_filename, 'rb') as infile:  
        compressed_data = infile.read()  

    decompressed_data = paq.decompress(compressed_data)  

    original_size = struct.unpack(">Q", decompressed_data[:8])[0]  
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]  
    num_positions = struct.unpack(">I", decompressed_data[12:16])[0]  
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))  

    # Extract "times" from 3-byte storage
    times = int.from_bytes(decompressed_data[16 + num_positions * 4: 16 + num_positions * 4 + 3], 'big')  

    chunked_data = decompressed_data[16 + num_positions * 4 + 3:]  

    total_chunks = len(chunked_data) // chunk_size  
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]  

    for pos in positions:  
        if 0 <= pos < len(chunked_data):  
            chunked_data[pos] = chunked_data[pos][::-1]  

    restored_data = b"".join(chunked_data)[:original_size]  

    restored_filename = compressed_filename.replace('.compressed.bin', '')  

    with open(restored_filename, 'wb') as outfile:  
        outfile.write(restored_data)  

    print(f"Decompressed: {restored_filename}, Size: {len(restored_data)}, Times: {times}")

    # Delete the compressed file after extraction
    os.remove(compressed_filename)

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

        # Ask user for "times" value (1 to 2^24)
        while True:
            try:
                times = int(input(f"Enter 'times' value (1 to {2**24}): "))  
                if 1 <= times <= 2**24:  
                    break  
                else:  
                    print(f"Error: Please enter a number between 1 and {2**24}.")  
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")  

        best_compressed_filename = find_best_chunk_strategy(input_filename, times)  

        # Delete all files except the best compressed file after compression
        print(f"Best compressed file: {best_compressed_filename}")

    elif mode == 2:  
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")  
        compressed_filename = f"{compressed_filename_base}.compressed.bin"  

        if not os.path.exists(compressed_filename):  
            print(f"Error: Compressed file {compressed_filename} not found!")  
            return  

        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()