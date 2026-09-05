
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()


# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
#     temperature=0,
# )

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("AURIX_GROQ_API_KEY"),
    temperature=0,
)

@tool
async def answer_validate_tool(summary,user_answer,question):
    """
    Validate the user's answer against the summary.
    """

    prompt = f"""
            You are a quiz answer validator.

            QUESTION:
            {user_answer}

            SUMMARY:
            {summary}

            USER ANSWER:
            {user_answer}

            Determine whether the user's answer is correct based ONLY on the summary.

            Rules:
            - correct = answer is fully correct
            - partially_correct = answer contains some correct information but is incomplete
            - incorrect = answer contradicts or does not match the summary
            - give score also for that answer when it is correct or partial correct or incorrect also
            - and give correct explanation for that also 

            Return ONLY valid JSON:

            {{
                "status": "correct",
                "feedback": "Your answer is correct because ..."
                "score": "0.0",
                "explanation":"explanation"
            }}
            """

    result = await llm.ainvoke(prompt)

    return result.content