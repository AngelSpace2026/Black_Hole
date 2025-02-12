from time import time
import os
import binascii
import zlib

class password_class:

    def strToBinary(self, s):
        return "".join(bin(ord(c))[2:].zfill(8) for c in s)

    def convertToHex(self, num):
        temp = ""
        while num != 0:
            rem = num % 16
            c = rem + 48 if rem < 10 else rem + 87
            temp += chr(c)
            num //= 16
        return temp

    def encryptString(self, S):
        ans = ""
        i = 0
        while i < len(S):
            ch = S[i]
            count = 0
            while i < len(S) and S[i] == ch:
                count += 1
                i += 1
            hex_count = self.convertToHex(count)
            ans += ch + hex_count
        return ans[::-1]


    def password1(self):
        name = input("What is the name of the file? ")
        if not os.path.exists(name):
            print('Path does not exist!')
            return None

        try:
            with open(name, "rb") as f:
                data = f.read()
                if not data:
                    raise ValueError("Empty file")
                if len(data) > 2**40:
                    raise ValueError("File too large")

            start_time = time()
            password = input("Please, enter password: ")
            encrypted_password = self.encryptString(password)
            binary_password = self.strToBinary(encrypted_password)
            int_password = int(binary_password, 2)

            size_data = bin(int.from_bytes(data, 'big'))[2:]
            size_data = size_data.zfill((len(data) * 8))

            combined_data = str(int_password) + size_data

            compressed_data = zlib.compress(combined_data.encode())

            with open(name + ".bin", "wb") as outfile:
                outfile.write(compressed_data)

            end_time = time()
            return end_time - start_time

        except (ValueError, binascii.Error, OSError) as e:
            print(f"An error occurred: {e}")
            return None

    def password2(self):
        name = input("What is the name of the file? ")
        if not os.path.exists(name):
            print('Path does not exist!')
            return None

        try:
            with open(name, "rb") as f:
                compressed_data = f.read()
                if not compressed_data:
                    raise ValueError("Empty file")

            start_time = time()
            password = input("Please, enter password: ")
            encrypted_password = self.encryptString(password)
            binary_password = self.strToBinary(encrypted_password)
            int_password = int(binary_password, 2)

            decompressed_data = zlib.decompress(compressed_data)

            extracted_password_bytes = decompressed_data[:len(str(int_password).encode())]
            if str(int_password).encode() != extracted_password_bytes:
                raise ValueError("Incorrect password")

            data_bytes = decompressed_data[len(str(int_password).encode()):]

            with open(name[:-4], "wb") as outfile:
                outfile.write(data_bytes)

            end_time = time()
            return end_time - start_time

        except (ValueError, binascii.Error, zlib.error, OSError) as e:
            print(f"An error occurred: {e}")
            return None


d = password_class()

while True:
    choice = input("Choose operation (1: Encrypt, 2: Decrypt, 0: Exit): ")
    if choice == '1':
        encryption_time = d.password1()
        if encryption_time is not None:
            print(f"Encryption successful. Time taken: {encryption_time:.4f} seconds")
    elif choice == '2':
        decryption_time = d.password2()
        if decryption_time is not None:
            print(f"Decryption successful. Time taken: {decryption_time:.4f} seconds")
    elif choice == '0':
        break
    else:
        print("Invalid choice.")

    method = input("Method compress 1,2,3,4: ")
    if method=="1":
         os.system("python Black_Hole_m1e.py")
    elif method=="2":
        os.system("python Black_Hole_m2e.py")
        
    elif method=="3":
        os.system("python Black_Hole_m3e.py")
        
    elif method=="4":
        os.system("python Black_Hole_m4e.py")            