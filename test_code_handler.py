import os
from tkinter import messagebox

class TestCodeHandler:
    def __init__(self, app_gui):
        self.app_gui = app_gui

    def Test_and_finalize_Code(self, error_message ):
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