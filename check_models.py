from dotenv import load_dotenv
load_dotenv()
import os

from google import genai

client = genai.Client(api_key=os.getenv("AURIX_GEMINI_KEY"))

for model in client.models.list():
    print(model.name)