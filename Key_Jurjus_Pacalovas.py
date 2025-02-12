import os
import paq
import hashlib

def xor_encrypt_decrypt(data, key):
    """Encrypts or decrypts data using XOR with a repeating key."""
    key_bytes = key.encode('utf-8')
    key_repeated = (key_bytes * ((len(data) + len(key_bytes) - 1) // len(key_bytes)))[:len(data)]
    return bytes([a ^ b for a, b in zip(data, key_repeated)])

def calculate_checksum(data):
    """Generates an SHA-256 checksum of the data for verification."""
    return hashlib.sha256(data).digest()

def encrypt_and_compress(filename, key):
    """Encrypts a file with XOR, adds a checksum, and compresses it using zlib."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    try:
        with open(filename, 'rb') as f:
            data = f.read()

        checksum = calculate_checksum(data)  # Calculate checksum before encryption
        encrypted_data = xor_encrypt_decrypt(checksum + data, key)  # Store checksum in encrypted data
        compressed_data = paq.compress(encrypted_data)

        encrypted_filename = filename + ".enc"
        with open(encrypted_filename, 'wb') as f:
            f.write(compressed_data)

        print(f"File '{filename}' encrypted and compressed as '{encrypted_filename}'.")

    except Exception as e:
        print(f"Error during encryption/compression: {e}")

def decompress_and_decrypt(filename, key):
    """Decompresses and decrypts a file, then verifies password correctness via checksum."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    try:
        with open(filename, 'rb') as f:
            compressed_data = f.read()

        try:
            decompressed_data = paq.decompress(compressed_data)
        except zlib.error as e:
            print(f"Decompression failed: {e}")
            return

        decrypted_data = xor_encrypt_decrypt(decompressed_data, key)

        # Extract checksum and original data
        stored_checksum = decrypted_data[:32]  # First 32 bytes contain SHA-256 checksum
        original_data = decrypted_data[32:]  # Remaining bytes are the actual file data

        # Validate checksum
        if stored_checksum != calculate_checksum(original_data):
            print("Error: Incorrect password or corrupted file!")
            return

        original_filename = filename[:-4]  # Remove .enc extension
        with open(original_filename, 'wb') as f:
            f.write(original_data)

        print(f"File '{filename}' decompressed and decrypted as '{original_filename}'.")

    except Exception as e:
        print(f"Error during decryption/decompression: {e}")

if __name__ == "__main__":
    key = input("Enter encryption key: ").strip()
    if not key:
        print("Error: Encryption key cannot be empty.")
        exit()

    filename = input("Enter filename: ").strip()
    if not filename:
        print("Error: Filename cannot be empty.")
        exit()

    action = input("Encrypt (e) or decrypt (d)? ").strip().lower()

    if action == 'e':
        encrypt_and_compress(filename, key)
    elif action == 'd':
        if not filename.endswith(".enc"):
            filename += ".enc"  # Ensure correct file extension
        decompress_and_decrypt(filename, key)
    else:
        print("Invalid choice. Please enter 'e' for encryption or 'd' for decryption.")