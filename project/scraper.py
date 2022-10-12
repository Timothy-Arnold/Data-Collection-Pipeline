import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    '''
    This class is used to collect all the URLs of product listings on Amazon in all 20 pages, after searching "laptop".

    Parameters:
    ----------
    URL: str
        The URL of the website (in this case Amazon's front page)
    
    Attributes:
    ----------
    link_list: list
        The list of URLs of all the product pages

    Methods:
    -------
    open_webpage()
        Opens the Amazon front page
    input_search()
        Types "laptop" into the search bar
    accept_cookies()
        Gets rid of the "Get cookies" popup
    get_links()
        Finds all the product links in the page and stores them in the list
    next_page()
        Moves to the next page
    scrape_all()
        Collects the product links from all 20 pages on Amazon and stores them in the list.
    '''
    def __init__(self, URL = "https://www.box.co.uk/laptops"):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.link_list = []
        time.sleep(1)

    def __open_webpage(self):
        self.driver.get(self.URL)
        time.sleep(3)

    def __get_links(self):
        product_container = self.driver.find_element(By.XPATH, '//div[@class = "product-list  "]')
        product_list_1 = product_container.find_elements(By.XPATH, '//div[@class = "product-list-item "]')
        product_list_2 = product_container.find_elements(By.XPATH, '//div[@class = "product-list-item middle"]')
        product_list = product_list_1 + product_list_2
        for product in product_list:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute("href")
            self.link_list.append(link)
        time.sleep(1)

    def __go_to_page(self, page_number):
        self.URL = f"https://www.box.co.uk/laptops/page/{page_number}"
        self.driver.get(self.URL)
        time.sleep(1)

    def scrape_all(self, number_of_pages = 20):
        Scraper.__open_webpage(self)
        # Get the first page's links
        Scraper.__get_links(self)
        for page_number in range(2, number_of_pages + 1):
            Scraper.__go_to_page(self, page_number)
            Scraper.__get_links(self)
        return self.link_list
        time.sleep(10)

if __name__ == '__main__':
    scrape = Scraper()
    scrape.scrape_all(10)
    print(scrape.link_list)
    print(f'There are {len(scrape.link_list)} properties in this page')