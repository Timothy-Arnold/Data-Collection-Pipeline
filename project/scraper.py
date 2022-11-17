import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Scraper:
    '''
    This class is used to collect all the URLs of the first 210 movies on rottentomatoes' "Most Popular Movies at Home" page'

    Parameters:
    ----------
    URL: str
        The URL of rottentomatoes' "Most Popular Movies at Home" page
    
    Attributes:
    ----------
    link_list: list
        The list of URLs of all the movie pages' URLs
    number_of_pages: int
        The number of times the "Load more" button is clicked, to view more movies

    Methods:
    -------
    open_webpage()
        Opens the rottentomatoes "Most Popular Movies at Home" page
    click_load_more()
        Clicks the load more button at the bottom of the page to show more movies
    get_links()
        Finds all the movie links in the page and stores them in the list
    scrape_all()
        Collects the movie links from the whole extended page and stores them in the list.
    '''
    def __init__(self, number_of_load_more_clicks=2):
        chromeOptions = Options()
        chromeOptions.headless = True
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

    def scrape_all(self):
        Scraper.__open_webpage(self)
        for click in range(self.number_of_load_more_clicks):
            Scraper.__click_load_more(self)
            time.sleep(2)
        Scraper.__get_links(self)
        return self.link_list

if __name__ == '__main__':
    scrape = Scraper()
    scrape.scrape_all()
    print(scrape.link_list)
    print(f"{len(scrape.link_list)} laptops' urls have been scraped")
    time.sleep(5)
    scrape.driver.quit()