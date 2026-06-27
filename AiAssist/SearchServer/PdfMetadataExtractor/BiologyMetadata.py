import pymupdf
from ..DataIngestion.LoadPdf import PdfToDocument  # for modular coding
# from DataIngestion.LoadPdf import PdfToDocument # for individual running
import re

class BiologyDocumentMetadata:

    def __init__(self,file_path):

        self.first_pages = None
        self.all_pages = None
        self.chapterName = None
        self.chapter_no = None
        self.topics = []
        self.all_details = []
        self.chaptername_details =[]
        self.current_line = None
        self.sub_topic = None
        self.page_count = None

        # module 
        self.raw_documents,self.total_pages = PdfToDocument(file_path).load_pdf_to_raw_documents()

    def details_about_chapter(self):
        
        self.first_pages = self.raw_documents[:1]

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
            
            return self.chapter_no

        else:
            print("details is not there")

    
    def get_chapter_name(self):
        if len(self.chaptername_details) != 0:
            self.chapterName = "".join(self.chaptername_details)
            print(self.chapterName)
            return self.chapterName

    def get_subTopics(self):
        self.all_pages = self.raw_documents

        for page in self.all_pages:
            data = page.get_text("dict")

            # Skip pages with no text.
            if "blocks" not in data:
                continue

            for block in data["blocks"]:
                # some blocks may contain images , drawings etc so skip those blocks
                if "lines" not in block:
                    continue

                lines = block["lines"]

                i = 0
                while i < len(lines):

                    # Combine all spans of the current line
                    self.current_line = ""
                    font_size = 0

                    for span in lines[i]["spans"]:
                        """
                        line 0 :- span : 2.1
                                  span : " How to Study Cells?"
                        """
                        self.current_line += span["text"]   #example :- every line have 2(number span , text span) spans not for every one based on document
                        font_size = max(font_size, span["size"])

                    self.current_line = self.current_line.strip() # this removes gap

                    # Only consider side heading text
                    if 14 <= font_size <= 15.9:

                        # this is for number and text in one line
                        match = re.match(rf"^{self.chapter_no}\.\d+\s+.+",self.current_line)
                        if match:
                            self.topics.append(self.current_line)
                            # print(f"Subtopic: {self.current_line}, Font Size: {font_size}")

                        # Number on one line, title on next line
                        elif re.match(rf"^{self.chapter_no}\.\d+$",self.current_line): # this is match for only number

                            # Check if there is a next line
                            if i + 1 < len(lines):

                                # Get text from the next line and join here only
                                next_line = "".join(span["text"] for span in lines[i + 1]["spans"]).strip()
                                
                                # get the font size of the next line
                                next_font = max(span["size"]for span in lines[i + 1]["spans"])

                                if next_line and 14 <= next_font <= 15.9:
                                    self.sub_topic = (f"{self.current_line}{next_line}")
                                    self.topics.append(self.sub_topic)

                                    # print(f"self.sub_topic: {self.sub_topic}, Font Size: {font_size}")

                    i += 1
        return self.topics
    
    def get_totalPages(self):
        self.page_count = self.total_pages
        return self.page_count


# file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"
# # # file_path = "d:\projects\personalProject\Education\EducationChatbotServer\data\gecu104.pdf"
# md = BiologyDocumentMetadata(file_path=file_path)
# # md.detailsAboutChapter()
# # md.get_chapter_no()
# # # md.get_chapter_name()
# # md.get_subTopics()
# md.get_totalPages()