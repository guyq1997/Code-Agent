import os
from tkinter import messagebox


class FileHandler:
    def __init__(self, file_browser):
        self.file_browser = file_browser

    def create_review_environment(self, scriptname, code):
        """
        This function creates a file 'review_code' based on the file name.
        """

        review_file_name = ["review_" + name for name in scriptname]
        review_file_path = [os.path.join(self.file_browser.root_dir, filename) for filename in review_file_name]

        for file_path in review_file_path:
            with open(file_path, "w") as review_file:
                review_file.write(code)