import paq
import json
import csv
import base64
from io import StringIO

print("Created by Jurijus Pacalovas.")

# Convert binary data to base-256 UTF-8 encoding
def encode_base256(data):
    return base64.b85encode(data).decode('utf-8')

# Decode base-256 UTF-8 back to binary
def decode_base256(data):
    return base64.b85decode(data.encode('utf-8'))

# Auto-detects data type and processes accordingly
def process_and_reverse(data):
    try:
        decoded_text = data.decode()
        
        # Try parsing JSON
        try:
            json_data = json.loads(decoded_text)
            if isinstance(json_data, dict):  # JSON Object
                reversed_data = json.dumps({k: v for k, v in reversed(json_data.items())}).encode()
            elif isinstance(json_data, list):  # JSON List
                reversed_data = json.dumps(json_data[::-1]).encode()
            else:
                reversed_data = decoded_text[::-1].encode()  # Fallback to string
        except json.JSONDecodeError:
            # Try CSV
            try:
                reader = csv.reader(StringIO(decoded_text), delimiter=',')
                data_rows = list(reader)
                reversed_rows = data_rows[::-1]
                output = StringIO()
                csv.writer(output).writerows(reversed_rows)
                reversed_data = output.getvalue().encode()
            except csv.Error:
                # Fallback to string processing
                reversed_data = decoded_text[::-1].encode()
    
    except UnicodeDecodeError:
        # Process as binary
        reversed_data = data[::-1]

    return reversed_data

# Compression and Reversal
def compress_and_reverse(input_filename, output_filename, base256):
    try:
        with open(input_filename, 'rb') as infile:
            data = infile.read()

        reversed_data = process_and_reverse(data)
        compressed_data = paq.compress(reversed_data)

        if base256:
            compressed_data = encode_base256(compressed_data).encode()

        with open(output_filename, 'wb') as outfile:
            outfile.write(compressed_data)

        print(f"File '{input_filename}' compressed and reversed to '{output_filename}'.")
        return 0

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

# Decompression and Restoration
def decompress_and_restore(input_filename, output_filename, base256):
    try:
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()

        if base256:
            compressed_data = decode_base256(compressed_data.decode())

        decompressed_data = paq.decompress(compressed_data)
        restored_data = process_and_reverse(decompressed_data)  # Reverse again to restore

        with open(output_filename, 'wb') as outfile:
            outfile.write(restored_data)

        print(f"File '{input_filename}' decompressed and restored to '{output_filename}'.")
        return 0

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

# Interactive user input
if __name__ == "__main__":
    mode = input("Enter mode (compress/extract): ").strip().lower()
    input_file = input("Enter input file name: ").strip()
    output_file = input("Enter output file name: ").strip()
    
    base256_choice = input("Use Base-256 encoding? (yes/no): ").strip().lower()
    base256 = base256_choice in ["yes", "y"]

    if mode == "compress":
        compress_and_reverse(input_file, output_file, base256)
    elif mode == "extract":
        decompress_and_restore(input_file, output_file, base256)
    else:
        print("Invalid mode selected.")