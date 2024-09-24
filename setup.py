from setuptools import setup, find_packages

setup(
    name="django_chatgpt_autocoder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",  # For ChatGPT interaction
        "python-dotenv",  # For environment variable handling
    ],
    entry_points={
        'console_scripts': [
            'autocoder = django_chatgpt_autocoder.main:run',  # Main entry point
        ],
    },
)
