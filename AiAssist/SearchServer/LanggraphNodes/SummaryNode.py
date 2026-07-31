from ..LanggraphTools import summary_tool,LanggraphState

async def summary_node(state:LanggraphState):

    result = await summary_tool.ainvoke(
        {
            "chapter_name":state['chapter_name']
        }
    )

    state["execution_plan"].pop(0)
    return {
        "summary":result
    }