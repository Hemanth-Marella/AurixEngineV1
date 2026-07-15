from ..VectorDB.BiologyCollection import Biology  # for modular coding

# from VectorDB.BiologyCollection import Biology # for individual implementation

from qdrant_client import models
import time

class RetrieveService:
    def __init__(self,query:str):
        self.user_query = query
        self.response = None

        self.collection_class = Biology()
        self.q_client = self.collection_class.getClient
        self.collection_name = self.collection_class.collection_name

        # results
        self.vector_results = None
        self.keyword_results = None
    
    def rrf_fusion(self):

        result = self.q_client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                models.Prefetch(
                    query=models.Document(
                        text=self.user_query,
                        model="sentence-transformers/all-MiniLM-L6-v2"
                    ),
                    using="embedding_vectors",
                    limit=5,
                ),
                models.Prefetch(
                    query=models.Document(
                        text=self.user_query,
                        model="Qdrant/bm25"
                    ),
                    using="keyword_vector",
                    limit=5,
                ),
            ],
            query=models.FusionQuery(
                fusion=models.Fusion.RRF
            ),
            limit=5,
        )

        self.response = result.points
        return self.response
    
    

    # FOR INDIVIDUALLY CHECKING
    # def dense_search(self):

    #     # self.start_time = time.perf_counter()

    #     self.vector_results = self.q_client.query_points(
    #         collection_name=self.collection_name,
    #         query=models.Document(
    #             text=self.user_query,
    #             model="sentence-transformers/all-MiniLM-L6-v2"
    #         ),
    #         using="embedding_vectors",
    #         limit=5
    #     )

    #     return self.vector_results
    
    # def sparse_search(self):

    #     # self.start_time = time.perf_counter()

    #     self.keyword_results = self.q_client.query_points(
    #         collection_name=self.collection_name,
    #         query=models.Document(
    #             text=self.user_query,
    #             model="Qdrant/bm25"
    #         ),
    #         using="keyword_vector",
    #         limit=5
    #     )

    #     return self.keyword_results
    
# query = input("enter a question : ")
# retriever = RetrieveService(query)
# rrf = retriever.rrf_fusion()

# for idx, result in enumerate(rrf, start=1):
#     if result.score >= 0.5:
#         print(result.payload['chapter_name'])
#         print(result.payload['text'])
#         print("********************")

# THIS IS FOR VECTOR SEARCH
# for idx , rrf in enumerate(rrf.points):
#     print(rrf.payload['page_no'])