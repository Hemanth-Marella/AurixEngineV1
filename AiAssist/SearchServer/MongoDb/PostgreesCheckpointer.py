from langgraph.checkpoint.memory import InMemorySaver


def create_checkpointer():
    checkpointer = InMemorySaver()
    return checkpointer