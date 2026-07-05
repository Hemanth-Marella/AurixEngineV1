# FOR MODULAR CODING
from ..PdfMetadataExtractor.BiologyMetadata import BiologyDocumentMetadata
# from .Routers.FileMetadataRouter import create_file_metadata
from ..FileHashing.AvalancheEffect import FileHasher
from ..MongoDb.FileMetadataConnection import MongoDB
from ..DataIngestion.adding_vectors_db import AddingVectorsToDb


# FOR INDIVIDUAL IMPLEMENTATION
# from SearchServer.PdfMetadataExtractor.BiologyMetadata import BiologyDocumentMetadata
# from Routers.FileMetadataRouter import create_file_metadata
# from SearchServer.FileHashing.AvalancheEffect import FileHasher
# from SearchServer.MongoDb.FileMetadataConnection import MongoDB
# from SearchServer.DataIngestion.adding_vectors_db import AddingVectorsToDb


# from fastapi import APIRouter,FastAPI
import asyncio


# app = FastAPI()


class PdfProcessingService:

    def __init__(self,pdf_bytes:bytes,filename:str):
        
        self.hasher = FileHasher(pdf_bytes)
        self.mongodb = MongoDB()
        self.document_metadata = BiologyDocumentMetadata(pdf_bytes,filename)
        self.adding_vactors = AddingVectorsToDb(pdf_bytes,filename)
        # self.router = create_file_metadata()

        # values
        self.hash_value = None

    def generate_hash(self):

        if self.hash_value is None:
            self.hash_value = self.hasher.creating_hash()

        return self.hash_value
    
    async def upload_document(self):

        hash_value = self.generate_hash()

        document = await self.mongodb.Aurix_collection.find_one(
            {"file_hash":hash_value}
        )

        if document is None:
            self.document_metadata.details_about_chapter()
            chapter_name = self.document_metadata.get_chapter_name()
            chapter_no = self.document_metadata.get_chapter_no()
            total_pages = self.document_metadata.get_totalPages()
            sub_topics = self.document_metadata.get_subTopics()
            await self.mongodb.Aurix_collection.insert_one(
                {
                    "file_hash": hash_value,
                    "chapter_name":chapter_name,
                    "chapter_no":chapter_no,
                    "total_pages":total_pages,
                    "sub_topics":sub_topics
                }
            )

            self.adding_vactors.add_vectors_to_cloud(chapter_name)
            return {
                "status": "uploaded",
                "file_hash": hash_value,
                "chapter_name":chapter_name,
            }
        else:
            return{
                "status" : "duplicate",
                "file_hash" : hash_value
            }
        
# file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology2.pdf"
# async def main():
#     upload = PdfProcessingService(file_path=file_path)
#     get =await upload.upload_document()
#     print(get)
# if __name__ == "__main__":
#     asyncio.run(main())