from langgraph.graph import StateGraph, START, END

from ..LanggraphTools import LanggraphState,RoutingFunction

from ..Agent.LangGraphDecisionAgent import langgrahDecisionAgent

from ..LanggraphNodes import ChapterNameNode,SubTopicExplanationNode,SubTopicNode,RouterNode,GenerationNode

# THIS CREATES AN EMPTY GRAPH NO NODES IS INVOLVED START -> END
graph_builder = StateGraph(LanggraphState)


# WE ARE JUST ADDING NODES NOT YET CONNECTED SO NOW START -> AGENTIC_NODE -> ROUTER -> CHAPTER_NAME -> SUB_TOPICS -> EXPLANATIONS -> END
graph_builder.add_node("agentic_node",langgrahDecisionAgent)
graph_builder.add_node("router", RouterNode.router_node)

graph_builder.add_node("chapter_name",ChapterNameNode.chapter_name_node)
graph_builder.add_node("sub_topics",SubTopicNode.sub_topic_node)
graph_builder.add_node("explanations",SubTopicExplanationNode.sub_topic_explanation_node)
graph_builder.add_node("answer",GenerationNode.generation_node)


# Flow  These are fixed graphs
# graph_builder.add_edge(START, "agentic_node")
# graph_builder.add_edge("agentic_node","chapter_name")
# graph_builder.add_edge("chapter_name", "sub_topics")
# graph_builder.add_edge("sub_topics", "explanations")
# graph_builder.add_edge("explanations", END)


# BASED ON ROUTER, THESE ARE EDGES TO CONNECT START AND AGENTIC NODE
graph_builder.add_edge(START, "agentic_node")

# Agent -> Router, ONE MORE CONNECTION TO AGENTIC NODE TO ROUTER NODE . AFTER 
graph_builder.add_edge("agentic_node", "router")

# Router -> Worker Nodes
#  CONDITIONAL ROUTING AND add_conditional_edges() decides the next node dynamically.
graph_builder.add_conditional_edges(
    "router",   # RUN ROUTING AFTER THE NODE FINISHES
    RoutingFunction.route,   # IF ROUTE RETURNS CHAPTER_NAME GO TO CHAPTER_NAME AND IF ROUTE RETURNS SUB_TOPICS GO TO SUB_TOPICS , IT RETURNS THE NODE
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
graph_builder.add_edge("chapter_name", "router")  
graph_builder.add_edge("sub_topics", "router")
graph_builder.add_edge("explanations", "router")
graph_builder.add_edge("answer","router")

graph = graph_builder.compile()