import os
from dotenv import load_dotenv

def load_env_vars():
    load_dotenv()  # Load environment variables from .env file if it exists
    
    
    openai_key = os.getenv("OPENAI_API_KEY")
    project_dir = os.getenv("PROJECT_DIR")

    
    if not openai_key:
        raise EnvironmentError("OPENAI_API_KEY is not set")
    
    if not project_dir or not os.path.exists(project_dir):
        raise EnvironmentError("PROJECT_DIR is not set or the directory does not exist")
    
