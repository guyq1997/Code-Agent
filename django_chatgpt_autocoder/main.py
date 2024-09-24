import os
from .env_setup import load_env_vars
from .gpt_interaction import get_gpt_response
from .file_editor import update_file

def run():
    load_env_vars()  # Load environment variables

    project_dir = os.getenv("PROJECT_DIR")
    
    while True:
        # Get user input for which file to edit and the prompt
        file_name = input("Enter the file you want to edit (e.g., views.py, models.py, template.html): ")
        file_path = os.path.join(project_dir, file_name)
        
        if not os.path.exists(file_path):
            print(f"Error: {file_name} does not exist in {project_dir}")
            continue
        
        prompt = input(f"Describe the changes you want to make to {file_name}: ")
        
        # Get the response from GPT and update the file
        existing_files = [file_path] if os.path.exists(file_path) else []
        gpt_response = get_gpt_response(prompt, existing_files)
        
        print(f"Generated code:\n{gpt_response}\n")
        
        # Update the file with generated code
        update_file(file_path, gpt_response)

        # Wait for next prompt
        more = input("Do you want to edit another file? (y/n): ")
        if more.lower() != 'y':
            break

