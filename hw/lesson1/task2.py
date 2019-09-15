import requests
import json

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'

github_api_url = 'https://api.github.com/users/'

user_name = 'dzverkov'
user_pass = 'pass'

response = requests.get(f'{github_api_url}{user_name}/repos',  auth=(user_name, user_pass)
                        , headers={'User-Agent': USER_AGENT})

data = response.json()
res = []

for item in data:
    res.append(item.get('name'))

with open('repos_auth.json', 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)
