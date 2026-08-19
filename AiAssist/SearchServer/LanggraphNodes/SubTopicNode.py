from ..LanggraphTools import sub_topic_tool
from ..LanggraphTools import LanggraphState

async def sub_topic_node(state:LanggraphState):

    try:
        result = await sub_topic_tool.ainvoke(
            {
                'file_hash':state["file_hash"],
            }
        )
        state["execution_plan"].pop(0)
        return {
            'sub_topics':result,
            "main_answer":result,
            'error':None
        }

    except Exception as e:
        return {
            "error":str(e),
            "failed_node":"sub_topic_node"
        }