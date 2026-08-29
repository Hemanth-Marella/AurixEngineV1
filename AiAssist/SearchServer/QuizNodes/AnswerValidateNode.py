from ..QuizTools.AnswerValidateTool import answer_validate_tool
from ..QuizTools.quiz_state import QuizState

async def answer_validate_node(state:QuizState):

    result = await answer_validate_tool(
        {
            "summary":state['summary'],
            "user_name":state['user_answer']
        }
    )

    state['execution_plan'].pop(0)
    return {
        "validate_answer":result
    }