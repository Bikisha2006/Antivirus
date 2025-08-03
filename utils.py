# utils.py
import os
import hashlib

def get_sha256_hash(file_path):
    """Return SHA-256 hash of a file."""
    try:
        with open(file_path, "rb") as f:
            bytes = f.read()
            return hashlib.sha256(bytes).hexdigest()
    except Exception as e:
        print(f"[!] Error reading file: {e}")
        return None

def get_files_in_directory(directory):
    """Return list of all files in directory (recursive)."""
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list