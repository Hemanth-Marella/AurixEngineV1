# from langgraph.checkpoint.mongodb import MongoDBSaver

# from ..MongoDb.FileMetadataConnection import MongoDB

# def create_checkpointer():

#     mongodb = MongoDB()

#     checkpointer = MongoDBSaver.from_conn_string(
#         mongodb.check_pointer_storage
#     )

#     return checkpointer



from langgraph.checkpoint.memory import InMemorySaver


def create_checkpointer():
    checkpointer = InMemorySaver()
    print("checkpointer is : ",checkpointer)
    return checkpointer