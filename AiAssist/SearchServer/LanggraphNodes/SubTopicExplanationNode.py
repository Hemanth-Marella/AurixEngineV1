from ..LanggraphTools import sub_topic_explanation_tool
from ..LanggraphTools import LanggraphState

async def sub_topic_explanation_node(state:LanggraphState):

    try:
        result = await sub_topic_explanation_tool.ainvoke(
            {
                'file_hash':state["file_hash"],
                'sub_topics':state['sub_topics'],
                'query':state['query']
            }
        )
        state['execution_plan'].pop(0)
        print(state)
        return {
            'explanations':result,
            'error':None
        }
    except Exception as e:
        return{
            "error":str(e),
            "failed_node":"sub_topic_explanation_node"
        }