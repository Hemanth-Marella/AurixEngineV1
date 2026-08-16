from .retrieval_service import RetrieveService
from ..MongoDb import MongoDB
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
import asyncio
from groq import RateLimitError


import os
from dotenv import load_dotenv
load_dotenv()


class SummaryService:

    def __init__(self,chapter_name:str,file_hash:str):

        self.mongodb = MongoDB()
        self.response = None
        self.chapter_name = chapter_name
        self.file_hash = file_hash
        self.document = None
        self.chunks = None
        self.chunk_size = 0
        self.summary = ""

        self.retrieval = RetrieveService(query=None)

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("AURIX_GEMINI_KEY"),
            temperature=0.1,
        )

    async def summary_answer(self):

        # Hierachial summarization i am using hereb 
        # here i am using rolling algorithm

        check_file_hash = await self.mongodb.summary_storage.find_one(
            {"file_hash":self.file_hash,
             "chapter_name": self.chapter_name}
        )

        if check_file_hash:

            self.summary = check_file_hash['summary']
            return self.summary

        else:

            print("enter into summary")

            self.document = await self.mongodb.Aurix_collection.find_one(
                {"chapter_name": self.chapter_name,
                "file_hash":self.file_hash}
            )

            try:
                if self.document is None:
                    raise ValueError("Chapter name not found.")

                self.chapter_name = self.document["chapter_name"]

                self.chunks = await self.retrieval.summary_extraction_chunks(
                    self.chapter_name
                )

                if not self.chunks:
                    raise ValueError("No chunks found for this chapter.")

                # one window
                self.chunk_size = 20

                for i in range(0,len(self.chunks),self.chunk_size):

                    window = self.chunks[i:i+self.chunk_size]
                    
                    context = "\n\n".join(record.payload["text"] for record in window)

                    prompt = f"""
                            You are an educational content summarizer.

                            Current Summary:
                            {self.summary}

                            New Context:
                            {context}

                            Instructions:
                            1. Read ONLY the "Current Summary" and the "New Context".
                            2. Update the summary using ONLY the information present in the "New Context".
                            3. Do NOT use your own knowledge, assumptions, or external information.
                            4. Do NOT add facts, explanations, examples, applications, or definitions that are not explicitly stated in the provided context.
                            5. If a concept is not mentioned in the "New Context", do not introduce it.
                            6. Merge new information with the existing summary where appropriate.
                            7. Remove duplicate or redundant information.
                            8. Preserve previously summarized information unless the new context explicitly corrects or expands it.
                            9. Keep the summary concise, logically organized, and factually faithful to the provided text.
                            10. If the "New Context" contains no important new information, return the current summary unchanged.

                            Important Rule:
                            The output must be completely grounded in the provided "Current Summary" and "New Context". Do not generate or infer any additional information beyond what is explicitly written.

                            Return only the updated summary.
                            """
                    
                    while True:
                        try:
                            response =await self.llm.ainvoke(prompt)
                            self.summary = response.content
                            break

                        except RateLimitError:
                            await asyncio.sleep(3)

                    # Small pause before the next window
                    await asyncio.sleep(1)


                await self.mongodb.summary_storage.update_one(
                    {
                        "file_hash": self.file_hash,
                        "chapter_name": self.chapter_name
                    },
                    {
                        "$set": {
                            "summary": self.summary
                        }
                    },
                    upsert=True
                )

                return self.summary

            except Exception as e:
                raise RuntimeError(f"Summary generation failed: {e}") from e
