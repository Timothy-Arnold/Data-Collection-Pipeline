import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from details import Details
from scraper import Scraper
from data_storage import Storage

class FullScrape:
    '''
    Scrapes movies from the rottentomatoes website
    
    This function scrapes the first 210 movie pages from the rottentomatoes website, then accesses these URLs to get the information of each movie.
    It then stores this text and image data in my local directory.

    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    '''
    def __init__(self):
        self.link_list = []
        self.details_dict_list =[]

    def __scrape_links(self):
        print("Scraping links")
        scrape = Scraper()
        self.link_list = scrape.scrape_all()
        print(self.link_list)
        link_list_length = len(self.link_list)
        print(f"{link_list_length} links have been scraped")
        time.sleep(3)

    def __get_details(self):
        chromeOptions = Options()
        chromeOptions.headless = True
        chromeOptions.add_argument("window-size=1920x1080")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chromeOptions)
        for link in self.link_list:
            driver.get(link)
            time.sleep(1)
            try:
                extraction = Details(driver)
                details_dict = extraction.extract_all_data()
                print(details_dict)
                self.details_dict_list.append(details_dict)
            except:
                print("Faulty link!")
                pass
            time.sleep(1)
            print(len(self.details_dict_list))

        number_of_products = len(self.details_dict_list)
        print(f"{number_of_products} movies have been scraped")

    def __store_raw_data(self):
        for details_dict in self.details_dict_list:
            store = Storage(details_dict)
            store.download_all_data()
        print("All downloaded!")

    def do_full_scrape(self):
        FullScrape.__scrape_links(self)
        FullScrape.__get_details(self)
        FullScrape.__store_raw_data(self)

if __name__ == '__main__':
    full_scrape = FullScrape()
    full_scrape.do_full_scrape()