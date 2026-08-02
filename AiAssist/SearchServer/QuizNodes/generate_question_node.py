from ..QuizTools import generate_questions_tool,QuizState


async def generate_questions_node(state:QuizState):

    result = await generate_questions_tool.ainvoke(
        {
            "no_of_questions":state['num_of_questions'],
            "difficulty_type":state['difficulty'],
            "chapter_name":state['chapter_name']
        }
    )

    print("enter into generate questions node")
    state['execution_plan'].pop(0) # remove the node after execution
    return {
        "generate_questions": result  # we updating the chapter name here to the state 
    }
