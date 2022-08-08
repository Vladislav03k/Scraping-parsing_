from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)

driver.get("https://gb.ru/login")

input = driver.find_element(By.ID, "user_email")
input.send_keys("study.ai_172@mail.ru")

input = driver.find_element(By.ID, "user_password")
input.send_keys("Password172")

input.send_keys(Keys.ENTER)

profile = driver.find_element(By.XPATH, "//a[contains(@href,'/users/')]")
href = profile.get_attribute("href")
driver.get(href)

profile = driver.find_element(By.CLASS_NAME, "text-sm")
href = profile.get_attribute("href")
driver.get(href)

timezone = driver.find_element(By.NAME, "user[time_zone]")
select = Select(timezone)
select.select_by_value("Vladivostok")

timezone.submit()
print()
# driver.close()

# driver.execute_script("")




