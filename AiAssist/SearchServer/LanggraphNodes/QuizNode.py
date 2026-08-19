
from ..LanggraphTools import LanggraphState,quiz_tool


async def quiz_node(state: LanggraphState):

    try:
        result = await quiz_tool.ainvoke({'state':state})
        state['execution_plan'].pop(0) # remove the node after execution
        return {
            "quiz_result":result,
            "main_answer":result
        }
    except Exception as e:

        return {
            "error":str(e),
            "failed_node":"chapter_name_node"
        }

