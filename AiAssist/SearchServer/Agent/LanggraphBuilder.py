from langgraph.graph import StateGraph, START, END

from ..LanggraphTools import LanggraphState

from ..Agent.LangGraphDecisionAgent import langgrahDecisionAgent

from ..LanggraphNodes import ChapterNameNode,SubTopicExplanationNode,SubTopicNode


graph_builder = StateGraph(LanggraphState)
graph_builder.add_node("chapter_name",ChapterNameNode.chapter_name_node)
graph_builder.add_node("sub_topics",SubTopicNode.sub_topic_node)
graph_builder.add_node("explanations",SubTopicExplanationNode.sub_topic_explanation_tool)


# Flow
graph_builder.add_edge(START, "chapter_name")
graph_builder.add_edge("chapter_name", "sub_topics")
graph_builder.add_edge("sub_topics", "explanations")
graph_builder.add_edge("explanations", END)

graph = graph_builder.compile()