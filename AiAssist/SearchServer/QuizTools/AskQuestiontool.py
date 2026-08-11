
from langchain.tools import tool
from ..MongoDb import MongoDB

@tool
async def ask_question_tool(file_hash:str):
    mongo_db = MongoDB()

    question_check = await mongo_db.question_generator.find_one(
        {"file_hash":file_hash}
    )

    if question_check:
        questions = question_check['questions']