import os
import random
import time
import math
import paq
from tqdm import tqdm
from qiskit import QuantumCircuit

# --- Quantum Dictionary Compressor ---
class QuantumDictionaryCompressor:
    def __init__(self, qubits=2000):
        self.qubits = qubits
        self.circuit = QuantumCircuit(qubits)
        self.last_refresh = 0
        self.cache = bytearray()
        self._initialize_quantum_state()

    def _initialize_quantum_state(self):
        for q in range(self.qubits):
            self.circuit.h(q)
        self.last_refresh = time.time()

    def _measure_qubits(self):
        return [0 if random.random() < 0.55 else 1 for _ in range(self.qubits)]

    def get_quantum_bits(self, num_bits):
        if time.time() - self.last_refresh > 60:
            self._refresh_quantum_state()
        needed_bytes = (num_bits + 7) // 8
        while len(self.cache) < needed_bytes:
            bits = self._measure_qubits()
            for i in range(0, len(bits), 8):
                byte = sum(bits[i+j] << (7-j) for j in range(8) if i+j < len(bits))
                self.cache.append(byte)
        result = bytes(self.cache[:needed_bytes])
        self.cache = self.cache[needed_bytes:]
        return result

    def _refresh_quantum_state(self):
        self.circuit = QuantumCircuit(self.qubits)
        for q in range(self.qubits):
            angle = random.uniform(0, math.pi/2)
            self.circuit.rx(angle, q)
            self.circuit.rz(angle/3, q)
        self.last_refresh = time.time()
        self.cache = bytearray()

# --- Transformations ---
def dictionary_specific_transforms(data, qc):
    data = bytes(((b << 3) | (b >> 5)) & 0xFF for b in data)
    noise = qc.get_quantum_bits(len(data) * 8)
    data = bytes((b + (noise[i] % 3)) % 256 for i, b in enumerate(data))
    block_size = 16
    transformed = bytearray()
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size:
            block += bytes(block_size - len(block))
        mask = qc.get_quantum_bits(block_size*8)
        transformed_block = bytes(b ^ mask[j] for j, b in enumerate(block))
        transformed.extend(transformed_block)
    return bytes(transformed)

def reverse_chunk(data, chunk_size=64):
    return data[::-1]

def add_random_noise(data, noise_level=10):
    return bytes([b ^ random.randint(0, noise_level) for b in data])

def subtract_1_from_each_byte(data):
    return bytes([(b - 1) % 256 for b in data])

def move_bits_left(data, n):
    n = n % 8
    return bytes([(b << n & 0xFF) | (b >> (8 - n)) for b in data])

def move_bits_right(data, n):
    n = n % 8
    return bytes([(b >> n & 0xFF) | (b << (8 - n)) & 0xFF for b in data])

def minus_1000_qubit_block(data):
    block_size_bytes = 125
    transformed_data = bytearray()
    metadata = bytearray()
    for i in range(0, len(data), block_size_bytes):
        block = data[i:i + block_size_bytes]
        if len(block) < block_size_bytes:
            block += bytes(block_size_bytes - len(block))
        rand_value = random.randint(1, 2**1000 - 1)
        rand_bytes = rand_value.to_bytes(block_size_bytes, 'big')
        transformed = bytes([(b - rand_bytes[j % block_size_bytes]) % 256 for j, b in enumerate(block)])
        transformed_data.extend(transformed)
        metadata.extend(rand_bytes)
    return bytes(transformed_data), bytes(metadata)

def add_block_size_64(data):
    transformed = bytearray()
    block_size = 64
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size:
            block += bytes(block_size - len(block))
        transformed.extend((block_size).to_bytes(2, 'big'))
        transformed.extend(block)
    return bytes(transformed)

def rle_encode_1byte(data):
    if not data:
        return data
    encoded = bytearray()
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1] and count < 255:
            count += 1
        else:
            encoded.extend([data[i-1], count])
            count = 1
    encoded.extend([data[-1], count])
    return bytes(encoded)

# --- Compression Logic ---
def apply_random_transformations(data, num_transforms=10):
    transforms = [
        (reverse_chunk, True),
        (add_random_noise, True),
        (subtract_1_from_each_byte, False),
        (move_bits_left, True),
        (move_bits_right, True),
        (minus_1000_qubit_block, False)
    ]
    for _ in range(num_transforms):
        func, needs_param = random.choice(transforms)
        try:
            if func == minus_1000_qubit_block:
                data, _ = func(data)
            elif needs_param:
                param = random.randint(1, 7)
                data = func(data, param)
            else:
                data = func(data)
        except Exception as e:
            print(f"Transformation error: {e}")
    if len(data) < 1024:
        data = rle_encode_1byte(data)
    return add_block_size_64(data)

def compress_data(data):
    return paq.compress(data)

def decompress_data(data):
    return paq.decompress(data)

def quantum_dict_compress(data, attempts=4, iterations=3):
    qc = QuantumDictionaryCompressor()
    best = compress_data(data)
    best_size = len(best)
    for _ in tqdm(range(attempts), desc="Quantum Dictionary Compression"):
        temp = data
        for _ in range(iterations):
            temp = dictionary_specific_transforms(temp, qc)
        compressed = compress_data(temp)
        if len(compressed) < best_size:
            best, best_size = compressed, len(compressed)
    return best

def compress_with_iterations(data, attempts=4, iterations=4):
    best = compress_data(data)
    best_size = len(best)
    for _ in tqdm(range(attempts), desc="Smart Hybrid Compression"):
        temp = data
        for _ in range(iterations):
            temp = apply_random_transformations(temp)
            compressed = compress_data(temp)
            if len(compressed) < best_size:
                best, best_size = compressed, len(compressed)
    return best

# --- CLI ---
def main():
    print("Quantum Smart Compressor")
    print("1 = Compress\n2 = Extract")
    option = input("Choose option: ").strip()

    if option == "1":
        in_file = input("Input file path: ")
        out_file = input("Output (compressed) file path: ")
        try:
            with open(in_file, 'rb') as f:
                data = f.read()

            print("Running hybrid quantum + smart compression...")
            result1 = quantum_dict_compress(data)
            result2 = compress_with_iterations(data)

            final_result = result1 if len(result1) < len(result2) else result2

            with open(out_file, 'wb') as f:
                f.write(final_result)
            print("Compression complete.")
        except Exception as e:
            print(f"Compression failed: {e}")

    elif option == "2":
        in_file = input("Compressed file path: ")
        out_file = input("Output (decompressed) file path: ")
        try:
            with open(in_file, 'rb') as f:
                compressed = f.read()
            decompressed = decompress_data(compressed)
            with open(out_file, 'wb') as f:
                f.write(decompressed)
            print("Extraction complete.")
        except Exception as e:
            print(f"Decompression failed: {e}")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
