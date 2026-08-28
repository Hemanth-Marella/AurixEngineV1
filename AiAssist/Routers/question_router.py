# ## THIS IS DIRECTLY CALLING THE TOOLS 
# # from fastapi import APIRouter
# # from fastapi.responses import StreamingResponse
# # from ..SearchServer.Tools.generationTool import generation_tool

# # from pydantic import BaseModel

# # router = APIRouter(prefix="/user", tags=["USER"])

# # class QuestionRequest(BaseModel):
# #     query: str

# # @router.post("/question")
# # async def user_question(request: QuestionRequest):

# #     service = generation_tool(request.query)

# #     def generate():
# #         for chunk in service:
# #             yield chunk.text

# #     return StreamingResponse(generate(), media_type="text/plain")



# # # THIS IS CALLING THE AGENT
# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
# from ..SearchServer.Agent.LangchainDecisionAgent import agent

# from pydantic import BaseModel
# from langchain.messages import HumanMessage,AIMessage,ToolMessage


# router = APIRouter(prefix="/user", tags=["USER"])
# class QuestionRequest(BaseModel):
#     query : str | None
#     file_hash : str | None

# @router.post("/question")
# async def user_question(request:QuestionRequest):

#     # print("file hash is : ",request.file_hash)
#     result =await agent.ainvoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": f"""{request.query} ? file_hash{request.file_hash}"""
#                 }
#             ],
#             "file_hash": request.file_hash
#         }
#     )

#     answer = result
#     messages = answer['messages']

#     human_message = {}
#     tool_message = {}
#     ai_message = {}

#     ## TO AVOID DUPLICATE TOOL CALLS TO CHECK
#     # for msg in result["messages"]:
#     #     if isinstance(msg, AIMessage):
#     #         print("=" * 80)
#     #         print("AI CONTENT:", msg.content)
#     #         print("TOOL CALLS:", msg.tool_calls)

#     for i in range(len(messages)):
#         print("types of message",messages[i].type)
#         if messages[i].type == "human":
#             human_message = {
#                 "human":messages[i].content.split("file_hash")[0].strip(" ?")
#             }

#         elif messages[i].type == "tool":
#             tool_message = {
#                 "tool":messages[i].content
#             }

#         elif messages[i].type == "ai":
#             ai_message = {
#                 "AI":messages[i].content
#             }
#     output = {
#         "human_message": human_message,
#         "tool_message": tool_message,
#         "ai_message":ai_message
#     }
#     return output

#     # # print(messages)
#     # query_type = messages[0].type
#     # human_content = messages[0].content.split("file_hash")[0].strip(" ?")
#     # human_message = {query_type:human_content}

#     # tool_type = messages[2].type
#     # tool_content = messages[2].content

#     # tool_message = {tool_type:tool_content}


#     # output = {
#     #     "human_message":human_message,
#     #     "tool_message":tool_message
#     # }
#     # # return human_message
#     # return output



#     # for message in messages:
#     #     return message.content

#     # messages = answer['messages']
#     # print(type(messages))

#     # for message in messages:
#     #     print(message)

#     # def generate():
#     #     for chunk in result:
#     #         return chunk
#             # print(chunk)
#             # yield chunk#["model"]["messages"][0].content[0]["text"]

#     # return StreamingResponse(generate(), media_type="text/plain")







# #### LANG GRAPH ROUTER ---------------------------------------------
# from fastapi import APIRouter
# from pydantic import BaseModel
# from ..SearchServer.Agent.LanggraphBuilder import graph
# from ..SearchServer.Services.chatHistoryService import ChatHistoryService
# import time



# router = APIRouter(
#     prefix="/user",tags=["USER"]
# )

# class QuestionRequest(BaseModel):
#     query : str | None
#     file_hash: str | None


# @router.post("/question")
# async def user_question(request:QuestionRequest):

#     assistant_message = ""

#     initial_state = {
#         "file_hash": request.file_hash,
#         "query": request.query,

#         "chapter_name": "",
#         "sub_topics": [],
#         "explanations": {},

#         "answer": "",
#         "execution_plan": [],

