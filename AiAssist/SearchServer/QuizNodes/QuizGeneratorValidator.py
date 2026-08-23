from ..QuizTools.quiz_state import QuizState

def quiz_generate_validator(state: QuizState):

    # Check difficulty
    if not state.get("difficulty"):
        return {
            "status": "missing",
            "missing_field": "difficulty",
            "question": "What difficulty level would you like for the quiz — Easy, Medium, or Hard?"
        }

    # Check number of questions
    if not state.get("num_of_questions"):
        return {
            "status": "missing",
            "missing_field": "num_of_questions",
            "question": "How many questions would you like?"
        }

    # Check quiz type
    if not state.get("quiz_type"):
        return {
            "status": "missing",
            "missing_field": "quiz_type",
            "question": "What type of quiz would you like — MCQ, True/False, or Fill in the Blanks?"
        }

    # Everything is available
    return {
        "status": "complete",
        "missing_field": None,
        "question": None
    }