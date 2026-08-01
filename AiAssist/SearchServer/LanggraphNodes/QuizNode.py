from ..QuizTools import QuizState
from ..Agent.quiz_graph import quiz_graph
from ..LanggraphTools import LanggraphState

def quiz_node(state: LanggraphState):

    try:

        quiz_state: QuizState = {
            "query" : state['query'],
            "chapter_name": state["chapter_name"],
            "summary": state["summary"],

            "num_of_questions": state["num_of_questions"],
            "quiz_type": state["quiz_type"],
            "difficulty": state["difficulty"],

            "current_question": 0,
            "score": 0,

            "user_answer": "",
            "correct_answer": "",

            "generate_questions": [],
            "quiz_completed": False,

            "execution_plan": [],
        }

        result = quiz_graph.invoke(quiz_state)

        print("quiz_graps : ",result)

        state['execution_plan'].pop(0)

        return state
    except Exception as e:
        return{
            "error":str(e),
            "failed_node":"quiz_node"
        }