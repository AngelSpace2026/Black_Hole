import os
import random
import paq

# Transformation functions to potentially improve compression
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

def apply_random_transforms(data, num_transforms=5):
    transforms = [reverse_chunk, add_random_noise, subtract_1_from_each_byte, 
                 move_bits_left, move_bits_right]
    for _ in range(num_transforms):
        transform = random.choice(transforms)
        if transform == reverse_chunk:
            data = transform(data, random.randint(1, len(data)))
        elif transform in [add_random_noise, move_bits_left, move_bits_right]:
            data = transform(data, random.randint(1, 8))
        else:
            data = transform(data)
    return data

# PAQ-specific compression functions
def paq_compress(data):
    """Compress data using PAQ"""
    return paq.compress(data)  # Removed the level parameter

def paq_decompress(data):
    """Decompress data using PAQ"""
    return paq.decompress(data)

def optimize_with_paq(data, attempts=1, iterations=7200):
    """Try multiple transformation combinations with PAQ compression"""
    best_result = paq_compress(data)
    best_size = len(best_result)
    
    for _ in range(attempts):
        current_data = data
        for _ in range(iterations):
            transformed = apply_random_transforms(current_data)
            compressed = paq_compress(transformed)
            
            if len(compressed) < best_size:
                best_result = compressed
                best_size = len(best_result)
                
            current_data = compressed  # Try compressing the compressed data
            
    return best_result

# File operations
def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

# User interface
def show_menu():
    print("\nPAQ Compression Tool")
    print("1. Compress file (PAQ)")
    print("2. Decompress file (PAQ)")
    print("3. Exit")
    return input("Choose option (1-3): ")

def get_compression_params():
    attempts = 1
    iterations = 7200
    return attempts, iterations

def main():
    while True:
        choice = show_menu()
        
        if choice == '1':  # Compress
            in_file = input("Input file to compress: ")
            if not os.path.exists(in_file):
                print(f"Error: File '{in_file}' not found!")
                continue
                
            out_file = input("Output compressed file: ")
            attempts, iterations = get_compression_params()
            
            try:
                data = read_file(in_file)
                compressed = optimize_with_paq(data, attempts, iterations)
                write_file(out_file, compressed)
                
                orig_size = len(data)
                comp_size = len(compressed)
                ratio = (comp_size / orig_size) * 100
                
                print(f"\nCompression complete using PAQ")
                print(f"Original size: {orig_size} bytes")
                print(f"Compressed size: {comp_size} bytes")
                print(f"Ratio: {ratio:.2f}%")
            except Exception as e:
                print(f"Compression failed: {str(e)}")
            
        elif choice == '2':  # Decompress
            in_file = input("Input file to decompress: ")
            if not os.path.exists(in_file):
                print(f"Error: File '{in_file}' not found!")
                continue
                
            out_file = input("Output decompressed file: ")
            
            try:
                compressed = read_file(in_file)
                decompressed = paq_decompress(compressed)
                write_file(out_file, decompressed)
                
                print(f"\nDecompression complete using PAQ")
                print(f"File saved to {out_file}")
            except Exception as e:
                print(f"Decompression failed: {str(e)}")
            
        elif choice == '3':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()