import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font
from file_handler import FileHandler
from openai_client import OpenAIClient
from error_handler import ErrorHandler
from views_handler import ViewsHandler  # Import the new ViewsHandler
from models_handler import ModelsHandler # Import the new ViewsHandler
from urls_handler import URLHandler
from html_handler import HTMLHandler

class AppGUI:

    def __init__(self, root, file_browser):
        self.root = root
        self.file_browser = file_browser
        self.current_selection = ""

        self.file_handler = FileHandler(file_browser)
        self.openai_client = OpenAIClient()
        self.error_handler = ErrorHandler(self)
        self.views_handler = ViewsHandler(self)  # Instantiate the ViewsHandler
        self.models_handler = ModelsHandler(self)  # Instantiate the ViewsHandler
        self.urls_handler = URLHandler(self)
        self.html_handler = HTMLHandler(self)

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

        # Check if the selected file is views.py
        if self.current_selection == "views.py":
            preprompt_text = self.views_handler.handle_views_file()
            
        elif self.current_selection == "models.py":
            preprompt_text = self.models_handler.handle_models_file()
        elif self.current_selection == "urls.py":
            preprompt_text = self.urls_handler.handle_urls_file()
        elif self.current_selection.endswith(".html"):
            preprompt_text = self.html_handler.handle_html_file()

        preprompt_text += "[Type the requirements in the following Input Area]"
       # Check if the selected file has existing content
        selected_file_path = os.path.join(self.file_browser.current_dir, self.current_selection)
        if os.path.isfile(selected_file_path):
            with open(selected_file_path, "r") as selected_file:
                existing_code = selected_file.read().strip()

            # If the file has existing code, append it to the prompt
            if len(existing_code) > 20:
                preprompt_text += f"\n\n\nPlease optimize this current code to realize my requirements:\n\n"
                preprompt_text += f"---------------------Existing Code Snippet----------------------------\n"
                preprompt_text += f"{existing_code}\n\n"
                
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

        # Initialize the prompt with the handler for the selected file
        if self.current_selection == "views.py":
            prompt_text = self.views_handler.handle_views_file()
        elif self.current_selection == "models.py":
            prompt_text = self.models_handler.handle_models_file()
        elif self.current_selection == "urls.py":
            prompt_text = self.urls_handler.handle_urls_file()
        elif self.current_selection.endswith(".html"):
            prompt_text = self.html_handler.handle_html_file()
        else:
            messagebox.showerror("Error", "Unsupported file type!")
            return

        # Append the input text to the prompt
        prompt_text += input_text

        # Check if the selected file has existing content
        selected_file_path = os.path.join(self.file_browser.current_dir, self.current_selection)
        if os.path.isfile(selected_file_path):
            with open(selected_file_path, "r") as selected_file:
                existing_code = selected_file.read().strip()

            # If the file has existing code, append it to the prompt
            if len(existing_code) > 20:
                prompt_text += f"\n\n# Please optimize this current code to realize my requirements:\n{existing_code}"

        # Call OpenAI API and get the response with the modified prompt
        code_response = self.openai_client.send_to_openai(prompt_text)

        # Extract the appropriate code based on the file type
        if self.current_selection.endswith(".py"):
            try:
                # Extract Python code
                extracted_code = self.openai_client.extract_python_code(code_response)

                # Create a test environment with the generated code
                self.file_handler.create_review_environment(extracted_code,file_type="py")

                # Run the generated code and handle errors
                self.file_handler.run_and_test_code(self.error_handler)
            except:
                messagebox.showerror("Error", "No python code extracted from the response!")

        elif self.current_selection.endswith(".html"):
            try:
                # Extract HTML code
                extracted_code = self.openai_client.extract_html_code(code_response)
                self.file_handler.create_review_environment(extracted_code,file_type="html")
                self.file_handler.run_and_test_code(self.error_handler)
            except:
                messagebox.showerror("Error", "No html code extracted from the response!")

            try:
                html_file = self.current_selection
                extracted_css_code = self.openai_client.extract_css_code(code_response)
                self.file_handler.create_review_environment(extracted_css_code,file_type="css")
                self.current_selection = os.path.join(self.file_browser.root_dir , "static/css/styles.css")
                self.file_handler.run_and_test_code(self.error_handler)
                self.current_selection = html_file
            except:
                messagebox.showerror("Error", "No CSS code extracted from the response! (No CSS code changes needed for this requirenment on html)")


        elif self.current_selection.endswith(".css"):
            try:
                # Extract CSS code
                extracted_code = self.openai_client.extract_css_code(code_response)

                # Create a test environment with the generated code
                self.file_handler.create_review_environment(extracted_code,file_type="css")

                # Run the generated code and handle errors
                self.file_handler.run_and_test_code(self.error_handler)
            except:
                messagebox.showerror("Error", "No python code extracted from the response!")

        else:
            messagebox.showerror("Error", "Unsupported file type for code extraction!")
            return

