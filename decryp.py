import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

# Specify the directory and key file path
DIRECTORY = "/home/project/test"
KEY_FILE = "encryption_key.bin"
PRIVATE_KEY_FILE = "private_key.pem"
PUBLIC_KEY_FILE = "public_key.pem"

# Decrypt file function using AES (existing functionality)
def decrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            nonce, tag, ciphertext = f.read(16), f.read(16), f.read()
        
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        
        with open(file_path, 'wb') as f:
            f.write(data)
        
        print(f"Decrypted {file_path} with AES")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

# Decrypt file function using RSA private key
def decrypt_file_with_private_key(file_path, private_key):
    try:
        with open(file_path, 'rb') as f:
            ciphertext = f.read()

        cipher = PKCS1_OAEP.new(private_key)  # Decrypt data using RSA private key with OAEP padding
        data = cipher.decrypt(ciphertext)
        
        with open(file_path, 'wb') as f:
            f.write(data)  # Write the decrypted data
        
        print(f"Decrypted {file_path} with RSA private key.")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

# Decrypt all files in the specified directory using AES and RSA
def decrypt_directory(directory, key, private_key=None):
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return
    
    print(f"Decrypting files in directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)  # AES decryption for each file

            if private_key:
                decrypt_file_with_private_key(file_path, private_key)  # RSA decryption for each file (if private_key is provided)
    print("Decryption complete.")

# Load RSA private key
def load_rsa_private_key():
    try:
        with open(PRIVATE_KEY_FILE, 'rb') as f:
            private_key = RSA.import_key(f.read())  # Import the RSA private key
        print(f"Private key loaded from {PRIVATE_KEY_FILE}")
        return private_key
    except FileNotFoundError:
        print(f"Private key file not found: {PRIVATE_KEY_FILE}")
        return None

# Main function to load key and decrypt directory
def main():
    try:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()  # Load the AES encryption key from file
        print(f"Loaded encryption key from {KEY_FILE}")
    except FileNotFoundError:
        print(f"Key file not found: {KEY_FILE}")
        return
    
    private_key = load_rsa_private_key()  # Load the RSA private key

    decrypt_directory(DIRECTORY, key, private_key)  # Decrypt directory with AES key and RSA private key

if __name__ == "__main__":
    main()

