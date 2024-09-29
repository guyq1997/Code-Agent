import tkinter as tk
from file_browser import FileBrowser
from app_gui import AppGUI

def main():
    root = tk.Tk()
    file_browser = FileBrowser()
    app = AppGUI(root, file_browser)
    root.mainloop()

if __name__ == "__main__":
    main()
