from qdrant_client import QdrantClient,models
import os
from dotenv import load_dotenv
load_dotenv()


class ClientConnect:

    def __init__(self):
        self.qdrant_connection = None
        self._connection_checking()  # connection method with private

    def _connection_checking(self): # connection is there or not checking
        try:
            if self.qdrant_connection is None:

                self.qdrant_connection = QdrantClient(url=os.getenv("AURIX_QDRANT_URL"),api_key=os.getenv("AURIX_QDRANT_API_KEY"))

                if self.qdrant_connection:
                    # print("connection is perfect")
                    return self.qdrant_connection # returning boolean value

        except Exception as e:
            print("error is ",e)


test = ClientConnect()
# test.connection_checking()
if test:
    print("connect123")
