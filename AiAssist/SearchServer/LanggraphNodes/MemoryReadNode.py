from ..LanggraphTools.LanggraphState import LanggraphState
from ..LanggraphTools.MemoryReadTool import memory_read_tool

async def memory_read_node(state:LanggraphState):

    result = await memory_read_tool.ainvoke(
        {'file_hash':state['file_hash']}
    )

    return {
        "memory_read":result
    }