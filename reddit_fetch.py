import requests

url = "https://www.reddit.com/r/nba/hot.json"

headers = {"User-Agent": "nba-bot"}

res = requests.get(url, headers=headers)
data = res.json()

post = data["data"]["children"][0]["data"]

title = post["title"]
link = post["url"]

translated = "Reddit 인기글 번역: " + title

print(translated)
print(link)
