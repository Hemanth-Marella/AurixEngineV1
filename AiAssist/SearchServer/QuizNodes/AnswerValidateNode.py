from ..QuizTools.AnswerValidateTool import answer_validate_tool
from ..QuizTools.quiz_state import QuizState

async def answer_validate_node(state:QuizState):

    print("enter into validate node")

    result = await answer_validate_tool.ainvoke(
        {
            "summary":state.get('summary'),
            "user_answer":state.get('user_answer'),
            "question":state.get('question')
        }
    )

    state['execution_plan'].pop(0)
    return {
        "validate_answer":result,
        "quiz_main_answer":result
    }