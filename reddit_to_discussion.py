import requests
import os
import feedparser

TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36mI"

print("Fetching Reddit RSS...")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

feed = feedparser.parse("https://www.reddit.com/r/nba/.rss")

for entry in feed.entries[:5]:

    title_en = entry.title
    link = entry.link

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

    print("Posted:", title)
