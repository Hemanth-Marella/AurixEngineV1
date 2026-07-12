from ..LanggraphTools import chapter_name_tool,LanggraphState


async def chapter_name_node(state:LanggraphState):

    result = await chapter_name_tool.ainvoke(
        {
            "file_hash": state["file_hash"],
            "query": state["query"]
        }
    )

    return {
        "chapter_name": result
    }
