# study.ai_172@mail.ru
# NextPassword172#
import time
from pprint import pprint

import selenium
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('start-maximized')

s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)
driver.get('https://account.mail.ru/login')

actions = ActionChains(driver)

wait = WebDriverWait(driver, 10)
# input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Имя аккаунта")]')))
input = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Имя аккаунта")]')
input.send_keys('study.ai_172@mail.ru')
input.send_keys(Keys.ENTER)

input = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Пароль")]')
input.send_keys('NextPassword172#')
input.send_keys(Keys.ENTER)

# itter = driver.find_element(By.XPATH, '//span[contains(@class, "button2__explanation")]')
# itter.click()
# itter = driver.find_element(By.XPATH, "//td/span/div/span/span/span[contains(@class, 'button2__txt')]").text


message_list = []

message = driver.find_element(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')
message.click()

message_info = {}

message_title = driver.find_element(By.CLASS_NAME, 'thread-subject').text
message_from = driver.find_element(By.XPATH, "//span[contains(@class, 'letter-contact')]").text
message_date = driver.find_element(By.CLASS_NAME, 'letter__date').text
message_text = driver.find_element(By.XPATH, "//div[contains(@class, 'letter__body')]").text

message_info['title'] = message_title
message_info['from'] = message_from
message_info['date'] = message_date
message_info['text'] = message_text

message_list.append(message_info)
my_itter = 0

while my_itter != 1097:
    actions.key_down(Keys.CONTROL).key_down(Keys.ARROW_DOWN).key_up(Keys.CONTROL).key_up(Keys.ARROW_DOWN)
    actions.perform()
    my_itter += 1
    message_info = {}
    try:
        message_title = driver.find_element(By.CLASS_NAME, 'thread-subject').text
    except:
        message_title = ''
    try:
        message_from = driver.find_element(By.XPATH, "//span[contains(@class, 'letter-contact')]").text
    except:
        message_from = ''
    try:
        message_date = driver.find_element(By.CLASS_NAME, 'letter__date').text
    except:
        message_date = ''
    try:
        message_text = driver.find_element(By.XPATH, "//div[contains(@class, 'letter__body')]").text
    except:
        message_text = ''


    message_info['title'] = message_title
    message_info['from'] = message_from
    message_info['date'] = message_date
    message_info['text'] = message_text

    message_list.append(message_info)
    #time.sleep(2)

driver.close()

client = MongoClient('localhost', 27017)

db = client['user0206']

messagedb = db.messagedb

messagedb.delete_many({})

for el in message_list:
    hash_obj = hashlib.sha256(el['date'].encode())
    hex_dig = hash_obj.hexdigest()
    print(hex_dig)
    el['_id'] = hex_dig

for i in range(len(message_list)):
    try:
        messagedb.insert_one(message_list[i])
    except dke:
        print(f'Сломались на {i} элементе')

for doc in messagedb.find():
    pprint(doc)

pprint(message_list)


#print()

# link_messages = set()
#
# SCROLL_PAUSE_TIME = 0.5
#
# #Позиция последнего элементы относительно верха == 52650
# absolute_top_position = 52650
# body_height = driver.execute_script("return document.body.scrollHeight")
# scroll_itter = absolute_top_position // body_height
#
# for itter in range(scroll_itter):
#     a_hrefs = driver.find_elements(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')
#     for a_el_href in a_hrefs:
#         # a_el_href = driver.find_element(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')
#         href = a_el_href.get_attribute('href')
#         link_messages.add(href)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# # while absolute_top_position < 52650:
#     a_hrefs = driver.find_elements(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')
#     for a_el_href in a_hrefs:
#         # a_el_href = driver.find_element(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')
#         href = a_el_href.get_attribute('href')
#         link_messages.add(href)
#         #a_el_href.send_keys(Keys.PAGE_DOWN)
#
#         # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Wait to load page
# time.sleep(SCROLL_PAUSE_TIME)

# Calculate new scroll height and compare with last scroll height
# new_height = driver.execute_script("return document.body.scrollHeight")
# last_height = new_height
# absolute_top_position += last_height
# while True:
#     a_hrefs = driver.find_elements(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')
#     for a_el_href in a_hrefs:
#         # a_el_href = driver.find_element(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')
#         href = a_el_href.get_attribute('href')
#         link_messages.add(href)
#         #a_el_href.send_keys(Keys.PAGE_DOWN)
#     a_hrefs[-1].send_keys(Keys.PAGE_DOWN)
#     a_hrefs = driver.find_elements(By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')

# print(link_messages)
