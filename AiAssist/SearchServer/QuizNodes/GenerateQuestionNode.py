from ..QuizTools import generate_questions_tool,QuizState


async def generate_questions_node(state:QuizState):

    print("enter into quiz node")

    result = await generate_questions_tool.ainvoke(
        {
            "summary": state.get("summary"),
            "chapter_name": state.get('chapter_name'),
            "file_hash":state.get('file_hash'),
            "num_of_question" : state.get('num_of_questions'),
            "difficulty":state.get('difficulty'),
            "quiz_type":state.get('quiz_type')
        }
    )
    state['execution_plan'].pop(0) # remove the node after execution
    return {
        "generate_questions": result,  # we updating the chapter name here to the state 
        "quiz_main_answer":result
    }
