import os

class FileBrowser:
    def __init__(self):
        self.current_dir = os.getcwd()

    def list_files(self, directory=None):
        """
        List the files and subdirectories in the given directory.
        If no directory is provided, it will use the current directory.
        """
        if directory:
            self.current_dir = directory
        try:
            items = os.listdir(self.current_dir)
            items.sort()
            dirs = ['DIR: ' + item for item in items if os.path.isdir(os.path.join(self.current_dir, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_dir, item))]
            return dirs + files
        except Exception as e:
            return [f"Error: {str(e)}"]

    def open_directory(self, subdirectory):
        """
        Navigate to the selected subdirectory.
        """
        self.current_dir = os.path.join(self.current_dir, subdirectory)
        return self.list_files()

    def go_back(self):
        """
        Go back to the parent directory.
        """
        self.current_dir = os.path.dirname(self.current_dir)
        return self.list_files()
