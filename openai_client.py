from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        api_key = 'your-openai-api-key'  # Replace with your OpenAI API Key

    def send_to_openai(self, prompt):
        client = OpenAI()

        # Non-streaming:
        print("----- standard request -----")
        print(prompt)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return completion.choices[0].message.content

    def extract_code(self, response, language="python"):
        """
        General method to extract code blocks of a specific language.
        :param response: The OpenAI response containing the code block.
        :param language: The code language or tag (e.g., 'python', 'html', 'css').
        :return: Extracted code or empty string if no code block is found.
        """
        start_tag = f"```{language}"
        end_tag = "```"
        if start_tag not in response:
            raise ValueError(f"No code block found for language: {language}")
        if start_tag in response:
            code = response.split(start_tag)[1].split(end_tag)[0]
            return code.strip()


    def extract_python_code(self, response):
        """
        Extracts Python code block from the OpenAI response.
        :param response: The OpenAI response containing the code block.
        :return: Extracted Python code.
        """
        return self.extract_code(response, "python")

    def extract_html_code(self, response):
        """
        Extracts HTML code block from the OpenAI response.
        :param response: The OpenAI response containing the code block.
        :return: Extracted HTML code.
        """
        return self.extract_code(response, "html")

    def extract_css_code(self, response):
        """
        Extracts CSS (style.css) code block from the OpenAI response.
        :param response: The OpenAI response containing the code block.
        :return: Extracted CSS code.
        """
        return self.extract_code(response, "css")
