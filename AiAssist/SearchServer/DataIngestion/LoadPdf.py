import pymupdf
from .Pdf_Validator import pdfValidator
from langchain_core.documents import Document

file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"

class PdfToDocument:

    def __init__(self,pdf_bytes: bytes, filename: str):

        self.loader = None
        self.file_loader = None
        self.documents = None

        self.page_count = None

        self.raw_documents = []
        self.embedding_documents = []

        self.validator = pdfValidator(filename, pdf_bytes)
        self.filename = self.validator.file_name
        self.pdf_bytes = pdf_bytes

    def load_pdf_to_raw_documents(self):

        try:
            self.loader = pymupdf.open(stream=self.pdf_bytes,filetype="pdf")
            self.page_count = self.loader.page_count
            # print(self.page_count)
            for page in self.loader:
                self.raw_documents.append(page)

            return self.raw_documents , self.page_count
        except Exception as e:
            print("error is ", e)
    
    def load_pdf_to_documents(self,chapter_name):

        try:
            self.file_loader = pymupdf.open(stream=self.pdf_bytes,filetype="pdf")
            for page_number,page in enumerate(self.file_loader,start=1):

                text = page.get_text()
                document = Document(
                    page_content=text,
                    metadata = {
                        "page":page_number-1,
                        "page_number" : page_number,
                        "chapter_name":chapter_name
                    }
                )

                self.embedding_documents.append(document)

            return self.embedding_documents

        except Exception as e:
            print("error is ", e)
        
        
# pdf = PdfToDocument(file_path=file_path)
# doc = pdf.load_pdf_to_documents()
# for documents in doc:
#     print(documents.metadata)
# pdf.load_pdf_to_raw_documents()
# for page_no,page in enumerate(pdf.all_documents[:3],start=1):
#     text = page.get_text()
#     page_no = page_no
#     print("page number is " ,page_no)
#     print("text length is ",len(text))
#     print(text)