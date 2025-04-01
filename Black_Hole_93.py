import os
import random
import paq
from binascii import unhexlify

# 1. Reverse data in chunks
def reverse_chunk(data, chunk_size):
    return data[::-1]

# 2. Add random noise to data
def add_random_noise(data, noise_level=10):
    return bytes([b ^ random.randint(0, noise_level) for b in data])

# 3. Subtract 1 from each byte
def subtract_1_from_each_byte(data):
    return bytes([(b - 1) % 256 for b in data])

# 4. Rotate bits left
def move_bits_left(data, n):
    n = n % 8
    return bytes([((b << n) | (b >> (8 - n))) & 0xff for b in data])

# 5. Rotate bits right
def move_bits_right(data, n):
    n = n % 8
    return bytes([((b >> n) | (b << (8 - n))) & 0xff for b in data])

# 6. Apply random transformations
def apply_random_transforms(data, num_transforms=5):
    transforms = [
        lambda d: reverse_chunk(d, random.randint(1, len(d))),
        add_random_noise,
        subtract_1_from_each_byte,
        lambda d: move_bits_left(d, random.randint(1, 7)),
        lambda d: move_bits_right(d, random.randint(1, 7))
    ]
    for _ in range(num_transforms):
        data = random.choice(transforms)(data)
    return data

# 7. Compress using PAQ
def compress_data(data):
    return paq.compress(data)

# 8. Strict PAQ extraction
def extract_paq(data):
    try:
        return paq.decompress(data), "valid"
    except paq.PAQError as e:
        if "corrupt" in str(e).lower():
            return data, "corrupt"
        return data, "error"

# 9. Compression with multiple attempts
def compress_with_iterations(data, attempts, iterations):
    best = data
    best_size = len(data)
    
    for _ in range(attempts):
        current = data
        for _ in range(iterations):
            transformed = apply_random_transforms(current)
            compressed = compress_data(transformed)
            
            if len(compressed) < best_size:
                best = compressed
                best_size = len(compressed)
        current = best
    
    return best

# 10. Your exact extraction logic
def extract_data(data):
    PAQ_MAGIC = unhexlify('006300')
    
    if len(data) >= 3 and data[:3] == PAQ_MAGIC:
        result, status = extract_paq(data)
        if status == "valid":
            print("Valid PAQ archive - extracted successfully")
            return result
        print("Corrupt PAQ archive - returning original")
        return data
    
    print("No PAQ header found - returning original")
    return data

# 11. Display menu
def show_menu():
    print("\nFile Processor Menu:")
    print("1. Compress file")
    print("2. Extract file")
    print("3. Exit")
    while True:
        choice = input("Select option (1-3): ").strip()
        if choice in ('1', '2', '3'):
            return choice
        print("Invalid input, please try again")

# 12. Get file paths
def get_file_names():
    while True:
        input_file = input("Enter input file path: ").strip()
        if os.path.exists(input_file):
            break
        print("File not found! Please try again")
    return input_file, input("Enter output file path: ").strip()

# 13. Get compression parameters
def get_attempts_and_iterations():
    attempts = 1
    iterations = 7200*15
    return attempts, iterations

# 14. Read file with error handling
def read_file(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# 15. Write file with error handling
def write_file(filename, data):
    try:
        with open(filename, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

# 16. Compression workflow
def compression_pipeline(input_file, output_file, attempts, iterations):
    data = read_file(input_file)
    if not data:
        return False
    
    print("Compressing... (this may take a while)")
    compressed = compress_with_iterations(data, attempts, iterations)
    
    if write_file(output_file, compressed):
        orig_size = len(data)
        new_size = len(compressed)
        ratio = (1 - (new_size / orig_size)) * 100
        print(f"Success! Compression ratio: {ratio:.2f}%")
        return True
    return False

# 17. Extraction workflow
def extraction_pipeline(input_file, output_file):
    data = read_file(input_file)
    if not data:
        return False
    
    print("Extracting...")
    extracted = extract_data(data)
    
    if write_file(output_file, extracted):
        print("Extraction complete")
        return True
    return False

# 18. Main program
def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            input_file, output_file = get_file_names()
            attempts, iterations = get_attempts_and_iterations()
            if not compression_pipeline(input_file, output_file, attempts, iterations):
                print("Compression failed")
        
        elif choice == '2':
            input_file, output_file = get_file_names()
            if not extraction_pipeline(input_file, output_file):
                print("Extraction failed")
        
        elif choice == '3':
            print("Exiting program...")
            break

if __name__ == "__main__":
    main()