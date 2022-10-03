# response = requests.get("https://www.logitech.com/en-gb/products/mice.html")
# html = response.content
# html = BeautifulSoup(html, 'html.parser')

# print(html.prettify())

# products = html.find_all("div")[-20:-1]

# for product in products:
#     data = product.find_all("span")
#     print(data)
#     data = [feature.text for feature in data]
#     print(data)

# print(html.prettify())

# print(html.title)

# print(html.title.name)

# print(html.title.string)

# print(html.title.parent.name)

# print(html.div)

# print(html.find_all("span", class_="currency-symbol"))

# print(html.find_all("span", class_="currency-symbol"))

# <div class="pricing-info"><span><span class="currency-symbol">£</span>119.99</span></div>

import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.amazon.co.uk/"

driver = webdriver.Chrome()

class Scraper:
    def open_webpage(self):
        driver.get(URL)
    def input_search(self):
        search = driver.find_element(By.ID, "twotabsearchtextbox")
        search.send_keys("gaming mouse")
        search.send_keys(Keys.RETURN)
    def accept_cookies(self):
        try:
            accept_cookies_button = driver.find_element(By.ID, "sp-cc-accept")
            accept_cookies_button.click()
        except:
            pass
    def next_page(self):
        next_button = driver.find_element(By.XPATH, '//a[@class = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
        next_button.send_keys(Keys.RETURN)

scrape = Scraper()
scrape.open_webpage()
scrape.input_search()
scrape.accept_cookies()
scrape.next_page()