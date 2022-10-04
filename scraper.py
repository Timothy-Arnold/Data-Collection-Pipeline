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
    def input_search(self, search_string):
        search = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search.send_keys(search_string)
        search.send_keys(Keys.RETURN)
        time.sleep(1)
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

def scrape():
    scrape = Scraper()
    scrape.open_webpage()
    scrape.accept_cookies()
    scrape.input_search("laptop")
    # Get first page's links
    scrape.get_links()
    for page in range(19):
        scrape.next_page()
        scrape.get_links()
    print(scrape.link_list)
    print(f'There are {len(scrape.link_list)} properties in this page')
    time.sleep(60)

if __name__ == '__main__':
    scrape()

# %%
import requests
from bs4 import BeautifulSoup

test_link = "https://www.amazon.co.uk/Razer-Blade-17-Display-Chamber/dp/B09Q6CVSW3/ref=sr_1_3?keywords=laptop&qid=1664886688&qu=eyJxc2MiOiI5LjQzIiwicXNhIjoiOC44MSIsInFzcCI6IjguMTkifQ%3D%3D&sr=8-3"

html_request = requests.get(test_link)
html_string = html_request.text
print(html_string)
# %%
