def compress_rle_positions(input_filename, output_filename):
    # Read the input file
    with open(input_filename, 'rb') as f:
        data = f.read()
    
    compressed_data = bytearray()
    length = len(data)
    i = 0

    # Store positions and repeats to write as a header
    positions = []

    while i < length:
        count = 1
        while i + 1 < length and data[i] == data[i + 1] and count < 255:
            count += 1
            i += 1
        
        # Only compress if there are more than 5 consecutive bytes
        if count > 4:
            # Save the value, count, and position
            compressed_data.append(data[i])
            compressed_data.append(count)
            # Save the original position to the positions list
            positions.append(i - count + 1)
        else:
            # Otherwise, add the bytes directly
            compressed_data.extend([data[i]] * count)
        
        i += 1
    
    # Convert positions to bytes (5 bytes each) and write to the header
    header = bytearray()
    for pos in positions:
        header.extend(pos.to_bytes(5, 'big'))
    
    # Write the header length, header, and compressed data to the output file
    with open(output_filename, 'wb') as f:
        # Write the length of the header as 2 bytes
        f.write(len(header).to_bytes(2, 'big'))
        f.write(header)
        f.write(compressed_data)
    
    print(f"Compression completed. {len(positions)} positions saved.")

def decompress_rle_positions(input_filename, output_filename):
    with open(input_filename, 'rb') as f:
        # Read the header length
        header_length = int.from_bytes(f.read(2), 'big')
        
        # Read the header (positions)
        header = f.read(header_length)
        positions = [int.from_bytes(header[i:i+5], 'big') for i in range(0, len(header), 5)]
        
        # Read the compressed data
        compressed_data = f.read()
    
    decompressed_data = bytearray()
    i = 0
    pos_index = 0
    decompressed_position = 0

    while i < len(compressed_data):
        value = compressed_data[i]
        
        if pos_index < len(positions) and decompressed_position == positions[pos_index]:
            # If this is a position with repeated bytes, use the count
            count = compressed_data[i + 1]
            decompressed_data.extend([value] * count)
            decompressed_position += count
            pos_index += 1
            i += 2  # Move to the next byte pair
        else:
            # Otherwise, just add the byte normally
            decompressed_data.append(value)
            decompressed_position += 1
            i += 1
    
    # Save the decompressed data to the output file
    with open(output_filename, 'wb') as f:
        f.write(decompressed_data)
    
    print("Decompression completed.")

if __name__ == "__main__":
    print("Black_Hole_48.py Crated: by Jurijus Pacalovas")
    action = input("Choose action (1=Compress, 2=Decompress): ")
    input_file = input("Enter input file name: ")
    long_output_file=len(input_file)
    if input_file[long_output_file-2:]==".b":
    	output_file = input_file[:long_output_file-2]
    else:
    	output_file=input_file+".b"

    if action == "1":
        compress_rle_positions(input_file, output_file)
    elif action == "2":
        decompress_rle_positions(input_file, output_file)
    else:
        print("Invalid option. Please select 1 or 2.")()