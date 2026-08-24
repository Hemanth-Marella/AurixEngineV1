from ..QuizTools import generate_questions_tool,QuizState


async def generate_questions_node(state:QuizState):

    print("enter into quiz node")

    result = await generate_questions_tool.ainvoke(
        {
            "summary": state["summary"],
            "chapter_name": state["chapter_name"],
            "file_hash":state['file_hash'],
            "state":state
        }
    )
    state['execution_plan'].pop(0) # remove the node after execution
    print(state['execution_plan'])
    return {
        "generate_questions": result  # we updating the chapter name here to the state 
    }
