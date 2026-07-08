from .reranking_service import RerankingService # for modular coding

# from Services.reranking_service import RerankingService

# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

class GenerationService:

    def __init__(self,query):

        self.query = query

        # self.llm = ChatGoogleGenerativeAI(
        #     model="gemini-2.5-flash",
        #     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
        #     temperature=0.1,
        #     max_tokens=1024
        # )

        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("AURIX_GROQ_API_KEY"),
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
                - Answer only from the given context.
                - Keep the answer clear and grammatically correct.
                - Use simple English.
                - Give 9-10 sentences if needed for better understanding.
                - Dont add extra information other than the context.

                Answer:
                """
        
        # response = self.llm.invoke(prompt)
        # return response.content
        stream_response = self.llm.stream(prompt)
        return stream_response
        

# query = input("Ask a Question : ")
# gen = GenerationService(query)
# out = gen.generate_answer()
# for chunk in out:
#     print(chunk.text,end="|",flush=True) # flush means immediately send response. it forces any buffered data to be delivered immediately.