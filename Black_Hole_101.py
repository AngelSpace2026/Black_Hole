import os
import random
import warnings
import paq
from enum import Enum, auto

# ===== Physical Constants =====
C = 299792458.0  # Speed of light (m/s)
G = 6.67430e-11  # Gravitational constant
HBAR = 1.054571817e-34  # Reduced Planck constant
K_B = 1.380649e-23  # Boltzmann constant

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
    return paq.compress(data)

def decompress_data(data):
    return paq.decompress(data)

def extract_with_regularity(data):
    return decompress_data(reverse_chunk(data, len(data)))

def compress_with_iterations(data, iterations):
    best = compress_data(data)
    best_size = len(best)
    
    current = data
    for i in range(iterations):
        transformed = reverse_chunk(current, len(current))
        compressed = compress_data(transformed)
        compressed_size = len(compressed)
        if compressed_size < best_size:
            best, best_size = compressed, compressed_size
        current = decompress_data(compressed)
        
        if i % 100 == 0 or i == iterations - 1:
            print(f"\rIteration {i+1}/{iterations} - Best size: {best_size} bytes", end="")
    print()
    return best

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
        self.rs = 2 * G * self.mass / C**2

    def _check_danger(self):
        if self.mass > 1e50: return DangerLevel.COSMIC
        if self.mass > 1e30: return DangerLevel.CRITICAL
        if self.rs <= 1e-35: return DangerLevel.WARNING
        return DangerLevel.SAFE

    def compress(self):
        danger = self._check_danger()
        print(f"\nData Size: {len(self.data):,} bytes")
        print(f"Required Energy: {self.energy:.3e} J")
        print(f"Equivalent Mass: {self.mass:.3e} kg")
        print(f"Schwarzschild Radius: {self.rs:.3e} m")
        
        if danger == DangerLevel.COSMIC:
            print("\nCOSMIC DOOMSDAY: Galaxy cluster collapsing!")
        elif danger == DangerLevel.CRITICAL:
            print("\nSTELLAR COLLAPSE: Neutron star density reached!")
        elif danger == DangerLevel.WARNING:
            print("\nQUANTUM FOAM: Micro black hole evaporation imminent")
        else:
            print("\nInsufficient energy for singularity")

# ===== Main Application =====
def main():
    compression_levels = {
        1: 300,
        2: 7200,
        3: 20000,
        4: 108000,
        5: 2000000000
    }

    while True:
        print("\n[Main Menu]")
        print("1. Compress File")
        print("2. Extract File")
        print("3. Extract with Regularity")
        print("4. Black Hole Sim")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            in_file = input("Input file to compress: ").strip()
            if not os.path.exists(in_file):
                print(f"Error: File '{in_file}' not found!")
                continue
                
            out_file = f"{in_file}.bin"
            
            try:
                with open(in_file, 'rb') as f:
                    data = f.read()
                
                print("\nCompression Levels:")
                print("1. Fast (300 iterations)")
                print("2. Medium (7,200 iterations)")
                print("3. Strong (20,000 iterations)")
                print("4. Extreme (108,000 iterations)")
                print("5. Maximum (2,000,000,000 iterations)")
                
                level_choice = input("\nSelect level (1-5): ").strip()
                
                if level_choice.isdigit() and int(level_choice) in compression_levels:
                    iterations = compression_levels[int(level_choice)]
                    print(f"\nCompressing with {iterations:,} iterations...")
                    compressed = compress_with_iterations(data, iterations)
                    
                    with open(out_file, 'wb') as f:
                        f.write(compressed)
                    
                    ratio = (len(data) - len(compressed)) / len(data) * 100
                    print(f"\nCompression complete!")
                    print(f"Original: {len(data):,} bytes")
                    print(f"Compressed: {len(compressed):,} bytes")
                    print(f"Ratio: {ratio:.2f}% reduction")
                    print(f"Saved as: {out_file}")
                else:
                    print("Invalid level selected")
                    
            except Exception as e:
                print(f"Compression error: {str(e)}")
                
        elif choice == '2':
            in_file = input("Input .bin file to extract: ").strip()
            if not os.path.exists(in_file):
                print(f"Error: File '{in_file}' not found!")
                continue
                
            if not in_file.endswith('.bin'):
                print("Warning: Expected .bin extension")
                
            out_file = in_file[:-4] if in_file.endswith('.bin') else f"{in_file}.extracted"
            
            try:
                with open(in_file, 'rb') as f:
                    data = f.read()
                
                extracted = decompress_data(data)
                
                with open(out_file, 'wb') as f:
                    f.write(extracted)
                
                print(f"\nExtracted {len(extracted):,} bytes to: {out_file}")
                
            except Exception as e:
                print(f"Extraction error: {str(e)}")
                
        elif choice == '3':
            in_file = input("Input .bin file for regularity extraction: ").strip()
            if not os.path.exists(in_file):
                print(f"Error: File '{in_file}' not found!")
                continue
                
            out_file = in_file[:-4] + "_regular" if in_file.endswith('.bin') else f"{in_file}.regular"
            
            try:
                with open(in_file, 'rb') as f:
                    data = f.read()
                
                extracted = extract_with_regularity(data)
                
                with open(out_file, 'wb') as f:
                    f.write(extracted)
                
                print(f"\nRegularity extraction complete!")
                print(f"Extracted {len(extracted):,} bytes to: {out_file}")
                
            except Exception as e:
                print(f"Extraction error: {str(e)}")
                
        elif choice == '4':
            try:
                size = int(input("Data size in bytes (1-1GB): ").strip())
                if not 1 <= size <= 1000000000:
                    print("Size must be between 1 and 1,000,000,000 bytes")
                    continue
                    
                data = os.urandom(size)
                BlackHoleCompressor(data).compress()
                
            except ValueError:
                print("Please enter a valid number")
                
        elif choice == '5':
            print("Exiting program...")
            break
            
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    warnings.simplefilter("ignore")
    main()