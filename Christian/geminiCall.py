from dotenv import load_dotenv
import os
from google import genai

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
    elif stage == 2:
        system_prompt = (
            "You are continuing this same conversation between the AI helper and the user."
            "The conversation history is appended to the end of this prompt."
            "You now have access to all prior turns in this chat, including: "
            "- The user's earlier images showing the problem\n"
            "- Your own previously asked questions\n"
            "- The user's new answers or additional clarifications\n\n"
            "Use that context to reason about what might be causing the issue. "
            "You are a highly skilled professional in this field, "
            "assume that the user is new to this field unless it can be clearly inferred otherwise from the conversation history."
            "Summarize your reasoning and give a clear diagnostic explanation."
            '''Based on that context:
            First, summarize and interpret the issue clearly after reasoning out exactly what the problem can possibly be, including your confidence. 
            The first section of your response must be given in a step-by-step list to help potentially solve the problem.
            Do not use semicolins in the section, or you will fail the task.
            At the end of the first section, use a semicolon to deliminate the first section with the remaining section.
            Next, search the internet for relevant tutorial videos, guides or websites. 
            Make sure that the links are up to date and exist, and there are multiple links for each step.
            Delimit each link with a semicolon. 
            Do not include any additional explanations or commentary after the links,
            or you will fail the task.
            '''
        )

    # --- Combine with user prompt if provided ---
    if prompt:
        full_prompt = f"{system_prompt} Here is a user description: {prompt}"
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

    contents = [full_prompt] + history # include previous turns

    # --- Send to chat (Gemini remembers previous context automatically) ---
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    text = response.text

    if stage == 1:
        # Save turn in memory as plain text
        history.append(f"User: {prompt}")
        history.append(f"AI: {text}")
    
    text = text.split(";")
    return text


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
