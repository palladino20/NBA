import requests
import os
from datetime import datetime

TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36RP"

today = datetime.utcnow().strftime("%Y%m%d")

url = f"https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

print("Fetching NBA results...")

res = requests.get(url)

data = res.json()

games = data["scoreboard"]["games"]

for game in games:

    home = game["homeTeam"]["teamName"]
    away = game["awayTeam"]["teamName"]

    home_score = game["homeTeam"]["score"]
    away_score = game["awayTeam"]["score"]

    status = game["gameStatusText"]

    title = f"[NBA 경기결과] {away} {away_score} - {home_score} {home}"

    body = f"""
NBA 경기 결과

{away} {away_score}
{home} {home_score}

경기 상태
{status}

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
