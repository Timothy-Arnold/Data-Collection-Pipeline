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
        self.link_list = []
    def open_webpage(self):
        self.driver.get(self.URL)
        time.sleep(2)
    def input_search(self):
        search = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search.send_keys("gaming mouse")
        search.send_keys(Keys.RETURN)
        time.sleep(2)
    def accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(By.ID, "sp-cc-accept")
            accept_cookies_button.click()
        except:
            pass
    def get_links(self):
        product_container = self.driver.find_element(By.XPATH, '//div[@class = "s-main-slot s-result-list s-search-results sg-row"]')
        product_list = product_container.find_elements(By.XPATH, '//div[@class = "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"]')
        for product in product_list:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute("href")
            self.link_list.append(link)
        time.sleep(1)
    def next_page(self):
        next_button = self.driver.find_element(By.XPATH, '//a[@class = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
        next_button.send_keys(Keys.RETURN)
        time.sleep(1)

#<a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
#<h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"
#//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[5]

def scrape():
    scrape = Scraper()
    scrape.open_webpage()
    scrape.accept_cookies()
    scrape.input_search()
    # Get first page's links
    scrape.get_links()
    for interation in range(18):
        scrape.next_page()
        scrape.get_links()
    print(f'There are {len(scrape.link_list)} properties in this page')
    print(scrape.link_list)
    time.sleep(60)

if __name__ == '__main__':
    scrape()