
from ..LanggraphTools import LanggraphState,quiz_tool


# async def quiz_node(state: LanggraphState):

#     try:
#         result = await quiz_tool.ainvoke({'state':state})

#         if result:
#             state['execution_plan'].pop(0)

#         return {
#             "quiz_result":result,
#             "main_answer":result
#         }
#     except Exception as e:

#         return {
#             "error":str(e),
#         }




# ## WITH INTERRUPT
# from langchain_core.tools import tool
# from ..QuizTools import QuizState
# from ..Agent.QuizGraph import quiz_graph
# from langgraph.types import interrupt


# async def quiz_node(state: LanggraphState):

#     quiz_state: QuizState = {
#         "file_hash" : state['file_hash'],
#         "query" : state['query'],
#         "chapter_name": state["chapter_name"],
#         "summary": state.get("summary", ""),

#         "num_of_questions": state['num_of_questions'], #state["num_of_questions"]
#         "quiz_type": state['quiz_type'] , #state["quiz_type"]
#         "difficulty": state['difficulty'] ,     #state["difficulty"],

#         "question":"",
#         "current_question": 0,
#         "score": 0,

#         "user_answer": "",
#         "correct_answer": "",
#         "quiz_main_answer":"",

#         "generate_questions": [],
#         "quiz_completed": False,

#         "execution_plan": [],
#     }

#     config = {
#         "configurable": {
#             "thread_id": quiz_state['file_hash']
#         }
#     }

#     result =await quiz_graph.ainvoke(quiz_state,config=config)

#     out_state = await quiz_graph.aget_state(config=config)

#     print("INTERRUPTS:")
#     print(result.get("__interrupt__"))
    
#     interrupts = result.get("__interrupt__")

#     if interrupts:
#         print("interrupt is happen")

#         interrupt_value = interrupts[0].value

#         quiz_result = {
#             "status": "waiting_for_user",
#             "thread_id": config["configurable"]["thread_id"],
#             "interrupt": [
#                 {
#                     "value": interrupt_value
#                 }
#             ]
#         }

#         # VERY IMPORTANT
#         return {
#             "quiz_result": quiz_result,
#             "execution_plan": state.get("execution_plan", [])
#         }


#     print("interrupt is not happen")

#     quiz_result = {
#         "status": "completed",
#         "thread_id": config["configurable"]["thread_id"],
#         "answer": result.get("quiz_main_answer"),
#         "execution_plan": result.get("execution_plan", [])
#     }

#     quiz_execution_plan = out_state.values.get("execution_plan", [])

#     print("QUIZ EXECUTION PLAN:", quiz_execution_plan)

#     if not quiz_execution_plan:
#         print("exe")
#         return {
#             "quiz_result": quiz_result,
#             "main_answer": quiz_result
#         }

#     # execution_plan is NOT empty
#     print("Quiz execution plan still has tasks:", quiz_execution_plan)












from langgraph.types import interrupt, Command

from ..QuizTools import QuizState
from ..Agent.QuizGraph import quiz_graph


async def quiz_node(state: LanggraphState):

    thread_id = state["file_hash"]

    quiz_config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    quiz_state = await quiz_graph.aget_state(
        config=quiz_config
    )

    print("QUIZ GRAPH NEXT:",quiz_state.next) # this is to get quiz next state if it contains ('user_answer',)

    if not quiz_state.next:

        quiz_state_data: QuizState = {

            "file_hash": state["file_hash"],
            "query": state["query"],
            "chapter_name": state["chapter_name"],
            "summary": state.get("summary",""),
            "num_of_questions": state["num_of_questions"],
            "quiz_type": state["quiz_type"],
            "difficulty": state["difficulty"],
            "question": "",
            "current_question": 0,
            "score": 0,
            "user_answer": "",
            "correct_answer": "",
            "quiz_main_answer": "",
            "generate_questions": [],
            "quiz_completed": False,
            "execution_plan": [],
        }

        result = await quiz_graph.ainvoke(
            quiz_state_data,
            config=quiz_config
        )

    else:
        user_answer = interrupt({
            "type": "quiz",
            "message": (
                "Please provide your answer."
            )
        })

        result = await quiz_graph.ainvoke(
            Command(resume=user_answer),
            config=quiz_config
        )

    interrupts = result.get("__interrupt__")

    if interrupts:

        interrupt_value = (
            interrupts[0].value
        )
        print(interrupt_value)

        user_answer = interrupt({
            "type": "quiz",
            "message": interrupt_value
        })

        result = await quiz_graph.ainvoke(
            Command(resume=user_answer),
            config=quiz_config
        )

    while result.get("__interrupt__"):

        interrupts = result.get("__interrupt__")

        interrupt_value = (interrupts[0].value)

        print(interrupt_value)
        user_answer = interrupt({
            "type": "quiz",
            "message": interrupt_value
        })

        result = await quiz_graph.ainvoke(
            Command(resume=user_answer),
            config=quiz_config
        )

    final_state = await quiz_graph.aget_state(config=quiz_config)

    values = final_state.values

    execution_plan = values.get("execution_plan",[])

    quiz_result = {

        "status": "completed",
        "thread_id": thread_id,
        "answer": values.get("quiz_main_answer","" ),
        "score": values.get("score",0 ),
        "quiz_completed": values.get("quiz_completed",False),
        "execution_plan": execution_plan
    }

    if not execution_plan:
        return {

            "quiz_result": quiz_result,
            "main_answer": quiz_result,
            "execution_plan": []
        }

    return {

        "quiz_result": quiz_result,
        "main_answer": quiz_result,
        "execution_plan": execution_plan
    }