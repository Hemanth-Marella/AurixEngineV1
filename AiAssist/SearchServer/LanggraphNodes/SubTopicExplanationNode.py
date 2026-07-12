from ..LanggraphTools import sub_topic_explanation_tool
from ..LanggraphTools import LanggraphState

async def sub_topic_node(state:LanggraphState):

    result = await sub_topic_explanation_tool.ainvoke(
        {
            'file_hash':state["file_hash"],
            'sub_topics':state['sub_topics'],
            'query':state['query']
        }
    )

    return {
        'sub_topics':result
    }