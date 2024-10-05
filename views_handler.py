import os
from tkinter import messagebox

class ViewsHandler:
    """
    A class to handle operations related to views in a Django project.

    This class provides methods to read file contents, create prompts for GPT,
    and handle interactions between the GUI and the backend.
    """

    def __init__(self, app_gui):
        """
        Initialize the ViewsHandler.

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

    def views_prompt(self, models_content, views_content):
        """
        Create and return the prompt for GPT.

        This method generates a prompt for GPT by combining the content of models.py and views.py,
        along with system instructions and user requirements.

        Args:
            models_content (str): The content of the models.py file.
            views_content (str): The content of the views.py file.

        Returns:
            list: A list of dictionaries representing the prompt for GPT.
        """
        models_path = os.path.join(self.project_directory, "backend/LabManagement/models.py")
        models_content = self.read_file_content(models_path)        

        views_path = os.path.join(self.app_gui.file_browser.current_dir, self.app_gui.current_selection)
        views_content = self.read_file_content(views_path)
        
        prompt = [
            {
                "role": "system", 
                "content": "You are a code assistant helping with Django framework scripts. "
                           "You will be provided with existing models.py and views.py code (delimited with XML tags). "
                           "First, review the existing code and understand the user requirements. "
                           "Then modify the views.py code step by step to meet the requirements. "
                           "Finally, generate the entire views.py code."
            },
            {
                "role": "user", 
                "content": f"<existing_models_py_code>\n{models_content}\n</existing_models_py_code>\n"
                           f"<existing_views_py_code>\n{views_content}\n</existing_views_py_code>\n"
                           f"Optimize current views.py with following requirements:\n"
            }
        ]

        return prompt
    
    def finalize_viewspy(self):
        """
        Finalize the generated views.py code.

        This method prompts the user to confirm if they want to paste the generated
        views.py code into the selected file. If confirmed, it reads the generated
        code from a review file and writes it to the selected file.
        """
        confirm = messagebox.askyesno("Finalize", "Do you want to paste the generated views.py into the selected file?")
        if confirm:
            selected_file_path = os.path.join(self.app_gui.file_browser.current_dir, self.app_gui.current_selection)

            review_file_path = os.path.join(self.app_gui.file_browser.root_dir, "review_views.py")
            # Read from the appropriate review file and write to the selected file

            try:
                with open(review_file_path, "r") as review_file:
                    generated_code = review_file.read()

                with open(selected_file_path, "w") as selected_file:
                    selected_file.write(generated_code)

                messagebox.showinfo("Success", f"Code has been pasted into {self.app_gui.current_selection}!")

            except FileNotFoundError:
                messagebox.showerror("Error", f"Review file review_views.py not found. Please generate code first.")