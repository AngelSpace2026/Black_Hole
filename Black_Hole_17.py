import paq
import os

print("Created by Jurijus Pacalovas.")

CHUNK_SIZE = 2**28  # Reverse data in chunks of 268,435,456 bytes (256 MB)

# Step 1: Reverse and save
def reverse_and_save(input_filename, reversed_filename):
    try:
        with open(input_filename, 'rb') as infile, open(reversed_filename, 'wb') as outfile:
            while chunk := infile.read(CHUNK_SIZE):
                outfile.write(chunk[::-1])  # Reverse the chunk before writing

        print(f"✅ File '{input_filename}' reversed and saved as '{reversed_filename}'.")
    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Step 2: Compress the reversed file
def compress_reversed(reversed_filename, compressed_filename):
    try:
        with open(reversed_filename, 'rb') as infile, open(compressed_filename, 'wb') as outfile:
            compressed_data = paq.compress(infile.read())  # Compress entire reversed file
            outfile.write(compressed_data)

        print(f"✅ Reversed file '{reversed_filename}' compressed into '{compressed_filename}'.")
    except FileNotFoundError:
        print(f"❌ Error: Input file '{reversed_filename}' not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Step 3: Decompress and restore the original file
def decompress_and_restore(compressed_filename, restored_filename):
    try:
        with open(compressed_filename, 'rb') as infile:
            compressed_data = infile.read()
        
        try:
            decompressed_data = paq.decompress(compressed_data)  # Try decompression
        except paq.error as e:
            print(f"❌ Error: The file '{compressed_filename}' is not a valid zlib-compressed file. ({e})")
            return
        
        # Reverse again in 268,435,456-byte chunks to restore the original order
        restored_data = b"".join([decompressed_data[i:i+CHUNK_SIZE][::-1] 
                                  for i in range(0, len(decompressed_data), CHUNK_SIZE)])
        
        with open(restored_filename, 'wb') as outfile:
            outfile.write(restored_data)

        print(f"✅ Compressed file '{compressed_filename}' decompressed and restored as '{restored_filename}'.")
    except FileNotFoundError:
        print(f"❌ Error: Input file '{compressed_filename}' not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Interactive user input
if __name__ == "__main__":
    mode = input("Enter mode (reverse-compress/extract): ").strip().lower()
    input_file = input("Enter input file name: ").strip()

    if mode == "reverse-compress":
        reversed_file = input_file + ".rev"  # Output file for reversed data
        compressed_file = input_file + ".b"  # Output file for compressed data

        reverse_and_save(input_file, reversed_file)  # Step 1: Reverse and Save
        compress_reversed(reversed_file, compressed_file)  # Step 2: Compress Reversed File

    elif mode == "extract":
        compressed_file = input_file + ".b"  # Input file for compressed data
        restored_file = input_file[:-2]  # Output file for restored data (removes .zip extension)

        decompress_and_restore(compressed_file, restored_file)  # Step 3: Decompress and Restore

    else:
        print("❌ Invalid mode selected.")
