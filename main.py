# main.py
import tkinter as tk
from gui import AntivirusGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = AntivirusGUI(root)
    root.mainloop()