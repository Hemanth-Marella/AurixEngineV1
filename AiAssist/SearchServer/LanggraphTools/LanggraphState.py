from typing import TypedDict

class LanggraphState(TypedDict):
    file_hash: str
    query: str
    chapter_name: str
    sub_topics: list[str]
    explanations: dict[str, str]
    answer:str
    execution_plan: list[str]