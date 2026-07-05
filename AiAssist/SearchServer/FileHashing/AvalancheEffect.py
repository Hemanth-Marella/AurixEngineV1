import hashlib

class FileHasher:

    def __init__(self, pdf_bytes: bytes):

        self.pdf_bytes = pdf_bytes

    def creating_hash(self):

        sha256 = hashlib.sha256()

        return hashlib.sha256(self.pdf_bytes).hexdigest()

# WORKS WITH PATHOF FILE ONLY
# class FileHasher:

#     def __init__(self,file):
#         self.file_path = file
#         self.file_hash = None

#     def creating_hash(self):
#         sha256 = hashlib.sha256()
        
#         with open(self.file_path,"rb") as file:
#             while chunk := file.read(8192):
#                 sha256.update(chunk)
#         self.file_hash = sha256.hexdigest()

#         return self.file_hash

# file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"