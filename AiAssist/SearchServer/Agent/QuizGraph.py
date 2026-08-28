from ..QuizNodes import generate_questions_node,QuizPlannerNode,ask_question_node,answer_node
from langgraph.graph import StateGraph, START, END
from .QuizAgent import quiz_agent_node
from ..Checkpointers.MongodbCheckpointer import create_checkpointer

from ..QuizTools import QuizState,QuizPlannerRouter

quiz_graph_builder = StateGraph(QuizState)

quiz_graph_builder.add_node("quiz_agent",quiz_agent_node)
quiz_graph_builder.add_node("generate_questions",generate_questions_node)
quiz_graph_builder.add_node("quiz_planner",QuizPlannerNode)
quiz_graph_builder.add_node("question",ask_question_node)
quiz_graph_builder.add_node("user_answer",answer_node)

quiz_graph_builder.add_edge(START,"quiz_agent")
quiz_graph_builder.add_edge("quiz_agent","quiz_planner")

quiz_graph_builder.add_conditional_edges(
    "quiz_planner",
    QuizPlannerRouter,
    {
        "generate_questions":"generate_questions",
        "question":"question",
        "user_answer":"user_answer",
        END:END,
    }
)

quiz_graph_builder.add_edge("generate_questions","quiz_planner")
quiz_graph_builder.add_edge("question","quiz_planner")
quiz_graph_builder.add_edge("user_answer","quiz_planner")

checkpointer = create_checkpointer()

quiz_graph = quiz_graph_builder.compile(
    checkpointer=checkpointer
)
