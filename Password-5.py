import os
import binascii
import getpass
from time import time
import zlib #Using zlib for compression

class PasswordClass:
    def process_file(self, password, filename, mode):
        """Encrypts or decrypts a file using the given password and mode."""
        try:
            start_time = time()
            with open(filename, "rb") as f_in:
                data = f_in.read()
            
            if mode == "encrypt":
                # Basic encryption (INSECURE - use a proper library for real use)
                encrypted_data = self.weak_encrypt(password, data)
                compressed_data = zlib.compress(encrypted_data) #add compression

            elif mode == "decrypt":
                # Basic decryption (INSECURE - use a proper library for real use)
                decompressed_data = zlib.decompress(data)
                encrypted_data = self.weak_decrypt(password, decompressed_data)
                
            else:
                raise ValueError("Invalid mode. Choose 'encrypt' or 'decrypt'.")

            with open(filename + ".bin", "wb") as f_out:
                f_out.write(compressed_data if mode == "encrypt" else encrypted_data)

            end_time = time()
            return end_time - start_time

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def weak_encrypt(self, password, data):
        """Weak encryption function (for demonstration only).  DO NOT USE IN PRODUCTION."""
        #This is a placeholder for a real encryption algorithm.
        #Replace this with a strong encryption algorithm from a reputable library.
        key = int(binascii.hexlify(password.encode()), 16) #Simple key generation. Insecure!
        encrypted = bytes([byte ^ (key >> (i % 8) & 0xFF) for i, byte in enumerate(data)])
        return encrypted

    def weak_decrypt(self, password, data):
        """Weak decryption function (for demonstration only). DO NOT USE IN PRODUCTION."""
        key = int(binascii.hexlify(password.encode()), 16)  #Simple key generation. Insecure!
        decrypted = bytes([byte ^ (key >> (i % 8) & 0xFF) for i, byte in enumerate(data)])
        return decrypted


if __name__ == "__main__":
    password_manager = PasswordClass()
    filename = input("Enter filename: ")
    mode = input("Enter mode (encrypt/decrypt): ").lower()
    password = getpass.getpass("Enter password: ")

    execution_time = password_manager.process_file(password, filename, mode)

    if execution_time is not None:
        print(f"Process completed in {execution_time:.4f} seconds.")