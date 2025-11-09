from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

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
            "Role: You are a domain expert helping a novice user diagnose a problem using the conversation so far (images, prior Q&A, and clarifications)."
            '''
            Your output will be separated into FOUR sections. 
            All the sections will be delimited by semicolons. DO NOT USE SEMICOLONS otherwise.
            Based on that context:
            First section: summarize and interpret the issue clearly in 1-2 sentences exactly what the problem can possibly be.
            Second section: Your confidence level about the problem diagnosis
            Third section: a detailed step-by-step guide to help solve the problem, which is formatted for readability.
            Fourth section: search the internet for relevant tutorial videos, guides or websites. 
            Only use the valid URLs retrieved from the Google Search tool.
            Do not include any additional explanations or commentary after the URLs.
            Fifth section: Based on the problem you identified, create a prompt for an AI that would find the most appropriate youtube videos.
            '''
        )

    # --- Combine with user prompt if provided ---
    if prompt:
        full_prompt = f"{system_prompt} Here is a user description: {prompt}"
    else:
        full_prompt = system_prompt

    # --- Handle (multiple) image uploads ---
    contents = [full_prompt] + history # include previous turns

    # Upload multiple files
    uploaded_files = [client.files.upload(file=path) for path in filepaths]
    contents.append(uploaded_files)

    # --- Send to chat (Gemini remembers previous context automatically) ---
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config
    )
    text = response.text

    if stage == 1:
        # Save turn in memory as plain text
        history.append(f"User: {prompt}")
        history.append(f"AI: {text}")
    
    text = [x for x in text.split(";") if x != ""]
    print(text)
    return text

#testing code
'''
if __name__ == "__main__":
    # First multimodal call
    result1 = call_read(
        stage=1,
        prompt="Bambulab A1 3d printer",
        filepaths=["test2.JPG"]
    )
    print("FIRST:", result1)

    name = input("Your answers: ")

    # Second text-only call (no images, continues same chat session)
    result2 = call_read(
        stage=2,
        prompt=name,
        filepaths=["test2.JPG"]
    )
    print("SECOND:", result2)
'''