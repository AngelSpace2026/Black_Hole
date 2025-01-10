from mpmath import mp

# Author: Jurijus Pacalovas

# Function to generate digits of pi after "3"
def generate_pi_digits(digits):
    if digits < 1:
        raise ValueError("The number of digits must be at least 1.")
    mp.dps = digits + 1  # Set the precision
    pi_value = str(mp.pi)[2:]  # Remove the "3."
    return pi_value

# Function to compress binary data using pi digits
def compress_with_pi(data, pi_digits):
    pi_sequence = [int(d) for d in pi_digits[:len(data)]]
    compressed_data = bytes([b ^ p for b, p in zip(data, pi_sequence)])
    return compressed_data

# Function to extract binary data using pi digits
def extract_with_pi(data, pi_digits):
    # Reverse the compression process
    return compress_with_pi(data, pi_digits)

# Function to generate and save digits of pi to a file
def generate_pi_and_save(digits, file_name):
    pi_digits = generate_pi_digits(digits)
    with open(file_name, 'w') as file:
        file.write(pi_digits)
    return pi_digits

# Main program loop
while True:
    print("\nOptions:")
    print("1. Compress using Pi")
    print("2. Extract using Pi")
    print("3. Generate and Save Pi Digits")
    print("4. Quit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        # Compression
        try:
            input_file = input("Enter the input file name for compression: ")
            pi_file = input("Enter the file name that contains pi digits: ")
            output_file = input("Enter the output file for saving compressed data: ")

            # Read binary data from the input file
            with open(input_file, 'rb') as file:
                binary_data = file.read()

            # Read pi digits from the pi file
            with open(pi_file, 'r') as file:
                pi_digits = file.read().strip()

            # Compress the binary data using digits of pi
            compressed_data = compress_with_pi(binary_data, pi_digits)

            # Save the compressed data to the specified output file
            with open(output_file, 'wb') as file:
                file.write(compressed_data)

            print(f"Compression complete. Saved to {output_file}.")
        except Exception as e:
            print(f"Error: {e}")
    
    elif choice == '2':
        # Extraction
        try:
            input_file = input("Enter the input file name for extraction: ")
            pi_file = input("Enter the file name that contains pi digits: ")
            output_file = input("Enter the output file for saving extracted data: ")

            # Read the compressed data from the input file
            with open(input_file, 'rb') as file:
                compressed_data = file.read()

            # Read pi digits from the pi file
            with open(pi_file, 'r') as file:
                pi_digits = file.read().strip()

            # Extract the data using digits of pi
            extracted_data = extract_with_pi(compressed_data, pi_digits)

            # Save the extracted data to the specified output file
            with open(output_file, 'wb') as file:
                file.write(extracted_data)

            print(f"Extraction complete. Saved to {output_file}.")
        except Exception as e:
            print(f"Error: {e}")
    
    elif choice == '3':
        # Generate and save pi digits
        try:
            digits = int(input("Enter the total number of digits to generate for pi (minimum 1): "))
            file_name = input("Enter the file name to save the generated value of pi: ")
            pi_data = generate_pi_and_save(digits, file_name)
            print(f"Pi digits saved to {file_name}.")
        except ValueError as e:
            print(f"Error: {e}")
    
    elif choice == '4':
        # Quit the program
        print("Exiting the program.")
        break
    
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")