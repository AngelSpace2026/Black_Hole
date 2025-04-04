import os
import paq

def rle_encode(data):
    if not data:
        return b""
    encoded = []
    count = 1
    prev_byte = data[0]
    for i in range(1, len(data)):
        if data[i] == prev_byte:
            count += 1
        else:
            encoded.append((prev_byte, count))
            prev_byte = data[i]
            count = 1
    encoded.append((prev_byte, count))
    result = b""
    for byte, count in encoded:
        result += byte.to_bytes(1, 'big') + count.to_bytes(2, 'big') # Use 2 bytes for count
    return result

def rle_decode(data):
    decoded = []
    i = 0
    while i < len(data):
        byte = data[i]
        count = int.from_bytes(data[i+1:i+3], 'big') # Read 2 bytes for count
        decoded.extend([byte] * count)
        i += 3 #Increment by 3 because count uses 2 bytes
    return bytes(decoded)

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

def apply_random_transformations(data, num_transforms=5):
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
            param = random.randint(1, 8) if transform != reverse_chunk else random.randint(1, len(data))
            try:
                data = transform(data, param)
            except Exception as e:
                print(f"Error applying transformation: {e}")
                return data  # Return original data if transformation fails.
        else:
            try:
                data = transform(data)
            except Exception as e:
                print(f"Error applying transformation: {e}")
                return data  # Return original data if transformation fails.
    return data

def compress_data(data):
    try:
        return paq.compress(data)
    except Exception as e:
        print(f"Error during PAQ compression: {e}")
        return data

def decompress_data(data):
    try:
        return paq.decompress(data)
    except Exception as e:
        print(f"Error during PAQ decompression: {e}")
        return data

def compress_with_iterations(data, attempts, iterations):
    best_compressed = paq.compress(data)
    best_size = len(best_compressed)

    for _ in range(attempts):
        current_data = data
        for _ in range(iterations):
            rle_encoded = rle_encode(current_data)
            compressed_data = paq.compress(rle_encoded) # Compress the RLE encoded data
            if len(compressed_data) < best_size:
                best_compressed = compressed_data
                best_size = len(compressed_data)
            current_data = rle_decode(paq.decompress(compressed_data)) # Decode before next iteration

    return best_compressed

def handle_file_io(func, file_name, data=None):
    try:
        if data is None:
            with open(file_name, 'rb') as f:
                return func(f.read())
        else:
            with open(file_name, 'wb') as f:
                f.write(data)
            return True
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"Error during file I/O: {e}")
        return None

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main():
    choice = input("Choose (1: Compress, 2: Extract): ")
    in_file, out_file = input("Input file: "), input("Output file: ")

    if choice == '1':
        attempts = 1
        iterations = 100
        data = handle_file_io(lambda x: x, in_file)
        if data:
            compressed_data = compress_with_iterations(data, attempts, iterations)
            handle_file_io(lambda x: x, out_file, compressed_data)
            print(f"Compressed to {out_file}")

    elif choice == '2':
        data = handle_file_io(decompress_data, in_file)
        if data:
            handle_file_io(lambda x: x, out_file, data)
            print(f"Extracted to {out_file}")

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
