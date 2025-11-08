from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_read(prompt=None, filepaths=None):
    
    # --- System instruction ---
    system_prompt = '''The user is experiencing problems, as shown in the images. 
        Analyze the problems you find in these images (taken from different angles, or showing different aspects of the issue). 
        Ask the user questions to provide more context about the problems you detect. 
        The questions must be independent, and all questions should be delimited by ASCII 31.
        Do not include any explanations or commentary apart from the delimited questions, or you will fail the task.'''

    # --- Combine with user prompt if provided ---
    if prompt:
        full_prompt = system_prompt + " Here is a user description of what's going wrong: " + prompt
    else:
        full_prompt = system_prompt

    # --- Handle image uploads ---
    contents = [full_prompt]
    if filepaths:
        # Ensure filepaths can be either a single string or a list
        if isinstance(filepaths, str):
            filepaths = [filepaths]
        uploaded_files = [client.files.upload(file=path) for path in filepaths]
        contents.extend(uploaded_files)

    # --- Generate the response ---
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    return response.text

if __name__ == "__main__":
    print(call_read("these are some confusing georgia tech cs prereq maps", ["test.png", "test1.png"]))