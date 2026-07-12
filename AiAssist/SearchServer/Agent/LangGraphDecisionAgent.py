from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from ..LanggraphTools import LanggraphState
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("AURIX_GEMINI_KEY"),
    temperature = 0
)

async def langgrahDecisionAgent(state: LanggraphState):

    prompt = f"""
        You are a routing agent.

        Available nodes:

        1. chapter_name
        - Returns the chapter name.

        2. sub_topics
        - Returns all subtopics of the chapter.

        3. explanation
        - Explains one or more subtopics.

        Your job is to return ONLY a Python list containing the node execution order.

        Examples:

        User: What is the chapter name?
        Output:
        ["chapter_name"]

        User: Give me the subtopics.
        Output:
        ["sub_topics"]

        User: Explain all subtopics.
        Output:
        ["sub_topics","explanation"]

        User: Give me chapter name, subtopics and explain everything.
        Output:
        ["chapter_name","sub_topics","explanation"]

        User:
        {state["query"]}
        """

    response = await llm.ainvoke(
        [HumanMessage(content=prompt)]
    )

    execution_plan = eval(response.content)

    return {
        "execution_plan": execution_plan
    }