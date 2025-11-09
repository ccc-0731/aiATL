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
            "Return a valid JSON object — not text, not markdown. "
            "It must have these exact fields:\n\n"
            "{\n"
            '  "title": "short clear summary of the detected problem",\n'
            '  "confidence": "high/medium/low",\n'
            '  "solutions": [\n'
            "    {\n"
            '      "title": "step title",\n'
            '      "description": "step-by-step fix instructions",\n'
            '      "url": "relevant YouTube or guide link (if found, else empty string)"\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            "The `solutions` array must contain 3–5 items. "
            "All URLs must come from valid search results retrieved with the GoogleSearch tool. "
            "If no link is available, leave it as an empty string."
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

    output = response.text.strip()

    # Clean up Markdown or stray formatting
    cleaned = (
        output.replace("```json", "")
              .replace("```", "")
              .strip()
    )

    # Try JSON parse
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        print("⚠️ Model returned invalid JSON. Here's raw text:\n", output)
        parsed = {"error": "invalid_json", "raw": output}



    if stage == 1:
        # Save turn in memory as plain text
        history.append(f"User: {prompt}")
        history.append(f"AI: {output}")

    return parsed


'''#testing code
if __name__ == "__main__":
    result2 = call_read(
        stage=2,
        prompt="The print head keeps colliding with the model halfway through the print.",
        filepaths=["noodles.JPG"]
    )
    print(json.dumps(result2, indent=2))'''