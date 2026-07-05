
# WORKS DIRECTLY WITH UPLOADED FILE
class pdfValidator:
    def __init__(self,filename:str,pdf_bytes:bytes):

        self.filename = filename
        self.pdf_bytes = pdf_bytes

        self.file_name = None
        self._validate()

    def _validate(self):

        print(type(self.filename))
        # print(self.filename)

        # validate file name
        if not self.filename:
            raise ValueError("Filename is Missing...")

        if not self.filename.lower().endswith(".pdf"):
            raise ValueError("uploaded file is not a pdf..")
        
        # validate file content
        if not self.pdf_bytes:
            raise ValueError("uploaded Pdf is Empty")
        
        # remove extension
        self.file_name = self.filename.rsplit(".",1)[0]



# WORK WITH ONLY PDF PATH 

# from pathlib import Path

# class PdfValidator:

#     def __init__(self,file):
#         self.file = file
#         self.file_name = None
#         self._fileName()

#     def _fileName(self):

#         try:
#             path = Path(self.file)

#             if not path.exists():
#                 raise FileNotFoundError("File does not exist")

#             if path.suffix.lower() != ".pdf":
#                 raise ValueError("File is not a PDF")
#                 # return
#             self.file_name = path.stem
#         except Exception as e:
#             print("Error : ",e)

# file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"
# file = GetFileName(file_path)
# print(file)