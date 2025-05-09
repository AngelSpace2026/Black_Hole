import os
import zstandard as zstd
import random
import struct
from pathlib import Path
from qiskit import QuantumCircuit

# Reverse chunks at specified indices
def reverse_chunks_at_positions(input_filename, reversed_filename, chunk_size, positions):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    if len(chunked_data[-1]) < chunk_size:
        chunked_data[-1] += b'\x00' * (chunk_size - len(chunked_data[-1]))

    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    with open(reversed_filename, 'wb') as outfile:
        outfile.write(b"".join(chunked_data))

# Compress using Zstd
def compress_with_zstd(reversed_filename, compressed_filename, chunk_size, positions, original_size):
    with open(reversed_filename, 'rb') as infile:
        reversed_data = infile.read()

    metadata = struct.pack(">Q", original_size)
    metadata += struct.pack(">H", chunk_size)
    metadata += struct.pack(">H", len(positions))
    metadata += struct.pack(f">{len(positions)}H", *positions)

    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(metadata + reversed_data)

    with open(compressed_filename, 'wb') as outfile:
        outfile.write(compressed_data)

# Decompression
def decompress_and_restore(compressed_filename, restored_filename):
    with open(compressed_filename, 'rb') as infile:
        compressed_data = infile.read()

    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)

    original_size = struct.unpack(">Q", decompressed_data[:8])[0]
    chunk_size = struct.unpack(">H", decompressed_data[8:10])[0]
    num_positions = struct.unpack(">H", decompressed_data[10:12])[0]
    positions = list(struct.unpack(f">{num_positions}H", decompressed_data[12:12 + num_positions * 2]))

    chunked_data = decompressed_data[12 + num_positions * 2:]
    total_chunks = len(chunked_data) // chunk_size
    chunked_data = [chunked_data[i * chunk_size:(i + 1) * chunk_size] for i in range(total_chunks)]

    for pos in positions:
        if 0 <= pos < len(chunked_data):
            chunked_data[pos] = chunked_data[pos][::-1]

    restored_data = b"".join(chunked_data)[:original_size]

    with open(restored_filename, 'wb') as outfile:
        outfile.write(restored_data)

# Find best chunking strategy with randomized chunk size
def find_best_chunk_strategy(input_filename):
    file_size = os.path.getsize(input_filename)
    best_chunk_size = 1
    best_positions = []
    best_compression_ratio = float('inf')

    print("📏 Finding the best chunk strategy...")

    for _ in range(64):  # Try 64 different random chunk sizes
        chunk_size = random.randint(1, 64) * random.randint(1, 64)  # Randomized multiplication
        chunk_size = min(chunk_size, file_size // 2)  # Ensure it doesn't exceed half the file size

        max_positions = file_size // chunk_size
        if max_positions > 0:
            positions_count = random.randint(1, min(max_positions, 64))
            positions = random.sample(range(max_positions), positions_count)

            reversed_file = input_filename + ".rev"
            compressed_file = f"compress.{Path(input_filename).name}.b"

            reverse_chunks_at_positions(input_filename, reversed_file, chunk_size, positions)
            compress_with_zstd(reversed_file, compressed_file, chunk_size, positions, file_size)

            compressed_size = os.path.getsize(compressed_file)
            compression_ratio = compressed_size / file_size

            if compression_ratio < best_compression_ratio:
                best_compression_ratio = compression_ratio
                best_chunk_size = chunk_size
                best_positions = positions

            os.remove(reversed_file)
            os.remove(compressed_file)

    print(f"✅ Best chunk size: {best_chunk_size}, Best positions: {best_positions} (Compression Ratio: {best_compression_ratio:.4f})")

    qubits = 2 ** (best_chunk_size + 1)
    print(f"🪐 Qubits calculated: {qubits} based on chunk size {best_chunk_size}")

    return best_chunk_size, best_positions, qubits

# Compression and Extraction Process
def process_compression(input_filename):
    print(f"🔧 Starting compression for {input_filename}")
    best_chunk_size, best_positions, qubits = find_best_chunk_strategy(input_filename)

    reversed_file = input_filename + ".rev"
    compressed_file = f"compress.{Path(input_filename).name}.b"
    restored_file = f"extract.{Path(input_filename).name}"

    reverse_chunks_at_positions(input_filename, reversed_file, best_chunk_size, best_positions)
    compress_with_zstd(reversed_file, compressed_file, best_chunk_size, best_positions, os.path.getsize(input_filename))
    print(f"✅ File compressed: {compressed_file}")

    decompress_and_restore(compressed_file, restored_file)
    print(f"✅ File extracted: {restored_file}")

def main():
    print("Created by Jurijus Pacalovas.")
    mode = input("Enter mode (1 for compress, 2 for extract): ").strip()
    if mode == "1":
        process_compression(input("Enter input file name to compress: ").strip())
    elif mode == "2":
        decompress_and_restore(input("Enter input file name to extract: ").strip(), "restored_file")

if __name__ == "__main__":
    main()