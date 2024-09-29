import os
from tkinter import messagebox

class URLHandler:

    def __init__(self, app_gui):
        self.app_gui = app_gui

    def handle_urls_file(self):
        """
        This method is triggered when views.py is selected. It checks for models.py and handles prompt creation.
        """
        project_directory = self.app_gui.file_browser.current_dir
        models_file = os.path.join(project_directory, "models.py")
        views_file = os.path.join(project_directory, "views.py")

        if not os.path.exists(models_file):
            messagebox.showerror("Error", "models.py not found in the project directory!")
            return
        if not os.path.exists(views_file):
            messagebox.showerror("Error", "views.py not found in the project directory!")
            return
        
        # Read the content of models.py to provide context to GPT
        with open(models_file, "r") as models:
            models_content = models.read()

        # Read the content of models.py to provide context to GPT
        with open(views_file, "r") as views:
            views_content = views.read()

        # Prepare the prompt with the content of both files
        prompt_text = f"""
        Below are the contents of models.py and views.py for a Django project. Based on these, generate a urls.py file that maps the views to the appropriate URLs.

        -------------------models.py-------------------
        {models_content}
        -------------------end models.py----------------------------

        -------------------views.py--------------------
        {views_content}
        -------------------end views.py----------------------------

        Now generate the urls.py file that connects these views with URLs.
        """
        return prompt_text
