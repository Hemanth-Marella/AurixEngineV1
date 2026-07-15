from ..LanggraphTools import generation_tool,LanggraphState


async def generation_node(state:LanggraphState):

    result = await generation_tool.ainvoke(
        {
            "query": state["query"],
            "file_hash": state["file_hash"],
        }
    )
    state['execution_plan'].pop(0) # remove the node after execution
    return {
        "answer": result
    }
