from typing import TypedDict

# this is not create or update any values . It just tells to langgraph  this graph state will contain these keys
# this is only define what fields are expected 
# the Langgraph state class does not store or update any values .
# "The state should have these keys and these data types."


# LANGGRAPH STATE WITHOUT MEMORY
# class LanggraphState(TypedDict):
#     file_hash: str
#     query: str
#     chapter_name: str
#     sub_topics: list[str]
#     explanations: dict[str, str]
#     answer:str
#     execution_plan: list[str]




#  LANGGRAPH STATE WITH MEMORY
class LanggraphState(TypedDict):
    file_hash: str
    query: str
    chapter_name: str
    sub_topics: list[str]
    explanations: dict[str, str]
    answer:str
    execution_plan: list[str]
    memory : list[str]