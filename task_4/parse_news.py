from lxml import html
import requests
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import hashlib

url_yandex = 'https://yandex.ru/'
url_mail = 'https://mail.ru'
url_lenta = 'https://lenta.ru/'

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}

# response = requests.get(url_mail, headers= headers)
#
# dom = html.fromstring(response.text)
#
# news = dom.xpath("//li[contains(@class, 'news-item-container')]")

list_news = []

# for one_news in news[1:]:
#     one_news_info = {}
#     one_name_source = 'https://mail.ru/'
#     one_news_text = one_news.xpath("//div/a/text()")
#     one_news_link = one_news.xpath("//div/a/@href")
#     one_news_date = datetime.now().strftime('%d-%m-%Y')
#
#     one_news_info['source'] = one_name_source
#     one_news_info['text'] = one_news_text
#     one_news_info['link'] = one_news_link
#     one_news_info['date'] = one_news_date
#     list_news.append(one_news_info)

response = requests.get(url_yandex, headers= headers)

dom = html.fromstring(response.text)

news = dom.xpath("//li[contains(@class, 'list__item')]")

for one_news in news:
    one_news_info = {}
    one_name_source = 'https://yandex.ru/'
    one_news_text = one_news.xpath("./a[contains(@class, 'home-link2 news__item')]/@aria-label")
    one_news_link = one_news.xpath("./a[contains(@class, 'home-link2 news__item')]/@href")
    one_news_date = datetime.now().strftime('%d-%m-%Y')

    one_news_info['source'] = one_name_source
    one_news_info['text'] = one_news_text[0].replace("\xa0", ' ')
    one_news_info['link'] = one_news_link[0]
    one_news_info['date'] = one_news_date
    list_news.append(one_news_info)

response = requests.get(url_lenta, headers= headers)

dom = html.fromstring(response.text)

news = dom.xpath("//a[contains(@class, 'card-mini')]")

for one_news in news:
    one_news_info = {}
    one_name_source = 'https://lenta.ru/'
    one_news_link = one_news.xpath("./div/span[contains(@class, 'card-mini__title')]/../../@href")
    one_news_text = one_news.xpath("./div/span[contains(@class, 'card-mini__title')]/text()")
    one_news_date = one_news.xpath("./div/div/time/text()")

    one_news_info['source'] = one_name_source
    one_news_info['text'] = one_news_text[0]
    one_news_info['link'] = one_news_link[0]
    one_news_info['date'] = one_news_date
    list_news.append(one_news_info)

client = MongoClient('localhost', 27017)

db = client['user0106']

newsdb = db.newsdb

newsdb.delete_many({})

for el in list_news:
    hash_obj = hashlib.sha256(el['link'].encode())
    hex_dig = hash_obj.hexdigest()
    print(hex_dig)
    el['_id'] = hex_dig

for i in range(len(list_news)):
    try:
        newsdb.insert_one(list_news[i])
    except dke:
        print(f'Сломались на {i} элементе')

for doc in newsdb.find():
    pprint(doc)

pprint(list_news)