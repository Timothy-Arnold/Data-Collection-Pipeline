from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Scraper:
    '''
    This class is used to collect all the URLs of product listings on box for the first 15 pages of laptops.

    Parameters:
    ----------
    URL: str
        The URL of box's laptop section
    
    Attributes:
    ----------
    link_list: list
        The list of URLs of all the product pages
    number_of_pages: int
        The number of pages of laptops on box whose URL's are going to be scraped.

    Methods:
    -------
    open_webpage()
        Opens the Amazon front page
    get_links()
        Finds all the product links in the page and stores them in the list
    go_to_page(page_number)
        Moves to the given page number
    scrape_all()
        Collects the product links from all 15 pages on box and stores them in the list.
    '''
    def __init__(self, number_of_pages=15):
        self.driver = webdriver.Chrome()
        self.link_list = []
        self.number_of_pages = number_of_pages
        time.sleep(1)

    def __open_webpage(self):
        self.driver.get("https://www.box.co.uk/laptops")
        time.sleep(2)

    def __get_links(self):
        product_container = self.driver.find_element(By.XPATH, '//div[@class = "product-list  "]')
        product_list_1 = product_container.find_elements(By.XPATH, '//div[@class = "product-list-item "]')
        product_list_2 = product_container.find_elements(By.XPATH, '//div[@class = "product-list-item middle"]')
        product_list = product_list_1 + product_list_2
        for product in product_list:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute("href")
            self.link_list.append(link)

    def __go_to_page(self, page_number):
        page_url = f"https://www.box.co.uk/laptops/page/{page_number}"
        self.driver.get(page_url)
        time.sleep(1)

    def scrape_all(self):
        Scraper.__open_webpage(self)
        # Get the first page's links
        Scraper.__get_links(self)
        for page_number in range(2, self.number_of_pages + 1):
            Scraper.__go_to_page(self, page_number)
            Scraper.__get_links(self)
        self.driver.quit()
        return self.link_list

if __name__ == '__main__':
    scrape = Scraper(2)
    scrape.scrape_all()
    print(scrape.link_list)
    print(f"{len(scrape.link_list)} laptops' urls have been scraped")
    