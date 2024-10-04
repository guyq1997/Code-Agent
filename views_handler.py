import os
from tkinter import messagebox

class ViewsHandler:
    def __init__(self, app_gui):
        self.app_gui = app_gui

    def handle_views_file(self):
        """
        This method is triggered when views.py is selected. It checks for models.py and handles prompt creation.
        """
        project_directory = self.app_gui.file_browser.root_dir
        models_file = os.path.join(project_directory, "backend/LabManagement/models.py")

        if not os.path.exists(models_file):
            messagebox.showerror("Error", "models.py not found in the project directory!")
            return

        # Read the content of models.py to provide context to GPT
        with open(models_file, "r") as models:
            models_content = models.read()

        # Add models.py content to the prompt for more context
        prompt_text = (
            f"You are helping me generate the views.py for a Django project. "
            f"The models.py file contains the following code:\n\n"
            f"-------------------models.py------------------\n"
            f"{models_content}\n"
            f"-------------------end models.py---------------------------\n\n"
            f"Based on this, generate the views.py with following logic:\n"
        )

        return prompt_text
