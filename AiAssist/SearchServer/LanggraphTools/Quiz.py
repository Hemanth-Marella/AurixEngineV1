from langchain_core.tools import tool
from ..QuizTools import QuizState
from ..Agent.QuizGraph import quiz_graph

@tool
async def quiz_tool(state) :

    """
    use this tool whenever user talking about the quiz . provide a quiz question like this ok
    """

    print("quiz node execution plan is ",state['execution_plan'])

    print("hitting the quiz node")

    quiz_state: QuizState = {
        "file_hash" : state['file_hash'],
        "query" : state['query'],
        "chapter_name": state["chapter_name"],
        "summary": state.get("summary", ""),

        "num_of_questions": 5, #state["num_of_questions"]
        "quiz_type": "mcq" , #state["quiz_type"]
        "difficulty": "Easy"   ,     #state["difficulty"],

        "current_question": 0,
        "score": 0,

        "user_answer": "",
        "correct_answer": "",

        "generate_questions": [],
        "quiz_completed": False,

        "execution_plan": [],
    }

    print("befor graph invokes")

    result =await quiz_graph.ainvoke(quiz_state)

    return state