import paq
import math
#Author Jurijus Pacalovas 

# Function to compress binary data
def compress_binary_data(data):
    compressed_data = paq.compress(data)
    return compressed_data

# Function to extract binary data
def extract_binary_data(compressed_data):
    extracted_data = paq.decompress(compressed_data)
    return extracted_data

# Function to generate a sequence of numbers by incrementing pi
def generate_pi_sequence(start, end):
    results = []
    for value in range(start, end + 1):
        result = math.pi + value
        results.append(result)
    return results

while True:
    print("Options:")
    print("1. Compress")
    print("2. Extract")
    print("3. Generate Pi Sequence and Quit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        # Compression
        input_file = input("Enter the input file name for compression: ")
        output_file = input("Enter the output file for saving compressed data: ")

        # Read binary data from the input file
        with open(input_file, 'rb') as file:
            binary_data = file.read()

        # Compress the binary data using paq
        compressed_data = compress_binary_data(binary_data)

        # Save the compressed data to the specified output file
        with open(output_file, 'wb') as file:
            file.write(compressed_data)

        print("Compression complete.")
    
    elif choice == '2':
        # Extraction
        input_file = input("Enter the input file name for extraction: ")
        output_file = input("Enter the output file for saving extracted data: ")

        # Read the compressed data from the input file
        with open(input_file, 'rb') as file:
            compressed_data = file.read()

        # Extract the data from the compressed data using paq
        extracted_data = extract_binary_data(compressed_data)

        # Save the extracted data to the specified output file
        with open(output_file, 'wb') as file:
            file.write(extracted_data)

        print("Extraction complete.")
    
    elif choice == '3':
        # Generate a sequence of numbers by incrementing pi and quit
        start_range = 5
        end_range = 2**20
        results = generate_pi_sequence(start_range, end_range)

        # Print the list of results
        for index, value in enumerate(results, start=start_range):
            print(f"Result {index}: {value}")

        break
    
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
