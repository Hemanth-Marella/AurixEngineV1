from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

from ..Tools import generation_tool, chapter_name_tool,sub_topic_tool ,sub_topic_explanation_tool

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
# )

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("AURIX_GROQ_API_KEY"),
    temperature=0.1,
    max_tokens=1024
)

agent = create_agent(
    model=llm,
    tools=[
        generation_tool,
        chapter_name_tool,
        sub_topic_tool,
        sub_topic_explanation_tool
    ],
    system_prompt="""
    You are an educational assistant.

    Always answer in bullet points.

    Example:
    • Point 1
    • Point 2
    • Point 3

    Keep the language simple.
    """
)