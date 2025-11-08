from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def gemini_call_readImg(prompt, filepath=None):
    if filepath:
        myfile = client.files.upload(file=filepath)
        contents = [prompt, myfile]
    else:
        contents = prompt
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=contents
    )
    return response.text

if __name__ == "__main__":
    print(gemini_call_readImg("test.png", "What problems can you find in this image? Ask the user about problems you find."))