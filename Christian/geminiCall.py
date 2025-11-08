from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def call_read(prompt, filepath=None):

    system_prompt = "The user is experiencing problems, as shown in the images. Analyze the problems that you find in these images (taken from different angles, or show different aspects of the problem). Ask the user to provide more context about problems you find."

    if prompt != None:
        prompt = system_prompt + " Here is a user description of what's going wrong: " + prompt
    else: 
        prompt = system_prompt
    
    if filepath:
        myfile = client.files.upload(file=filepath)
        contents = [prompt, myfile]
    else:
        contents = prompt
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=contents
    )
    return response.text

#if __name__ == "__main__":
 #   print(call_read("test.png", "The user is experiencing problems, as shown in the images. Analyze the problems that you find in these images (taken from different angles, or show different aspects of the problem). Ask the user to provide more context about problems you find."))