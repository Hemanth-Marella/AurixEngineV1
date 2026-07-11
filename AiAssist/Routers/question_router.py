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
    result =await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""{request.query} ? file_hash{request.file_hash}"""
                }
            ],
            "file_hash": request.file_hash
        }
    )

    answer = result
    messages = answer['messages']

    human_message = {}
    tool_message = {}
    ai_message = {}

    ## TO AVOID DUPLICATE TOOL CALLS TO CHECK
    # for msg in result["messages"]:
    #     if isinstance(msg, AIMessage):
    #         print("=" * 80)
    #         print("AI CONTENT:", msg.content)
    #         print("TOOL CALLS:", msg.tool_calls)

    for i in range(len(messages)):
        print("types of message",messages[i].type)
        if messages[i].type == "human":
            human_message = {
                "human":messages[i].content.split("file_hash")[0].strip(" ?")
            }

        elif messages[i].type == "tool":
            tool_message = {
                "tool":messages[i].content
            }

        elif messages[i].type == "ai":
            ai_message = {
                "AI":messages[i].content
            }
    output = {
        "human_message": human_message,
        "tool_message": tool_message,
        "ai_message":ai_message
    }
    return output

    # # print(messages)
    # query_type = messages[0].type
    # human_content = messages[0].content.split("file_hash")[0].strip(" ?")
    # human_message = {query_type:human_content}

    # tool_type = messages[2].type
    # tool_content = messages[2].content

    # tool_message = {tool_type:tool_content}


    # output = {
    #     "human_message":human_message,
    #     "tool_message":tool_message
    # }
    # # return human_message
    # return output















    # for message in messages:
    #     return message.content

    # messages = answer['messages']
    # print(type(messages))

    # for message in messages:
    #     print(message)

    # def generate():
    #     for chunk in result:
    #         return chunk
            # print(chunk)
            # yield chunk#["model"]["messages"][0].content[0]["text"]

    # return StreamingResponse(generate(), media_type="text/plain")