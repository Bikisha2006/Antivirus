# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from scanner import scan_directory
from quarantine import move_to_quarantine

class AntivirusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Antivirus Scanner")
        self.root.geometry("600x400")

        # GUI Elements
        self.path_label = tk.Label(root, text="Select folder to scan:")
        self.path_label.pack(pady=10)

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        self.scan_button = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.scan_button.pack(pady=10)

        self.results_box = tk.Listbox(root, width=80, height=15)
        self.results_box.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def start_scan(self):
        folder = self.path_entry.get()
        if not os.path.exists(folder):
            messagebox.showerror("Error", "Invalid folder path.")
            return

        self.results_box.delete(0, tk.END)
        scan_results = scan_directory(folder)

        for result in scan_results:
            status = result["status"]
            file = result["file"]
            hash_val = result["hash"][:10] + "..." if result["hash"] else ""

            if status == "infected":
                self.results_box.insert(tk.END, f"[INFECTED] {file} (Hash: {hash_val})")
                self.results_box.itemconfig(tk.END, bg="red", fg="white")
            elif status == "clean":
                self.results_box.insert(tk.END, f"[CLEAN] {file}")
            elif status == "error":
                self.results_box.insert(tk.END, f"[ERROR] {file}")
                self.results_box.itemconfig(tk.END, fg="red")

        if any(r["status"] == "infected" for r in scan_results):
            prompt = messagebox.askyesno("Scan Complete", "Malware found! Move infected files to quarantine?")
            if prompt:
                for r in scan_results:
                    if r["status"] == "infected":
                        if move_to_quarantine(r["file"]):
                            print(f"[+] Moved {r['file']} to quarantine")