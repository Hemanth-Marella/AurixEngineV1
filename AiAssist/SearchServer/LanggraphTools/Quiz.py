from langchain_core.tools import tool
from ..QuizTools import QuizState
from ..Agent.QuizGraph import quiz_graph

@tool
async def quiz_tool(state) :

    """
    use this tool whenever user talking about the quiz . provide a quiz question like this ok
    """

    quiz_state: QuizState = {
        "file_hash" : state['file_hash'],
        "query" : state['query'],
        "chapter_name": state["chapter_name"],
        "summary": state.get("summary", ""),

        "num_of_questions": state['num_of_questions'], #state["num_of_questions"]
        "quiz_type": state['quiz_type'] , #state["quiz_type"]
        "difficulty": state['difficulty'] ,     #state["difficulty"],

        "question":"",
        "current_question": 0,
        "score": 0,

        "user_answer": "",
        "correct_answer": "",

        "generate_questions": [],
        "quiz_completed": False,

        "execution_plan": [],
    }


    result =await quiz_graph.ainvoke(quiz_state)

    return result