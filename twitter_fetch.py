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

    try:

        res = requests.get(rss_url, timeout=10)

        if res.status_code != 200:
            print("RSS failed:", account)
            continue

        try:
            root = ET.fromstring(res.content)
        except:
            print("XML parse failed:", account)
            continue

        items = root.findall(".//item")[:3]

        for item in items:

            tweet = item.find("title").text
            link = item.find("link").text

            title = f"[NBA 기자 트윗] {tweet}"

            body = f"""
NBA 기자 트윗

{tweet}

원문:
{link}
"""

            post_to_github(title, body)

    except Exception as e:
        print("Error:", account, e)
        continue
