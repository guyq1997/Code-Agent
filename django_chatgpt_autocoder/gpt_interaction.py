import os
from openai import OpenAI

def get_gpt_response(prompt, context_files):
    # Ensure you have set the OpenAI API key as an environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OpenAI API key not set in environment variables")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Read the content from the context files to include in the prompt
    context = ""
    for file in context_files:
        with open(file, 'r') as f:
            context += f"\n\nContext from {file}:\n" + f.read()

    # Combine the context and the user's prompt
    full_prompt = f"{prompt}\n\n{context}"

    # Use the ChatGPT completion API to get the response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can change this to "gpt-4" if you have access
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )
    
    # Extract the response content (the generated code)
    gpt_response = response.choices[0].message.content
    
    return gpt_response
