import requests
from github import Github
from pprint import pprint
import json

username = "Vladislav03k"

url = f'https://api.github.com/users/{username}?tab=repositories'

user_repo = requests.get(url).json()

pprint(user_repo)

with open('user_repo.json', 'w') as f:
    json.dump(user_repo, f)

#json.dump(user_repo)
#g = Github()

#user = g.get_user(username)

#for repo in user.get_repos():
   # print(repo)