from langchain_core.tools import tool
from ..MongoDb.FileMetadataConnection import MongoDB 
from ..Services import generation_service

@tool
async def sub_topic_explanation_tool(file_hash: str, query: str) -> str:
    """
    Use this tool only when the user asks to explain the subtopics of the uploaded PDF.

    Examples:
    - "Explain the subtopics."
    - "Give me the subtopics and explain them."
    - "Explain all the subtopics from the uploaded PDF."

    Inputs:
    - file_hash: The uploaded PDF's file hash.
    - query: The user's original question.

    Behavior:
    - Retrieve the list of subtopics for the uploaded PDF.
    - For each subtopic, retrieve the relevant content only from the uploaded PDF.
    - Generate an explanation using only the retrieved PDF context.
    - Do not use external knowledge or information outside the uploaded PDF.

    Output:
    - Returns the explanation for each subtopic.
    """

    mongodb = MongoDB()
    service = generation_service
    document =await  mongodb.Aurix_collection.find_one(
        {"file_hash":file_hash}
    )

    if document:

        sub_topics_list = document['sub_topics']

    explanations = {}

    for topic in sub_topics_list:

        topic_query = (
            f"Explain the subtopic '{topic}' "
            f"using only the uploaded PDF."
        )

        generation = generation_service.GenerationService(topic_query)

        answer = await generation.generate_answer()

        explanations[topic] = answer

    return explanations
