import os
import subprocess
from tkinter import messagebox


class FileHandler:
    def __init__(self, file_browser):
        self.file_browser = file_browser

    def create_review_environment(self, code, file_type="py"):
        """
        This function creates a file 'review_code' based on the file_type (default is 'py').
        """
        # Mapping of file type to extension
        file_extension_map = {
            "py": "review_code.py",
            "html": "review_code.html",
            "css": "review_code.css"
        }

        # Determine file name based on file type
        if file_type not in file_extension_map:
            raise ValueError(f"Unsupported file type: {file_type}")

        review_file_name = file_extension_map[file_type]
        review_file_path = os.path.join(self.file_browser.current_dir, review_file_name)

        with open(review_file_path, "w") as review_file:
            review_file.write(code)

    def run_and_test_code(self, error_handler):
        #try:
            #subprocess.run(["python3", review_file_path], check=True, capture_output=True)
            #messagebox.showinfo("Success", "Code ran successfully without errors!")
            #error_handler.finalize_code()

        #except subprocess.CalledProcessError as e:
            #error_message = e.stderr.decode('utf-8')
            # error_handler.handle_error(error_message)
        error_handler.finalize_code()
