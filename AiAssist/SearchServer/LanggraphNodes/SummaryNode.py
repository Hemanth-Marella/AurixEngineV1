from ..LanggraphTools import summary_tool,LanggraphState

async def summary_node(state:LanggraphState):

    try:
        result = await summary_tool.ainvoke(
            {
                "chapter_name":state['chapter_name']
            }
        )
        state["execution_plan"].pop(0)
        return {
            "summary":result,
            "error":None
        }

    except Exception as e:
        return {
            "error":str(e),
            "failed_node":"summary_node"
        }