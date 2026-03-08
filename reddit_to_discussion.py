import requests
import os

# GitHub 정보
TOKEN = os.environ["GITHUB_TOKEN"]
REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36mI"

# Reddit API
url = "https://www.reddit.com/r/nba/hot.json?limit=5"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; NBACommunityBot/1.0)"
}

res = requests.get(url, headers=headers)

if res.status_code != 200:
    print("Reddit API error:", res.status_code)
    exit()

data = res.json()

post = data["data"]["children"][0]["data"]

title_en = post["title"]
link = "https://reddit.com" + post["permalink"]

# 간단 번역 (AI 없이)
title_kr = "[Reddit 인기글] " + title_en

body = f"""
Reddit NBA 인기글

제목:
{title_en}

원문 링크
{link}

토론해봅시다.
"""

# GitHub GraphQL
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
"title": title_kr,
"body": body
}

headers = {
"Authorization": f"Bearer {TOKEN}"
}

response = requests.post(
"https://api.github.com/graphql",
json={"query": query, "variables": variables},
headers=headers
)

print(response.json())
