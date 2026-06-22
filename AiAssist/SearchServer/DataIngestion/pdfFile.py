from pathlib import Path

class GetFileName:

    def __init__(self,file):
        self.file = file
        self.file_name = None
        self._fileName()

    def _fileName(self):

        try:
            path = Path(self.file)

            if not path.exists():
                raise FileNotFoundError("File does not exist")

            if path.suffix.lower() != ".pdf":
                raise ValueError("File is not a PDF")
                # return
            self.file_name = path.stem
        except Exception as e:
            print("Error : ",e)

# file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"
# file = GetFileName(file_path)
# print(file)