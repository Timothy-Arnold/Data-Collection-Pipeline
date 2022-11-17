import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
    def __init__(self, number_of_load_more_clicks=2):
        chromeOptions = Options()
        chromeOptions.headless = False
        self.driver = webdriver.Chrome(options=chromeOptions)
        self.link_list = []
        self.number_of_load_more_clicks = number_of_load_more_clicks
        time.sleep(2)

    def __open_webpage(self):
        self.driver.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=5")
        time.sleep(2)

    def __click_load_more(self):
        load_more_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Load more")]')
        load_more_button.click()
        time.sleep(2)

    def __get_links(self):
        print("Getting Links!")
        product_container = self.driver.find_element(By.XPATH, '//div[@class = "discovery-tiles"]')
        product_list = product_container.find_elements(By.XPATH, '//a[@class = "js-tile-link"]')
        for product in product_list:
            # a_tag = product.find_element(By.TAG_NAME, 'a')
            link = product.get_attribute("href")
            self.link_list.append(link)
        time.sleep(2)

    def __go_to_page(self, page_number):
        page_url = f"https://www.laptopsdirect.co.uk/ct/laptops-and-netbooks/laptops?pageNumber={page_number}"
        self.driver.get(page_url)
        time.sleep(1)

    def scrape_all(self):
        Scraper.__open_webpage(self)
        for click in range(self.number_of_load_more_clicks):
            Scraper.__click_load_more(self)
            time.sleep(3)
        Scraper.__get_links(self)
        return self.link_list

if __name__ == '__main__':
    scrape = Scraper(3)
    scrape.scrape_all()
    print(scrape.link_list)
    print(f"{len(scrape.link_list)} laptops' urls have been scraped")
    