import os
import subprocess
from tkinter import messagebox


class FileHandler:
    def __init__(self, file_browser):
        self.file_browser = file_browser

    def create_review_environment(self, code):
        review_file_path = os.path.join(self.file_browser.current_dir, "review_code.py")
        with open(review_file_path, "w") as review_file:
            review_file.write(code)

    def run_and_test_code(self, error_handler):
        review_file_path = os.path.join(self.file_browser.current_dir, "review_code.py")

        try:
            subprocess.run(["python3", review_file_path], check=True, capture_output=True)
            messagebox.showinfo("Success", "Code ran successfully without errors!")
            error_handler.finalize_code()

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode('utf-8')
            # error_handler.handle_error(error_message)
            error_handler.finalize_code()
