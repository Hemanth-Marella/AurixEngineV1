from langchain.tools import tool
from ..MongoDb import MongoDB

@tool
async def ask_question_tool(file_hash: str, current_question: int = 0):

    """
    Retrieve exactly one quiz question from MongoDB for the given PDF.

    Args:
        file_hash: Unique identifier of the uploaded PDF.
        current_question: Zero-based index of the question to retrieve.
            0 = first question,
            1 = second question,
            2 = third question, etc.

    Behavior:
        - Find the quiz questions stored in MongoDB using file_hash.
        - Use current_question as the index.
        - Return only the requested question.
        - Do not return all questions.
        - Do not generate a new question.
        - Do not modify current_question.
        - If the index is outside the available questions, indicate that the quiz is completed.
        - The LangGraph state is responsible for incrementing current_question
          after the user answers the current question.

    Returns:
        A dictionary containing:
        - question: The requested quiz question.
        - current_question: The index of the returned question.
        - has_next: Whether another question exists.
    """

    mongo_db = MongoDB()

    question_check = await mongo_db.question_generator.find_one(
        {"file_hash": file_hash}
    )

    if not question_check:
        return {
            "question": None,
            "current_question": current_question,
            "error": "No questions found"
        }

    questions = question_check["questions"]

    # No more questions
    if current_question >= len(questions):
        return {
            "question": None,
            "current_question": current_question,
            "error": "Quiz completed"
        }

    return {
        "question": questions[current_question]
    }