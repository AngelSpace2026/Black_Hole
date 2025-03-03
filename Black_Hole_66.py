import os
import random
import struct
import time
import paq

# Reverse chunks at specified positions with spacing
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, number_of_positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split into chunks  
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]  

    # Add padding if needed  
    if len(chunked_data[-1]) < chunk_size:  
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))  

    # Calculate positions with spacing between reversals  
    max_position = len(chunked_data)  # Number of chunks  
    positions = [i * (2**31) // max_position for i in range(number_of_positions)]  

    # Reverse specified chunks  
    for pos in positions:  
        if 0 <= pos < len(chunked_data):  
            chunked_data[pos] = chunked_data[pos][::-1]  

    # Write the reversed data to the output file  
    with open(reversed_filename, 'wb') as outfile:  
        outfile.write(b"".join(chunked_data))

# Encode data with leading zeros in 8-byte blocks
def encode_leading_zeros(data):
    encoded_data = bytearray()
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        leading_zeros = len(block) - len(block.lstrip(b'\x00'))
        encoded_data.append(leading_zeros)
        encoded_data.extend(block.lstrip(b'\x00'))
    return bytes(encoded_data)

# Decode data by adding back leading zeros
def decode_leading_zeros(encoded_data):
    decoded_data = bytearray()
    i = 0
    while i < len(encoded_data):
        leading_zeros = encoded_data[i]
        i += 1
        block = encoded_data[i:i + 8 - leading_zeros]
        decoded_data.extend(b'\x00' * leading_zeros)
        decoded_data.extend(block)
        i += len(block)
    return bytes(decoded_data)

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, original_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Encode leading zeros  
    reversed_data = encode_leading_zeros(reversed_data)  

    # Pack metadata (original_size, chunk_size, positions)  
    metadata = struct.pack(">Q", original_size)  # Store the original size  
    metadata += struct.pack(">I", chunk_size)  # Chunk size (as I for unsigned int)  
    metadata += struct.pack(">I", len(positions))  # Number of positions (as I for unsigned int)  
    metadata += struct.pack(f">{len(positions)}I", *positions)  # Positions (as a list of unsigned ints)  

    # Compress the file  
    compressed_data = paq.compress(metadata + reversed_data)  

    # Get the current compressed size  
    compressed_size = len(compressed_data)  

    # Save compressed file  
    with open(compressed_filename, 'wb') as outfile:  
        outfile.write(compressed_data)  

    return compressed_size

# Decompress and restore data (missing function)
def decompress_and_restore_paq(compressed_filename):
    # Check if the compressed file exists
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    with open(compressed_filename, 'rb') as infile:  
        compressed_data = infile.read()  

    # Decompress the data  
    decompressed_data = paq.decompress(compressed_data)  

    # Extract metadata  
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]  # Original size (from last compression)  
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]  # Chunk size  
    num_positions = struct.unpack(">I", decompressed_data[12:16])[0]  # Number of reversed positions  
    positions = list(struct.unpack(f">{num_positions}I", decompressed_data[16:16 + num_positions * 4]))  # Reversed positions  

    # Reconstruct chunks (data after metadata)  
    chunked_data = decompressed_data[16 + num_positions * 4:]  

    # Decode leading zeros  
    chunked_data = decode_leading_zeros(chunked_data)  

    # Reverse chunks back  
    total_chunks = len(chunked_data) // chunk_size  
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]  

    for pos in positions:  
        if 0 <= pos < len(chunked_data):  
            chunked_data[pos] = chunked_data[pos][::-1]  

    # Combine the chunks  
    restored_data = b"".join(chunked_data)  

    # Ensure the restored data is exactly the size of the original file (truncate or pad)  
    restored_data = restored_data[:original_size]  # Truncate to original size if needed  

    # Automatically generate the restored file name based on the compressed file name  
    restored_filename = compressed_filename.replace('.compressed.bin', '')  # Remove .compressed.bin extension  

    # Write the restored data to the file  
    with open(restored_filename, 'wb') as outfile:  
        outfile.write(restored_data)  

    # Compare the restored data with the original data  
    if restored_data == open(restored_filename, 'rb').read():  
        print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")  
        print(f"Restored file size matches the original size.")  
    else:  
        print("Decompression failed. The restored file does not match the original file.")

# Find the best chunk strategy and keep searching infinitely (for compression)
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_compression_ratio = float('inf')
    previous_size = 10**12  # Use a very large number to ensure first compression happens  
    best_compressed_filename = input_filename + ".compressed.bin"
    reversed_filename = f"{input_filename}.reversed.bin"

    positions = []  # Initially empty
    for chunk_size in range(1, 256):  # Modify the range to 1 to 256  
        max_positions = file_size // chunk_size  
        if max_positions > 0:  
            positions_count = random.randint(1, min(max_positions, 64))  
            positions = [i * (2**31) // file_size for i in range(positions_count)]  # Calculate positions  

            reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions_count)  

            compressed_size = compress_with_paq(reversed_filename, best_compressed_filename, chunk_size, positions, file_size)  

            # Track the best compression results
            if compressed_size < previous_size:
                previous_size = compressed_size
                best_compression_ratio = compressed_size / file_size
                print(f"Improved compression: {compressed_size} bytes, Compression ratio: {compressed_size / file_size:.4f}")

            print("Sleeping for 3 seconds...")  # Print message before sleeping
            time.sleep(3)  # Sleep for 3 seconds after each compression attempt

    return best_compressed_filename

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
        # Now user is prompted to enter the base name of the compressed file to extract  
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")  

        # Add the .compressed.bin extension to the input filename  
        compressed_filename = f"{compressed_filename_base}.compressed.bin"  

        # Check if the compressed file exists  
        if not os.path.exists(compressed_filename):  
            print(f"Error: Compressed file {compressed_filename} not found!")  
            return  

        # Perform the extraction (restoring) process  
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()