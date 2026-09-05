from ..QuizTools.quiz_state import QuizState
from langgraph.types import interrupt
from ..QuizTools.AnswerTool import get_answer_tool

async def answer_node(state: QuizState):
    print("before interrupt")

    # Pause here and wait for frontend/user
    user_answer = interrupt({
        "type": "quiz_answer",
        "question": state.get('question')
    })

    print("after interrupt")

    state["execution_plan"].pop(0)

    return {
        "user_answer": user_answer,
        "quiz_main_answer": user_answer
    }