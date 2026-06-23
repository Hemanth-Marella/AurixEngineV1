import pymupdf
from .pdfFile import GetFileName

file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"

class PdfToDocument:

    def __init__(self,file_path):

        self.loader = None
        self.all_documents = []

        self.getfileDetails = GetFileName(file_path)

        self.filename = self.getfileDetails.file_name
        self.file = self.getfileDetails.file

        self._load_pdf_to_documents()

    def _load_pdf_to_documents(self):

        print("file name is ",self.filename)
        print("file is :" ,self.file)

        self.loader = pymupdf.open(self.file)
        for page in self.loader:
            self.all_documents.append(page)

        return self.all_documents
    
# pdf = PdfToDocument(file_path=file_path)
# for page in pdf.all_documents[:3]:
#     text = page.get_text()
#     print(text)