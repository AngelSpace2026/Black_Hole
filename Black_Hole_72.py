import os
import random
import struct
import paq

# Apply the "minus bytes" operation to handle leading zeros or chunks
def apply_minus_operation(value, file_size):
    """ This function applies a minus operation to values based on leading zeros or chunk size. """
    if value <= 0:
        return value + (2**file_size - 1)  # Adjust for file size instead of large numbers
    elif value <= (2**24 - 1):  # Adjust for values within a 3-byte range
        return value + 3
    else:  # For values greater than 255
        return value + 1

# Function to manage leading zeros in the input byte data
def manage_leading_zeros(input_data):
    """ This function processes the input byte data to handle leading zeros and minimize byte usage. """
    if not isinstance(input_data, bytes):
        raise ValueError("Input data must be of type 'bytes'")
    
    # Strip leading zeros
    stripped_data = input_data.lstrip(b'\x00')
    
    # If all data is zero, just keep one byte
    if not stripped_data:
        stripped_data = b'\x00'  
    
    # Count leading zeros in bytes
    leading_zeros = 0
    for byte in stripped_data:
        if byte == 0:
            leading_zeros += 8  # Each zero byte adds 8 bits of leading zeros
        elif byte == 255:
            leading_zeros += 8  # Treat bytes full of 1s as leading ones to reverse
        else:
            # Handle partial byte of leading zeros
            leading_zeros += (8 - len(bin(byte)) + bin(byte).index('1') - 2) if byte != 0 else 0

    # Return data and count of leading zeros for debugging
    print(f"Leading zeros count: {leading_zeros} bits")
    return stripped_data, leading_zeros

# Reverse chunks at specified positions with spacing
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, number_of_positions, file_size):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    # Split into chunks
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Add padding if needed
    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

    # Randomly select positions between 1 and 2**31
    positions = [random.randint(1, 2**31) for _ in range(number_of_positions)]  # Random positions from 1 to 2^31

    # Reverse specified chunks at random positions
    for pos in positions:
        if pos < len(chunked_data):  # Ensure the position is valid within the number of chunks
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

# Find the best chunk strategy and run 255 iterations for improving compression
def find_best_strategy(input_filename):
    file_size = os.path.getsize(input_filename)  # Get file size
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')
    best_count = 0

    previous_size = 10**12  # Use a very large number to ensure first compression happens
    first_attempt = True  # Flag to track if it's the first attempt

    for iteration in range(255):  # Perform a fixed number of iterations (255 iterations)
        max_chunk_size = min(file_size, 2**24 - 1)

        if max_chunk_size < 1:
            print("Error: File is too small to compress.")
            return

        # Randomly choose a chunk size from 1 to 24, ensuring it's never larger than the file size
        chunk_size = random.randint(1, min(2**24 - 1, file_size))  # Choose chunk size within valid range

        print(f"Iteration {iteration + 1}: Trying chunk size: {chunk_size}")  # Debugging output for chunk size

        max_positions = file_size // chunk_size
        if max_positions > 0:
            positions_count = random.randint(1, min(max_positions, 64))

            # Generate random positions between 1 and 2^31
            positions = [random.randint(1, 2**31) for _ in range(positions_count)]  # Random positions from 1 to 2^31

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

    # Reverse the chunks at the specified positions
    chunked_data = [reversed_data[i:i + chunk_size] for i in range(0, len(reversed_data), chunk_size)]

    # Reverse back the chunks at the positions
    for pos in positions:
        if pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

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
            print("Error: Invalid input. Please enter 1 for compress or 2 for extract.")
    
    if mode == 1:
        input_filename = input("Enter the filename to compress: ")
        find_best_strategy(input_filename)
    elif mode == 2:
        compressed_filename = input("Enter the base name of the compressed file to extract (without .compressed.bin): ")
        decompress_and_restore_paq(compressed_filename + ".compressed.bin")

if __name__ == "__main__":
    main()