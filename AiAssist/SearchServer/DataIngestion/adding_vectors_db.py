# Modular coding
from .LoadPdf import PdfToDocument
from ..VectorDB.BiologyCollection import Biology
from ..VectorDB.ClientConnection import ClientConnect
from .Chunking import embedding_chunking


# for individual implementation
# from DataIngestion.LoadPdf import PdfToDocument
# from VectorDB.BiologyCollection import Biology
# from VectorDB.ClientConnection import ClientConnect
# from DataIngestion.Chunking import embedding_chunking

# libraries
from qdrant_client import models
from rank_bm25 import BM25Okapi
import uuid

# .
class AddingVectorsToDb:

    def __init__(self,pdf_bytes:bytes,filename:str):
        self.biology_collection = Biology() # collection
        self.client = ClientConnect()
        self.getClient = self.client.connection_checking()
        self.process_pdf = PdfToDocument(pdf_bytes,filename)

        self.documents = None
        self.chunks = None
        
    def generate_documents(self,chapter_name):
        try:
            if self.documents is None:
                self.documents = self.process_pdf.load_pdf_to_documents(chapter_name) # return list of documents
                if self.documents:
                    print("documents created") 
                return self.documents
        except Exception as e:
            print(f"documents creation error : {e}")

    def generate_chunks(self,chapter_name):
        try:
            if self.documents is None:
                self.generate_documents(chapter_name)

            self.chunks = embedding_chunking(
                documents=self.documents,
                chunk_size=500,
                chunk_overlap=80
            )

            print("chunks created")

            return self.chunks
        except Exception as e:
            print(f"chunks error is : {e}")

    def add_vectors_to_cloud(self,chapter_name):

        try:
            if self.chunks is None:
                self.generate_chunks(chapter_name)
            collection_name = self.biology_collection.createCollection()
            print("collection name is :",collection_name)
            vectors = []
            for chunk in self.chunks:
            # for chunk_index, chunk in enumerate(self.chunks):
                vectors.append(
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector={
                            "embedding_vectors":models.Document(
                                text=chunk.page_content,
                                model ="sentence-transformers/all-MiniLM-L6-v2",
                            ),
                            "keyword_vector":models.Document(
                                text=chunk.page_content,
                                model="Qdrant/bm25"
                            )
                        },
                        payload={
                            "page_no":chunk.metadata.get("page_number"),
                            "chapter_name":chunk.metadata.get("chapter_name"),
                            # "chunk_index":chunk_index,
                            "text":chunk.page_content
                        }
                    )
                )
            
            batch_size = 30
            for i in range(0,len(vectors),batch_size):
                batch = vectors[i:i+batch_size]
                self.getClient.upsert(
                    collection_name=collection_name,
                    points=batch
                )

        except Exception as e:
            print("error is : ", e)

    
