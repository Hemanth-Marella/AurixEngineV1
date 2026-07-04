from .retrieval_service import RetrieveService  # this is for modular coding

# from Services.retrieval_service import RetrieveService

from sentence_transformers import CrossEncoder

class RerankingService:

    def __init__(self,query):

        self.query = query

        self.retrieval = RetrieveService(self.query)
        self.refusion = self.retrieval.rrf_fusion()
        # Small model (~80 MB)
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L4-v2",
            max_length=584,
        )

    def get_rankings(self):

        documents = [
            result.payload["text"]
            for result in self.refusion
        ]

        pairs = [[self.query,doc.payload['text']] for doc in self.refusion] # creating pairs with query with each extract page content

        scores = self.model.predict(pairs) # here it provides scoresbased on query and content

        # if we send refusion instead of documents we can get all metadata . is we store only document text data that is not good it extract only document text
          # x[0] means text , x[1] means score
        reranking_results = sorted(
            zip(self.refusion,scores), 
            key=lambda x: x[1],
            reverse=True
        )

        return reranking_results

# query = input("enter a query : ")
# reranker = RerankingService(query)
# output = reranker.get_rankings()    
# for idx, (result, score) in enumerate(output):
#     print(f"Rank {idx+1}")
#     print("Score :", score)
#     print("Text  :", result.payload["text"])
#     print("Page  :", result.payload["page_no"])
#     print("Chapter :", result.payload["chapter_name"])
#     print()