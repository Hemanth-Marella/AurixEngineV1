import pymupdf
from .pdfFile import GetFileName
from langchain_community.document_loaders import PyMuPDFLoader

file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"

class PdfToDocument:

    def __init__(self,file_path):

        self.loader = None
        self.file_loader = None
        self.documents = None

        self.page_count = None

        self.all_documents = []

        self.getfileDetails = GetFileName(file_path)
        self.filename = self.getfileDetails.file_name
        self.file = self.getfileDetails.file

    def load_pdf_to_raw_documents(self):

        try:
            self.loader = pymupdf.open(self.file)
            self.page_count = self.loader.page_count
            # print(self.page_count)
            for page in self.loader:
                self.all_documents.append(page)

            return self.all_documents , self.page_count
        except Exception as e:
            print("error is ", e)
    
    def load_pdf_to_documents(self):

        try:
            self.file_loader = PyMuPDFLoader(file_path=self.file)
            self.documents = self.file_loader.load()

            for doc in self.documents:
                doc.metadata["page_no"] = doc.metadata['page']

        except Exception as e:
            print("error is ", e)
            

    
# pdf = PdfToDocument(file_path=file_path)
# pdf.load_pdf_to_raw_documents()
# for page_no,page in enumerate(pdf.all_documents[:3],start=1):
#     text = page.get_text()
#     page_no = page_no
#     print("page number is " ,page_no)
#     print("text length is ",len(text))
#     print(text)