#         "memory": [],

#         "quiz": "",
#         "summary": "",

#         "num_of_questions": 0,
#         "quiz_type": "",
#         "difficulty": "",

#         "error": None,
#         "failed_node": None,

#         "quiz_result": None,

#         "main_answer": ""
#     }

#     # the actual state values is come from graph.invoke . Here only update the state is happened when the node perform operation
#     # every nodes recieves this data only i mean graph.invoke(initialstate) data only
#     # the graph is execute here
    
#     # Yes. graph.invoke() (or graph.ainvoke()) is responsible for:

#     # Creating the initial state from your input.
#     # Passing the current state to each node.
#     # Updating the state with each node's returned values.
#     # Sharing the updated state with subsequent nodes.
#     # Returning the final state after execution.

#     start_time = time.perf_counter()
#     result = await graph.ainvoke(initial_state)  # here we are providing actual data to nodes and edges to perform 

#     end_time = time.perf_counter()

#     execution_time = end_time - start_time
#     print("execution time is :",execution_time)

#     return result.get("main_answer")   # instead of this get last message from mongodb is good because before return only it is updated ok 












from fastapi import APIRouter
from pydantic import BaseModel
from langgraph.types import Command

from ..SearchServer.Agent.LanggraphBuilder import graph
from ..SearchServer.QuizTools.quiz_state import QuizState


router = APIRouter(prefix="/user",tags=["USER"])


# -----------------------------
# Request models
# -----------------------------

class QuestionRequest(BaseModel):
    file_hash: str
    query: str


class QuizAnswerRequest(BaseModel):
    file_hash: str
    answer: str
    thread_id: str


# =========================================================
# 1. START / NORMAL QUESTION ENDPOINT
# =========================================================

@router.post("/question")
async def user_question(request: QuestionRequest):
    print("router is working")

    try:

        initial_state = {
        "file_hash": request.file_hash,
        "query": request.query,

        "chapter_name": "",
        "sub_topics": [],
        "explanations": {},

        "answer": "",
        "execution_plan": [],

        "memory": [],

        "quiz": "",
        "summary": "",

        "num_of_questions": 0,
        "quiz_type": "",
        "difficulty": "",

        "error": None,
        "failed_node": None,

        "quiz_result": None,

        "main_answer": ""
    }

        # IMPORTANT:
        # Every execution needs a thread_id
        config = {
            "configurable": {
                "thread_id": request.file_hash
            }
        }

        result = await graph.ainvoke(
            initial_state,
            config=config
        )
        # print("quiz router result is",result)

        ## TO CHECK HERE INTERRUPT IS HAPPENED OR NOT OK 
        # print("GRAPH RESULT:")
        # print(result)

        print("INTERRUPTS:")
        # print(result.get("__interrupt__"))

        interrupts = result.get("__interrupt__")

        if interrupts:

            print("interrupt is happen")

            interrupt_value = interrupts[0].value

            return {
                "status": "waiting_for_user",
                "thread_id": request.file_hash,
                "interrupt": [
                    {
                        "value": interrupt_value
                    }
                ]
            }
        print("interrupt is not happen")
        return {
            "status": "completed",
            "thread_id": request.file_hash,
            "answer": result.get("answer"),
            "execution_plan": result.get("execution_plan", [])
        }

    except Exception as e:
        print("error came")

        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/quiz/answer")
async def quiz_answer(request: QuizAnswerRequest):

    try:

        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }

        result = await graph.ainvoke(
            Command(resume=request.answer),
            config=config
        )

        interrupts = result.get("__interrupt__")

        if interrupts:

            interrupt_value = interrupts[0].value

            return {
                "status": "waiting_for_user",
                "thread_id": request.thread_id,
                "interrupt": [
                    {
                        "value": interrupt_value
                    }
                ]
            }

        return {
            "status": "completed",
            "thread_id": request.thread_id,
            "quiz_completed": True,
            "score": result.get("score", 0),
            "execution_plan": result.get(
                "execution_plan",
                []
            ),
            "answer":result.get('main_answer')
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }