from langgraph.graph import StateGraph, START, END

from ..LanggraphTools import LanggraphState,PlannerRouter

from ..Agent.LangGraphDecisionAgent import langgrahDecisionAgent

from ..LanggraphNodes import ChapterNameNode,SubTopicExplanationNode,SubTopicNode,PlannerNode,GenerationNode,MemoryNode

# THIS CREATES AN EMPTY GRAPH NO NODES IS INVOLVED START -> END
# CREATE THE GRAPH . 
graph_builder = StateGraph(LanggraphState)


# WE ARE JUST ADDING NODES NOT YET CONNECTED SO NOW START -> AGENTIC_NODE -> ROUTER -> CHAPTER_NAME -> SUB_TOPICS -> EXPLANATIONS -> END
graph_builder.add_node("agentic_node",langgrahDecisionAgent)
graph_builder.add_node("Planner", PlannerNode.planner_node)

graph_builder.add_node("chapter_name",ChapterNameNode.chapter_name_node)
graph_builder.add_node("sub_topics",SubTopicNode.sub_topic_node)
graph_builder.add_node("explanations",SubTopicExplanationNode.sub_topic_explanation_node)
graph_builder.add_node("answer",GenerationNode.generation_node)
graph_builder.add_node("memory",MemoryNode.memory_node)


# BASED ON ROUTER, THESE ARE EDGES TO CONNECT START AND AGENTIC NODE
# WITH MEMORY
graph_builder.add_edge(START,"memory")
graph_builder.add_edge("memory", "agentic_node")

# WITHOUT MEMORY
# graph_builder.add_edge(START, "agentic_node")

# Agent -> Router, ONE MORE CONNECTION TO AGENTIC NODE TO ROUTER NODE . AFTER 
graph_builder.add_edge("agentic_node", "Planner")


## HOW GRAPH WORKS IN CONDITIONAL EDGES
# Planner
#    │
#    ▼
# planner_route()
#    │
#    ▼
# chapter_name
#    │
#    ▼
# Planner
#    │
#    ▼
# planner_route()

# Router -> Worker Nodes
#  CONDITIONAL ROUTING AND add_conditional_edges() decides the next node dynamically.
graph_builder.add_conditional_edges(
    "Planner",   # RUN ROUTING AFTER THE NODE FINISHES
    PlannerRouter.planner_route,   # IF ROUTE RETURNS CHAPTER_NAME GO TO CHAPTER_NAME AND IF ROUTE RETURNS SUB_TOPICS GO TO SUB_TOPICS , IT RETURNS THE NODE
    #  HERE DICTIONARY IS FOR CHECKING 
    #  This dictionary matches the returned value to the next node.
    # It matches the value returned by route() to the node that should execute next.
    {
        "chapter_name": "chapter_name",
        "sub_topics": "sub_topics",
        "explanations": "explanations",
        "answer":"answer",
        END: END,  # IF ROUTE RETURNS END STOP GRAPH
    },
)

# Worker Nodes -> Router
# chapter_name -> router -> sub_topics -> router -> explanations -> router
# Here conditional edges return a one node and after completed that node it will switch to router
graph_builder.add_edge("chapter_name", "Planner")  
graph_builder.add_edge("sub_topics", "Planner")
graph_builder.add_edge("explanations", "Planner")
graph_builder.add_edge("answer","Planner")


# CREATE THE EXECUTABLE GRAPH
# NODES ARE CONNECTED , EDGES ARE FIXED AND THE GRAPH IS READY TO RUN
# this graph.compile will not share any values . It only builds the executable graph . 
graph = graph_builder.compile()