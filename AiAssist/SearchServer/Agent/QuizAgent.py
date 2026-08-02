from ..Services import summary_service
from langchain_google_genai import ChatGoogleGenerativeAI
from ..QuizTools import quiz_state,generate_questions_tool
from ..QuizNodes import generate_question_node
from langchain.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("AURIX_GEMINI_KEY"),
    temperature=0.1,
)

async def quiz_agent_node(state:quiz_state.QuizState):

    print("entr into quiz agent")

    try:
        prompt = f"""

                You are a Quiz Planning Assistant.

                Available Nodes:

                1. generate_questions
                - Generate quiz questions from the summary.

                2. evaluate_answer
                - Evaluate the user's answer for the current question.

                3. next_question
                - Move to the next question if available.

                4. finish_quiz
                - Finish the quiz and return the final score.

                Rules:
                - Select only from the available nodes.
                - Return only a Python list.
                - Do not explain anything.
                - Do not generate quiz questions.
                - Do not add any node that is not listed above.

                Examples:

                User: Start a quiz.
                Output:
                ["generate_questions"]

                User: I answered the first question.
                Output:
                ["evaluate_answer", "next_question"]

                User: My answer is Photosynthesis.
                Output:
                ["evaluate_answer", "next_question"]

                User: There are no more questions.
                Output:
                ["finish_quiz"]

                User:
                {state['query']}

        """

        response = await llm.ainvoke(
            [HumanMessage(content=prompt)]
        )
    
        execution_plan = eval(response.content)
    
        print("execution plan :" , execution_plan)
    
        return {
            "execution_plan": execution_plan
        }

    except Exception as e:
        raise ValueError("quiz generation error is ",e)