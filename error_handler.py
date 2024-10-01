import os
from tkinter import messagebox

class ErrorHandler:
    def __init__(self, app_gui):
        self.app_gui = app_gui

    def handle_error(self, error_message):
        # Path to the review_code.py file
        review_file_path = os.path.join(self.app_gui.file_browser.current_dir, "review_code.py")
        
        # Read the generated code from review_code.py
        with open(review_file_path, "r") as review_file:
            generated_code = review_file.read()

        # Construct the retry prompt with the error message and the generated code
        retry_prompt = (
            f"The following error occurred in the code: {error_message}\n"
            "Can you fix it?\n\n"
            "Generated code:\n\n"
            f"{generated_code.strip()}"
        )
        
        # Display the retry prompt in the GUI text area
        # self.app_gui.scrolled_text.delete("1.0", "end")
        self.app_gui.scrolled_text.insert("end", retry_prompt)

        # Ask the user whether to send the retry prompt or finalize the current code
        confirm_send = messagebox.askyesno("Retry or Finalize", "Do you want to send the retry prompt or finalize the current code?")
        
        if confirm_send:
            # Send the retry prompt to OpenAI for a fix
            code_response = self.app_gui.openai_client.send_to_openai(retry_prompt)
            python_code = self.app_gui.openai_client.extract_python_code(code_response)

            # Update the review_code.py file with the new generated code
            self.app_gui.file_handler.create_review_environment(python_code)

            # Re-run the corrected code
            self.app_gui.file_handler.run_and_test_code(self)
        else:
            # Finalize the current code without retrying
            self.finalize_code()


    def finalize_code(self): 
        confirm = messagebox.askyesno("Finalize", "Do you want to paste the generated code into the selected file?")
        if confirm:
            selected_file_path = os.path.join(self.app_gui.file_browser.current_dir, self.app_gui.current_selection)

            # Infer the file extension from the selected file
            _, file_extension = os.path.splitext(self.app_gui.current_selection)
            file_extension = file_extension.lower()  # Handle case sensitivity

            # Determine the review file path based on the selected file type
            if file_extension == ".py":
                review_file_name = "review_code.py"
            elif file_extension == ".html":
                review_file_name = "review_code.html"
            elif file_extension == ".css":
                review_file_name = "review_code.css"
            else:
                messagebox.showerror("Error", "Unsupported file format. Only .py, .html, and .css are supported.")
                return

            review_file_path = os.path.join(self.app_gui.file_browser.current_dir, review_file_name)
            # Read from the appropriate review file and write to the selected file

            try:
                with open(review_file_path, "r") as review_file:
                    generated_code = review_file.read()

                with open(selected_file_path, "w") as selected_file:
                    selected_file.write(generated_code)

                messagebox.showinfo("Success", f"Code has been pasted into {self.app_gui.current_selection}!")

            except FileNotFoundError:
                messagebox.showerror("Error", f"Review file '{review_file_name}' not found. Please generate code first.")