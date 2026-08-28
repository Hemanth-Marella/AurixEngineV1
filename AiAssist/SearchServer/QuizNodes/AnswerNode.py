from ..QuizTools.quiz_state import QuizState
from langgraph.types import interrupt
from ..QuizTools.AnswerTool import get_answer_tool

# async def answer_node(state:QuizState):

#     result = await get_answer_tool.ainvoke(
#         {
#             "file_hash": state["file_hash"],
#             "query" : state['query']
#         }
#     )

#     state['execution_plan'].pop(0)
#     return {
#         'user_answer':result
#     }


from langgraph.types import interrupt
from ..QuizTools.quiz_state import QuizState


async def answer_node(state: QuizState):

    print("enter into answer node")
    print("before interrupt")

    # Pause here and wait for frontend/user
    user_answer = interrupt({
        "type": "quiz_answer",
        "question": state["question"]
    })

    print("after interrupt")

    print("User answer:", user_answer)

    state["execution_plan"].pop(0)

    return {
        "user_answer": user_answer
    }