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

def compress_with_iterations(data, attempts=1, iterations=2000000000):
    best1 = compress_data(data)
    best2 = best1  # Initialize second best as the same
    best_size1 = len(best1)
    best_size2 = best_size1
    
    for _ in range(attempts):
        current = data
        for _ in range(iterations):
            transformed = reverse_chunk(current, len(current))
            compressed = compress_data(transformed)
            compressed_size = len(compressed)
            
            if compressed_size < best_size1:
                best2, best_size2 = best1, best_size1
                best1, best_size1 = compressed, compressed_size
            elif best_size1 < compressed_size < best_size2:
                best2, best_size2 = compressed, compressed_size
            
            current = decompress_data(compressed)
    
    return best1, best2

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

# ===== Main Application =====
def main():
    while True:
        print("\n1. Compress File\n2. Extract File\n3. Extract with Regularity\n4. Black Hole Sim\n5. Exit")
        choice = input("Choice: ")

        if choice == '1':
            in_file = input("Input file: ")
            out_file1 = input("Best compressed output file: ")
            out_file2 = input("Second best compressed output file: ")
            with open(in_file, 'rb') as f:
                data = f.read()
            compressed1, compressed2 = compress_with_iterations(data, 1, 2000000000)
            with open(out_file1, 'wb') as f:
                f.write(compressed1)
            with open(out_file2, 'wb') as f:
                f.write(compressed2)
            print(f"Compressed {len(data)} → {len(compressed1)} bytes (best)")
            print(f"Compressed {len(data)} → {len(compressed2)} bytes (second best)")

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
            size = int(input("Data size (bytes): "))
            data = os.urandom(size)
            BlackHoleCompressor(data).compress()

        elif choice == '5':
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    warnings.simplefilter("ignore")  # Hide overflow warnings
    main()