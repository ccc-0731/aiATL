from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# shared conversation memory 
history = []

# create a single chat session with memory

def call_read(stage, prompt=None, filepaths=None):
    
    # --- System instruction based on stage ---
    if stage == 1:
        system_prompt = (
            '''"The user is experiencing problems, as shown in the images. 
            Analyze the problems you find in these images (taken from different angles, 
            or showing different aspects of the issue). 
            Ask the user questions to provide more context about the problems you detect, 
            in order to figure out exactly what the problem is. 
            The questions must be independent, and all questions should be delimited by a semicolon. 
            Ask as few questions as necessary. 
            Do not include any explanations or commentary apart from the delimited questions,
            or you will fail the task.'''
        )
        config = None

    elif stage == 2:
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        config = types.GenerateContentConfig(
            tools=[grounding_tool]
        )

        system_prompt = (
            "Role: You are a domain expert helping a novice diagnose a problem. "
            "Use the prior conversation (images, Q&A) as context. "
            "Return a valid python string with two sections, delimited by a '|'."
            "It must follow this format:\n\n"
            "RESPONSE | PROMPT"
            "where: The RESPONSE is a short clear summary of the detected problem, and step-by-step fixes."
            "The PROMPT is a detailed description for what youtube videos that are relevant."
        )

    # combine prompt
    full_prompt = f"{system_prompt}\n\nUser said: {prompt or ''}"

    # --- Handle (multiple) image uploads ---
    contents = [full_prompt] + history

    # Upload multiple files
    uploaded_files = [client.files.upload(file=path) for path in filepaths]
    contents += uploaded_files

    # --- Send to chat (Gemini remembers previous context automatically) ---
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config
    )

    output = response.text


    if stage == 1:
        # Save turn in memory as plain text
        history.append(f"User: {prompt}")
        history.append(f"AI: {output}")
        output = response.text
        return [x for x in output.split(";") if x != ""]

    if stage == 2:
        return [x for x in output.split("|") if x != ""]

'''testing code
if __name__ == "__main__":
    test_image = ["noodles.JPG"]
    questions = call_read(stage=1, filepaths=test_image)
    print("Stage 1 Questions:", questions)

    user_answer = "The print failed halfway through; I was using PLA with a cold bed."
    output = call_read(stage=2, prompt=user_answer, filepaths=test_image)
    print("Stage 2 Output:", output)
'''