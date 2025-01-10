import random
import paq
import os

print("Created by Jurijus Pacalovas.")

def generate_headings_and_variations():
    """Generates data file only if it doesn't already exist."""
    file_name = input("Enter the name of the file to save the output (e.g., table4.txt): ").strip()
    if os.path.exists(file_name):
        print(f"The file '{file_name}' already exists. Skipping generation.")
        return True  # Indicate success (file already exists)

    try:
        with open(file_name, "w") as file:
            max_headings = 2**17
            variations_per_heading = 128
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


def decompress_file(input_filename, output_filename):
    try:
        with open(input_filename, 'rb') as infile:
            compressed_data = infile.read()
        decompressed_data = paq.decompress(compressed_data)
        with open(output_filename, 'wb') as outfile:
            outfile.write(decompressed_data)
        print(f"Decompression successful (paq only). Output saved to {output_filename}")
        return True
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return False
    except paq.error as e:
        print(f"Error during decompression: {e}")
        return False
    except Exception as e:
        print(f"An error occurred during decompression: {e}")
        return False


def main():
    if not generate_headings_and_variations():
        print("Data generation failed. Exiting.")
        return

    while True:
        print("\nChoose an option:")
        print("1: Compress the data file")
        print("2: Decompress a file")
        print("3: Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            input_file = input("Enter the name of the input file (e.g., table4.txt): ")
            output_file = input("Enter the name of the output file (e.g., table4.paq): ")
            if not compress_file(input_file, output_file):
                print("Compression failed.")

        elif choice == '2':
            input_file = input("Enter the name of the compressed file to decompress (e.g., table4.paq): ")
            output_file = input("Enter the name of the output file for decompression (e.g., table4_decompressed.txt): ")
            if not decompress_file(input_file, output_file):
                print("Decompression failed.")

        elif choice == '3':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
