import pymupdf
# from ..DataIngestion.LoadPdf import PdfToDocument  # for modular coding
from DataIngestion.LoadPdf import PdfToDocument # for individual running
import re

class BiologyDocumentMetadata:

    def __init__(self,file_path):

        self.first_pages = None
        self.all_pages = None
        self.chapterName = None
        self.chapter_no = None
        self.topics = []
        self.load = PdfToDocument(file_path)
        self.all_details = []
        self.chaptername_details =[]

    def detailsAboutChapter(self):
        
        self.first_pages = self.load.all_documents[:1]

        for page in self.first_pages:
            self.data = page.get_text("dict")
            
            if "blocks" in self.data:
                for block in self.data["blocks"]:
                    if "lines" in block:
                        for lines in block["lines"]:
                            
                            for span in lines["spans"]:
                                text = span["text"]
                                font_size = span["size"]

                                if font_size >= 22 and font_size <= 28:
                                    self.chaptername_details.append(text)

                                elif font_size >= 28:
                                    self.all_details.append(text)


    def get_chapter_no(self):
        if len(self.all_details) != 0:
            self.chapter_no = next((item for item in self.all_details if str(item).isdigit()),None)
            print(self.chapter_no)
            return self.chapter_no

        else:
            print("details is not there")

    
    def get_chapter_name(self):
        if len(self.chaptername_details) != 0:
            self.chapterName = "".join(self.chaptername_details)
            print(self.chapterName)
            return self.chapterName
        
    def get_subTopics(self):
        self.all_pages = self.load.all_documents

        for page in self.all_pages:
            data = page.get_text("dict")

            if "blocks" in data:
                for block in data["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text = span["text"]
                                font_size = span["size"]

                                # print(text)

                                if font_size >= 14 and font_size <= 15.9:
                                    matches = re.findall(
                                        rf"^{self.chapter_no}\.\d+[\s\r\n*]+.+",
                                        text,
                                        re.MULTILINE
                                    )
                                    # self.topics.extend(matches)
                                    for match in matches:

                                        print(f"Subtopic: {match}, Font Size: {font_size}")

            # self.topics.extend(matches)

        # print(self.topics)

        # return self.topics
            
            
file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"
# # file_path = "d:\projects\personalProject\Education\EducationChatbotServer\data\gecu104.pdf"
md = BiologyDocumentMetadata(file_path=file_path)
md.detailsAboutChapter()
md.get_chapter_no()
# md.get_chapter_name()
md.get_subTopics()