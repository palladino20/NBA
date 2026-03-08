import requests
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36RN"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

print("Fetching Reddit posts...")

url = "https://www.reddit.com/r/nba/top.json?limit=5&t=day"

res = requests.get(url, headers={"User-agent": "nba-bot"})
data = res.json()

posts = data["data"]["children"]

for post in posts:

    title = post["data"]["title"]
    link = "https://reddit.com" + post["data"]["permalink"]

    new_title = "[Reddit NBA 인기글] " + title

    body = f"""
🔥 Reddit NBA 인기글

{title}

원문:
{link}

자동 번역/수집 봇
"""

    query = """
    mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input:{
        repositoryId:$repositoryId,
        categoryId:$categoryId,
        title:$title,
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
        "title": new_title,
        "body": body
    }

    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )

    print("Posted:", new_title)
