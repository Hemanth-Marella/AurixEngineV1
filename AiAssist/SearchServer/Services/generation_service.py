from .reranking_service import RerankingService # for modular coding

# from Services.reranking_service import RerankingService

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class GenerationService:

    def __init__(self,query):

        self.query = query

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("AURIX_GEMINI_KEY"),
            temperature=0.1,
            max_tokens=1024
        )

        self.reranker = RerankingService(query)
        self.generate_rankings = self.reranker.get_rankings()

    def generate_answer(self):

        answers = []
        # chapter_name = ""
        for idx,(result,score) in enumerate(self.generate_rankings):
            answers.append(result.payload['text'])

        # chapters = []

        if not answers:
            return "Your Question is Out of Chapter , Please ask questions based on chapter"
        context = "\n\n".join(answers)

        prompt = f"""
                You are an AI Educational Assistant.

                You must answer the user's question ONLY using the provided context.

                Context:
                {context}

                Question:
                {self.query}

                Instructions:
                1. Read the context carefully.
                2. Answer only from the provided context.
                3. Do not add information that is not present in the context.
                4. If context is long add bullet points.
                5. Give Answer More than 10 points which is more relevant to query.
                4. If the answer cannot be found in the context, reply:
                "The answer is not available in the provided chapter."
                6. Give no relevant text

                Answer:
                """
        
        # response = self.llm.invoke(prompt)
        # return response.content
        response_1 = self.llm.stream(prompt)
        return response_1
        

# query = input("Ask a Question : ")
# gen = GenerationService(query)
# out = gen.generate_answer()
# for chunk in out:
#     print(chunk.text,end="|",flush=True) # flush means immediately send response. it forces any buffered data to be delivered immediately.