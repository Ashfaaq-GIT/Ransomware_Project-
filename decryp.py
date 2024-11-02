import os
from Crypto.Cipher import AES

# Specify the directory and key file path
DIRECTORY = "/home/project/test"
KEY_FILE = "encryption_key.bin"

# Decrypt file function
def decrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            nonce, tag, ciphertext = f.read(16), f.read(16), f.read()
        
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        
        with open(file_path, 'wb') as f:
            f.write(data)
        
        print(f"Decrypted {file_path}")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

# Decrypt all files in the specified directory
def decrypt_directory(directory, key):
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return
    
    print(f"Decrypting files in directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)
    print("Decryption complete.")

# Main function to load key and decrypt directory
def main():
    try:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()  # Load the encryption key from file
        print(f"Loaded encryption key from {KEY_FILE}")
    except FileNotFoundError:
        print(f"Key file not found: {KEY_FILE}")
        return
    
    decrypt_directory(DIRECTORY, key)

if __name__ == "__main__":
    main()

