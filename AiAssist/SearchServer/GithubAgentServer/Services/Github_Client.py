from pathlib import Path
import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class GithubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.username = os.getenv("GITHUB_USERNAME")
        self.repository = os.getenv("GITHUB_REPOSITORY")
        self.token = os.getenv("GITHUB_TOKEN")

        self.repo_url = f"{self.BASE_URL}/repos/{self.username}/{self.repository}"
        self.content_url = f"{self.repo_url}/contents/"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    @staticmethod
    def _error(response):
        return {"error": response.status_code, "message": response.text}

    def _get(self, url):
        return requests.get(url, headers=self.headers, timeout=15)


    def get_repository(self):
        response = self._get(self.repo_url)

        if response.status_code != 200:
            return self._error(response)

        return response.json()

    def get_list_files(self):
        response = self._get(self.content_url)

        if response.status_code != 200:
            return self._error(response)

        data = response.json()

        if not isinstance(data, list):
            return {"error": "Unexpected response", "message": data}

        return [{"type": item["type"], "path": item["path"]} for item in data]

    # GET ONE FILE
    def get_file(self, file_path):
        response = self._get(f"{self.content_url}{file_path}")

        if response.status_code != 200:
            return self._error(response)

        data = response.json()

        # Directory
        if isinstance(data, list):
            return {
                "type": "directory",
                "path": file_path,
                "contents": [
                    {"type": item["type"], "path": item["path"]} for item in data
                ],
            }

        # Not a regular file
        if data.get("type") != "file":
            return {"error": "The requested path is not a file"}

        # Read file
        decoded_content = base64.b64decode(data["content"]).decode("utf-8")

        return {"file_path": file_path, "content": decoded_content}


    # GET REPOSITORY TREE
    def get_repository_tree(self, directory=""):
        response = self._get(f"{self.content_url}{directory}")

        if response.status_code != 200:
            return self._error(response)

        tree = []

        for item in response.json():
            if item["type"] == "file":
                tree.append({"type": "file", "path": item["path"]})

            elif item["type"] == "dir":
                tree.append({
                    "type": "directory",
                    "path": item["path"],
                    "children": self.get_repository_tree(item["path"]),
                })

        return tree

    # # GET USER FILE FROM REPOSITORY

    # def get_user_file(self, selected_file):

    #     stored_file_path = "self.content_url"

    #     stored_file_path += f"/{selected_file}"

    #     response = self._get(f"{stored_file_path}")

    #     if response.status_code != 200:
    #         return self._error(response)

    #     for item in response.json():
    #         if item["type"] == "file":
    #             decoded_content = base64.b64decode(item["content"]).decode("utf-8")

    #             return {"file_path":selected_file,"content":decoded_content}

    #         elif item["type"] == "dir":
    #             print(item["dir"])
    #             return self.get_user_file(selected_file)

    # ## GET DIRECT FILE FROM USER
    # def get_user_file(self, selected_file):
    
    #         stored_file_path = self.content_url/selected_file
    
    #         response = self._get(f"{self.content_url}{selected_file}")
    
    #         repo_root = Path(self.repository)
    
    #         selected_path = Path(selected_file)
    
    #         repo_path = selected_path.relative_to(repo_root)
    
    #         github_path = repo_path.as_posix()
    
    #         response = self._get(
    #             f"{self.content_url}{github_path}"
    #         )
    
    #         return response

client = GithubClient()
