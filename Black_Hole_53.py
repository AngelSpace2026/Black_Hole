import os
import paq
from mpmath import mp

print("Created by Jurijus Pacalovas.")
print("Black_Hole_53")

# Symbol and space mapping (5-bit representation)
symbol_map = {
    " ": 0b00001,
    ".": 0b00010,
    ",": 0b00011,
    "?": 0b00100,
    "!": 0b00101,
    "-": 0b00110,
    "'": 0b00111,
    '"': 0b01000,
    ":": 0b01001,
    ";": 0b01010,
    "(": 0b01011,
    ")": 0b01100,
    "[": 0b01101,
    "]": 0b01110,
    "{": 0b01111,
    "}": 0b10000,
    "/": 0b10001,
    "\\": 0b10010,
    "@": 0b10011,
    "#": 0b10100,
    "$": 0b10101,
    "%": 0b10110,
    "^": 0b10111,
    "&": 0b11000,
    "*": 0b11001,
    "+": 0b11010,
    "=": 0b11011,
    "<": 0b11100,
    ">": 0b11101,
    "|": 0b11110,
    "~": 0b11111
}

reverse_symbol_map = {v: k for k, v in symbol_map.items()}

# Generate digits of pi
def generate_pi_digits(digits):
    if digits < 1:
        raise ValueError("The number of digits must be at least 1.")
    mp.dps = digits + 1
    pi_value = str(mp.pi)[2:]
    return pi_value

# Reverse bits 2-15
def reverse_bits(byte):
    mask = 0b01111110
    relevant_bits = (byte & mask) >> 1
    reversed_bits = int('{:06b}'.format(relevant_bits)[::-1], 2)
    return (byte & ~mask) | (reversed_bits << 1)

def reverse_bits_in_data(data):
    return bytes(reverse_bits(byte) for byte in data)

# XOR encoding with Pi digits
def encode_with_pi(data, pi_digits):
    pi_sequence = [int(d) for d in pi_digits[:len(data)]]
    return bytes([b ^ p for b, p in zip(data, pi_sequence)])

# Convert binary to base 256
def binary_to_base256(binary_string):
    if len(binary_string) % 8 != 0:
        raise ValueError("The binary string length must be a multiple of 8.")
    
    byte_chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    base256_values = [int(chunk, 2) for chunk in byte_chunks]
    
    return base256_values

# Compress and encode using paq and binary to base 256
def compress_with_zlib_and_encode(input_filename, output_filename):
    try:
        # Open the input file and read data
        with open(input_filename, "rb") as infile:
            data = infile.read()

        # Compress data using paq
        compressed_data = paq.compress(data)

        # Convert binary data to base 256 (optional, may be useful for processing)
        binary_data = ''.join(format(byte, '08b') for byte in compressed_data)
        base256_values = binary_to_base256(binary_data)

        # Reverse bits of base256 values
        reversed_data = bytes(base256_values)

        # Generate Pi digits for encoding
        pi_digits = generate_pi_digits(len(reversed_data))

        # XOR encoding with Pi digits
        encoded_data = encode_with_pi(reversed_data, pi_digits)

        # Write encoded data to the output file
        with open(output_filename, "wb") as outfile:
            outfile.write(encoded_data)
            print(f"Compressed and encoded file saved to '{output_filename}'.")
    except Exception as e:
        print(f"An error occurred during compression: {e}")

# Decode and decompress using paq and binary to base 256
def decode_with_zlib_and_pi(input_filename, output_filename):
    try:
        # Read the encoded data
        with open(input_filename, "rb") as infile:
            encoded_data = infile.read()

        # Generate Pi digits for decoding
        pi_digits = generate_pi_digits(len(encoded_data))

        # XOR decoding with Pi digits
        decoded_data = encode_with_pi(encoded_data, pi_digits)

        # Convert binary data back from base256 to bytes
        binary_data = ''.join(format(byte, '08b') for byte in decoded_data)
        base256_values = binary_to_base256(binary_data)

        # Decompress data using paq
        decompressed_data = paq.decompress(bytes(base256_values))

        # Write decompressed data to the output file
        with open(output_filename, "wb") as outfile:
            outfile.write(decompressed_data)
            print(f"Extracted file saved to '{output_filename}'.")
    except Exception as e:
        print(f"An error occurred during extraction: {e}")

def main():
    print("Choose an option:")
    print("1. Compress a file")
    print("2. Decode a file")
    print("3. Exit")

    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == '1':
            input_file = input("Enter the name of the file to compress: ").strip()
            output_file = input_file + ".b"
            compress_with_zlib_and_encode(input_file, output_file)
        elif choice == '2':
            input_file = input("Enter the name of the file to extract: ").strip()
            output_file = input_file[:-2]
            decode_with_zlib_and_pi(input_file, output_file)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()