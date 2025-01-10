def compress_rle_8bit(input_filename, output_filename):
    with open(input_filename, 'rb') as f:
        data = f.read()

    compressed_data = bytearray()
    length = len(data)
    i = 0

    while i < length:
        count = 1
        while i + 1 < length and data[i] == data[i + 1] and count < 255:
            count += 1
            i += 1
        
        if count > 1:
            # Use a marker (0xFF), the byte value, and the repetition count
            compressed_data.append(0xFF)
            compressed_data.append(data[i])
            compressed_data.append(count)
        else:
            # Otherwise, just add the byte directly
            compressed_data.append(data[i])
        
        i += 1

    # Write the compressed data to the output file
    with open(output_filename, 'wb') as f:
        f.write(compressed_data)
    
    print("Compression completed.")

def decompress_rle_8bit(input_filename, output_filename):
    with open(input_filename, 'rb') as f:
        compressed_data = f.read()

    decompressed_data = bytearray()
    i = 0

    while i < len(compressed_data):
        if compressed_data[i] == 0xFF:
            # Read the value and repetition count
            value = compressed_data[i + 1]
            count = compressed_data[i + 2]
            decompressed_data.extend([value] * count)
            i += 3  # Move to the next byte after the marker, value, and count
        else:
            # Regular byte, just add it
            decompressed_data.append(compressed_data[i])
            i += 1
    
    # Write the decompressed data to the output file
    with open(output_filename, 'wb') as f:
        f.write(decompressed_data)
    
    print("Decompression completed.")

if __name__ == "__main__":
    print("Black_Hole_47.py Crated: by Jurijus Pacalovas")
    action = input("Choose action (1=Compress, 2=Decompress): ")
    input_file = input("Enter input file name: ")
    long_output_file=len(input_file)
    if input_file[long_output_file-2:]==".b":
    	output_file = input_file[:long_output_file-2]
    else:
    	output_file=input_file+".b"

    if action == "1":
        compress_rle_8bit(input_file, output_file)
    elif action == "2":
        decompress_rle_8bit(input_file, output_file)
    else:
        print("Invalid option. Please select 1 or 2.")