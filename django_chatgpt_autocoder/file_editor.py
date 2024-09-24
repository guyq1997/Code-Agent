import os

def read_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def update_file(file_path, new_content):
    with open(file_path, 'w') as f:
        f.write(new_content)
        print(f"Updated {file_path} successfully!")
