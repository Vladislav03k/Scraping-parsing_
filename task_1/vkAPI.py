#access_token=6a0f5afb4fdd8564517f5e322bcbc5252c289740e88dd6ccfbe6f2412a220abea65eb73a7bf21d0fe4199&expires_in=86400&user_id=92908535
# &expires_in=86400&user_id=92908535
import json

import requests
from pprint import pprint

url = "https://api.vk.com/method/groups.get"

params = {'access_token': '6a0f5afb4fdd8564517f5e322bcbc5252c289740e88dd6ccfbe6f2412a220abea65eb73a7bf21d0fe4199',
         'user_ids' : '92908535',
          'v' : '5.131'}
response = requests.get(url, params= params)

j_data = response.json()

pprint(j_data)

with open('vk_groups.json', 'w') as f:
    json.dump(j_data, f)

