# from .ClientConnection import ClientConnect   # for modular coding
from QdrantConnection.ClientConnection import ClientConnect  # for individual checking
from qdrant_client import models

class Biology:

    def __init__(self,collection_name="Biology"):

        self.collection_name = collection_name
        self.collection = None
        self.client = ClientConnect()
        self.getClient = self.client.qdrant_connection

    def createCollection(self):

        try:

            if not self.client:
                raise ValueError("qdrant is not connected")
            
            self.collections = self.getClient.get_collections().collections  # get all collections from qdrant cloud
            self.collection_names = [collection.name for collection in self.collections] # store all collection names to check

            if self.collection_name not in self.collection_names:
                print("collection is not there")
                self.collection = self.getClient.create_collection(
                    collection_name=self.collection_name,
                    vectors_config={
                        "embedding_vectors":models.VectorParams(
                            size=385,
                            distance=models.Distance.COSINE
                        )
                    },
                    sparse_vectors_config={
                        "keyword_vector":models.SparseVectorParams(
                            index=models.SparseIndexParams(on_disk=False)
                        )
                    }
                )
                print(f"existing collections :,{self.getClient.get_collections()}")

        except Exception as e:
            print("error is : ",e)
            

obj1 = Biology()
obj1.createCollection()
