import os
import random
import math
import warnings
import paq
from enum import Enum, auto

# ===== Physical Constants =====
C = 299792458.0          # Speed of light (m/s)
G = 6.67430e-11          # Gravitational constant
HBAR = 1.054571817e-34   # Reduced Planck constant
K_B = 1.380649e-23       # Boltzmann constant
M_P = 1.67262192369e-27  # Proton mass (kg)

# Derived Planck units
PLANCK_LENGTH = math.sqrt(HBAR * G / C**3)

# ===== Practical Compression System =====
def reverse_chunk(data):
    return data[::-1]

def add_random_noise(data, noise_level=10):
    return bytes(b ^ random.randint(0, noise_level) for b in data)

def subtract_1_from_each_byte(data):
    return bytes((b - 1) % 256 for b in data)

def move_bits_left(data, n):
    n = n % 8
    return bytes(((b << n) & 0xFF) | (b >> (8 - n)) for b in data)

def move_bits_right(data, n):
    n = n % 8
    return bytes((b >> n) | ((b << (8 - n)) & 0xFF) for b in data)

def apply_random_transforms(data, num_transforms=5):
    transforms = [
        reverse_chunk,
        add_random_noise,
        subtract_1_from_each_byte,
        lambda d: move_bits_left(d, random.randint(1, 8)),
        lambda d: move_bits_right(d, random.randint(1, 8))
    ]
    for _ in range(num_transforms):
        data = random.choice(transforms)(data)
    return data

def compress_data(data):
    return paq.compress(data)  # Zlib compression after PAQ placeholder

def decompress_data(data):
    return paq.decompress(data)

def compress_with_iterations(data, attempts=1, iterations=7200*15):
    best = compress_data(data)
    best_size = len(best)
    
    for _ in range(attempts):
        current = data
        for _ in range(iterations):
            transformed = apply_random_transforms(current)
            compressed = compress_data(transformed)
            
            if len(compressed) < best_size:
                best = compressed
                best_size = len(compressed)
            
            current = decompress_data(compressed)
    
    return best

def extract_data(data):
    return decompress_data(data)

# ===== Main Application =====
def main():
    while True:
        print("\n1. Compress File\n2. Extract File\n3. Extract with Regularity\n4. Black Hole Sim\n5. Exit")
        choice = input("Choice: ").strip()
        
        if choice == '1':
            in_file = input("Input file: ").strip()
            out_file = input("Output file: ").strip()
            
            try:
                with open(in_file, 'rb') as f:
                    data = f.read()
                
                compressed = compress_with_iterations(data)
                
                with open(out_file, 'wb') as f:
                    f.write(compressed)
                
                print(f"Compressed {len(data)} → {len(compressed)} bytes")
            except FileNotFoundError:
                print("Error: File not found.")
            
        elif choice == '2':
            in_file = input("Input compressed file: ").strip()
            out_file = input("Output file: ").strip()
            
            try:
                with open(in_file, 'rb') as f:
                    data = f.read()
                
                decompressed = extract_data(data)
                
                with open(out_file, 'wb') as f:
                    f.write(decompressed)
                
                print(f"Extracted {len(decompressed)} bytes")
            except FileNotFoundError:
                print("Error: File not found.")
            except zlib.error:
                print("Error: Invalid compressed file.")
                
        elif choice == '3':
            in_file = input("Input compressed file: ").strip()
            out_file = input("Output file: ").strip()
            
            try:
                with open(in_file, 'rb') as f:
                    data = f.read()
                
                decompressed = extract_data(data)  # Placeholder for regularity-based extraction
                
                with open(out_file, 'wb') as f:
                    f.write(decompressed)
                
                print(f"Extracted with Regularity: {len(decompressed)} bytes")
            except FileNotFoundError:
                print("Error: File not found.")
            except zlib.error:
                print("Error: Invalid compressed file.")
                
        elif choice == '4':
            try:
                size = int(input("Data size (bytes): ").strip())
                data = os.urandom(size)
                BlackHoleCompressor(data).compress()
            except ValueError:
                print("Invalid input. Please enter a number.")
            
        elif choice == '5':
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    warnings.simplefilter("ignore")  # Hide overflow warnings
    main()
