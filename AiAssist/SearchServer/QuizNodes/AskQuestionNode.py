## WITHOUT INTERRUPT

from ..QuizTools.quiz_state import QuizState
from ..QuizTools.AskQuestiontool import ask_question_tool

async def ask_question_node(state: QuizState):
    print("enter into ask question node")
    print(state.get('current_question'))
    current_question = 0

    result = await ask_question_tool.ainvoke({
        "file_hash": state.get('file_hash'),
        "current_question": current_question
    })

    state['execution_plan'].pop(0)

    return {
        "question": result["question"],
        "quiz_main_answer":result['question']
    }
