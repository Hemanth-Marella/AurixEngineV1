from ..Services.summary_service import SummaryService
# from Services.summary_service import SummaryService
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from .quiz_state import QuizState
import os
load_dotenv()
from langchain.tools import tool

@tool
async def generate_questions_tool(summary,chapter_name):

    """
        Generate quiz questions from the provided chapter summary.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("AURIX_GEMINI_KEY"),
        temperature=0.1,
    )

    question_prompt = f"""

         You are an expert educational quiz generator.

        Your task is to generate quiz questions ONLY from the provided chapter summary.

        ## Chapter Summary
        {summary}

        ## Instructions

        - Generate exactly 5 questions.
        - Difficulty level: Easy.
        - Chapter: {chapter_name}.
        - Questions must be based ONLY on the provided summary.
        - Do not use outside knowledge.
        - Cover different concepts from the summary.
        - Include both important and smaller concepts.
        - Avoid asking the same concept twice.
        - Questions should test conceptual understanding rather than simple memorization.
        - Keep questions clear and grammatically correct.
        - Do NOT provide answers.
        - Do NOT provide explanations.
        - Do NOT provide hints.
        - Do NOT number sub-points.
        - Return only the questions.

        ## Difficulty Guidelines

        If difficulty is "Easy":
        - Ask direct factual or definition-based questions.

        If difficulty is "Medium":
        - Ask conceptual understanding questions.

        If difficulty is "Hard":
        - Ask analytical or application-based questions.

        ## Output Format

        Return valid JSON only.

        
        "chapter_name": "{chapter_name}",
        "difficulty": "Easy",
        "total_questions": 5,
        "questions": [
            {
            "question_no": 1,
            "question": "..."
            }
        ]

        Do not return markdown.
        Do not use ```json.
        Return only valid JSON.

    """

    response =await llm.ainvoke(question_prompt)

    print("response is ",response.content)

    return response.content

