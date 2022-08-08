import requests
from pprint import pprint

url = 'https://oauth.vk.com/authorize?client_id=8169809&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52'

response = requests.get(url)

print(response.headers)
print(response.text)