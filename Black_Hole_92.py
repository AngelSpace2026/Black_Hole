import os
import random
import paq

# Transformation functions (same as before)
def reverse_chunk(data, chunk_size):
    return data[::-1]

def add_random_noise(data, noise_level=10):
    return bytes([byte ^ random.randint(0, noise_level) for byte in data])

def subtract_1_from_each_byte(data):
    return bytes([(byte - 1) % 256 for byte in data])

def move_bits_left(data, n):
    n = n % 8
    return bytes([(byte << n) & 0xFF | (byte >> (8 - n)) & 0xFF for byte in data])

def move_bits_right(data, n):
    n = n % 8
    return bytes([(byte >> n) & 0xFF | (byte << (8 - n)) & 0xFF for byte in data])

# Always compress with PAQ after transformations
def apply_random_transforms(data, num_transforms=5):
    transforms = [reverse_chunk, add_random_noise, subtract_1_from_each_byte, 
                 move_bits_left, move_bits_right]
    for _ in range(num_transforms):
        transform = random.choice(transforms)
        if transform == reverse_chunk:
            data = transform(data, random.randint(1, len(data)))
        elif transform in [subtract_1_from_each_byte]:
            data = transform(data)
        else:
            data = transform(data, random.randint(1, 8))
    # Always compress with PAQ after transformations
    return paq.compress(data)

# Compression now always uses PAQ
def compress_data(data):
    return paq.compress(data)

# Decompression always uses PAQ
def decompress_data(data):
    return paq.decompress(data)

# Modified compression with iterations to always use PAQ
def compress_with_iterations(data, attempts, iterations):
    best_compressed = paq.compress(data)  # Start with straight PAQ compression
    best_size = len(best_compressed)
    
    for _ in range(attempts):
        current_data = data
        for _ in range(iterations):
            # Apply transforms and compress with PAQ
            transformed = apply_random_transforms(current_data)
            
            # Keep the best compression
            if len(transformed) < best_size:
                best_compressed = transformed
                best_size = len(best_compressed)
            
            # For next iteration, decompress to continue transforming
            current_data = paq.decompress(transformed)
    
    return best_compressed

# Extraction is just PAQ decompression
def extract_data(data):
    return paq.decompress(data)

# UI functions remain the same
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
    iterations = 7200
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