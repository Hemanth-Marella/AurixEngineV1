from ..LanggraphTools import sub_topic_tool
from ..LanggraphTools import LanggraphState

async def sub_topic_node(state:LanggraphState):

    result = await sub_topic_tool.ainvoke(
        {
            'file_hash':state["file_hash"],
            'chapter_name':state['chapter_name']
        }
    )

    return {
        'sub_topics':result
    }