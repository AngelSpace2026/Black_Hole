import random
import paq
import pickle
import os
import hashlib
import io

print("Created by Jurijus Pacalovas.")

def generate_7bit_random(count):
    """Generates a list of 7-bit random numbers."""
    return [random.randint(0, 127) for _ in range(count)]

def generate_headings_and_variations(filename="data.pkl"):
    """Generates data with a 7-bit PRNG and saves it to a pickle file."""
    max_headings = 2**17  # Adjust as needed. Large number, be mindful of memory usage.
    variations_per_heading = 128 # Adjust as needed
    random.seed(42) #for reproducibility. Remove for truly random data.
    data = {'table': {}} # Initialize with a 'table' dictionary
    for heading in range(max_headings):
        data['table'][heading] = generate_7bit_random(variations_per_heading)
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print(f"Data generated and saved to {filename}")
    return True


def compress_file(input_filename, output_filename):
    try:
        with open(input_filename, 'rb') as infile:
            data = infile.read() # Read the entire file content
        compressed_paq = paq.compress(data)
        with open(output_filename, 'wb') as outfile:
            outfile.write(compressed_paq)
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
        with open(output_file, 'wb') as outfile:
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


def verify_data(original_file, decompressed_file):
    try:
        with open(original_file, 'rb') as f1, open(decompressed_file, 'rb') as f2:
            hash1 = hashlib.sha256(f1.read()).hexdigest()
            hash2 = hashlib.sha256(f2.read()).hexdigest()
        return hash1 == hash2
    except FileNotFoundError:
        print("Error: One or both files not found for verification.")
        return False
    except Exception as e:
        print(f"An error occurred during data verification: {e}")
        return False


def main():
    if not os.path.exists("data.pkl"):
        if not generate_headings_and_variations():
            print("Data generation failed. Exiting.")
            return

    while True:
        print("\nChoose an option:")
        print("1: Compress the data file (data.pkl)")
        print("2: Decompress a file")
        print("3: Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            output_file = input("Enter the name of the output file (data.paq): ")
            if not compress_file("data.pkl", output_file):
                print("Compression failed.")

        elif choice == '2':
            input_file = input("Enter the name of the compressed file to decompress (data.paq): ")
            output_file = input("Enter the name of the output file for decompression (data_decompressed.pkl): ")
            if decompress_file(input_file, output_file):
                if verify_data("data.pkl", output_file):
                    print("Decompression successful and data verified.")
                else:
                    print("Decompression successful, but data verification failed!")
            else:
                print("Decompression failed.")

        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
