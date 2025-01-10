import random
import paq
import os

print("Created by Jurijus Pacalovas.")

def generate_headings_and_variations(chunk):
    """Generates data file only if it doesn't already exist."""
    file_name = input("Enter the name of the file to save the output (e.g., table4.txt): ").strip()
    if os.path.exists(file_name):
        print(f"The file '{file_name}' already exists. Skipping generation.")
        return True  # Indicate success (file already exists)

    try:
        with open(file_name, "w") as file:
            max_headings = 2**17
            variations_per_heading = chunk
            half_variations = variations_per_heading // 2
            random.seed(42)  # for reproducibility

            for heading in range(max_headings):
                heading_bits = f"{heading:017b}"
                first_half = random.sample(range(256), half_variations)
                second_half = list(reversed(first_half))
                variations_8_bits = first_half + second_half

                for variation in variations_8_bits:
                    variation_bits_8 = f"{variation:08b}"
                    variation_bits_7 = f"{variation % 128:07b}"
                    file.write(f"{heading_bits} {variation_bits_8} {variation_bits_7}\n")
                file.write("\n")

        print(f"Data generated and saved to '{file_name}'.")
        return True
    except Exception as e:
        print(f"An error occurred during data generation: {e}")
        return False


def compress_file(input_filename, output_filename):
    try:
        with open(input_filename, 'rb') as infile:
            data = infile.read()
        compressed_data = paq.compress(data)
        with open(output_filename, 'wb') as outfile:
            outfile.write(compressed_data)
        print(f"Compression successful (paq only). Output saved to {output_filename}")
        return True
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred during compression: {e}")
        return False


def decompress_and_convert_to_utf8(input_filename, output_filename):
    try:
        # Decompress the binary data using PAQ decompression (or any other compression method)
        with open(input_filename, 'rb') as infile:  # Open the input as binary
            compressed_data = infile.read()

        # Decompress the data using PAQ (assuming PAQ is used for compression)
        decompressed_data = paq.decompress(compressed_data)

        # Try to save the raw decompressed binary data to output to inspect
        with open(output_filename, 'wb') as outfile:
            outfile.write(decompressed_data)

        print(f"Decompression successful. Raw decompressed data saved to {output_filename}")
        return True
    except Exception as e:
        print(f"An error occurred during decompression or conversion: {e}")
        return False


def main():
    while True:
        print("\nChoose an option:")
        print("1: Generate data file")
        print("2: Compress the data file with 18-bit encoding")
        print("3: Decompress and convert the file to UTF-8")
        print("4: Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            try:
                while True:  # Loop until valid chunk size is entered
                    try:
                        chunk = int(input("Enter the chunk size (must be between 25 and 128): "))
                        if 25 <= chunk <= 128:
                            break
                        else:
                            print("Chunk size must be between 25 and 128. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                if not generate_headings_and_variations(chunk):
                    print("Data generation failed.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '2':
            input_file = input("Enter the name of the input file (e.g., table4.txt): ")
            output_file = input("Enter the name of the output file (e.g., table4.paq): ")
            if not compress_file(input_file, output_file):
                print("Compression failed.")

        elif choice == '3':
            input_file = input("Enter the name of the compressed file to decompress (e.g., table4.paq): ")
            output_file = input("Enter the name of the output file for decompression (e.g., table4_decompressed.txt): ")
            if not decompress_and_convert_to_utf8(input_file, output_file):
                print("Decompression failed.")

        elif choice == '4':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()