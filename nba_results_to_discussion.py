import requests
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPOSITORY_ID = "R_kgDORhJD1g"
CATEGORY_ID = "DIC_kwDORhJD1s4C36RP"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

print("Fetching NBA games...")

url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
data = requests.get(url).json()

games = data["scoreboard"]["games"]

for game in games:

    if game["gameStatusText"] != "Final":
        continue

    home = game["homeTeam"]["teamName"]
    away = game["awayTeam"]["teamName"]

    home_score = game["homeTeam"]["score"]
    away_score = game["awayTeam"]["score"]

    title = f"[NBA 경기결과] {away} {away_score} - {home_score} {home}"

    body = f"""
🏀 NBA 경기 결과

{away} {away_score}
{home} {home_score}

경기 종료

NBA 자동 봇
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
        "title": title,
        "body": body
    }

    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )

    print("Status:", r.status_code)
    print("Response:", r.text)

    if r.status_code == 200:
        print("Posted:", title)
    else:
        print("Failed:", title)
