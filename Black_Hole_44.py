import os
import struct
import paq

# Compress file using PAQ without reversing
def compress_with_paq(input_filename):
    with open(input_filename, 'rb') as infile:
        original_data = infile.read()

    original_size = len(original_data)

    # Pack metadata: original file size (8 bytes)
    metadata = struct.pack(">Q", original_size)  

    compressed_data = paq.compress(metadata + original_data)

    compressed_filename = f"{input_filename}.compressed.bin"

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

    print(f"Compressed file saved as: {os.path.abspath(compressed_filename)}")

# Decompress and restore data
def decompress_with_paq(compressed_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    decompressed_data = paq.decompress(compressed_data)

    original_size = struct.unpack(">Q", decompressed_data[:8])[0]  # Extract original file size
    restored_data = decompressed_data[8:8 + original_size]  # Extract original content

    # Remove .compressed.bin from filename
    if compressed_filename.endswith(".compressed.bin"):
        restored_filename = compressed_filename.replace(".compressed.bin", "")
    else:
        restored_filename = compressed_filename + ".restored"

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

    print(f"File extracted to: {os.path.abspath(restored_filename)}")

# Main function
def main():
    print("Created by Jurijus Pacalovas.")

    mode = int(input("Enter mode (1 for compress, 2 for extract): "))

    if mode == 1:
        input_filename = input("Enter input file name to compress: ")
        compress_with_paq(input_filename)

    elif mode == 2:
        compressed_filename = input("Enter compressed file name to extract: ")
        decompress_with_paq(compressed_filename)

if __name__ == "__main__":
    main()