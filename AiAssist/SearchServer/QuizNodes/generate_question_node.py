from ..QuizTools import generate_questions_tool,QuizState


async def generate_questions_node(state:QuizState):

    result = await generate_questions_tool.ainvoke(
        {
            "summary": state["summary"],
            "chapter_name": state["chapter_name"],
        }
    )

    print("enter into generate questions node")
    state['execution_plan'].pop(0) # remove the node after execution
    return {
        "generate_questions": result  # we updating the chapter name here to the state 
    }
