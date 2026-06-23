import pymupdf
from DataIngestion.LoadPdf import PdfToDocument
import re

class BiologyDocumentMetadata:

    def __init__(self,file_path):

        self.first_pages = None
        self.chapterName = None
        self.topics = []
        self.load = PdfToDocument(file_path)
        self.all_details = []

    def getChapterName(self):
        self.all_pages = self.load.all_documents
        print("all pages is",len(self.all_pages))
        self.first_pages = self.load.all_documents[:2]
        for page in self.first_pages:
            self.data = page.get_text("dict")
            # regular = re.match(r"^")
            if "blocks" in self.data:
                for block in self.data["blocks"]:
                    if "lines" in block:
                        for lines in block["lines"]:
                            
                            for span in lines["spans"]:
                                text = span["text"]
                                font_size = span["size"]

                                if font_size >= 22:
                                    # print(f"text of the line is {text} and font size is {font_size}")
                                    self.all_details.append(text)
        # print(self.all_details)

    def sub_topics(self):
        if len(self.all_details) != 0:
            chapter_no = next((item for item in self.all_details if str(item).isdigit()),None)
            print(chapter_no)
            print("details is there")

        else:
            print("details is not there")
            
# file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology6.pdf"
file_path = "d:\projects\personalProject\Education\EducationChatbotServer\data\gecu104.pdf"
md = BiologyDocumentMetadata(file_path=file_path)
md.getChapterName()
md.sub_topics()