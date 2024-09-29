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
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return completion.choices[0].message.content

    def extract_python_code(self, response):
        if "```python" in response:
            code = response.split("```python")[1].split("```")[0]
        else:
            code = response
        return code.strip()
