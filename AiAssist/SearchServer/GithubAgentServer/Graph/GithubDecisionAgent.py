# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# token = os.getenv("GITHUB_TOKEN")

# headers = {
#     "Authorization": f"Bearer {token}",
#     "Accept": "application/vnd.github+json"
# }

# response = requests.get(
#     "https://api.github.com/user",
#     headers=headers
# )

# print("Status:", response.status_code)
# print("Response:", response.json())







import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

owner=""
repo=""

# github api endpoint
url = f"https://api.github.com/repos/{owner}/{repo}/contents/"

# this is calls the git hub api
response = requests.get(url, headers=headers)

print("Status:", response.status_code)

data = response.json()

if response.status_code == 200:

    if isinstance(data, list):

        print("\nRepository files:\n")

        for file in data:
            print(file["type"], file["path"])

    else:
        print("Unexpected response:")
        print(data)

else:

    print("\nGitHub API Error:")
    print(data)