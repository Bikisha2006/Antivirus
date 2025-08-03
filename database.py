# database.py
import json
import os

MALWARE_DB = "malware_hashes.json"

def load_malware_hashes():
    if not os.path.exists(MALWARE_DB):
        print(f"[!] Malware database not found: {MALWARE_DB}")
        return []
    with open(MALWARE_DB, "r") as f:
        return json.load(f).get("malware_hashes", [])