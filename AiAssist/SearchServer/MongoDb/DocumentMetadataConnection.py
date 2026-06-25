# DIRECTLY CREATING HOST AND PORT INSIDE CODE 

# from motor.motor_asyncio import AsyncIOMotorClient
# import os
from dotenv import load_dotenv
load_dotenv()

# class MongoDB:

#     def __init__(self):
#         self.client = AsyncIOMotorClient(
#             "mongodb://localhost:27017"
#         )

#         self.db = self.client.AurixDataBase
#         self.chapters_collection = self.db.DocumentMetadata

# # mongodb = MongoDB()

# from motor.motor_asyncio import AsyncIOMotorClient




# STORING HOST AND PORT ON .ENV FILE
import os
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    def __init__(self):

        db_host = os.getenv("MONGODBHOST")
        db_port = os.getenv("MONGODBPORT")

        print("HOST =", os.getenv("MONGODBHOST"))
        print("PORT =", os.getenv("MONGODBPORT"))

        if not db_host or not db_port:
            raise ValueError("Missing MongoDB environment variables")

        self.client = AsyncIOMotorClient(f"mongodb://{db_host}:{db_port}")

        self.db = self.client["AurixDataBase"]
        self.Aurix_collection = self.db["DocumentMetadata"]

# mongodb = MongoDB()

# from motor.motor_asyncio import AsyncIOMotorClient
# import asyncio

# async def check_db():
#     client = AsyncIOMotorClient("mongodb://localhost:27017")

#     dbs = await client.list_database_names()
#     print(dbs)

# if __name__ == "__main__":
#     asyncio.run(check_db())