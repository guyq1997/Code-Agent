import os
from tkinter import messagebox

class UrlsHandler:
    """
    A class to handle operations related to URL configurations in a Django project.

    This class provides methods to read file contents and create prompts for GPT
    to generate appropriate URL configurations based on models and views.
    """

    def __init__(self, app_gui):
        """
        Initialize the URLHandler.

        Args:
            app_gui: The main application GUI object.
        """
        self.app_gui = app_gui
        self.project_directory = app_gui.file_browser.root_dir

    def read_file_content(self, file_path):
        """
        Read and return the content of a file.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The content of the file if successful, None otherwise.
        """
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"{os.path.basename(file_path)} not found in the project directory!")
            return None
        with open(file_path, "r") as file:
            return file.read()

    def urls_prompt(self):
        """
        Create and return the prompt for GPT to generate URLs.

        This method generates a prompt for GPT by combining the content of models.py and views.py,
        along with instructions to generate appropriate URL configurations in urls.py.

        Returns:
            list: A list of dictionaries representing the prompt for GPT.
        """
        models_path = os.path.join(self.project_directory, "backend/LabManagement/models.py")
        views_path = os.path.join(self.project_directory, "backend/LabManagement/views.py")
        urls_path = os.path.join(self.project_directory, "backend/LabManagement/urls.py")

        models_content = self.read_file_content(models_path)
        views_content = self.read_file_content(views_path)
        urls_content = self.read_file_content(urls_path)


        prompt = [
            {
                "role": "system",
                "content": "You are a code assistant helping with Django framework scripts. "
                           "You will be provided with existing models.py, views.py and urls.py code (delimited with XML tags). "
                           "First, review the existing code and understand the user requirements. "
                           "Then modify the urls.py code step by step to meet the requirements. "
                           "Finally, generate the entire urls.py code."
            },
            {
                "role": "user",
                "content": f"<existing_models_py_code>\n{models_content}\n</existing_models_py_code>\n"
                           f"<existing_views_py_code>\n{views_content}\n</existing_views_py_code>\n"
                           f"<existing_urls_py_code>\n{urls_content}\n</existing_urls_py_code>\n"
                           f"Based on these models and views, generate a urls.py file that connects these views with appropriate URLs.\n"
            }
        ]

        return prompt
    
    def finalize_urlspy(self):
        """
        Finalize the generated views.py code.

        This method prompts the user to confirm if they want to paste the generated
        views.py code into the selected file. If confirmed, it reads the generated
        code from a review file and writes it to the selected file.
        """
        confirm = messagebox.askyesno("Finalize", "Do you want to paste the generated urls.py into the selected file?")
        if confirm:
            selected_file_path = os.path.join(self.app_gui.file_browser.current_dir, self.app_gui.current_selection)

            review_file_path = os.path.join(self.app_gui.file_browser.root_dir, "review_urls.py")
            # Read from the appropriate review file and write to the selected file

            try:
                with open(review_file_path, "r") as review_file:
                    generated_code = review_file.read()

                with open(selected_file_path, "w") as selected_file:
                    selected_file.write(generated_code)

                messagebox.showinfo("Success", f"Code has been pasted into {self.app_gui.current_selection}!")

            except FileNotFoundError:
                messagebox.showerror("Error", f"Review file review_urls.py not found. Please generate code first.")