
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()


class GithubClient:

    def __init__(self):

        self.username = os.getenv("GITHUB_USERNAME")
        self.repository = os.getenv("GITHUB_REPOSITORY")

        self.repo_url = (f"https://api.github.com/repos/"
                f"{self.username}/{self.repository}"
        )

        self.content_url = (f"https://api.github.com/repos/"
                            f"{self.username}/{self.repository}/contents/"
        )

        self.token = os.getenv("GITHUB_TOKEN")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get_repository(self):

        response = requests.get(self.repo_url,headers=self.headers)

        if response.status_code == 200:
            return response.json()

        return {
            "error": response.status_code,
            "message": response.text
        }

    def get_list_files(self):

        response = requests.get(self.content_url,headers=self.headers)

        if response.status_code != 200:
            return {
                "error": response.status_code,
                "message": response.text
            }

        data = response.json()

        if isinstance(data, list):

            files = []

            for item in data:
                files.append({"type": item["type"],"path": item["path"]})

            return files

        return {
            "error": "Unexpected response",
            "message": data
        }

    def get_file(self, file_path):

        file_url = f"{self.content_url}{file_path}"
        response = requests.get(file_url,headers=self.headers)

        if response.status_code != 200:

            return {
                "error": response.status_code,
                "message": response.text
            }

        data = response.json()

        # Directory
        if isinstance(data, list):

            return {
                "type": "directory",
                "path": file_path,
                "contents": [
                    {
                        "type": item["type"],
                        "path": item["path"]
                    }
                    for item in data
                ]
            }

        # this is for file
        if data.get("type") != "file":

            return {
                "error": "The requested path is not a file"
            }

        encoded_content = data["content"]

        decoded_content = base64.b64decode(encoded_content).decode("utf-8")

        return {
            "file_path": file_path,
            "content": decoded_content
        }


file = input("Enter a file name : ")

github = GithubClient()
result = github.get_file(file)
# result = github.get_list_files()
print(result)