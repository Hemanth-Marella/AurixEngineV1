import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="google/gemma-4-26b-a4b-it:free",
    api_key=os.getenv("AURIX_OPEN_ROUTER_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2,
)

response = llm.invoke("What is Artificial Intelligence?")

print(response.content)