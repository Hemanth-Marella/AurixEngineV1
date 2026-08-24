from ..QuizTools.quiz_state import QuizState
from ..QuizTools.AskQuestiontool import ask_question_tool

async def ask_question_node(state: QuizState):
    print("enter into ask question node")

    result = await ask_question_tool.ainvoke({
        "file_hash": state["file_hash"],
        "current_question": state["current_question"]
    })

    return {
        "question": result["question"]
    }