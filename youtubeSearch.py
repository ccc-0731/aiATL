import os
from dotenv import load_dotenv
import autogen
from autogen import AssistantAgent, LLMConfig
from autogen.tools.experimental import YoutubeSearchTool

load_dotenv()
def promptToVideos(prompt:str) -> list[str]:
    llm_config = llm_config = LLMConfig(
        model="gemini-pro",
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

    # Iterate through the chat automatically with console output
    response.process()

if __name__ == "__main__":
    promptToVideos("find me videos on frogs")
