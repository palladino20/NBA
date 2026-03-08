import requests
import feedparser
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36RN"

feed = feedparser.parse("https://nitter.net/anthonyVslater/rss")

latest = feed.entries[0]

title = "Anthony Slater 트윗"
body = f"""
{latest.title}

원문:
{latest.link}

NBA 커뮤니티 의견은?
"""

query = f"""
mutation {{
  createDiscussion(
    input: {{
      repositoryId: "{REPOSITORY_ID}"
      categoryId: "{CATEGORY_ID}"
      title: "{title}"
      body: \"\"\"{body}\"\"\"
    }}
  ) {{
    discussion {{
      url
    }}
  }}
}}
"""

requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    },
)