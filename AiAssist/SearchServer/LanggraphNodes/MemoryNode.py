from ..LanggraphTools import LanggraphState,memory_tool

# here state is a variable which is type of langgraphstate like name:str
# here state is hold the data from graph.ainvoke ok
# langgraph state does not store any values it is only definition
async def memory_node(state: LanggraphState):

    try:

        result = await memory_tool.ainvoke(
            {
                "file_hash": state["file_hash"],
                "query": state["query"],
                "result": state
            }
        )

        state["execution_plan"].pop(0)

        return {
            "main_answer": result.get("main_answer")
        }

    except Exception as e:

        return {
            "error": str(e)
        }