import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from details import Details
from scraper import Scraper
from data_storage import Storage

class FullScrape:
    '''
    Scrapes laptops from the box website.
    
    This function scrapes the first 15 pages of laptops' product page urls on the box website, then accesses these URLs to get the information of each laptop.
    It then stores this technical and image data in a volume.

    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    '''
    def __init__(self, number_of_pages=15):
        self.number_of_pages = number_of_pages
        self.link_list = []
        self.details_dict_list =[]
        self.link_list_index = 0

    def __scrape_links(self):
        print("Scraping links")
        scrape = Scraper(self.number_of_pages)
        self.link_list = scrape.scrape_all()
        print(self.link_list)
        link_list_length = len(self.link_list)
        print(f"{link_list_length} links have been scraped")
        time.sleep(2)

    def __start_warp(self):
        subprocess.run("systemctl enable --now warp-svc.service", shell=True, stderr=subprocess.STDOUT, timeout=60)
        time.sleep(2)
        # Start WARP
        subprocess.run("systemctl start warp-svc.service", shell=True, stderr=subprocess.STDOUT)
        subprocess.run("systemctl status warp-svc.service", shell=True, stderr=subprocess.STDOUT)
        time.sleep(2)
        # First register the warp-cli
        subprocess.run("warp-cli --accept-tos register", shell=True, stderr=subprocess.STDOUT, timeout=60)
        subprocess.run("warp-cli --accept-tos register", shell=True, stderr=subprocess.STDOUT, timeout=60)
        time.sleep(2)
        # First connect to WARP
        subprocess.run("warp-cli --accept-tos connect", shell=True, stderr=subprocess.STDOUT)
        print(subprocess.run("warp-cli --accept-tos status", shell=True, stderr=subprocess.STDOUT))
        print("WARP started!")

    def __reconnect_to_warp(self):
        print("Restarting WARP")
        subprocess.run("warp-cli --accept-tos disconnect", shell=True, stderr=subprocess.STDOUT)
        print(subprocess.run("warp-cli --accept-tos status", shell=True, stderr=subprocess.STDOUT))
        time.sleep(3)
        subprocess.run("warp-cli --accept-tos connect", shell=True, stderr=subprocess.STDOUT)
        print(subprocess.run("warp-cli --accept-tos status", shell=True, stderr=subprocess.STDOUT))

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
            time.sleep(3)
            try:
                extraction = Details(driver)
                details_dict = extraction.extract_all_data()
                print(details_dict)
                self.details_dict_list.append(details_dict)
            except:
                print("Big Box Clearance Link")
                pass
            self.link_list_index += 1
            if self.link_list_index % 10 == 0:
                FullScrape.__reconnect_to_warp(self)
                pass

        number_of_products = len(self.details_dict_list)
        print(f"{number_of_products} laptops have been scraped")

    def __store_raw_data(self):
        for details_dict in self.details_dict_list:
            store = Storage(details_dict)
            store.download_all_data()
        print("All downloaded to volume!")

    def do_full_scrape(self):
        FullScrape.__scrape_links(self)
        FullScrape.__start_warp(self)
        FullScrape.__get_details(self)
        FullScrape.__store_raw_data(self)

if __name__ == '__main__':
    full_scrape = FullScrape(3)
    full_scrape.do_full_scrape()