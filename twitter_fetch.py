import requests
import os

TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36RN"

title = "Anthony Slater: Warriors update"
body = """
https://x.com/anthonyVslater

새 트윗이 올라왔습니다.

내용:
Warriors rotation update tonight.
"""

query = """
mutation($repositoryId:ID!, $categoryId:ID!, $title:String!, $body:String!) {
  createDiscussion(input:{
    repositoryId:$repositoryId
    categoryId:$categoryId
    title:$title
    body:$body
  }) {
    discussion {
      id
    }
  }
}
"""

variables = {
"repositoryId": REPOSITORY_ID,
"categoryId": CATEGORY_ID,
"title": title,
"body": body
}

headers = {
"Authorization": f"Bearer {TOKEN}"
}

requests.post(
"https://api.github.com/graphql",
json={"query": query, "variables": variables},
headers=headers
)
