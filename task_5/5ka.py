from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

s = Service('./chromedriver')
options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)
driver.get("https://5ka.ru/special_offers")

print()

button = driver.find_element(By.XPATH, "//span[contains(text(),'Принять')]")
button.click()
button = driver.find_element(By.XPATH, "//span[contains(text(),'Понятно')]")
button.click()

page = 0
while page < 3:
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "add-more-btn")))
        # button = driver.find_element(By.CLASS_NAME, "add-more-btn")
        button.click()
        page += 1
    except:
        break

time.sleep(1)
goods = driver.find_elements(By.XPATH, "//div[@class='product-card item']")
for good in goods:
    name = good.find_element(By.CLASS_NAME, "item-name").text
    pprint(name)
