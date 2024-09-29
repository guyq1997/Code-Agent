import os
from tkinter import messagebox

class HTMLHandler:

    def __init__(self, app_gui):
        self.app_gui = app_gui

    def handle_html_file(self):
        """
        This method is triggered when views.py is selected. It checks for models.py and handles prompt creation.
        """
        project_directory = self.app_gui.file_browser.current_dir
        models_file = os.path.join(project_directory, "models.py")
        views_file = os.path.join(project_directory, "views.py")
        urls_file = os.path.join(project_directory, "urls.py")
        basehtml_file = os.path.join(project_directory, "templates/base.html")

        if not os.path.exists(models_file):
            messagebox.showerror("Error", "models.py not found in the project directory!")
            return
        if not os.path.exists(views_file):
            messagebox.showerror("Error", "views.py not found in the project directory!")
            return
        if not os.path.exists(urls_file):
            messagebox.showerror("Error", "urls.py not found in the project directory!")
            return
        if not os.path.exists(basehtml_file):
            messagebox.showerror("Error", "base html not found in the project directory!")
            return
               
        # Read the content of models.py to provide context to GPT
        with open(models_file, "r") as models:
            models_content = models.read()

        with open(views_file, "r") as views:
            views_content = views.read()

        with open(urls_file, "r") as urls:
            urls_content = urls.read()
            
        with open(basehtml_file, "r") as basehtml:
            basehtml_content = basehtml.read()

        
        # Prepare the prompt with the content of both files
        prompt_text = f"""
        Below are the contents of models.py, views.py, urls.py and base.html for a Django project. Based on these, generate a html file.

        -------------------models.py-------------------
        {models_content}
        -------------------end models.py----------------------------

        -------------------views.py--------------------
        {views_content}
        -------------------end views.py----------------------------

        -------------------urls.py--------------------
        {urls_content}
        -------------------end urls.py----------------------------

        -------------------base.html--------------------
        {basehtml_content}
        -------------------end base.html----------------------------

        Now generate the html file based on base.html with following requirements:
        """
        return prompt_text