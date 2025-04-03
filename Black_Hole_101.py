import os
import random
import warnings
import paq
from enum import Enum, auto

# ===== Physical Constants =====
C = 299792458.0          # Speed of light (m/s)
G = 6.67430e-11          # Gravitational constant
HBAR = 1.054571817e-34   # Reduced Planck constant
K_B = 1.380649e-23       # Boltzmann constant

# ===== Compression System =====
def reverse_chunk(data, chunk_size):
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

def compress_data(data):
    return paq.compress(data)  # Use paq compression

def decompress_data(data):
    return paq.decompress(data)  # Use paq decompression

def extract_with_regularity(data):
    return decompress_data(reverse_chunk(data, len(data)))

def compress_with_iterations(data, attempts=1, iterations=7200):
    best = compress_data(data)  # Start with the initial compression
    best_size = len(best)
    
    for _ in range(attempts):
        current = data
        for _ in range(iterations):
            transformed = reverse_chunk(current, len(current))
            compressed = compress_data(transformed)
            compressed_size = len(compressed)
            
            if compressed_size < best_size:
                best = compressed
                best_size = compressed_size
            
            current = decompress_data(compressed)
    
    return best  # Return only the best compression result

# ===== Black Hole Physics =====
class DangerLevel(Enum):
    SAFE = auto()
    WARNING = auto()
    CRITICAL = auto()
    COSMIC = auto()

class BlackHoleCompressor:
    def __init__(self, data):
        self.data = data
        self.bits = len(data) * 8
        self.energy = self.bits * K_B * 1.4e32
        self.mass = self.energy / C**2
        self.rs = 2 * G * self.mass / C**2  # Schwarzschild radius

    def _check_danger(self):
        if self.mass > 1e50:
            return DangerLevel.COSMIC
        if self.mass > 1e30:
            return DangerLevel.CRITICAL
        if self.rs <= 1e-35:
            return DangerLevel.WARNING
        return DangerLevel.SAFE

    def compress(self):
        danger = self._check_danger()
        print(f"\nData Size: {len(self.data)} bytes")
        print(f"Required Energy: {self.energy:.3e} J")
        print(f"Equivalent Mass: {self.mass:.3e} kg")
        print(f"Schwarzschild Radius: {self.rs:.3e} m")

        if danger == DangerLevel.COSMIC:
            print("\n COSMIC DOOMSDAY: Galaxy cluster collapsing!")
        elif danger == DangerLevel.CRITICAL:
            print("\n STELLAR COLLAPSE: Neutron star density reached!")
        elif danger == DangerLevel.WARNING:
            print("\n QUANTUM FOAM: Micro black hole evaporation imminent")
        else:
            print("\n Insufficient energy for singularity")
        
        # For compression, simply return the original data as 'compressed'
        # In a real scenario, we would apply some transformation here
        return self.data  # Returning the data as-is for now.

    def extract(self):
        # Simulate the extraction process (inverse of compression).
        # If compression reverses the data, extraction would reverse it back.
        print(f"\nExtracting from black hole compressed data ({len(self.data)} bytes)...")
        extracted_data = reverse_chunk(self.data, len(self.data))  # Reversing back
        return extracted_data

# ===== Main Application =====
def main():
    while True:
        print("\n1. Compress File\n2. Extract File\n3. Extract with Regularity\n4. Black Hole Compress\n5. Black Hole Extract\n6. Exit")
        choice = input("Choice: ")

        if choice == '1':
            in_file = input("Input file: ")
            out_file = input("Best compressed output file: ")
            with open(in_file, 'rb') as f:
                data = f.read()
            
            print("\nChoose Iteration Level:")
            print("1. Level 1 (300)\n2. Level 2 (7200)\n3. Level 3 (20000)\n4. Level 4 (7200 * 15)\n5. Level 5 (2000000000)")
            level = input("Enter level (1-5): ")
            
            levels = {'1': 300, '2': 7200, '3': 20000, '4': 7200 * 15, '5': 2000000000}
            iterations = levels.get(level, 300)  # Default to Level 1 if invalid
            
            compressed = compress_with_iterations(data, 1, iterations)
            
            with open(out_file, 'wb') as f:
                f.write(compressed)
            
            print(f"Compressed {len(data)} → {len(compressed)} bytes (best)")

        elif choice == '2':
            in_file = input("Input compressed file: ")
            out_file = input("Output file: ")
            with open(in_file, 'rb') as f:
                data = f.read()
            extracted = decompress_data(data)
            with open(out_file, 'wb') as f:
                f.write(extracted)
            print(f"Extracted: {len(extracted)} bytes")

        elif choice == '3':
            in_file = input("Input compressed file: ")
            out_file = input("Output file: ")
            with open(in_file, 'rb') as f:
                data = f.read()
            extracted = extract_with_regularity(data)
            with open(out_file, 'wb') as f:
                f.write(extracted)
            print(f"Extracted with Regularity: {len(extracted)} bytes")

        elif choice == '4':
            in_file = input("Input file for Black Hole compression: ")
            out_file = input("Output file for Black Hole compression: ")
            
            with open(in_file, 'rb') as f:
                data = f.read()

            black_hole_compressor = BlackHoleCompressor(data)
            compressed_data = black_hole_compressor.compress()  # Compress using black hole method

            with open(out_file, 'wb') as f:
                f.write(compressed_data)

            print(f"Black Hole compressed {len(data)} → {len(compressed_data)} bytes")

        elif choice == '5':
            in_file = input("Input file for Black Hole extraction: ")
            out_file = input("Output file for Black Hole extraction: ")

            with open(in_file, 'rb') as f:
                data = f.read()

            black_hole_compressor = BlackHoleCompressor(data)
            extracted_data = black_hole_compressor.extract()  # Extract using black hole method

            with open(out_file, 'wb') as f:
                f.write(extracted_data)

            print(f"Black Hole extracted {len(data)} → {len(extracted_data)} bytes")

        elif choice == '6':
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    warnings.simplefilter("ignore")  # Hide overflow warnings
    main()