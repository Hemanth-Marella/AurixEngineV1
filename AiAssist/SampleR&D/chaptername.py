import pymupdf
from pathlib import Path

class ChapterName:

    def __init__(self, file):
        self.file = file
        self._getChaptername()

    def _getChaptername(self):

        try:
            path = Path(self.file)

            if not path.exists():
                print("File does not exist")
                return

            if path.suffix.lower() != ".pdf":
                print("File is not a PDF")
                return

            print("Valid PDF file")

            loader = pymupdf.open(path)

            # Continue processing...

        except Exception as e:
            print("Error:", e)


file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"
chapter = ChapterName(file_path)

# loader = pymupdf.open(file_path)

# pages = loader[:2]
# for page in pages:

#     data = page.get_text("dict")

#     if data:
#         for block in data["blocks"]:

#             if "lines" in block:
#                 for line in block["lines"]:

#                     if "spans" in line:
#                         for span in line["spans"]:

#                             text = span['text']
#                             bbox = span["bbox"]

#                             if re.search(r"^\s*Chapter\s*$", text, re.IGNORECASE):
#                                 font_size = span['size']
#                                 font_name = span['font']
#                                 # print(f"font_size is {font_size}  and font style is {font_name} and text is {text} and bbox is{bbox}")
#                                 print("done")
#                             else:
#                                 print("not done")
