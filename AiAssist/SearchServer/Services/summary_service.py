from .retrieval_service import RetrieveService
from ..MongoDb import MongoDB
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from groq import RateLimitError


import os
from dotenv import load_dotenv
load_dotenv()


class SummaryService:

    def __init__(self,chapter_name):

        self.mongodb = MongoDB()
        self.response = None
        self.chapter_name = chapter_name
        self.document = None
        self.chunks = None
        self.context = None
        self.chunk_size = 0
        self.summary = ""

        self.retrieval = RetrieveService(query=None)

        # self.llm = ChatGoogleGenerativeAI(
        #     model="gemini-2.5-flash",
        #     google_api_key=os.getenv("AURIX_GEMINI_KEY"),
        #     temperature=0.1,
        #     max_tokens=1024
        # )

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("AURIX_GROQ_API_KEY"),
            temperature=0,
            # max_tokens=1024, # output can generate only this much tokens 
        )


    # async def summary_answer(self):

    #     # Hierachial summarization i am using hereb 
    #     # here i am using rolling algorithm

    #     self.document = await self.mongodb.Aurix_collection.find_one(
    #         {"chapter_name": self.chapter_name}
    #     )

    #     try:
    #         if self.document is None:
    #             raise ValueError("Chapter name not found.")

    #         self.chapter_name = self.document["chapter_name"]

    #         self.chunks = await self.retrieval.summary_extraction_chunks(
    #             self.chapter_name
    #         )

    #         if not self.chunks:
    #             raise ValueError("No chunks found for this chapter.")

    #         # one window
    #         self.chunk_size = 10

    #         for i in range(0,len(self.chunks),self.chunk_size):

    #             window = self.chunks[i:i+self.chunk_size]
                
    #             context = "\n\n".join(record.payload["text"] for record in window)

    #             prompt = f"""
    #                     You are an educational content summarizer.

    #                     Current Summary:
    #                     {self.summary}

    #                     New Context:
    #                     {context}

    #                     Instructions:
    #                     1. Read ONLY the "Current Summary" and the "New Context".
    #                     2. Update the summary using ONLY the information present in the "New Context".
    #                     3. Do NOT use your own knowledge, assumptions, or external information.
    #                     4. Do NOT add facts, explanations, examples, applications, or definitions that are not explicitly stated in the provided context.
    #                     5. If a concept is not mentioned in the "New Context", do not introduce it.
    #                     6. Merge new information with the existing summary where appropriate.
    #                     7. Remove duplicate or redundant information.
    #                     8. Preserve previously summarized information unless the new context explicitly corrects or expands it.
    #                     9. Keep the summary concise, logically organized, and factually faithful to the provided text.
    #                     10. If the "New Context" contains no important new information, return the current summary unchanged.

    #                     Important Rule:
    #                     The output must be completely grounded in the provided "Current Summary" and "New Context". Do not generate or infer any additional information beyond what is explicitly written.

    #                     Return only the updated summary.
    #                     """
                
    #             while True:
    #                 try:
    #                     response = self.llm.invoke(prompt)
    #                     self.summary = response.content
    #                     break

    #                 except RateLimitError:
    #                     print("Rate limit reached. Waiting 3 seconds...")
    #                     await asyncio.sleep(3)

    #             # Small pause before the next window
    #             await asyncio.sleep(1)

    #         return self.summary

    #     except Exception as e:
    #         raise ValueError(f"Error in summary: {str(e)}")


    async def summary_answer(self):

        self.document = await self.mongodb.Aurix_collection.find_one(
            {"chapter_name": self.chapter_name}
        )

        try:

            if self.document is None:
                raise ValueError("Chapter name not found.")

            self.chapter_name = self.document["chapter_name"]

            self.chunks = await self.retrieval.summary_extraction_chunks(
                self.chapter_name
            )

            # for report in self.chunks:
            #     print(report)

            if not self.chunks:
                raise ValueError("No chunks found.")

            # Smaller window reduces incorrect merging
            self.chunk_size = 5

            self.summary = ""

            # ----------------------------
            # Rolling Summarization
            # ----------------------------
            for start in range(0, len(self.chunks), self.chunk_size):

                print(start)

                window = self.chunks[start:start + self.chunk_size]

                context = ""

                for idx, record in enumerate(window, start=1):
                    context += f"""
    ========== CHUNK {idx} ==========
    {record.payload["text"]}

    """

                prompt = f"""
    You are an educational summarization assistant.

    Current Summary:
    {self.summary}

    New Context:
    {context}

    Task:
    Read ONLY the Current Summary and the New Context.

    Instructions:

    1. Extract only the important information from the New Context.

    2. Merge it into the Current Summary.

    3. Use ONLY the provided text.

    4. Do NOT use external knowledge.

    5. Do NOT infer missing information.

    6. Do NOT add examples.

    7. Do NOT add explanations.

    8. Do NOT add applications.

    9. Do NOT combine unrelated concepts.

    10. Keep plant tissues and animal tissues separate.

    11. Preserve the wording as closely as possible to the source.

    12. Remove duplicate information.

    13. If no important information exists, return the Current Summary unchanged.

    Return ONLY the updated summary.
    """

                while True:

                    try:

                        response = self.llm.invoke(prompt)

                        self.summary = response.content.strip()

                        break

                    except RateLimitError:

                        print("Rate limit reached. Waiting 3 seconds...")
                        await asyncio.sleep(3)

                await asyncio.sleep(1)

            # ---------------------------------------------------
            # Final Cleanup Pass
            # ---------------------------------------------------

            cleanup_prompt = f"""
    You are an educational content editor.

    Below is a summary created from multiple chunks of the SAME chapter.

    Summary:
    {self.summary}

    Task:

    1. Remove duplicate points.

    2. Merge repeated ideas.

    3. Keep related information together.

    4. Preserve all important information.

    5. Do NOT add any new information.

    6. Do NOT use outside knowledge.

    7. Do NOT infer relationships.

    8. Keep plant tissues and animal tissues separate.

    9. Organize the summary using headings and bullet points.

    10. If two statements appear contradictory, keep both exactly as written instead of trying to correct them.

    Return ONLY the cleaned summary.
    """

            while True:

                try:

                    response = self.llm.invoke(cleanup_prompt)

                    self.summary = response.content.strip()

                    break

                except RateLimitError:

                    print("Rate limit reached. Waiting 3 seconds...")
                    await asyncio.sleep(3)

            return self.summary

        except Exception as e:
            raise ValueError(f"Error in summary: {str(e)}")