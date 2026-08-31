
from ..LanggraphTools import LanggraphState
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
            "validate_answer":"",
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

        print("interrupt is happen in quiz")

        interrupt_value = (interrupts[0].value)
        print(interrupt_value)

        user_answer = interrupt({
            "type": "quiz",
            "message": interrupt_value
        })

        print("in quiz after user_answer")

        result = await quiz_graph.ainvoke(
            Command(resume=user_answer),
            config=quiz_config
        )

    # while result.get("__interrupt__"):
    #     print("interrupt is happen in quiz while condition")

    #     interrupts = result.get("__interrupt__")

    #     interrupt_value = (interrupts[0].value)

    #     print(interrupt_value)
    #     user_answer = interrupt({
    #         "type": "quiz",
    #         "message": interrupt_value
    #     })

    #     result = await quiz_graph.ainvoke(
    #         Command(resume=user_answer),
    #         config=quiz_config
    #     )

    ## these are just to get execution plan from graph state 
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

    # this will implement if there no any execution plans
    if not execution_plan:
        
        state['execution_plan'].pop(0)
        
        return {
            "quiz_result": quiz_result,
            "main_answer": quiz_result,
            "execution_plan": state['execution_plan']
        }

    return {
        "quiz_result": quiz_result,
        "main_answer": quiz_result,
        "execution_plan": execution_plan
    }