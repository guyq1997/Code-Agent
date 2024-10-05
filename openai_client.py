from openai import OpenAI
from pydantic import BaseModel
import json
from typing import List, Tuple

class Response(BaseModel):
    script_name: str
    code: str

class ResponseFormat(BaseModel):
    generated_scripts: list[Response]

class OpenAIClient:
    def __init__(self):
        api_key = 'your-openai-api-key'  # Replace with your OpenAI API Key

    def send_to_openai(self, prompt,format_class):
        client = OpenAI()

        # Non-streaming:
        print("----- standard request -----")
        print(prompt)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[prompt],
            response_format=ResponseFormat
        )


        return completion.choices[0].message.content


    def extract_code(response_content: str) -> List[Tuple[str, str]]:
        """
        Extracts script names and corresponding code from an OpenAI API response.
        Args:
            response_content (str): A string containing the JSON response
                                    from the OpenAI API.
        Returns:
            List[Tuple[str, str]]: A list of tuples, where each tuple contains
                                two elements:
                                - The script name (str)
                                - The corresponding code (str)
                                Returns an empty list if parsing fails or
                                if the expected data is not found.
        """
        try:
            # Parse the JSON response
            response_data = json.loads(response_content)
            
            # Extract the generated scripts
            generated_scripts = response_data.get('generated_scripts', [])
            
            # Create a list of tuples (script_name, code)
            extracted_code = [(script['script_name'], script['code']) for script in generated_scripts]
            
            return extracted_code
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            return []
        except KeyError as e:
            print(f"Error: Missing key in response - {e}")
            return []