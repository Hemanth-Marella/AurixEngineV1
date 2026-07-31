from ..QuizNodes import generate_questions_node,QuizPlannerNode
from langgraph.graph import StateGraph, START, END
from .quiz_agent import quiz_agent_node

from ..QuizTools import QuizState,QuizPlannerRouter

quiz_graph_builder = StateGraph(QuizState)

quiz_graph_builder.add_node("quiz_agent",quiz_agent_node)
quiz_graph_builder.add_node("generate_questions",generate_questions_node)
quiz_graph_builder.add_node("quiz_planner",QuizPlannerNode)

quiz_graph_builder.add_edge(START,"quiz_agent")
quiz_graph_builder.add_edge("quiz_agent","quiz_planner")

quiz_graph_builder.add_conditional_edges(
    "quiz_planner",
    QuizPlannerRouter,
    {
        "generate_questions":"generate_questions",
        END:END,
    }
)

quiz_graph_builder.add_edge("generate_questions","quiz_planner")

quiz_graph = quiz_graph_builder.compile()
