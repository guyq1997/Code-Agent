import os
from tkinter import messagebox

class ModelsHandler:
    def __init__(self, app_gui):
        self.app_gui = app_gui

    def handle_models_file(self):
        """
        This method is triggered when models.py is selected. It checks for models.py and handles prompt creation.
        """
        prompt=[
        {
            "role": "system", 
            "content": "You extract email addresses into JSON data."
        },
        {
            "role": "user", 
            "content":  f"You are helping me generate the models.py for a Django project.\n"
                        f"Generate the models.py with following logic:\n"
        }
    ],

        return prompt