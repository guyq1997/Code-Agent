import os
from tkinter import messagebox

class HTMLHandler:

    def __init__(self, app_gui):
        self.app_gui = app_gui

    def handle_html_file(self):
        """
        This method is triggered when views.py is selected. It checks for models.py and handles prompt creation.
        """
        project_directory = self.app_gui.file_browser.root_dir
        models_file = os.path.join(project_directory, "models.py")
        views_file = os.path.join(project_directory, "views.py")
        urls_file = os.path.join(project_directory, "urls.py")
        basehtml_file = os.path.join(project_directory, "templates/base_dashboard.html")
        style_file = os.path.join(project_directory, "static/css/styles.css")

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
        if not os.path.exists(style_file):
            messagebox.showerror("Error", "style file not found in the project directory!")
            return
                              
        # Read the content of models.py to provide context to GPT
        with open(models_file, "r") as models:
            models_content = models.read()

        with open(views_file, "r") as views:
            views_content = views.read()

        with open(urls_file, "r") as urls:
            urls_content = urls.read()
            
        with open(basehtml_file, "r", encoding="utf-8") as basehtml:
            basehtml_content = basehtml.read()
            
        with open(style_file, "r") as style:
            style_content = style.read()
        
        # Prepare the prompt with the content of both files
        prompt_text = f"""
        Below are the contents of models.py, views.py, urls.py, base_dashboard.html and styles.css for a Django project.

        -------------------models.py-------------------
        {models_content}
        -------------------end models.py----------------------------

        -------------------views.py--------------------
        {views_content}
        -------------------end views.py----------------------------

        -------------------urls.py--------------------
        {urls_content}
        -------------------end urls.py----------------------------

        -------------------base_dashboard.html--------------------
        {basehtml_content}
        -------------------end base_dashboard.html----------------------------

        -------------------style.css--------------------
        {style_content}
        -------------------end style.css----------------------------

        Help me generate an entire and complete html file based on provided context above. Give me the whole styles.css if modification on styles.css is necessary. 
        Please realize following requirements:
        """
        return prompt_text