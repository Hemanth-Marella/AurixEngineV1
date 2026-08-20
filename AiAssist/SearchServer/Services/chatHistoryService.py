from ..MongoDb import MongoDB
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import os

class ChatHistoryService:

    def __init__(self,file_hash:str,query:str,state:dict):

        self.file_hash = file_hash
        self.query = query
        self.mongodb = MongoDB()
        self.answer = state

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("AURIX_GROQ_API_KEY"),
            temperature=0.1,
            max_tokens=1024
        )

    async def chat_history(self):

        ai_message = ""

        if self.answer.get("chapter_name"):
            ai_message += f"Chapter Name: {self.answer['chapter_name']}\n"

        if self.answer.get("sub_topics"):
            ai_message += f"Sub Topics: {', '.join(self.answer['sub_topics'])}\n"

        if self.answer.get("explanations"):
            ai_message += f"Explanation: {self.answer['explanations']}"

        if self.answer.get("answer"):
            ai_message += f"Answer: {self.answer['answer']}"

        if self.answer.get("quiz_result"):
            quiz = self.answer["quiz_result"]

            ai_message = quiz.get("generate_questions", "")

        history =await self.mongodb.Chat_History.find_one({"file_hash" : self.file_hash})

        message = {
            "user": self.query,
            "assistant": ai_message
        }

        if history:

            history["messages"].append(message)

            history["messages"] = history["messages"][-10:]

            await self.mongodb.Chat_History.update_one(
                {"file_hash": self.file_hash},
                {"$set": {"messages": history["messages"]}}
            )

            print("updated")

        else:

            await self.mongodb.Chat_History.insert_one({
                "file_hash": self.file_hash,
                "messages": [message]
            })
        return True
