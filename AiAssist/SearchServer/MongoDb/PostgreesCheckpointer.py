import os
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

postgres_uri = os.getenv("POSTGRES_URI")


def create_checkpointer():

    checkpointer = PostgresSaver.from_conn_string(postgres_uri)

    with checkpointer as saver:
        saver.setup()
        return saver