import os
import binascii
import math
import random
import heapq
import paq
import zlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HUFFMAN_THRESHOLD = 1024  # Bytes

class Node:
    def __init__(self, left=None, right=None, symbol=None):
        self.left = left
        self.right = right
        self.symbol = symbol

    def is_leaf(self):
        return self.left is None and self.right is None

class SmartCompressor:
    def __init__(self):
        self.max_intersections = 28

    def binary_to_file(self, binary_data, filename):
        try:
            n = int(binary_data, 2)
            num_bytes = (len(binary_data) + 7) // 8
            hex_str = "%0*x" % (num_bytes * 2, n)
            if len(hex_str) % 2 != 0:
                hex_str = '0' + hex_str
            byte_data = binascii.unhexlify(hex_str)
            with open(filename, 'wb') as f:
                f.write(byte_data)
            return True
        except Exception as e:
            logging.error(f"Error saving file: {str(e)}")
            return False

    def file_to_binary(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = f.read()
                if not data:
                    logging.error("Error: Empty file")
                    return None
                binary_str = bin(int(binascii.hexlify(data), 16))[2:]
                return binary_str.zfill(len(data) * 8)
        except Exception as e:
            logging.error(f"Error reading file: {str(e)}")
            return None

    def calculate_frequencies(self, binary_str):
        frequencies = {}
        for bit in binary_str:
            frequencies[bit] = frequencies.get(bit, 0) + 1
        return frequencies

    def build_huffman_tree(self, frequencies):
        heap = [(freq, symbol) for symbol, freq in frequencies.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            freq1, symbol1 = heapq.heappop(heap)
            freq2, symbol2 = heapq.heappop(heap)
            heapq.heappush(heap, (freq1 + freq2, Node(symbol1, symbol2)))
        return heap[0][1]

    def generate_huffman_codes(self, root, current_code="", codes={}):
        if root.is_leaf():
            codes[root.symbol] = current_code
            return codes
        self.generate_huffman_codes(root.left, current_code + "0", codes)
        self.generate_huffman_codes(root.right, current_code + "1", codes)
        return codes


    def compress_data_huffman(self, binary_str):
        frequencies = self.calculate_frequencies(binary_str)
        huffman_tree = self.build_huffman_tree(frequencies)
        huffman_codes = self.generate_huffman_codes(huffman_tree)
        if '0' not in huffman_codes:
            huffman_codes['0'] = '0'
        if '1' not in huffman_codes:
            huffman_codes['1'] = '1'
        compressed_str = ''.join(huffman_codes[bit] for bit in binary_str)
        return compressed_str

    def decompress_data_huffman(self, compressed_str):
        frequencies = self.calculate_frequencies(compressed_str)
        huffman_tree = self.build_huffman_tree(frequencies)
        huffman_codes = self.generate_huffman_codes(huffman_tree)
        reversed_codes = {code: symbol for symbol, code in huffman_codes.items()}
        decompressed_str = ""
        current_code = ""
        for bit in compressed_str:
            current_code += bit
            if current_code in reversed_codes:
                symbol = reversed_codes[current_code]
                decompressed_str += symbol
                current_code = ""
        return decompressed_str

    def compress_data_zlib(self, data_bytes):
        compressed_data = paq.compress(data_bytes)
        return compressed_data

    def decompress_data_zlib(self, compressed_data):
        try:
            decompressed_data = paq.decompress(compressed_data)
            return decompressed_data
        except zlib.error as e:
            logging.error(f"zlib decompression error: {e}")
            return None

    def compress(self, filename, attempts=1, iterations=100):
        if not os.path.exists(filename):
            logging.error(f"Error: File '{filename}' not found.")
            return
        logging.info(f"Compressing {filename}...")
        with open(filename, 'rb') as f:
            data_bytes = f.read()

        output_file = filename + '.bin'

        if len(data_bytes) < HUFFMAN_THRESHOLD:
            compressed_data = self.compress_data_huffman(self.file_to_binary(filename))
            success = self.binary_to_file(compressed_data, output_file)
            if not success:
                logging.error(f"Error saving compressed file: {output_file}")
                return
        else:
            compressed_data = self.compress_data_zlib(data_bytes)
            with open(output_file, 'wb') as f:
                f.write(compressed_data)

        orig_size = os.path.getsize(filename)
        comp_size = os.path.getsize(output_file)
        ratio = (comp_size / orig_size) * 100
        logging.info(f"\nCompression complete!")
        logging.info(f"Original: {orig_size} bytes")
        logging.info(f"Compressed: {comp_size} bytes")
        logging.info(f"Ratio: {ratio:.2f}%")
        logging.info(f"Saved as: {output_file}")

    def decompress(self, filename):
        if not os.path.exists(filename):
            logging.error(f"Error: File '{filename}' not found.")
            return
        logging.info(f"Decompressing {filename}...")
        try:
            with open(filename, 'rb') as f:
                compressed_data = f.read()
            output_file = filename[:-4] #Remove .bin extension

            try:
                decompressed_data = self.decompress_data_zlib(compressed_data)
                if decompressed_data:
                    with open(output_file, 'wb') as f:
                        f.write(decompressed_data)
                    logging.info("Decompressed using Black_Hole_91.")
                    return
            except Exception as e:
                logging.warning(f"zlib decompression failed: {e}. Trying Huffman...")


            compressed_binary = self.file_to_binary(filename)
            if compressed_binary:
                decompressed_data = self.decompress_data_huffman(compressed_binary)
                if decompressed_data:
                    self.binary_to_file(decompressed_data, output_file)
                    logging.info("Decompressed using Huffman.")
                else:
                    logging.error("Error: Huffman decompression failed.")
                    return
            else:
                logging.error("Error: Huffman decompression failed.")
                return
        except Exception as e:
            logging.exception(f"An error occurred during decompression: {e}")

        comp_size = os.path.getsize(filename)
        decomp_size = os.path.getsize(output_file)
        logging.info(f"\nDecompression complete!")
        logging.info(f"Compressed: {comp_size} bytes")
        logging.info(f"Decompressed: {decomp_size} bytes")
        logging.info(f"Saved as: {output_file}")


def main():
    compressor = SmartCompressor()
    while True:
        print("\nSmart Compression System")
        print("1. Compress File")
        print("2. Decompress File")
        print("3. Exit")
        choice = input("Select option (1-3): ").strip()
        if choice == '1':
            filename = input("Enter file to compress: ").strip()
            if filename:
                try:
                    attempts = int(input("Enter number of attempts (1 or more): "))
                    iterations = int(input("Enter number of iterations (1 or more): "))
                    if attempts < 1 or iterations < 1:
                        print("Attempts and iterations must be 1 or greater.")
                        continue
                    compressor.compress(filename, attempts, iterations)
                except ValueError:
                    print("Invalid input. Please enter integers for attempts and iterations.")
        elif choice == '2':
            filename = input("Enter file to decompress: ").strip()
            if filename:
                compressor.decompress(filename)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again")

if __name__ == "__main__":
    main()