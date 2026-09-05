from ..QuizTools.quiz_state import QuizState
from langgraph.types import interrupt


async def input_validate(state: QuizState):

    print("graph chapter name",state.get('chapter_name'))

    if not state.get("num_of_questions"):
        num_of_questions = interrupt({
            "type": "quiz_answer",
            "question": "How many questions do you want?"
        })

        return {
            "num_of_questions": num_of_questions
        }

    if not state.get("difficulty"):
        print(state["num_of_questions"])

        difficulty = interrupt({
            "type": "quiz_answer",
            "question": "What difficulty do you want? (easy/medium/hard)"
        })

        return {
            "difficulty": difficulty
        }

    if not state.get("quiz_type"):
        quiz_type = interrupt({
            "type": "quiz_answer",
            "question": "Which type of quiz do you want? (shortanswer/mcq/fill_in_blank)"
        })

        return {
            "quiz_type": quiz_type
        }

    execution_plan = state["execution_plan"].copy()
    execution_plan.pop(0)

    return {
        "execution_plan": execution_plan,
        "input_validate": True
    }