import os
import shutil
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import time
from datetime import datetime

# Directories
SOURCE_DIR = "/home/project/test"
BACKUP_DIR = "/home/project/Project/Backup"
KEY_FILE = "encryption_key.bin"  # Path to save the encryption key


def backup_files(source_dir, backup_dir):
    """Backup all files from source_dir to backup_dir."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            src_file = os.path.join(root, file)
            backup_file = os.path.join(backup_dir, file)

            # Skip if already exists in the backup folder
            if not os.path.exists(backup_file):
                shutil.copy2(src_file, backup_file)
                print(f"Backed up: {src_file} to {backup_file}")
            else:
                print(f"File already exists in backup: {backup_file}")


def encrypt_file(file_path, key):
    """Encrypt a single file."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        with open(file_path, 'wb') as f:
            f.write(cipher.nonce + tag + ciphertext)

        print(f"Encrypted: {file_path}")
    except Exception as e:
        print(f"Failed to encrypt {file_path}: {e}")


def decrypt_file(file_path, key):
    """Decrypt a single file."""
    try:
        with open(file_path, 'rb') as f:
            nonce, tag, ciphertext = f.read(16), f.read(16), f.read()

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

        with open(file_path, 'wb') as f:
            f.write(data)

        print(f"Decrypted: {file_path}")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")


def decrypt_backup_files(backup_dir, key):
    """Decrypt all encrypted files in the backup directory."""
    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)


def encrypt_directory(directory, key):
    """Encrypt all files in a directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)


def main():
    # Generate encryption key
    key = get_random_bytes(32)  # AES-256
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    print(f"Encryption key saved to {KEY_FILE}")

    # Step 1: Backup files before encryption
    print("Backing up files...")
    backup_files(SOURCE_DIR, BACKUP_DIR)

    # Step 2: Decrypt backup files if they are encrypted
    print("Decrypting backup files...")
    decrypt_backup_files(BACKUP_DIR, key)

    # Step 3: Encrypt the files in the test directory
    print("Encrypting files in the test directory...")
    encrypt_directory(SOURCE_DIR, key)

    print("Encryption process completed.")


if __name__ == "__main__":
    main()

