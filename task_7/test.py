import requests
import wget

url = 'https://www.castorama.ru/media/catalog/product/cache/thumbnail/80x/9df78eab33525d08d6e5fb8d27136e95/f/5/f5fc84_588850_1.jpg'
wget.download(url)

response = requests.get(url)

with open('palms.jpg', 'wb') as f:
    f.write(response.content)

response = requests.get(url, stream=True)
handle = open('palms.jpg', "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:  # filter out keep-alive new chunks
        handle.write(chunk)
