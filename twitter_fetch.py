import requests
import os
import xml.etree.ElementTree as ET

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36RN"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# 가져올 기자 목록
accounts = [
    "ShamsCharania",
    "wojespn",
    "anthonyVslater"
]

def post_to_github(title, body):

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
        "title": title,
        "body": body
    }

    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )

    print("Status:", r.status_code)
    print(title)


for account in accounts:

    print("Fetching:", account)

    rss_url = f"https://rsshub.app/twitter/user/{account}"

    res = requests.get(rss_url)

    root = ET.fromstring(res.content)

    items = root.findall(".//item")[:3]

    for item in items:

        tweet = item.find("title").text
        link = item.find("link").text

        title = f"[NBA 기자 트윗] {tweet}"

        body = f"""
NBA 기자 트윗 자동 수집

{tweet}

원문:
{link}

자동 봇
"""

        post_to_github(title, body)
