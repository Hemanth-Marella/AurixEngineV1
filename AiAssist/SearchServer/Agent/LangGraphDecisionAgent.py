# from langchain_core.messages import HumanMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from ..LanggraphTools import LanggraphState
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# import os

# load_dotenv()


# # USE ONLY THIS WHEN YOU USE GRMINI API 

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
#     temperature = 0
# )

# async def langgrahDecisionAgent(state: LanggraphState):

#     prompt = f"""

#         You are educational assistant

#         Available nodes:

#         1. chapter_name
#         - Returns only the chapter name.

#         2. sub_topics
#         - Returns the list of subtopics.

#         3. explanations
#         - Explain one or more subtopics only when the user explicitly asks to explain subtopics.

#         4. answer
#         - Answer any question about the PDF content.
#         5. quiz
#         - Generate quiz questions based on the summary of the chapter.

#         Examples:

#         User: What is the chapter name?
#         Output:
#         ["chapter_name"]

#         User: List all subtopics.
#         Output:
#         ["sub_topics"]

#         User: Explain all subtopics.
#         Output:
#         ["sub_topics","explanations"]

#         User: Why are plant tissues different from animal tissues?
#         Output:
#         ["answer"]

#         User: What is photosynthesis?
#         Output:
#         ["answer"]

#         User: Explain osmosis.
#         Output:
#         ["answer"]

#         User: Provide a Quize.
#         output:
#         ["chapter_name","summary","quiz"]

#         User:
#         {state["query"]}
#     """

#     response = await llm.ainvoke(
#         [HumanMessage(content=prompt)]
#     )

#     execution_plan = eval(response.content)
#     print("execution plan is ",execution_plan)

#     return {
#         "execution_plan": execution_plan
#     }






# USE THIS CODE ONLY WHEN YOU USE GROP API KEY

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from ..LanggraphTools import LanggraphState

import os
import json

load_dotenv()

# Uncomment if using Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("AURIX_GEMINI_KEY"),
    temperature=0,
)

# llm = ChatGroq(
#     model="openai/gpt-oss-20b",
#     api_key=os.getenv("AURIX_GROQ_API_KEY"),
#     temperature=0,
# )


async def langgrahDecisionAgent(state: LanggraphState):

    prompt = f"""
                You are an educational assistant.

                Your job is ONLY to decide which nodes should be executed.
                For every request must and should use memory as last node not front or middle node ok 

                DO NOT answer the user's question.

                Available Nodes:

                1. chapter_name
                - Returns only the chapter name.

                2. sub_topics
                - Returns all subtopics in the chapter.

                3. explanations
                - Explains one or more subtopics.
                - Use this ONLY when the user explicitly asks to explain subtopics.

                4. answer
                - Answers any question about the PDF content.

                5. quiz
                - Generates quiz questions from the chapter and summary.Because questions is asking from the Summary only .

                Rules:

                - Return ONLY a JSON array.
                - Do not explain anything.
                - Do not use markdown.
                - Do not return any extra text.

                Examples:

                User: What is the chapter name?
                Output:
                ["chapter_name","memory"]

                User: List all subtopics.
                Output:
                ["sub_topics","memory"]

                User: Explain all subtopics.
                Output:
                ["sub_topics", "explanations","memory"]

                User: Explain osmosis.
                Output:
                ["answer","memory"]

                User: What is photosynthesis?
                Output:
                ["answer","memory"]

                User: Why are plant tissues different from animal tissues?
                Output:
                ["answer","memory"]

                User: provide a quiz.
                for quiz chapter name , summary and quiz are more important
                Output:
                ["chapter_name","summary","quiz","memory"]

                User:
                {state["query"]}
            """

    try:
        response = await llm.ainvoke(
            [HumanMessage(content=prompt)]
        )

        # Parse JSON safely
        execution_plan = json.loads(response.content)

        # Validate response
        valid_nodes = {
            "chapter_name",
            "sub_topics",
            "explanations",
            "answer",
            "summary",
            "quiz",
            "memory",
        }

        execution_plan = [
            node for node in execution_plan if node in valid_nodes
        ]

        return {
            "execution_plan": execution_plan
        }

    except json.JSONDecodeError as e:
        print("JSON Parsing Error:", e)

        return {
            "execution_plan": ["answer"]
        }

    except Exception as e:
        print("Planner Error:", e)

        return {
            "execution_plan": ["answer"]
        }

