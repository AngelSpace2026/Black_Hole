import os
import random
import struct
import paq

# Apply the minus operation for modifying values
def apply_minus_operation(value, file_size):
    if value <= 0:
        return value + (2**file_size - 1)  # Use file_size instead of 2**255
    elif value <= (2**24 - 1):  # Add 3 bytes if the value is within the range -2**24+1 to -1
        return value + 3
    else:  # Add 1 byte for values within the range 1 - 255
        return value + 1

# Manage leading zeros and ones and minimize byte usage
def manage_leading_zeros(input_data):
    """ This function processes the input byte data to handle leading zeros and ones."""
    if not isinstance(input_data, bytes):
        raise ValueError("Input data must be of type 'bytes'")
    
    # Strip leading zeros
    stripped_data = input_data.lstrip(b'\x00')  
    
    # If the stripped data is empty (i.e., all were zeros), keep a single byte
    if not stripped_data:
        stripped_data = b'\x00'    
    
    # Count leading zeros and ones (0xFF)
    leading_zeros = 0
    leading_ones = 0
    for byte in stripped_data:
        if byte == 0:
            leading_zeros += 8
        elif byte == 255:
            leading_ones += 8
        else:
            # Calculate number of leading zeros in the current byte
            leading_zeros += (8 - len(bin(byte)) + bin(byte).index('1') - 2) if byte != 0 else 0
    
    print(f"Leading zeros count: {leading_zeros} bits")
    print(f"Leading ones count: {leading_ones} bits")

    # Replace leading zeros and ones with a single byte for efficient compression
    if leading_zeros > 8:
        stripped_data = b'\x00' + stripped_data[1:]
    if leading_ones > 8:
        stripped_data = b'\xFF' + stripped_data[1:]

    # Return processed data
    return stripped_data

# Reverse chunks at specified positions with spacing
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, number_of_positions, file_size):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Add padding if needed
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

    # Calculate positions with spacing between reversals, using file_size instead of 2**255
    max_position = len(chunked_data)  # Number of chunks
    positions = [random.randint(1, 2**31) for _ in range(number_of_positions)]  # Random positions between 1 and 2^31

    # Reverse specified chunks
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using PAQ with metadata
def compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, original_size, first_attempt, file_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    # Pack metadata
    metadata = struct.pack(">Q", original_size)  # Store the original size
    metadata += struct.pack(">I", chunk_size)  # Chunk size
    metadata += struct.pack(">I", len(positions))  # Number of positions
    metadata += struct.pack(f">{len(positions)}I", *positions)  # Positions

    # Apply the "minus" operation to metadata values
    new_metadata_len = apply_minus_operation(len(metadata), file_size)  # Modify the metadata length
    metadata = metadata[:new_metadata_len]  # Slice the metadata to the modified length

    # Compress the file
    compressed_data = paq.compress(metadata + reversed_data)

    # Get the current compressed size
    compressed_size = len(compressed_data)

    if first_attempt:
        # First attempt always overwrites
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        first_attempt = False
        return compressed_size, first_attempt
    elif compressed_size < previous_size:
        # Save only if compression is better and print improvement message
        with open(compressed_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        previous_size = compressed_size
        print(f"Improved compression with chunk size {chunk_size} and {len(positions)} reversed positions.")
        print(f"Compression size: {compressed_size} bytes, Compression ratio: {compressed_size / original_size:.4f}")
        return previous_size, first_attempt
    else:
        return previous_size, first_attempt  # Do not overwrite if it's larger

# Find the best chunk strategy and keep searching infinitely (for compression)
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)  # Get file size
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')
    best_count = 0

    previous_size = 10**12  # Use a very large number to ensure first compression happens
    first_attempt = True  # Flag to track if it's the first attempt

    while True:  # Infinite loop to keep improving
        for chunk_size in range(1, 256):  # Modify the range to 1 to 256
            print(f"Trying chunk size: {chunk_size}")  # Debugging output for chunk size
            max_positions = file_size // chunk_size
            if max_positions > 0:
                positions_count = random.randint(1, min(max_positions, 64))

                # Calculate positions with spacing between reversals, using file_size instead of 2**255
                positions = [random.randint(1, 2**31) for _ in range(positions_count)]

                print(f"Positions selected: {positions}")  # Debugging output for positions

                reversed_filename = f"{input_filename}.reversed.bin"
                reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions_count, file_size)

                compressed_filename = f"{input_filename}.compressed.bin"
                compressed_size, first_attempt = compress_with_paq(reversed_filename, compressed_filename, chunk_size, positions, previous_size, file_size, first_attempt, file_size)

                if compressed_size < previous_size:
                    # Update the best values when a better compression ratio is found
                    previous_size = compressed_size
                    best_chunk_size = chunk_size
                    best_positions = positions
                    best_compression_ratio = compressed_size / file_size
                    best_count += 1

                    # Print improved compression details
                    print(f"Improved compression with chunk size {chunk_size} and {len(positions)} reversed positions.")
                    print(f"Compression size: {compressed_size} bytes, Compression ratio: {compressed_size / file_size:.4f}")

# Decompress and restore PAQ compressed file
def decompress_and_restore_paq(compressed_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    # Decompress using PAQ
    decompressed_data = paq.decompress(compressed_data)

    # Extract metadata
    original_size = struct.unpack(">Q", decompressed_data[:8])[0]
    chunk_size = struct.unpack(">I", decompressed_data[8:12])[0]
    positions_count = struct.unpack(">I", decompressed_data[12:16])[0]
    positions = list(struct.unpack(f">{positions_count}I", decompressed_data[16:16 + positions_count * 4]))

    # Extract the reversed data
    reversed_data = decompressed_data[16 + positions_count * 4:]

    # Split the data into chunks
    chunked_data = [reversed_data[i:i + chunk_size] for i in range(0, len(reversed_data), chunk_size)]

    # Reverse back the chunks at the positions
    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]  # Reverse the chunk

    # Restore the original data by joining the chunks
    restored_data = b"".join(chunked_data)

    # Trim any padding if the restored data is longer than the original size
    if len(restored_data) > original_size:
        restored_data = restored_data[:original_size]

    # Ensure the restored data matches the original size
    if len(restored_data) != original_size:
        raise ValueError(f"Restored data size ({len(restored_data)}) does not match original size ({original_size}).")

    # Write the restored data to a file
    restored_filename = compressed_filename.replace(".compressed.bin", "")
    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"Decompression and restoration complete. Restored file saved as: {restored_filename}")

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
        input_filename = input("Enter input filename (with extension): ")
        find_best_chunk_strategy(input_filename)
    elif mode == 2:
        input_filename = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        compressed_filename = f"{input_filename}.compressed.bin"
        decompress_and_restore_paq(compressed_filename)

if __name__ == "__main__":
    main()
        
        