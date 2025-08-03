# scanner.py
from utils import get_sha256_hash, get_files_in_directory
from database import load_malware_hashes


def scan_file(file_path):
    file_hash = get_sha256_hash(file_path)
    if not file_hash:
        return {"file": file_path, "status": "error", "hash": None}

    malware_hashes = load_malware_hashes()
    if file_hash in malware_hashes:
        return {"file": file_path, "status": "infected", "hash": file_hash}
    else:
        return {"file": file_path, "status": "clean", "hash": file_hash}


def scan_directory(directory):
    results = []
    files = get_files_in_directory(directory)
    for file in files:
        result = scan_file(file)
        results.append(result)
    return results