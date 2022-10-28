import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from details import Details
from scraper import Scraper
from data_storage import Storage

def do_full_scrape(pages=15):
    '''
    Scrapes laptops from the box website.
    
    This function scrapes the first 15 pages of laptops' product page urls on the box website, then accesses these URLs to get the information of each laptop.
    It then stores this technical and image data in my local directory, as well as uploads it to my S3 bucket.

    Parameters
    ----------
    None
    
    Returns
    ----------
    None
    '''
    scrape = Scraper(pages)
    link_list = scrape.scrape_all()
    print(link_list)
    link_list_length = len(link_list)
    print(f"{link_list_length} links have been scraped")
    time.sleep(2)
    # Initialize list of detail_dict's
    details_dict_list = []
    chromeOptions = Options()
    chromeOptions.headless = True
    chromeOptions.add_argument("window-size=1920x1080")
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chromeOptions)
    for link in link_list[:5]:
        driver.get(link)
        time.sleep(3)
        try:
            extraction = Details(driver)
            details_dict = extraction.extract_all_data()
            print(details_dict)
            details_dict_list.append(details_dict)
        except:
            print("Page didn't work")
            pass
    number_of_products = len(details_dict_list)
    print(f"{number_of_products} laptops have been scraped")
    for details_dict in details_dict_list:
        store = Storage(details_dict)
        store.download_all_data()
    print("All downloaded and uploaded!")

if __name__ == '__main__':
    do_full_scrape(2)