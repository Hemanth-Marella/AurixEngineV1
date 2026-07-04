from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

from ..Tools import generation_tool, chapter_name_tool

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("AURIX_GEMINI_KEY"),
)

agent = create_agent(
    model=llm,
    tools=[
        generation_tool,
        chapter_name_tool,
    ]
)