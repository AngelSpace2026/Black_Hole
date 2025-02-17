import paq

CHUNK_SIZE = 8191  # Set the chunk size to 8191 bytes

def reverse_and_compress(input_filename, output_filename):
    try:
        with open(input_filename, 'rb') as infile, open(output_filename, 'wb') as outfile:
            while chunk := infile.read(CHUNK_SIZE):
                reversed_chunk = chunk[::-1]  # Reverse the 8191-byte chunk
                compressed_chunk = paq.compress(reversed_chunk)
                outfile.write(compressed_chunk)
        
        print(f"File '{input_filename}' compressed with reversed 8191-byte chunks into '{output_filename}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decompress_and_restore(input_filename, output_filename):
    try:
        with open(input_filename, 'rb') as infile, open(output_filename, 'wb') as outfile:
            while compressed_chunk := infile.read():
                decompressed_chunk = paq.decompress(compressed_chunk)
                restored_chunk = decompressed_chunk[::-1]  # Reverse again to restore original
                outfile.write(restored_chunk)
        
        print(f"File '{input_filename}' decompressed and restored into '{output_filename}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Interactive user input
if __name__ == "__main__":
    mode = input("Enter mode (compress/extract): ").strip().lower()
    input_file = input("Enter input file name: ").strip()
    output_file = input("Enter output file name: ").strip()

    if mode == "compress":
        reverse_and_compress(input_file, output_file)
    elif mode == "extract":
        decompress_and_restore(input_file, output_file)
    else:
        print("Invalid mode selected.")