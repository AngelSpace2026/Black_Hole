import os
import random
import struct
import paq

# Apply the minus operation for modifying values
def apply_minus_operation(value):
    """
    This function modifies the given value by adding a specific number of bytes 
    depending on its size, as part of the compression transformation process.
    """
    if value <= 0:
        # If the value is less than or equal to 0, wrap it around to the maximum possible value (2^255 - 1)
        return value + (2**255 - 1)
    elif value <= (2**24 - 1):
        # If the value is within the range of 3 bytes, add 3 bytes (represented by adding 3 to the value)
        return value + 3
    else:
        # If the value is larger than 2^24 - 1, add 1 byte (represented by adding 1 to the value)
        return value + 1

# Reverse chunks at specified positions
def reverse_chunks(input_filename, reversed_filename, chunk_size, num_reversals, num_sets):
    """
    This function reads the input file, splits the data into chunks, and performs
    multiple reversals on the chunks at random positions, which are then saved 
    to the output file.
    """
    with open(input_filename, 'rb') as infile:
        # Read the file content into memory
        data = infile.read()

    # Split data into chunks of the specified chunk size
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    # If the last chunk is smaller than the chunk size, pad it with zero bytes
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

    total_chunks = len(chunked_data)

    # Perform a number of random reversals of the chunks
    for _ in range(num_reversals):
        if total_chunks > 1:
            positions = [random.randint(0, total_chunks - 1) for _ in range(min(num_sets, total_chunks))]
            for pos in positions:
                # Reverse the chunks at the chosen positions
                chunked_data[pos] = chunked_data[pos][::-1]

    # Write the reversed data back to the output file
    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using PAQ
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, num_reversals, num_sets, prev_size, original_size, first_attempt):
    """
    This function compresses the file using PAQ, with additional metadata based on 
    the chunking and reversal parameters. It also applies the minus operation for 
    modifying values to help with compression.
    """
    with open(reversed_filename, 'rb') as infile:
        # Read the reversed file data into memory
        reversed_data = infile.read()

    # Create metadata from the original file size, chunk size, number of reversals, and number of sets
    metadata = struct.pack(">Q", original_size)  # Pack the original file size as an 8-byte unsigned long long
    metadata += struct.pack(">I", chunk_size)   # Pack the chunk size as a 4-byte unsigned integer
    metadata += struct.pack(">I", num_reversals) # Pack the number of reversals as a 4-byte unsigned integer
    metadata += struct.pack(">I", num_sets)      # Pack the number of sets as a 4-byte unsigned integer

    # Apply the minus operation to modify the length of the metadata
    new_metadata_len = apply_minus_operation(len(metadata))
    metadata = metadata[:new_metadata_len]  # Truncate the metadata based on the modified length

    # Compress the data using PAQ, combining metadata and reversed data
    compressed_data = paq.compress(metadata + reversed_data)
    compressed_size = len(compressed_data)

    if first_attempt:
        # If this is the first attempt, save the compressed file
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        return compressed_size, False
    elif compressed_size < prev_size:
        # If the compressed size is smaller than the previous size, save the new compressed file
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        print(f"Improved compression! Size: {compressed_size} bytes. Ratio: {compressed_size / original_size:.4f}")
        return compressed_size, False
    else:
        return prev_size, False

# Decompress and restore
def decompress_and_restore_paq(compressed_filename):
    """
    This function decompresses a PAQ-compressed file, extracts the metadata, 
    and restores the original file by performing the inverse of the chunk reversals.
    """
    if not os.path.exists(compressed_filename):
        raise FileNotFoundError(f"Compressed file not found: {compressed_filename}")

    with open(compressed_filename, 'rb') as infile:
        # Read the compressed data
        compressed_data = infile.read()

    # Decompress the data using PAQ
    decompressed_data = paq.decompress(compressed_data)

    # Extract the metadata (original file size, chunk size, number of reversals, and number of sets)
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]
    num_reversals = struct.unpack(">I", decompressed_data[12:16])[0]
    num_sets = struct.unpack(">I", decompressed_data[16:20])[0]

    # The rest of the data contains the chunked data
    chunked_data = decompressed_data[20:]

    # Ensure chunk size is not greater than the remaining data
    chunk_size = min(chunk_size, len(chunked_data))
    total_chunks = max(1, len(chunked_data) // chunk_size)
    
    # Split the chunked data into individual chunks
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    # Reverse the chunks at random positions based on the number of reversals and sets
    for _ in range(num_reversals):
        if total_chunks > 1:
            positions = [random.randint(0, total_chunks - 1) for _ in range(min(num_sets, total_chunks))]
            for pos in positions:
                chunked_data[pos] = chunked_data[pos][::-1]

    # Concatenate the chunks back together
    restored_data = b"".join(chunked_data)[:original_size]

    # Generate the restored filename by removing the '.compressed.bin' extension
    restored_filename = compressed_filename.replace('.compressed.bin', '')

    # Write the restored data back to the file
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompression complete. Restored file size: {len(restored_data)} bytes")

# Find best chunk strategy (10,000 iterations)
def find_best_chunk_strategy(input_filename):
    """
    This function iteratively tests different chunk strategies (e.g., chunk sizes, 
    number of reversals, and number of sets) and selects the best compression strategy 
    based on file size.
    """
    file_size = os.path.getsize(input_filename)
    best_compression_ratio = float('inf')

    prev_size = 10**12  # Initial value for the best compression size
    first_attempt = True

    # Run 10,000 iterations to find the best compression strategy
    for iteration in range(1, 10_001):
        for chunk_size in range(1, 256):
            # Calculate the maximum number of positions that can fit within the chunk size
            max_positions = file_size // chunk_size
            if max_positions > 0:
                # Randomly select the number of reversals and sets for this iteration
                num_reversals = random.randint(1, 64)
                num_sets = random.randint(1, min(max_positions, 64))

                # Reverse the chunks and generate a filename for the reversed data
                reversed_filename = f"{input_filename}.reversed.bin"
                reverse_chunks(input_filename, reversed_filename, chunk_size, num_reversals, num_sets)

                # Compress the reversed chunks and get the compressed file size
                compressed_filename = f"{input_filename}.compressed.bin"
                compressed_size, first_attempt = compress_with_paq(reversed_filename, compressed_filename, chunk_size, num_reversals, num_sets, prev_size, file_size, first_attempt)

                if compressed_size < prev_size:
                    # Update the best compression result if this iteration produces a better size
                    prev_size = compressed_size
                    best_compression_ratio = compressed_size / file_size
                    print(f"Iteration {iteration}: New best compression: {compressed_size} bytes. Ratio: {best_compression_ratio:.4f}")

        # Report progress every 1000 iterations
        if iteration % 1000 == 0:
            print(f"Progress: {iteration}/10,000 iterations completed.")

# Main function
def main():
    """
    The main function provides a user interface to either compress or decompress files.
    It uses the find_best_chunk_strategy function to find the optimal compression strategy.
    """
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
        # Find the best compression strategy for the input file
        find_best_chunk_strategy(input_filename)
    elif mode == 2:
        compressed_filename_base = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{compressed_filename_base}.compressed.bin"

        if not os.path.exists(compressed_filename):
            print(f"Error: Compressed file {compressed_filename} not found!")
            return

        # Decompress and restore the file from the compressed data
        decompress_and_restore_paq(compressed_filename)

# Run the main function
if __name__ == "__main__":
    main()