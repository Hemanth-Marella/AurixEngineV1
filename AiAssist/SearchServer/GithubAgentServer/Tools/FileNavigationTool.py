## THIS FILE IS FOR GET FILE FROM GITHUB BASED ON USER REQUEST

from ..Services import GithubClient
from langchain.tools import tool
# from langgraph.types import interrupt

import base64


class FileNavigationTool:

    def __init__(self, github_client):
        self.github_client = github_client

    def get_path(self, path=""):

        response = self.github_client.get_path_contents(path)

        if response.status_code != 200:
            return {
                "success": False,
                "error": response.text
            }

        data = response.json()

        # FILE
        if isinstance(data, dict) and data["type"] == "file":

            content = base64.b64decode(
                data["content"]
            ).decode("utf-8")

            return {
                "success": True,
                "type": "file",
                "path": data["path"],
                "name": data["name"],
                "content": content
            }

        # DIRECTORY
        if isinstance(data, list):

            items = []

            for item in data:items.append({"name": item["name"],"path": item["path"],"type": item["type"]})

            return {
                "success": True,
                "type": "directory",
                "path": path,
                "items": items
            }

        return {
            "success": False,
            "error": "Unknown GitHub response"
        }
    