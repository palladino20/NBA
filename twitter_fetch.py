import requests
import os
import xml.etree.ElementTree as ET

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36RN"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

accounts = [
    "ShamsCharania",
    "wojespn",
    "anthonyVslater"
]

# 이미 올린 트윗 읽기
posted = set()

if os.path.exists("posted_tweets.txt"):
    with open("posted_tweets.txt") as f:
        posted = set(f.read().splitlines())

def save_posted(link):
    with open("posted_tweets.txt", "a") as f:
        f.write(link + "\n")

def post_to_github(title, body):

    query = """
    mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input:{
        repositoryId:$repositoryId,
        categoryId:$categoryId,
        title:$title,
        body:$body
      }) {
        discussion { id }
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

    print("Posted:", title)


for account in accounts:

    print("Fetching:", account)

    rss_url = f"https://nitter.net/{account}/rss"

    res = requests.get(rss_url)

    if res.status_code != 200:
        print("RSS fetch failed:", account)
        continue

    try:
        root = ET.fromstring(res.content)
    except:
        print("XML parse error:", account)
        continue

    items = root.findall(".//item")[:5]

    for item in items:

        tweet = item.find("title").text
        link = item.find("link").text

        # 중복 체크
        if link in posted:
            print("Skip duplicate:", link)
            continue

        title = f"[NBA 기자 트윗] {tweet}"

        body = f"""
NBA 기자 트윗

{tweet}

원문:
{link}

자동 수집 봇
"""

        post_to_github(title, body)

        save_posted(link)

