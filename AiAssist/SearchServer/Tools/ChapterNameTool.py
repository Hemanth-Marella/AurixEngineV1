import asyncio
from bson import ObjectId
from MongoDb.FileMetadataConnection import MongoDB


async def get_chapter_name(document_id: str):
    mongodb = MongoDB()

    document = await mongodb.Aurix_collection.find_one(
        {"_id": ObjectId(document_id)}
    )

    print(document)

    if document is None:
        return None

    return document["chapter_name"]


async def main():
    document_id = "6a3ddf24de351f42f45c5ff0"

    chapter_name = await get_chapter_name(document_id)
    print(chapter_name)


if __name__ == "__main__":
    asyncio.run(main())