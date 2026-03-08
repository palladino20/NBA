import requests
import os

TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36mI"

url = "https://api.reddit.com/r/nba/hot?limit=5"

headers = {
    "User-Agent": "NBACommunityBot/1.0"
}

res = requests.get(url, headers=headers)

data = res.json()

posts = data["data"]["children"]

for post in posts:

    title_en = post["data"]["title"]
    link = "https://reddit.com" + post["data"]["permalink"]

    title = "[Reddit NBA] " + title_en

    body = f"""
Reddit NBA 인기글

제목:
{title_en}

원문
{link}

토론해봅시다.
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

    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )

    print(r.text)
