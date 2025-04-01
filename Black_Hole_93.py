import os
import random
import paq

# Function 1: Reverse data in chunks
def reverse_chunk(data, chunk_size):
    return data[::-1]

# Function 2: Add random noise to data
def add_random_noise(data, noise_level=10):
    return bytes([byte ^ random.randint(0, noise_level) for byte in data])

# Function 3: Subtract 1 from each byte
def subtract_1_from_each_byte(data):
    return bytes([(byte - 1) % 256 for byte in data])

# Function 4: Move bits left (rotate)
def move_bits_left(data, n):
    n = n % 8  # Ensure n is within the range of 0 to 7
    return bytes([(byte << n) & 0xFF | (byte >> (8 - n)) & 0xFF for byte in data])

# Function 5: Move bits right (rotate)
def move_bits_right(data, n):
    n = n % 8  # Ensure n is within the range of 0 to 7
    return bytes([(byte >> n) & 0xFF | (byte << (8 - n)) & 0xFF for byte in data])

# Function 6: Apply random transformations
def apply_random_transforms(data, num_transforms=5):
    transforms = [reverse_chunk, add_random_noise, subtract_1_from_each_byte, move_bits_left, move_bits_right]
    for _ in range(num_transforms):
        transform = random.choice(transforms)
        if transform == reverse_chunk:  # For reverse_chunk, we need a chunk_size argument
            chunk_size = random.randint(1, len(data))  # Random chunk size
            data = transform(data, chunk_size)
        elif transform in [subtract_1_from_each_byte]:  # These do not need an extra argument
            data = transform(data)
        else:  # These transformations require a random shift value
            data = transform(data, random.randint(1, 8))
    return data

# Function 7: Compress data using zlib
def compress_data(data):
    return paq.compress(data)

# Function 8: Decompress data using zlib
def decompress_data(data):
    return paq.decompress(data)

# Function 9: Run compression with multiple attempts and iterations
def compress_with_iterations(data, attempts, iterations):
    best_compressed = data
    best_size = len(data)
    
    for _ in range(attempts):
        for _ in range(iterations):
            transformed_data = apply_random_transforms(data)
            compressed_data = compress_data(transformed_data)
            
            if len(compressed_data) < best_size:
                best_compressed = compressed_data
                best_size = len(compressed_data)
    
    return best_compressed

# Function 10: Extract compressed data with 006300 check
def extract_data(data):
    # Check if first 3 bytes are 0x00, 0x63, 0x00
    if len(data) >= 3 and data[:3] == b'\x00\x63\x00':
        try:
            # Try to decompress with paq
            return decompress_data(data)
        except:
            # If decompression fails, return original
            return data
    else:
        # If first 3 bytes don't match, return original
        return data

# Function 11: Show the user a menu for compressing or extracting
def show_menu():
    print("Select operation:")
    print("1. Compress")
    print("2. Extract")
    return input("Enter 1 for compression or 2 for extraction: ")

# Function 12: Get user input for file names
def get_file_names():
    input_file = input("Enter input file name: ")
    output_file = input("Enter output file name: ")
    return input_file, output_file

# Function 13: Get user input for number of attempts and iterations
def get_attempts_and_iterations():
    attempts = 1
    iterations = 7200*15
    return attempts, iterations

# Function 14: Read file
def read_file(file_name):
    with open(file_name, 'rb') as f:
        return f.read()

# Function 15: Write file
def write_file(file_name, data):
    with open(file_name, 'wb') as f:
        f.write(data)

# Function 16: Compression pipeline
def compression_pipeline(input_file, output_file, attempts, iterations):
    data = read_file(input_file)
    best_compressed = compress_with_iterations(data, attempts, iterations)
    write_file(output_file, best_compressed)
    print(f"File compressed and saved as {output_file}")

# Function 17: Extraction pipeline
def extraction_pipeline(input_file, output_file):
    compressed_data = read_file(input_file)
    extracted_data = extract_data(compressed_data)
    write_file(output_file, extracted_data)
    print(f"File extracted and saved as {output_file}")

# Function 18: Main function for user interface
def main():
    operation = show_menu()
    input_file, output_file = get_file_names()
    
    if operation == '1':  # Compress
        attempts, iterations = get_attempts_and_iterations()
        compression_pipeline(input_file, output_file, attempts, iterations)
    elif operation == '2':  # Extract
        extraction_pipeline(input_file, output_file)
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()