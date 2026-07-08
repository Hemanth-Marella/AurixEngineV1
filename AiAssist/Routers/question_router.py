## THIS IS DIRECTLY CALLING THE TOOLS 
# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
# from ..SearchServer.Tools.generationTool import generation_tool

# from pydantic import BaseModel

# router = APIRouter(prefix="/user", tags=["USER"])

# class QuestionRequest(BaseModel):
#     query: str

# @router.post("/question")
# async def user_question(request: QuestionRequest):

#     service = generation_tool(request.query)

#     def generate():
#         for chunk in service:
#             yield chunk.text

#     return StreamingResponse(generate(), media_type="text/plain")



# # THIS IS CALLING THE AGENT
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..SearchServer.Agent.DecisionAgent import agent

from pydantic import BaseModel
from langchain.messages import HumanMessage,AIMessage,ToolMessage


router = APIRouter(prefix="/user", tags=["USER"])
class QuestionRequest(BaseModel):
    query : str | None
    file_hash : str | None

@router.post("/question")
async def user_question(request:QuestionRequest):

    # print("file hash is : ",request.file_hash)
    result =agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""{request.query}"""
                }
            ],
            "file_hash": request.file_hash
        }
    )

    # answer = await result
    # messages = answer['messages']

#     print(messages)
#     return messages
    # for message in messages:
    #     return message.content

    # messages = answer['messages']
    # print(type(messages))

    # for message in messages:
    #     print(message)

    def generate():
        for chunk in result:
            # return chunk
            print(chunk)
            yield chunk#["model"]["messages"][0].content[0]["text"]

    return StreamingResponse(generate(), media_type="text/plain")