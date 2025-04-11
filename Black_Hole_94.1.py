import paq

def compress(data, iterations):
    """Compress data using observed bit pattern multiple times"""
    for _ in range(iterations):
        compressed = bytearray()
        for byte in data:
            if byte == 0:
                compressed.append(0)
                continue
            val = byte >> 2
            if val == 0x1F:
                compressed.append(0x1F)
            else:
                compressed.append(val)
        data = compressed
    return data

def extract(data, iterations):
    """Extract data by reversing the compression multiple times"""
    for _ in range(iterations):
        extracted = bytearray()
        for byte in data:
            if byte == 0:
                extracted.append(0)
                continue
            val = (byte << 2) | 1
            extracted.append(val)
        data = extracted
    return data

def hex_dump(data, bytes_per_line=8):
    """Generate formatted hex dump"""
    dump = []
    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i+bytes_per_line]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        dump.append(f'{i:08X} {hex_part.ljust(24)} {ascii_part}')
    return '\n'.join(dump)

def main():
    print("Data Compression/Extraction Tool with Iteration + Zlib")
    print("1. Compress")
    print("2. Extract")
    print("3. View Hex Dump")
    
    action = input("Select operation (1/2/3): ")

    if action == '1':
        input_file = input("Input file to compress: ")
        output_file = input("Output file for compressed data: ")
        iterations = int(input("Number of compression iterations: "))
        
        with open(input_file, 'rb') as f:
            data = f.read()
        
        compressed = compress(data, iterations)
        compressed_zlib = paq.compress(bytes(compressed))  # FIX: convert bytearray to bytes
        
        with open(output_file, 'wb') as f:
            f.write(compressed_zlib)
        
        print(f"Compressed paq")
        print("Hex dump of final compressed data:")
        print(hex_dump(compressed_zlib))

    elif action == '2':
        input_file = input("Input file to extract: ")
        output_file = input("Output file for extracted data: ")
        iterations = int(input("Number of extraction iterations: "))
        
        with open(input_file, 'rb') as f:
            compressed_zlib = f.read()
        
        decompressed = paq.decompress(compressed_zlib)
        extracted = extract(decompressed, iterations)
        
        with open(output_file, 'wb') as f:
            f.write(extracted)
        
        print(f"Extracted paq")
        print("Hex dump of extracted data:")
        print(hex_dump(extracted))

    elif action == '3':
        file = input("File to view: ")
        with open(file, 'rb') as f:
            data = f.read()
        print(hex_dump(data))

    else:
        print("Invalid selection")

if __name__ == "__main__":
    main()