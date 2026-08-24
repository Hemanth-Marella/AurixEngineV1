
from ..LanggraphTools import LanggraphState,quiz_tool


async def quiz_node(state: LanggraphState):

    try:
        result = await quiz_tool.ainvoke({'state':state})
        print("quiz_node agent result is ",result)
        state['execution_plan'].pop(0) # remove the node after execution
        return {
            "quiz_result":result,
            "main_answer":result
        }
    except Exception as e:

        return {
            "error":str(e),
        }

