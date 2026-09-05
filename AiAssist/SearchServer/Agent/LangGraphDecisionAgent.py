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






# # USE THIS CODE ONLY WHEN YOU USE GROP API KEY

# from langchain_core.messages import HumanMessage
# from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from ..LanggraphTools import LanggraphState

# import os
# import json

# load_dotenv()

# # Uncomment if using Gemini
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
#     temperature=0,
# )

# # llm = ChatGroq(
# #     model="openai/gpt-oss-20b",
# #     api_key=os.getenv("AURIX_GROQ_API_KEY"),
# #     temperature=0,
# # )


# async def langgrahDecisionAgent(state: LanggraphState):

#     previous_messages = state["memory_read"]

#     prompt = f"""
#                 You are an educational assistant.

#                 Your job is ONLY to decide which nodes should be executed.
#                 For every request must and should use memory as last node not front or middle node ok 

#                 DO NOT answer the user's question.

#                 Available Nodes:

#                 1. chapter_name
#                 - Returns only the chapter name.

#                 2. sub_topics
#                 - Returns all subtopics in the chapter.

#                 3. explanations
#                 - Explains one or more subtopics.
#                 - Use this ONLY when the user explicitly asks to explain subtopics.

#                 4. answer
#                 - Answers any question about the PDF content.

#                 5. quiz
#                 - Generates quiz questions from the chapter and summary.Because questions is asking from the Summary only .

#                 Rules:

#                 - Return ONLY a JSON array.
#                 - Do not explain anything.
#                 - Do not use markdown.
#                 - Do not return any extra text.

#                 Examples:

#                 User: What is the chapter name?
#                 Output:
#                 ["chapter_name","memory"]

#                 User: List all subtopics.
#                 Output:
#                 ["sub_topics","memory"]

#                 User: Explain all subtopics.
#                 Output:
#                 ["sub_topics", "explanations","memory"]

#                 User: Explain osmosis.
#                 Output:
#                 ["answer","memory"]

#                 User: What is photosynthesis?
#                 Output:
#                 ["answer","memory"]

#                 User: Why are plant tissues different from animal tissues?
#                 Output:
#                 ["answer","memory"]

#                 User: provide a quiz.
#                 for quiz chapter name , summary and quiz are more important
#                 Output:
#                 ["chapter_name","summary","quiz","memory"]

#                 User:
#                 {state["query"]}
#             """

#     try:
#         response = await llm.ainvoke(
#             [HumanMessage(content=prompt)]
#         )

#         # Parse JSON safely
#         execution_plan = json.loads(response.content)

#         # Validate response
#         valid_nodes = {
#             "chapter_name",
#             "sub_topics",
#             "explanations",
#             "answer",
#             "summary",
#             "quiz",
#             "memory",
#             "memory_read",
#         }

#         execution_plan = [
#             node for node in execution_plan if node in valid_nodes
#         ]

#         return {
#             "execution_plan": execution_plan
#         }

#     except json.JSONDecodeError as e:
#         print("JSON Parsing Error:", e)

#         return {
#             "execution_plan": ["answer"]
#         }

#     except Exception as e:
#         print("Planner Error:", e)

#         return {
#             "execution_plan": ["answer"]
#         }


























# USE THIS CODE ONLY WHEN YOU USE GROQ API KEY

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from ..LanggraphTools import LanggraphState

import os
import json

load_dotenv()


# Gemini
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
#     temperature=0,
# )


# Groq
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("AURIX_GROQ_API_KEY"),
    temperature=0,
)


async def langgrahDecisionAgent(state: LanggraphState):

    # Current user query
    current_query = state["query"]

    # Previous conversation retrieved by memory_read
    previous_messages = state.get("memory_read", [])

    prompt = f"""
You are the main decision-making agent of an educational AI system.

Your job is ONLY to decide which nodes should be executed.

You must use the previous conversation when the current user
query depends on previous messages.

DO NOT answer the user's question.

========================
CURRENT USER QUERY
========================

{current_query}


========================
PREVIOUS CONVERSATION
========================

{previous_messages}


========================
AVAILABLE NODES
========================

1. chapter_name
- Returns only the chapter name.

2. sub_topics
- Returns all subtopics in the chapter.

3. explanations
- Explains one or more subtopics.
- Use this ONLY when the user explicitly asks to explain
  subtopics.

4. answer
- Answers any question about the PDF content.

5. summary
- Generates a summary of the chapter.

6. quiz
- Generates quiz questions from the chapter and summary.
- Quiz questions must be generated from the summary.


========================
MEMORY RULE
========================

The "memory" node is used to save/update the latest
user query and generated answer.

For EVERY request:

"memory" MUST be the LAST node.

Never put "memory" at the beginning.

Never put "memory" in the middle.

Examples:

Correct:
["answer", "memory"]

Correct:
["summary", "quiz", "memory"]

Incorrect:
["memory", "answer"]

Incorrect:
["answer", "memory", "quiz"]


========================
PREVIOUS CONVERSATION RULE
========================

"memory_read" has already retrieved previous messages.

Use those messages to understand the current query.

For example:

Previous conversation:
User: What is photosynthesis?
Assistant: Photosynthesis is the process by which plants make food.

Current query:
Why is it important?

The current query means:

Why is photosynthesis important?

Therefore the execution plan should be:

["answer", "memory"]


========================
GENERAL RULES
========================

- Return ONLY a JSON array.
- Do not explain anything.
- Do not use markdown.
- Do not return any extra text.
- Do not answer the user's question.
- Use previous conversation only when necessary.
- Resolve references such as "it", "this", "that", "they",
  "previous one", "same topic", etc.
- Do not invent context that is not present in the conversation.


========================
EXAMPLES
========================

User: What is the chapter name?

Output:
["chapter_name", "memory"]


User: List all subtopics.

Output:
["sub_topics", "memory"]


User: Explain all subtopics.

Output:
["sub_topics", "explanations", "memory"]


User: Explain osmosis.

Output:
["answer", "memory"]


User: What is photosynthesis?

Output:
["answer", "memory"]


User: Why are plant tissues different from animal tissues?

Output:
["answer", "memory"]


User: Provide a quiz.

Output:
["chapter_name", "summary", "quiz", "memory"]


========================
NOW DECIDE THE EXECUTION PLAN
========================

Current user query:
{current_query}
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
            node
            for node in execution_plan
            if node in valid_nodes
        ]

        # Make sure memory is ALWAYS the last node
        if "memory" in execution_plan:
            execution_plan.remove("memory")

        execution_plan.append("memory")

        return {
            "execution_plan": execution_plan
        }

    except json.JSONDecodeError as e:

        print("JSON Parsing Error:", e)

        return {
            "execution_plan": ["answer", "memory"]
        }

    except Exception as e:

        print("Planner Error:", e)

        return {
            "execution_plan": ["answer", "memory"]
        }