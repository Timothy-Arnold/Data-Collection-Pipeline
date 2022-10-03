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

class Scraper:
    def __init__(self, URL = "https://www.amazon.co.uk/"):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.product_list = []
    def open_webpage(self):
        self.driver.get(self.URL)
        time.sleep(2)
    def input_search(self):
        search = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search.send_keys("gaming mouse")
        search.send_keys(Keys.RETURN)
    def accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(By.ID, "sp-cc-accept")
            accept_cookies_button.click()
        except:
            pass
    def next_page(self):
        next_button = self.driver.find_element(By.XPATH, '//a[@class = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
        next_button.send_keys(Keys.RETURN)
    def get_link(self):
        product = self.driver.find_element(By.XPATH, '//h2[@class = "a-size-mini a-spacing-none a-color-base s-line-clamp-2"]')
        a_tag = product.find_element(by=By.TAG_NAME, value='a')
        link = a_tag.get_attribute("href")
        self.product_list.append(link)
        print(self.product_list)

#<a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
#<h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"

def scrape():
    scrape = Scraper()
    scrape.open_webpage()
    scrape.input_search()
    scrape.accept_cookies()
    scrape.get_link()
    scrape.next_page()
    time.sleep(5)

if __name__ == '__main__':
    scrape()