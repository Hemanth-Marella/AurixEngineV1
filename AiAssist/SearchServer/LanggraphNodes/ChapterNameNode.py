from ..LanggraphTools import chapter_name_tool,LanggraphState

async def chapter_name_node(state:LanggraphState):

    try:

        result = await chapter_name_tool.ainvoke(
            {
                "file_hash": state["file_hash"],
                "query": state["query"]
            }
        )
        state['execution_plan'].pop(0) # remove the node after execution
        print("chapter name")
        return {
            "chapter_name": result,  # we updating the chapter name here to the state 
            "main_answer":result
        }

    except Exception as e:
        return {
            "error":str(e),
            "failed_node":"chapter_name_node"
        }











## WITH INTERRUPT OK
# from ..LanggraphTools import chapter_name_tool,LanggraphState

# async def chapter_name_node(state:LanggraphState):

#         result = await chapter_name_tool.ainvoke(
#             {
#                 "file_hash": state["file_hash"],
#                 "query": state["query"]
#             }
#         )
#         state['execution_plan'].pop(0) # remove the node after execution
#         print("chapter name")
#         return {
#             "chapter_name": result,  # we updating the chapter name here to the state 
#             "main_answer":result
#         }
