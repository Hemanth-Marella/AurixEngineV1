from ..LanggraphTools import LanggraphState,memory_tool

# here state is a variable which is type of langgraphstate like name:str
# here state is hold the data from graph.ainvoke ok
# langgraph state does not store any values it is only definition
async def memory_node(state:LanggraphState):

    result = await memory_tool.ainvoke(
        {'file_hash':state['file_hash']}
    )

    # state['execution_plan'].pop()

    return {
        "memory":result
    }