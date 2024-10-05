import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font
from file_handler import FileHandler
from openai_client import OpenAIClient
from views_handler import ViewsHandler  # Import the new ViewsHandler
from models_handler import ModelsHandler # Import the new ViewsHandler
from urls_handler import UrlsHandler
from models_handler import ModelsHandler

class AppGUI:

    def __init__(self, root, file_browser):
        self.root = root
        self.file_browser = file_browser
        self.current_selection = ""

        self.file_handler = FileHandler(file_browser)
        self.openai_client = OpenAIClient()
        self.views_handler = ViewsHandler(self)  # Instantiate the ViewsHandler
        self.models_handler = ModelsHandler(self)  # Instantiate the ViewsHandler
        self.urls_handler = UrlsHandler(self)


        self.setup_fonts()
        self.setup_ui()

    def setup_fonts(self):
        # Set up custom fonts
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Helvetica", size=12)
        
        self.text_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.input_font = font.Font(family="Helvetica", size=12)  # Larger font for input areas

    def setup_ui(self):
        self.root.title("Python Repo Browser")
        self.root.geometry("1200x800")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.choose_button = tk.Button(self.top_frame, text="Choose Project", command=self.choose_directory)
        self.choose_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.file_label = tk.Label(self.top_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.back_button = tk.Button(self.left_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.file_listbox = tk.Listbox(self.left_frame)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.file_listbox.bind("<Double-Button-1>", self.open_item)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Non-editable label for pre-defined prompt
        self.predefined_prompt_label = tk.Label(self.main_frame, text="Pre-defined Prompt:", anchor="w")
        self.predefined_prompt_label.pack(anchor=tk.NW, padx=5, pady=5)

        self.predefined_prompt = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=120, height=20, state="disabled", bg="lightgrey", font=self.input_font)
        self.predefined_prompt.pack(fill=tk.X,padx=10, pady=5)

        self.input_text = tk.Label(self.main_frame, text="Type your prompt below:")
        self.input_text.pack(anchor=tk.NW, padx=5, pady=5)

        self.scrolled_text = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=120, height=10, font=self.input_font)
        self.scrolled_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.submit_button = tk.Button(self.main_frame, text="Submit Prompt", command=self.submit_prompt, font=self.button_font)
        self.submit_button.pack(padx=5, pady=5)

    def choose_directory(self):
        """
        Let the user select a directory and update the file list.
        Also, set this as the root work directory in the FileBrowser.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.file_browser.set_root_directory(directory)  # Set the root work directory
            self.update_file_list(directory)

    def update_file_list(self, directory):
        files = self.file_browser.list_files(directory)
        self.file_listbox.delete(0, tk.END)
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def open_item(self, event):
        selected_item = self.file_listbox.get(self.file_listbox.curselection())
        if selected_item.startswith("DIR: "):
            directory_name = selected_item[5:]
            files = self.file_browser.open_directory(directory_name)
            self.file_listbox.delete(0, tk.END)
            for file in files:
                self.file_listbox.insert(tk.END, file)
        else:
            self.file_label.config(text=f"{selected_item} is selected!")
            self.current_selection = selected_item
            self.update_predefined_prompt()

    def go_back(self):
        files = self.file_browser.go_back()
        self.file_listbox.delete(0, tk.END)
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def update_predefined_prompt(self):
        """
        Update the predefined prompt based on the currently selected file.
        """
        handlers = {
            "models.py": self.models_handler.models_prompt,
            "views.py": self.views_handler.views_prompt,
            "urls.py": self.urls_handler.urls_prompt
        }

        if self.current_selection in handlers:
            prompt_func = handlers[self.current_selection]
            prompt = prompt_func()
            
            preprompt_system = prompt[0]["content"]
            preprompt_user = prompt[1]["content"]
            preprompt_text = f"System:\n{preprompt_system}\n\n\nUser:\n{preprompt_user}"
        else:
            preprompt_text = "Not a valid file"

        self.predefined_prompt.config(state="normal")
        self.predefined_prompt.delete(1.0, tk.END)
        self.predefined_prompt.insert(tk.END, preprompt_text)
        self.predefined_prompt.config(state="disabled")


    def submit_prompt(self):
        """
        Submit the prompt to OpenAI API, including the content of the selected file (if it exists).
        """
        input_text = self.scrolled_text.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showerror("Error", "Prompt cannot be empty!")
            return

        if not self.current_selection:
            messagebox.showerror("Error", "No file selected!")
            return

        handlers = {
            "models.py": (self.models_handler.models_prompt, self.models_handler.finalize_modelspy),
            "views.py": (self.views_handler.views_prompt, self.views_handler.finalize_viewspy),
            "urls.py": (self.urls_handler.urls_prompt, self.urls_handler.finalize_urlspy)
        }

        if self.current_selection not in handlers:
            messagebox.showerror("Error", "Unsupported file type!")
            return

        prompt_func, finalize_func = handlers[self.current_selection]
        prompt = prompt_func()
        prompt += input_text

        try:
            code_response = self.openai_client.send_to_openai(prompt)
            extracted_code = self.openai_client.extract_code(code_response)
            self.file_handler.create_review_environment(extracted_code)
            finalize_func()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return
            


