import os
from dotenv import load_dotenv
import autogen
from autogen import AssistantAgent, LLMConfig
from autogen.tools.experimental import YoutubeSearchTool
import json
import re

def extract_urls(text):
    url_pattern = r'https?://[^\s]+'
    return re.findall(url_pattern, text)
load_dotenv()
def promptToVideos(prompt:str):
    llm_config = LLMConfig(
        model="gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        api_type="google"
    )

    assistant = AssistantAgent(
        name="assistant",
        llm_config=llm_config,
    )

    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    assert youtube_api_key is not None, "Please set YOUTUBE_API_KEY environment variable"

    youtube_tool = YoutubeSearchTool(
        youtube_api_key=youtube_api_key,
    )
    # Register the tool with the assistant
    youtube_tool.register_for_llm(assistant)

    response = assistant.run(
    message=prompt,
    tools=assistant.tools,
    max_turns=2,
    user_input=False,
    )
    response.process()
    
    urls = extract_urls(str(assistant.chat_messages))

    correct_urls = []
    for x in urls:
        correct_urls.append(x[0:-3])
    clean_urls = []
    for x in correct_urls:
        clean_urls.append(x[0:23]+"embed/"+x[23:])
    print(clean_urls)
    return correct_urls




if __name__ == "__main__":
    print(promptToVideos("give me videos about fishing in the mississippi"))
