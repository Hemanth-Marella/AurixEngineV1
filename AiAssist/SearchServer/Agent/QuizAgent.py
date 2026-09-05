from ..Services import summary_service
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from ..QuizTools import quiz_state,generate_questions_tool
from ..QuizNodes import GenerateQuestionNode
from langchain.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
#     temperature=0.1,
# )

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("AURIX_GROQ_API_KEY"),
    temperature=0,
)

async def quiz_agent_node(state:quiz_state.QuizState):

    try:
        prompt = f"""

                You are a Quiz Planning Assistant.

                Available Nodes:

                1. generate_questions
                - Generate quiz questions from the summary.

                2. question
                - selecting question from mongodb.

                3. user_answer
                - getting answer from user.

                4. validate_answer
                - validate the user answer with sumamry.
                5. input_validate
                - validate the users input whether it is available or not

                Rules:
                - Select only from the available nodes.
                - Return only a Python list.
                - Do not explain anything.
                - Do not generate quiz questions.
                - Do not add any node that is not listed above.

                Examples:

                User: Start a quiz.
                Output:
                ["input_validate","generate_questions","question","user_answer","validate_answer"]

                User:
                {state['query']}

        """

        response = await llm.ainvoke(
            [HumanMessage(content=prompt)]
        )
    
        execution_plan = eval(response.content)

        print("quiz_execution plan is ,",execution_plan)
    
        return {
            "execution_plan": execution_plan
        }

    except Exception as e:
        raise ValueError("quiz generation error is ",e)