# quarantine.py
import os
import shutil

QUARANTINE_DIR = "quarantine/"

def move_to_quarantine(file_path):
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    try:
        shutil.move(file_path, os.path.join(QUARANTINE_DIR, os.path.basename(file_path)))
        return True
    except Exception as e:
        print(f"[!] Error moving file to quarantine: {e}")
        return False