from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from ..LanggraphTools import LanggraphState
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("AURIX_GEMINI_KEY"),
    temperature = 0
)

# llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     api_key=os.getenv("AURIX_GROQ_API_KEY"),
#     temperature=0.1,
#     max_tokens=1024
# )

async def langgrahDecisionAgent(state: LanggraphState):

    prompt = f"""

        You are educational assistant

        Available nodes:

        1. chapter_name
        - Returns only the chapter name.

        2. sub_topics
        - Returns the list of subtopics.

        3. explanations
        - Explain one or more subtopics only when the user explicitly asks to explain subtopics.

        4. answer
        - Answer any question about the PDF content.

        Examples:

        User: What is the chapter name?
        Output:
        ["chapter_name"]

        User: List all subtopics.
        Output:
        ["sub_topics"]

        User: Explain all subtopics.
        Output:
        ["sub_topics","explanations"]

        User: Why are plant tissues different from animal tissues?
        Output:
        ["answer"]

        User: What is photosynthesis?
        Output:
        ["answer"]

        User: Explain osmosis.
        Output:
        ["answer"]

        User:
        {state["query"]}
        """

    response = await llm.ainvoke(
        [HumanMessage(content=prompt)]
    )

    execution_plan = eval(response.content)

    print("execution plan :" , execution_plan)

    return {
        "execution_plan": execution_plan
    }