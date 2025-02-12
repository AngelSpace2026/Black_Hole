import os
print("Created by Jurijus Pacalovas.")

def compress(input_file, output_file):
    # Read input file in binary
    with open(input_file, 'rb') as file:
        data = file.read()
    
    compressed_data = []
    
    # Compress zeros (Length 6 to 2^28)
    count_zero = 0
    for byte in data:
        if byte == 0:
            count_zero += 1
        else:
            if count_zero > 0:
                compressed_data.append(0)  # Mark the start of zero sequence
                compressed_data.append(count_zero)  # Store the length of zeros
            compressed_data.append(byte)
            count_zero = 0
    
    # If there were trailing zeros
    if count_zero > 0:
        compressed_data.append(0)
        compressed_data.append(count_zero)

    # Compress ones (Length 6 to 2^28)
    count_one = 0
    final_compressed_data = []
    for byte in compressed_data:
        if byte == 255:  # All bits are ones
            count_one += 1
        else:
            if count_one > 0:
                final_compressed_data.append(255)
                final_compressed_data.append(count_one)
            final_compressed_data.append(byte)
            count_one = 0

    if count_one > 0:
        final_compressed_data.append(255)
        final_compressed_data.append(count_one)
    
    # Save the compressed data to output file
    with open(output_file, 'wb') as file:
        file.write(bytes(final_compressed_data))

def extract(input_file):
    # Read compressed data from the input file
    with open(input_file, 'rb') as file:
        compressed_data = file.read()

    extracted_data = bytearray()
    i = 0
    while i < len(compressed_data):
        byte = compressed_data[i]
        i += 1
        if byte == 0:
            # Decompress zeros
            count = compressed_data[i]
            extracted_data.extend([0] * count)
            i += 1
        elif byte == 255:
            # Decompress ones
            count = compressed_data[i]
            extracted_data.extend([255] * count)
            i += 1
        else:
            extracted_data.append(byte)
    
    # Automatically create the output file name by removing the .b extension
    output_file = input_file.rsplit('.', 1)[0]  # Remove the last part of the name if there is a .b extension
    
    # Save the extracted data to the output file
    with open(output_file, 'wb') as file:
        file.write(extracted_data)
    print(f"Extraction complete. Output saved to {output_file}")

def main():
    # Ask user for operation
    operation = input("Enter operation (compress:1/extract:2): ").strip().lower()
    
    # Ask user for input file name
    input_file = input("Enter input file name: ").strip()

    if operation == "1":
        # Compress and save to output file with .b extension
        output_file = input_file + ".b"
        compress(input_file, output_file)
        print(f"Compression complete. Output saved to {output_file}")
    elif operation == "2":
        # Extract the file and automatically handle output name
        extract(input_file)
    else:
        print("Invalid operation. Please choose 'compress' (1) or 'extract' (2).")

if __name__ == "__main__":
    main()