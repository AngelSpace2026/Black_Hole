import os
import random
import paq  # Ensure you have a compatible PAQ module

# Transformation functions

def reverse_chunk(data, chunk_size):
    return data[::-1]

def add_random_noise(data, noise_level=10):
    return bytes([byte ^ random.randint(0, noise_level) for byte in data])

def subtract_1_from_each_byte(data):
    return bytes([(byte - 1) % 256 for byte in data])

def move_bits_left(data, n):
    n = n % 8
    return bytes([(byte << n & 0xFF) | (byte >> (8 - n)) & 0xFF for byte in data])

def move_bits_right(data, n):
    n = n % 8
    return bytes([(byte >> n & 0xFF) | (byte << (8 - n)) & 0xFF for byte in data])

# Apply random transformations
def apply_random_transforms(data, num_transforms=5):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True)
    ]
    
    for _ in range(num_transforms):
        transform, needs_param = random.choice(transforms)
        if needs_param:
            if transform == reverse_chunk:
                param = random.randint(1, len(data))
            else:
                param = random.randint(1, 8)
            data = transform(data, param)
        else:
            data = transform(data)
    
    return paq.compress(data)

# Compression using PAQ
def compress_data(data):
    return paq.compress(data)

# Decompression using PAQ
def decompress_data(data):
    return paq.decompress(data)

# Iterative compression with best result selection
def compress_with_iterations(data, attempts, iterations):
    best_compressed = paq.compress(data)
    best_size = len(best_compressed)

    for _ in range(attempts):
        current_data = data
        for _ in range(iterations):
            transformed = apply_random_transforms(current_data)
            if len(transformed) < best_size:
                best_compressed = transformed
                best_size = len(best_compressed)
            current_data = paq.decompress(transformed)
    
    return best_compressed

# Extraction
def extract_data(data):
    return paq.decompress(data)

# UI functions
def show_menu():
    print("1. Compress")
    print("2. Extract")
    return input("Choose (1/2): ")

def get_file_names():
    input_file = input("Input file: ")
    output_file = input("Output file: ")
    return input_file, output_file

def get_attempts_and_iterations():
    attempts = 1
    iterations = 7200*15
    return attempts, iterations

def read_file(file_name):
    with open(file_name, 'rb') as f:
        return f.read()

def write_file(file_name, data):
    with open(file_name, 'wb') as f:
        f.write(data)

def compression_pipeline(input_file, output_file, attempts, iterations):
    data = read_file(input_file)
    compressed = compress_with_iterations(data, attempts, iterations)
    write_file(output_file, compressed)
    print(f"Compressed to {output_file}")

def extraction_pipeline(input_file, output_file):
    data = read_file(input_file)
    extracted = extract_data(data)
    write_file(output_file, extracted)
    print(f"Extracted to {output_file}")

def main():
    choice = show_menu()
    in_file, out_file = get_file_names()
    if choice == '1':
        attempts, iterations = get_attempts_and_iterations()
        compression_pipeline(in_file, out_file, attempts, iterations)
    elif choice == '2':
        extraction_pipeline(in_file, out_file)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()