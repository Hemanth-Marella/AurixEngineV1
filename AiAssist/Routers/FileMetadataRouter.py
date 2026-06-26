from fastapi import FastAPI
from fastapi import APIRouter
from SearchServer.MongoDb.FileMetadataConnection import MongoDB
from SearchServer.Tools.BiologyMetadata import BiologyDocumentMetadata

# app = FastAPI()
# router = APIRouter()

router = APIRouter(   # for this docs is not open
    prefix="/chapter",
    tags=["Chapter"]
)
file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology3.pdf"
@router.post("/")
async def create_file_metadata():
    mongodb = MongoDB()
    metadata = BiologyDocumentMetadata(file_path=file_path)

    metadata.details_about_chapter()

    chapter_no = metadata.get_chapter_no()
    chapter_name = metadata.get_chapter_name()
    sub_topics = metadata.get_subTopics()
    total_pages = metadata.get_totalPages()

    result = await mongodb.Aurix_collection.insert_one(
        {
            "chapter_name":chapter_name,
            "chapter_no":chapter_no,
            "total_pages":total_pages,
            "sub_topics":sub_topics
        }
    )

    # if result:
    #     print("inserted")

    return {
        "chapter_name":chapter_name,
        "chapter_no":chapter_no,
        "total_pages":total_pages,
        "sub_topics":sub_topics
    }
