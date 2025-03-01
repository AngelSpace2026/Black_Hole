import os
import random
import struct
import paq

# Reverse specified chunks at positions
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split into chunks  
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]  

    # Add padding if needed  
    if len(chunked_data[-1]) < chunk_size:  
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))  

    # Reverse specified chunks  
    for pos in positions:  
        if 0 <= pos < len(chunked_data):  
            chunked_data[pos] = chunked_data[pos][::-1]  

    with open(reversed_filename, 'wb') as outfile:  
        outfile.write(b"".join(chunked_data))

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, original_size, first_attempt):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata (1-byte size instead of 8 bytes)
    metadata = struct.pack(">B", original_size % 256)  # 1-byte representation of size  
    metadata += struct.pack(">I", chunk_size)  # Chunk size (unsigned int)  
    metadata += struct.pack(">I", len(positions))  # Number of positions (unsigned int)  
    metadata += struct.pack(f">{len(positions)}I", *positions)  # Positions list  

    # Compress the file  
    compressed_data = paq.compress(metadata + reversed_data)  

    # Add four extra bytes at the start (00630001)
    extra_bytes = b'\x00\x63\x00\x01'  # This is the sequence you want to add  
    final_compressed_data = extra_bytes + compressed_data  

    # Get the current compressed size  
    compressed_size = len(final_compressed_data)  

    if first_attempt:  
        # First attempt always overwrites  
        with open(compressed_filename, 'wb') as outfile:  
            outfile.write(final_compressed_data)  
        first_attempt = False  
        return compressed_size, first_attempt  
    elif compressed_size < previous_size:  
        # Save only if compression is better  
        with open(compressed_filename, 'wb') as outfile:  
            outfile.write(final_compressed_data)  
        previous_size = compressed_size  
        return previous_size, first_attempt  
    else:  
        return previous_size, first_attempt  

# Decompress and restore data (removing first 4 bytes always)
def decompress_and_restore_paq(compressed_filename):
    # Ensure file exists
    if not os.path.exists(compressed_filename):  
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")  

    # Read compressed file  
    with open(compressed_filename, 'rb') as infile:  
        compressed_data = infile.read()  

    # Remove the first four bytes
    compressed_data = compressed_data[4:]  # Always remove the first 4 bytes

    # Decompress data  
    decompressed_data = paq.decompress(compressed_data)  

    # Extract metadata  
    original_size = struct.unpack(">B", decompressed_data[:1])[0]  # Read 1-byte size  
    chunk_size = struct.unpack(">I", decompressed_data[1:5])[0]  # Chunk size  
    num_positions = struct.unpack(">I", decompressed_data[5:9])[0]  # Number of reversed positions  
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[9:9 + num_positions * 4]))  # Positions  

    # Reconstruct chunks  
    chunked_data = decompressed_data[9 + num_positions * 4:]  
    total_chunks = len(chunked_data) // chunk_size  
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]  

    # Reverse chunks back  
    for pos in positions:  
        if 0 <= pos < len(chunked_data):  
            chunked_data[pos] = chunked_data[pos][::-1]  

    # Combine chunks and truncate to original size  
    restored_data = b"".join(chunked_data)[:original_size]  

    # Auto-generate restored filename  
    restored_filename = compressed_filename.replace('.compressed.bin', '')  # Remove .compressed.bin extension  

    # Write the restored data to the file  
    with open(restored_filename, 'wb') as outfile:  
        outfile.write(restored_data)

# Find the best chunk strategy (infinite loop)
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')
    best_count = 0

    previous_size = 10**12  # Use a very large number to ensure first compression happens  
    first_attempt = True  # Flag to track if it's the first attempt  

    while True:  # Infinite loop to keep improving  
        for chunk_size in range(1, 256):  
            max_positions = file_size // chunk_size  
            if max_positions > 0:  
                positions_count = random.randint(1, min(max_positions, 64))  
                positions = random.sample(range(max_positions), positions_count)  

                reversed_filename = f"{input_filename}.reversed.bin"  
                reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions)  

                compressed_filename = f"{input_filename}.compressed.bin"  
                compressed_size, first_attempt = compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, file_size, first_attempt)  

                if compressed_size < previous_size:  
                    # Update the best values when a better compression ratio is found  
                    previous_size = compressed_size  
                    best_chunk_size = chunk_size  
                    best_positions = positions  
                    best_compression_ratio = compressed_size / file_size  
                    best_count += 1  

                    # Save the best result found so far  
                    #print(f"Improved compression with chunk size {chunk_size} and {len(positions)} reversed positions. Compression ratio: {best_compression_ratio:.4f}")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")

    # Loop to ensure the user only inputs 1 or 2 for mode selection  
    while True:  
        try:  
            mode = int(input("Enter mode (1 for compress, 2 for extract): "))  
            if mode not in [1, 2]:  
                print("Error: Please enter 1 for compress or 2 for extract.")  
            else:  
                break  # Exit loop if valid input is provided  
        except ValueError:  
            print("Error: Invalid input. Please enter a number (1 or 2).")  
    
    if mode == 1:    
        input_filename = input("Enter input file name to compress: ")  
        # Check if the input file exists  
        if not os.path.exists(input_filename):  
            print(f"Error: File {input_filename} not found!")  
            return  
        find_best_chunk_strategy(input_filename)  # Infinite search  
          
    elif mode == 2:    
        # Now user is prompted to enter the base name of the compressed file (without .compressed.bin)  
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")  

        # Add the .compressed.bin extension to the input filename  
        compressed_filename = f"{compressed_filename_base}.compressed.bin"  
          
        # Perform the extraction (restoring) process  
        if not os.path.exists(compressed_filename):  
            print(f"Error: Compressed file {compressed_filename} not found!")  
            return  
          
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()