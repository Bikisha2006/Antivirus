import unittest
import os
import shutil
import json
from utils import get_sha256_hash, get_files_in_directory
from scanner import scan_file, scan_directory
from quarantine import move_to_quarantine
from database import load_malware_hashes

TEST_DIR = "test_samples"
QUARANTINE_DIR = "quarantine"
CLEAN_FILE = os.path.join(TEST_DIR, "clean.txt")
INFECTED_FILE = os.path.join(TEST_DIR, "infected.txt")
MALWARE_DB = "malware_hashes.json"

class TestAntivirus(unittest.TestCase):

    def setUp(self):
        # Clean test folders before each test
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        if os.path.exists(QUARANTINE_DIR):
            shutil.rmtree(QUARANTINE_DIR)
        if os.path.exists(MALWARE_DB):
            os.remove(MALWARE_DB)

        os.makedirs(TEST_DIR, exist_ok=True)
        os.makedirs(QUARANTINE_DIR, exist_ok=True)

        # Create files
        with open(CLEAN_FILE, "w") as f:
            f.write("This is a clean file.")

        with open(INFECTED_FILE, "w") as f:
            f.write("This file is malware!")

        # Add infected hash to DB
        infected_hash = get_sha256_hash(INFECTED_FILE)
        with open(MALWARE_DB, "w") as f:
            json.dump({"malware_hashes": [infected_hash]}, f)

    def test_get_sha256_hash(self):
        hash_val = get_sha256_hash(CLEAN_FILE)
        self.assertIsInstance(hash_val, str)
        self.assertEqual(len(hash_val), 64)

    def test_get_files_in_directory(self):
        files = get_files_in_directory(TEST_DIR)
        self.assertIn(CLEAN_FILE, files)
        self.assertIn(INFECTED_FILE, files)

    def test_scan_file_clean(self):
        result = scan_file(CLEAN_FILE)
        self.assertEqual(result["status"], "clean")

    def test_scan_file_infected(self):
        result = scan_file(INFECTED_FILE)
        self.assertEqual(result["status"], "infected")

    def test_scan_directory(self):
        results = scan_directory(TEST_DIR)
        statuses = [r["status"] for r in results]
        self.assertIn("infected", statuses)
        self.assertIn("clean", statuses)

    def test_move_to_quarantine(self):
        move_to_quarantine(INFECTED_FILE)
        quarantined_path = os.path.join(QUARANTINE_DIR, "infected.txt")
        self.assertTrue(os.path.exists(quarantined_path))

    def test_load_malware_hashes(self):
        move_to_quarantine(INFECTED_FILE)
        new_path = os.path.join(QUARANTINE_DIR, "infected.txt")
        quarantine_hash = get_sha256_hash(new_path)
        hashes = load_malware_hashes()
        self.assertIn(quarantine_hash, hashes)

    def tearDown(self):
        # Optional: clean up everything after each test
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        shutil.rmtree(QUARANTINE_DIR, ignore_errors=True)
        if os.path.exists(MALWARE_DB):
            os.remove(MALWARE_DB)

if __name__ == "__main__":
    unittest.main()
    