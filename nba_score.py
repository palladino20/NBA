import requests

url = "https://www.balldontlie.io/api/v1/games"

res = requests.get(url)

data = res.json()

game = data["data"][0]

title = f"{game['home_team']['full_name']} vs {game['visitor_team']['full_name']} 경기 결과"

body = f"""
{game['home_team']['full_name']} {game['home_team_score']}

{game['visitor_team']['full_name']} {game['visitor_team_score']}

경기 토론해봅시다.
"""

print(title)
print(body)
